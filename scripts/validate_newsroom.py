from __future__ import annotations

import argparse
import json
import re
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SECTIONS = [
    "LINE Digest",
    "TL;DR",
    "Top 5",
    "Money Map",
    "Watchlist",
    "Web Edition",
]
ALLOWED_IMAGE_KINDS = {"photo", "branded_scene", "conceptual"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply deterministic FrontBrief.AI pre-publication gates."
    )
    parser.add_argument("--article", required=True, type=Path)
    parser.add_argument("--caption", required=True, type=Path)
    parser.add_argument("--poster-spec", required=True, type=Path)
    parser.add_argument(
        "--ledger",
        default=Path("social/poster/ledger.json"),
        type=Path,
    )
    parser.add_argument("--articles-dir", default=Path("articles"), type=Path)
    return parser.parse_args()


def rooted(path: Path) -> Path:
    return path if path.is_absolute() else PROJECT_ROOT / path


def read_json(path: Path) -> dict[str, Any]:
    with rooted(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def canonical_url(value: str) -> str:
    parsed = urlparse(value.strip())
    query = [
        (key, val)
        for key, val in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith("utm_")
        and key.lower() not in {"fbclid", "gclid", "mc_cid", "mc_eid"}
    ]
    path = parsed.path.rstrip("/") or "/"
    return urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            path,
            "",
            urlencode(sorted(query)),
            "",
        )
    )


def normalize(value: str) -> str:
    value = re.sub(r"https?://\S+", "", value.lower())
    value = re.sub(r"[^a-z0-9]+", " ", value)
    stop = {
        "a",
        "an",
        "and",
        "at",
        "for",
        "in",
        "is",
        "of",
        "on",
        "the",
        "to",
        "with",
    }
    return " ".join(word for word in value.split() if word not in stop)


def similar(left: str, right: str) -> bool:
    left_n = normalize(left)
    right_n = normalize(right)
    if not left_n or not right_n:
        return False
    left_words = set(left_n.split())
    right_words = set(right_n.split())
    jaccard = len(left_words & right_words) / max(1, len(left_words | right_words))
    ratio = SequenceMatcher(None, left_n, right_n).ratio()
    return jaccard >= 0.58 or ratio >= 0.76


def section(text: str, name: str) -> str:
    match = re.search(
        rf"(?:^|\n)##\s+{re.escape(name)}\s*\n([\s\S]*?)(?=\n##\s+|$)",
        text,
        flags=re.IGNORECASE,
    )
    return match.group(1).strip() if match else ""


def validate_article(text: str, run_date: str) -> list[str]:
    errors: list[str] = []
    if not text.startswith(f"# FrontBrief.AI — {run_date}\n"):
        errors.append("article H1 must be '# FrontBrief.AI — YYYY-MM-DD'")
    for name in REQUIRED_SECTIONS:
        if not section(text, name):
            errors.append(f"missing or empty section: {name}")
    top_five = re.findall(r"^###\s+([1-5])\.\s+(.+)$", section(text, "Top 5"), re.MULTILINE)
    if [number for number, _ in top_five] != ["1", "2", "3", "4", "5"]:
        errors.append("Top 5 must contain exactly the numbered headings 1 through 5")
    top_body = section(text, "Top 5")
    if len(re.findall(r"^-\s+Link:\s+https?://", top_body, re.MULTILINE)) != 5:
        errors.append("each Top 5 item must have exactly one direct Link URL")
    line_digest = section(text, "LINE Digest")
    if len(line_digest) > 4490:
        errors.append("LINE Digest exceeds 4490 characters")
    if not line_digest.startswith(f"FrontBrief.AI — {run_date}"):
        errors.append("LINE Digest must start with the brand and run date")
    return errors


def validate_caption(text: str) -> list[str]:
    errors: list[str] = []
    if len(text) > 2200:
        errors.append("Instagram caption exceeds 2200 characters")
    hashtags = re.findall(r"(?<!\w)#[A-Za-z0-9_]+", text)
    if len(hashtags) > 5:
        errors.append("Instagram caption has more than five hashtags")
    if not hashtags or hashtags[-1] != "#FrontBriefAI":
        errors.append("the final hashtag must be #FrontBriefAI")
    if "full brief in bio" not in text.lower():
        errors.append("Instagram caption is missing the 'Full brief in bio' CTA")
    return errors


def validate_spec(spec: dict[str, Any], run_date: date) -> list[str]:
    errors: list[str] = []
    required = {
        "date",
        "category",
        "headline",
        "subhead",
        "poster_story",
        "poster_shape",
        "image_kind",
        "image_url",
        "visual_source_url",
        "source_url",
        "publication_date",
        "brief_stories",
    }
    missing = sorted(required - spec.keys())
    if missing:
        return [f"poster spec missing: {', '.join(missing)}"]
    if spec["date"] != run_date.isoformat():
        errors.append("poster spec date does not match article date")
    if spec["image_kind"] not in ALLOWED_IMAGE_KINDS:
        errors.append("image_kind cannot be a bare logo")
    for key in ("image_url", "visual_source_url", "source_url"):
        if not valid_url(str(spec[key])):
            errors.append(f"{key} must be a direct public URL")
    try:
        poster_published = date.fromisoformat(str(spec["publication_date"]))
        poster_age = (run_date - poster_published).days
        if poster_age < 0 or poster_age > 5:
            errors.append("poster story is outside the 0–5 day freshness window")
    except (TypeError, ValueError):
        errors.append("poster story has an invalid publication_date")
    stories = spec["brief_stories"]
    if not isinstance(stories, list) or len(stories) != 5:
        errors.append("brief_stories must contain exactly five records")
        return errors
    for index, story in enumerate(stories, start=1):
        for key in ("headline", "publication_date", "event_date", "source_url"):
            if not story.get(key):
                errors.append(f"brief story {index} missing {key}")
        if story.get("source_url") and not valid_url(story["source_url"]):
            errors.append(f"brief story {index} has an invalid source_url")
        try:
            published = date.fromisoformat(story["publication_date"])
            age = (run_date - published).days
            if age < 0 or age > 5:
                errors.append(f"brief story {index} is outside the 0–5 day freshness window")
        except (TypeError, ValueError):
            errors.append(f"brief story {index} has an invalid publication_date")
        try:
            event = date.fromisoformat(story["event_date"])
            event_age = (run_date - event).days
            if event_age < 0 or event_age > 5:
                errors.append(f"brief story {index} event is outside the 0–5 day window")
        except (TypeError, ValueError):
            errors.append(f"brief story {index} has an invalid event_date")
    return errors


def recent_article_stories(articles_dir: Path, run_date: date) -> list[dict[str, str]]:
    stories: list[dict[str, str]] = []
    for path in rooted(articles_dir).glob("????-??-??-ai-brief.md"):
        try:
            article_date = date.fromisoformat(path.name[:10])
        except ValueError:
            continue
        age = (run_date - article_date).days
        if age <= 0 or age > 5:
            continue
        top_five = section(path.read_text(encoding="utf-8"), "Top 5")
        headings = re.findall(r"^###\s+[1-5]\.\s+(.+)$", top_five, re.MULTILINE)
        links = re.findall(r"^-\s+Link:\s+(https?://\S+)", top_five, re.MULTILINE)
        for index, headline in enumerate(headings):
            stories.append(
                {
                    "date": article_date.isoformat(),
                    "headline": headline,
                    "source_url": links[index] if index < len(links) else "",
                }
            )
    return stories


def validate_archive(
    spec: dict[str, Any],
    article_text: str,
    ledger: dict[str, Any],
    run_date: date,
    articles_dir: Path,
) -> list[str]:
    errors: list[str] = []
    previous = [
        entry
        for entry in ledger.get("entries", [])
        if entry.get("date") and entry["date"] < run_date.isoformat()
    ]
    previous.sort(key=lambda entry: entry["date"])
    if previous and previous[-1].get("poster_shape") == spec.get("poster_shape"):
        errors.append("poster shape repeats the previous run")
    recent = [
        entry
        for entry in previous
        if 0 < (run_date - date.fromisoformat(entry["date"])).days <= 5
    ]
    for entry in recent:
        if similar(str(spec.get("poster_story", "")), str(entry.get("poster_story", ""))):
            errors.append(f"poster story duplicates ledger entry {entry['date']}")
    article_headlines = re.findall(
        r"^###\s+[1-5]\.\s+(.+)$",
        section(article_text, "Top 5"),
        re.MULTILINE,
    )
    if len(article_headlines) == 5:
        for index, headline in enumerate(article_headlines):
            if not similar(headline, str(spec["brief_stories"][index]["headline"])):
                errors.append(f"brief_stories[{index}] does not match article item {index + 1}")

    candidate_stories = spec.get("brief_stories", [])
    for left_index, left in enumerate(candidate_stories):
        for right_index, right in enumerate(candidate_stories[left_index + 1 :], left_index + 1):
            if canonical_url(str(left.get("source_url", ""))) == canonical_url(
                str(right.get("source_url", ""))
            ) or similar(
                str(left.get("headline", "")), str(right.get("headline", ""))
            ):
                errors.append(
                    f"brief stories {left_index + 1} and {right_index + 1} are duplicates"
                )

    recent_stories = recent_article_stories(articles_dir, run_date)
    for index, candidate in enumerate(candidate_stories, start=1):
        for archived in recent_stories:
            same_source = (
                candidate.get("source_url")
                and canonical_url(str(candidate.get("source_url", "")))
                == canonical_url(str(archived.get("source_url", "")))
            )
            same_story = similar(
                str(candidate.get("headline", "")),
                str(archived.get("headline", "")),
            )
            if same_source or same_story:
                errors.append(
                    f"brief story {index} duplicates article archive entry {archived['date']}"
                )
                break

    if article_headlines:
        lead = article_headlines[0]
        for entry in recent:
            if similar(lead, str(entry.get("article_lead", ""))):
                errors.append(f"article lead duplicates ledger entry {entry['date']}")
    return errors


def main() -> int:
    args = parse_args()
    article_text = rooted(args.article).read_text(encoding="utf-8")
    caption_text = rooted(args.caption).read_text(encoding="utf-8").strip()
    spec = read_json(args.poster_spec)
    ledger = read_json(args.ledger)
    try:
        run_date = date.fromisoformat(str(spec.get("date", "")))
    except ValueError as exc:
        raise SystemExit(f"FAIL: invalid poster spec date: {exc}") from exc

    errors = [
        *validate_article(article_text, run_date.isoformat()),
        *validate_caption(caption_text),
        *validate_spec(spec, run_date),
        *validate_archive(spec, article_text, ledger, run_date, args.articles_dir),
    ]
    if errors:
        print("FrontBrief pre-publication gates: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("FrontBrief pre-publication gates: PASS")
    print(f"- edition: {run_date.isoformat()}")
    print("- freshness: all five stories are 0–5 days old")
    print("- duplicates: no recent lead/poster match")
    print("- poster: category, shape, image provenance, and layout inputs valid")
    print("- channels: article, LINE, Web Edition, and Instagram caption valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
