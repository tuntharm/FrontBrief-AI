from __future__ import annotations

import json
import logging
import re
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import yaml
from bs4 import BeautifulSoup
from dateutil import parser as date_parser


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"

USER_AGENT = (
    "tharm-ai-deeptech-brief/1.0 "
    "(public RSS/metadata fetcher; contact: repository owner)"
)


def configure_logging(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    logging.Formatter.converter = time.gmtime
    return logging.getLogger(name)


def ensure_directories() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in {path}")
    return data


def read_json(path: Path, default: Any | None = None) -> Any:
    if not path.exists():
        if default is not None:
            return default
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False, sort_keys=True)
        handle.write("\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def clean_text(value: str | None, max_length: int | None = None) -> str:
    if not value:
        return ""
    text = BeautifulSoup(value, "html.parser").get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text).strip()
    if max_length and len(text) > max_length:
        return text[: max_length - 1].rsplit(" ", 1)[0].rstrip() + "..."
    return text


def parse_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, tuple) and len(value) >= 6:
        parsed = datetime(*value[:6], tzinfo=UTC)
    else:
        try:
            parsed = date_parser.parse(str(value), fuzzy=True)
        except (TypeError, ValueError, OverflowError):
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def isoformat_utc(value: datetime | None) -> str | None:
    if not value:
        return None
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def canonicalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=False)
        if not key.lower().startswith("utm_")
        and key.lower() not in {"fbclid", "gclid", "mc_cid", "mc_eid"}
    ]
    normalized_query = urlencode(query, doseq=True)
    path = parts.path.rstrip("/") or parts.path
    return urlunsplit(
        (
            parts.scheme.lower(),
            parts.netloc.lower(),
            path,
            normalized_query,
            "",
        )
    )


def normalize_title(title: str) -> str:
    title = clean_text(title).lower()
    title = re.sub(r"[^a-z0-9]+", " ", title)
    return re.sub(r"\s+", " ", title).strip()


def london_report_date() -> str:
    from zoneinfo import ZoneInfo

    return datetime.now(ZoneInfo("Europe/London")).strftime("%Y-%m-%d")


def clamp_score(value: Any, min_score: int = 0, max_score: int = 5) -> int:
    try:
        score = int(round(float(value)))
    except (TypeError, ValueError):
        return min_score
    return max(min_score, min(max_score, score))


def graceful_truncate(text: str, max_chars: int, suffix: str) -> str:
    text = text.strip()
    if len(text) <= max_chars:
        return text
    budget = max_chars - len(suffix)
    if budget <= 0:
        return text[:max_chars]
    cut = text[:budget].rstrip()
    newline_cut = cut.rfind("\n")
    if newline_cut > budget * 0.65:
        cut = cut[:newline_cut].rstrip()
    else:
        space_cut = cut.rfind(" ")
        if space_cut > budget * 0.8:
            cut = cut[:space_cut].rstrip()
    return cut + suffix
