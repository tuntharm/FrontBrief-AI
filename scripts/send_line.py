from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "reports"
LOGGER = logging.getLogger("send_line")
LINE_PUSH_ENDPOINT = "https://api.line.me/v2/bot/message/push"
LINE_MAX_CHARS = 4490


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


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


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


def load_digest(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"LINE digest file not found: {path}")
    digest = path.read_text(encoding="utf-8").strip()
    if not digest:
        raise RuntimeError(f"LINE digest file is empty: {path}")
    return graceful_truncate(
        digest,
        LINE_MAX_CHARS,
        "\n\n[Truncated to fit LINE. Full report is in GitHub.]",
    )


def push_line_message(token: str, recipient: str, text: str) -> requests.Response:
    payload: dict[str, Any] = {
        "to": recipient,
        "messages": [{"type": "text", "text": text}],
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return requests.post(LINE_PUSH_ENDPOINT, headers=headers, json=payload, timeout=20)


def main() -> int:
    configure_logging()
    token = required_env("LINE_CHANNEL_ACCESS_TOKEN")
    recipient = required_env("LINE_TO")
    digest = load_digest(REPORTS_DIR / "latest_line_digest.txt")

    LOGGER.info("Sending one LINE text message to configured recipient")
    response = push_line_message(token, recipient, digest)
    if response.status_code < 200 or response.status_code >= 300:
        raise RuntimeError(
            f"LINE push failed with HTTP {response.status_code}: {response.text[:500]}"
        )
    LOGGER.info("LINE push succeeded with HTTP %s", response.status_code)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
