from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = PROJECT_ROOT / "articles"
REPORTS_DIR = PROJECT_ROOT / "reports"
MAX_LINE_CHARS = 4490


@dataclass
class TopSignal:
    headline: str
    why_it_matters: str
    link: str = ""


SIGNAL_SECTION_HEADINGS = [
    "Global AI / Frontier Models",
    "AI Infrastructure / Markets",
    "Research / Technical Signal",
    "Product / Startup / Adoption Signal",
    "Tharm's Deeptech Lens",
    "Tharm’s Deeptech Lens",
]


def newest_article() -> Path:
    articles = sorted(ARTICLES_DIR.glob("*.md"), key=article_sort_key, reverse=True)
    if not articles:
        raise FileNotFoundError("No Markdown articles found in articles/.")
    return articles[0]


def article_sort_key(path: Path) -> tuple[str, float, str]:
    match = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
    date_key = match.group(1) if match else "0000-00-00"
    return date_key, path.stat().st_mtime, path.name


def extract_report_date(path: Path, text: str) -> str:
    filename_match = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
    if filename_match:
        return filename_match.group(1)
    title_match = re.search(r"^#\s+.*?(\d{4}-\d{2}-\d{2})\s*$", text, flags=re.MULTILINE)
    if title_match:
        return title_match.group(1)
    return "unknown-date"


def section_body(text: str, heading: str) -> str:
    pattern = rf"^##\s+{re.escape(heading)}\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", text[start:], flags=re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def bullet_text(line: str) -> str:
    return re.sub(r"^\s*[-*]\s+", "", line).strip()


def extract_tldr(text: str) -> list[str]:
    body = section_body(text, "TL;DR")
    bullets = [bullet_text(line) for line in body.splitlines() if re.match(r"^\s*[-*]\s+", line)]
    return [first_sentence(bullet, limit=360) for bullet in bullets if bullet][:3]


def first_sentence(value: str, limit: int = 220) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    if not value:
        return "No concise rationale found in the article."
    sentence = re.split(r"(?<=[.!?])\s+", value)[0]
    if len(sentence) > limit:
        sentence = sentence[: limit - 3].rsplit(" ", 1)[0].rstrip() + "..."
    return sentence


def field_value(block: str, field_name: str) -> str:
    pattern = rf"^\s*[-*]\s+(?:\*\*)?{re.escape(field_name)}:?(?:\*\*)?\s*(.+?)\s*$"
    match = re.search(pattern, block, flags=re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def signal_source_body(text: str) -> str:
    top_signals = section_body(text, "Top Signals") or section_body(text, "Top 5")
    if top_signals:
        return top_signals

    bodies = [section_body(text, heading) for heading in SIGNAL_SECTION_HEADINGS]
    bodies = [body for body in bodies if body]
    return "\n\n".join(bodies) if bodies else text


def extract_top_signals(text: str) -> list[TopSignal]:
    body = signal_source_body(text)
    heading_matches = list(re.finditer(r"^###\s+(.+?)\s*$", body, flags=re.MULTILINE))
    signals: list[TopSignal] = []
    for index, match in enumerate(heading_matches[:5]):
        start = match.end()
        end = heading_matches[index + 1].start() if index + 1 < len(heading_matches) else len(body)
        block = body[start:end]
        why = (
            field_value(block, "Why it matters")
            or field_value(block, "Research/founder/investor relevance")
            or field_value(block, "What happened")
            or first_sentence(block)
        )
        signals.append(
            TopSignal(
                headline=match.group(1).strip(),
                why_it_matters=first_sentence(why),
                link=field_value(block, "Link"),
            )
        )
    return signals


def extract_founder_takeaway(text: str) -> str:
    body = section_body(text, "Founder / Investor Takeaway") or section_body(text, "Founder Takeaway")
    lines = [
        re.sub(r"^\s*[-*]\s+", "", line).strip()
        for line in body.splitlines()
        if line.strip()
    ]
    return first_sentence(" ".join(lines), limit=520)


def extract_line_digest_section(text: str) -> str:
    """Return the article's hand-written `## LINE Digest` section, if present.

    When the article author provides this section, it is sent to LINE verbatim
    (only truncated to the char limit) instead of mechanically extracting
    sentences from the long-form body. This keeps LINE messages standalone and
    punchy rather than scraping context-dependent prose.
    """
    return section_body(text, "LINE Digest")


def graceful_truncate(text: str, max_chars: int = MAX_LINE_CHARS) -> str:
    text = text.strip()
    if len(text) <= max_chars:
        return text
    suffix = "\n\n[Truncated. Full report is in GitHub.]"
    budget = max_chars - len(suffix)
    cut = text[:budget].rstrip()
    newline_cut = cut.rfind("\n")
    if newline_cut > budget * 0.65:
        cut = cut[:newline_cut].rstrip()
    else:
        space_cut = cut.rfind(" ")
        if space_cut > budget * 0.8:
            cut = cut[:space_cut].rstrip()
    return cut + suffix


def display_article_path(article_path: Path) -> str:
    resolved = article_path.resolve()
    try:
        return resolved.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return article_path.as_posix()


def build_digest(article_path: Path, text: str) -> str:
    report_date = extract_report_date(article_path, text)
    tldr = extract_tldr(text) or ["No TL;DR bullets found in the article."]
    top_signals = extract_top_signals(text)
    founder_takeaway = extract_founder_takeaway(text)

    top_lines: list[str] = []
    for index, signal in enumerate(top_signals[:5], start=1):
        top_lines.append(f"{index}. [{signal.headline}] — {signal.why_it_matters}")
        if signal.link:
            top_lines.append(f"   Read: {signal.link}")
    if not top_lines:
        top_lines = ["1. No signal sections found in the article."]

    digest = "\n".join(
        [
            f"FrontBrief.AI — {report_date}",
            "",
            "TL;DR:",
            *[f"{index}. {bullet}" for index, bullet in enumerate(tldr[:3], start=1)],
            "",
            "Top Signals:",
            *top_lines,
            "",
            "Founder Takeaway:",
            founder_takeaway,
            "",
            "Full report:",
            display_article_path(article_path),
        ]
    )
    return graceful_truncate(digest)


def main() -> int:
    article_path = newest_article()
    article_text = article_path.read_text(encoding="utf-8")
    digest_section = extract_line_digest_section(article_text)
    if digest_section:
        digest = graceful_truncate(digest_section)
    else:
        digest = build_digest(article_path, article_text)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORTS_DIR / "latest_line_digest.txt"
    output_path.write_text(digest.rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {output_path.relative_to(PROJECT_ROOT).as_posix()} from {article_path.relative_to(PROJECT_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
