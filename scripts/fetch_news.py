from __future__ import annotations

import argparse
import hashlib
import re
from datetime import UTC, datetime, timedelta
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlsplit

import feedparser
import requests
from bs4 import BeautifulSoup

from utils import (
    CONFIG_DIR,
    DATA_DIR,
    USER_AGENT,
    canonicalize_url,
    clean_text,
    configure_logging,
    ensure_directories,
    isoformat_utc,
    load_yaml,
    normalize_title,
    parse_datetime,
    write_json,
)


LOGGER = configure_logging("fetch_news")
DATE_PATTERNS = [
    re.compile(r"\b(20\d{2}[/-]\d{1,2}[/-]\d{1,2})\b"),
    re.compile(
        r"\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+20\d{2})\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+20\d{2})\b",
        re.IGNORECASE,
    ),
]


def source_iter(config: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    tracks = config.get("tracks", {})
    if not isinstance(tracks, dict):
        raise ValueError("config/sources.yml must contain a tracks mapping")
    sources: list[tuple[str, dict[str, Any]]] = []
    for track, track_sources in tracks.items():
        for source in track_sources or []:
            if source.get("enabled", True):
                sources.append((track, source))
    return sources


def request_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml, application/atom+xml, text/xml, text/html;q=0.8, */*;q=0.5",
        }
    )
    return session


def make_item(
    *,
    title: str,
    source: str,
    url: str,
    track: str,
    published_at: datetime | None,
    summary: str = "",
    include_undated: bool = False,
) -> dict[str, Any]:
    canonical_url = canonicalize_url(url)
    item_id = hashlib.sha1(f"{canonical_url}|{normalize_title(title)}".encode("utf-8")).hexdigest()[:16]
    return {
        "id": item_id,
        "title": clean_text(title, 300),
        "source": source,
        "url": canonical_url,
        "published_at": isoformat_utc(published_at),
        "summary": clean_text(summary, 1000),
        "track": track,
        "fetched_at": isoformat_utc(datetime.now(UTC)),
        "include_undated": include_undated,
    }


def fetch_rss_source(
    session: requests.Session,
    track: str,
    source: dict[str, Any],
    timeout: int,
    per_source_limit: int,
) -> list[dict[str, Any]]:
    name = str(source["name"])
    url = str(source["url"])
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    parsed = feedparser.parse(response.content)
    if parsed.bozo:
        LOGGER.warning("Feed parse warning for %s: %s", name, parsed.bozo_exception)

    items: list[dict[str, Any]] = []
    for entry in parsed.entries[:per_source_limit]:
        title = clean_text(entry.get("title"), 300)
        link = entry.get("link") or entry.get("id")
        if not title or not link:
            continue
        published_at = (
            parse_datetime(entry.get("published_parsed"))
            or parse_datetime(entry.get("updated_parsed"))
            or parse_datetime(entry.get("published"))
            or parse_datetime(entry.get("updated"))
            or parse_datetime(entry.get("created"))
        )
        summary = entry.get("summary") or entry.get("description") or entry.get("subtitle") or ""
        items.append(
            make_item(
                title=title,
                source=name,
                url=str(link),
                track=track,
                published_at=published_at,
                summary=str(summary),
                include_undated=bool(source.get("include_undated", False)),
            )
        )
    return items


def matches_patterns(url: str, include_patterns: list[str], exclude_patterns: list[str]) -> bool:
    if include_patterns and not any(pattern in url for pattern in include_patterns):
        return False
    if exclude_patterns and any(pattern in url for pattern in exclude_patterns):
        return False
    return True


def find_date_near_link(link_text: str, surrounding_text: str) -> datetime | None:
    combined = f"{link_text} {surrounding_text[:500]}"
    for pattern in DATE_PATTERNS:
        match = pattern.search(combined)
        if match:
            return parse_datetime(match.group(1))
    return None


def fetch_url_source(
    session: requests.Session,
    track: str,
    source: dict[str, Any],
    timeout: int,
    per_source_limit: int,
) -> list[dict[str, Any]]:
    name = str(source["name"])
    url = str(source["url"])
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    base_netloc = urlsplit(url).netloc
    include_patterns = list(source.get("include_url_patterns") or [])
    exclude_patterns = list(source.get("exclude_url_patterns") or [])
    same_domain_only = bool(source.get("same_domain_only", True))

    items: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    for link in soup.find_all("a", href=True):
        title = clean_text(link.get_text(" ", strip=True), 300)
        if len(title) < 18:
            continue
        item_url = canonicalize_url(urljoin(url, link["href"]))
        if item_url in seen_urls:
            continue
        if same_domain_only and urlsplit(item_url).netloc != base_netloc:
            continue
        if not matches_patterns(item_url, include_patterns, exclude_patterns):
            continue
        parent_text = clean_text(link.parent.get_text(" ", strip=True) if link.parent else "", 1000)
        published_at = find_date_near_link(title, parent_text)
        items.append(
            make_item(
                title=title,
                source=name,
                url=item_url,
                track=track,
                published_at=published_at,
                summary=parent_text,
                include_undated=bool(source.get("include_undated", False)),
            )
        )
        seen_urls.add(item_url)
        if len(items) >= per_source_limit:
            break
    return items


def fetch_source(
    session: requests.Session,
    track: str,
    source: dict[str, Any],
    timeout: int,
    per_source_limit: int,
) -> list[dict[str, Any]]:
    source_type = str(source.get("type", "rss")).lower()
    if source_type == "rss":
        return fetch_rss_source(session, track, source, timeout, per_source_limit)
    if source_type == "url":
        return fetch_url_source(session, track, source, timeout, per_source_limit)
    raise ValueError(f"Unsupported source type {source_type!r} for {source.get('name')}")


def is_recent(item: dict[str, Any], cutoff: datetime, include_undated: bool) -> bool:
    published_at = parse_datetime(item.get("published_at"))
    if not published_at:
        return include_undated
    return published_at >= cutoff


def better_item(existing: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    existing_summary_len = len(existing.get("summary") or "")
    candidate_summary_len = len(candidate.get("summary") or "")
    if candidate_summary_len > existing_summary_len:
        return candidate
    if not existing.get("published_at") and candidate.get("published_at"):
        return candidate
    return existing


def deduplicate(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_url: dict[str, dict[str, Any]] = {}
    for item in items:
        url = item.get("url")
        if not url:
            continue
        if url in by_url:
            by_url[url] = better_item(by_url[url], item)
        else:
            by_url[url] = item

    deduped: list[dict[str, Any]] = []
    normalized_titles: list[str] = []
    for item in sorted(
        by_url.values(),
        key=lambda row: row.get("published_at") or "",
        reverse=True,
    ):
        title_key = normalize_title(str(item.get("title", "")))
        if not title_key:
            continue
        duplicate_index = next(
            (
                index
                for index, existing_title in enumerate(normalized_titles)
                if SequenceMatcher(None, title_key, existing_title).ratio() >= 0.92
            ),
            None,
        )
        if duplicate_index is not None:
            deduped[duplicate_index] = better_item(deduped[duplicate_index], item)
            normalized_titles[duplicate_index] = title_key
            continue
        deduped.append(item)
        normalized_titles.append(title_key)
    return deduped


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch recent AI/deeptech candidate items.")
    parser.add_argument("--sources", default=str(CONFIG_DIR / "sources.yml"), help="Path to sources YAML.")
    parser.add_argument("--lookback-hours", type=int, default=None, help="Override source lookback window.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_directories()
    config = load_yaml(Path(args.sources))
    defaults = config.get("defaults", {})
    lookback_hours = int(args.lookback_hours or defaults.get("lookback_hours", 48))
    per_source_limit = int(defaults.get("per_source_limit", 15))
    timeout = int(defaults.get("request_timeout_seconds", 20))
    cutoff = datetime.now(UTC) - timedelta(hours=lookback_hours)

    session = request_session()
    raw_items: list[dict[str, Any]] = []
    successful_sources = 0
    failed_sources = 0

    sources = source_iter(config)
    LOGGER.info("Fetching %d enabled sources with a %d hour lookback", len(sources), lookback_hours)
    for track, source in sources:
        name = source.get("name", source.get("url", "unnamed source"))
        try:
            items = fetch_source(session, track, source, timeout, per_source_limit)
            successful_sources += 1
            raw_items.extend(items)
            LOGGER.info("Fetched %d items from %s", len(items), name)
        except Exception as exc:  # noqa: BLE001 - source failures should not stop the run.
            failed_sources += 1
            LOGGER.warning("Source failed: %s (%s)", name, exc)

    if successful_sources == 0:
        LOGGER.error("All enabled sources failed. Check network access and source URLs.")
        return 2

    include_undated_default = bool(defaults.get("include_undated", False))
    recent_items = [
        item
        for item in raw_items
        if is_recent(item, cutoff, bool(item.get("include_undated", include_undated_default)))
    ]
    cleaned_items = deduplicate(recent_items)

    metadata = {
        "fetched_at": isoformat_utc(datetime.now(UTC)),
        "lookback_hours": lookback_hours,
        "enabled_sources": len(sources),
        "successful_sources": successful_sources,
        "failed_sources": failed_sources,
        "raw_item_count": len(raw_items),
        "candidate_count": len(cleaned_items),
    }
    write_json(DATA_DIR / "news_raw.json", {"metadata": metadata, "items": raw_items})
    write_json(DATA_DIR / "news_candidates.json", {"metadata": metadata, "items": cleaned_items})
    LOGGER.info("Saved %d raw items and %d cleaned candidates", len(raw_items), len(cleaned_items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
