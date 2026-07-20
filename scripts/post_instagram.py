from __future__ import annotations

import logging
import os
import re
import time
from pathlib import Path

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = PROJECT_ROOT / "articles"
POSTER_DIR = PROJECT_ROOT / "social" / "poster"
CAPTION_DIR = PROJECT_ROOT / "social" / "caption"
LOGGER = logging.getLogger("post_instagram")

INSTAGRAM_API = "https://graph.instagram.com/v21.0"
REPO_RAW = "https://raw.githubusercontent.com/tuntharm/FrontBrief-AI/main"
MAX_CAPTION = 2200
BRAND = "FrontBrief.AI"
SLOGAN = "A daily brief from the AI frontier."
# Instagram caption hashtags: at most 5, and the LAST one must be #FrontBriefAI.
HASHTAGS = "#AI #ArtificialIntelligence #TechNews #AINews #FrontBriefAI"


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


def newest_article() -> Path:
    articles = sorted(ARTICLES_DIR.glob("????-??-??-ai-brief.md"), reverse=True)
    if not articles:
        raise FileNotFoundError("No article files found in articles/")
    return articles[0]


def poster_url_for(article: Path) -> str:
    date = article.stem.replace("-ai-brief", "")
    return f"{REPO_RAW}/social/poster/{date}-ai-brief.png"


def caption_file_for(article: Path) -> Path:
    return CAPTION_DIR / f"{article.stem}.txt"


def load_caption(article: Path) -> str | None:
    """Return the routine-authored IG caption for this day, if present."""
    path = caption_file_for(article)
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8").strip()
    return text or None


def build_caption(article_text: str) -> str:
    # Pull headline from first Top 5 item
    headline_m = re.search(r"^### 1\. (.+)$", article_text, re.MULTILINE)
    headline = headline_m.group(1).strip() if headline_m else BRAND

    # Pull the single "Why it's interesting" sentence
    why_m = re.search(r"-\s*Why it.s interesting:\s*(.+)", article_text)
    why = why_m.group(1).strip() if why_m else ""

    # Pull first sentence of Money Map
    money_m = re.search(r"## Money Map\s+(.+?)(?:\n\n|\n#)", article_text, re.DOTALL)
    money_line = ""
    if money_m:
        first_sentence = money_m.group(1).strip().split(". ")[0]
        money_line = f"Money view: {first_sentence}."

    parts = [f"{BRAND} — {SLOGAN}", f"\n{headline}"]
    if why:
        parts.append(f"\n{why}")
    if money_line:
        parts.append(f"\n{money_line}")
    parts.append(f"\n{HASHTAGS}")

    caption = "\n".join(parts)
    if len(caption) > MAX_CAPTION:
        budget = MAX_CAPTION - len(HASHTAGS) - 10
        caption = caption[:budget].rsplit("\n", 1)[0] + f"\n\n{HASHTAGS}"
    return caption


def create_container(user_id: str, token: str, image_url: str, caption: str) -> str:
    resp = requests.post(
        f"{INSTAGRAM_API}/{user_id}/media",
        params={"image_url": image_url, "caption": caption, "access_token": token},
        timeout=30,
    )
    resp.raise_for_status()
    container_id = resp.json()["id"]
    LOGGER.info("Created media container: %s", container_id)
    return container_id


def wait_for_container(token: str, container_id: str, max_wait: int = 90) -> None:
    for _ in range(max_wait // 5):
        resp = requests.get(
            f"{INSTAGRAM_API}/{container_id}",
            params={"fields": "status_code", "access_token": token},
            timeout=15,
        )
        resp.raise_for_status()
        status = resp.json().get("status_code", "IN_PROGRESS")
        LOGGER.info("Container status: %s", status)
        if status == "FINISHED":
            return
        if status == "ERROR":
            raise RuntimeError("Instagram container processing failed with ERROR status")
        time.sleep(5)
    raise TimeoutError("Instagram container did not finish within %ds" % max_wait)


def publish_container(user_id: str, token: str, container_id: str) -> str:
    resp = requests.post(
        f"{INSTAGRAM_API}/{user_id}/media_publish",
        params={"creation_id": container_id, "access_token": token},
        timeout=30,
    )
    resp.raise_for_status()
    post_id = resp.json()["id"]
    LOGGER.info("Published post: %s", post_id)
    return post_id


def main() -> int:
    configure_logging()
    user_id = required_env("INSTAGRAM_USER_ID")
    token = required_env("INSTAGRAM_ACCESS_TOKEN")

    article = newest_article()
    image_url = poster_url_for(article)

    LOGGER.info("Posting poster: %s", image_url)
    caption = load_caption(article)
    if caption:
        LOGGER.info("Using routine-authored caption: %s", caption_file_for(article))
    else:
        LOGGER.info("No caption file found; building caption from the article")
        caption = build_caption(article.read_text(encoding="utf-8"))
    LOGGER.info("Caption (%d chars):\n%s", len(caption), caption)

    container_id = create_container(user_id, token, image_url, caption)
    wait_for_container(token, container_id)
    publish_container(user_id, token, container_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
