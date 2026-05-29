from __future__ import annotations

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from openai import OpenAI

from utils import (
    CONFIG_DIR,
    DATA_DIR,
    REPORTS_DIR,
    clamp_score,
    configure_logging,
    ensure_directories,
    graceful_truncate,
    load_yaml,
    london_report_date,
    read_json,
    write_json,
    write_text,
)


LOGGER = configure_logging("summarise")
DEFAULT_MODEL = "gpt-5.4"
LINE_MAX_CHARS = 4490
SCORE_FIELDS = [
    "phd_relevance",
    "investment_relevance",
    "technical_novelty",
    "moat_implication",
    "urgency",
]

SYSTEM_INSTRUCTION = """You are an intelligence analyst for a PhD researcher and future deeptech founder/investor. Your job is to filter signal from noise. Be concise, technical where useful, and commercially aware. Do not hype. Do not include generic AI news unless it affects infrastructure economics, scientific ML, engineering simulation, deeptech commercialisation, or investment structure."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score AI/deeptech candidates and write reports.")
    parser.add_argument("--candidates", default=str(DATA_DIR / "news_candidates.json"))
    parser.add_argument("--scoring", default=str(CONFIG_DIR / "scoring.yml"))
    parser.add_argument("--report-date", default=None, help="Override YYYY-MM-DD report date.")
    return parser.parse_args()


def extract_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.lower().startswith("json"):
            stripped = stripped[4:].strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(stripped[start : end + 1])


def openai_json(client: OpenAI, model: str, system: str, user: str) -> dict[str, Any]:
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        response_format={"type": "json_object"},
    )
    content = completion.choices[0].message.content or "{}"
    return extract_json_object(content)


def compact_candidates(candidates: list[dict[str, Any]], limit: int = 60) -> list[dict[str, Any]]:
    sorted_candidates = sorted(candidates, key=lambda item: item.get("published_at") or "", reverse=True)
    compact: list[dict[str, Any]] = []
    for item in sorted_candidates[:limit]:
        compact.append(
            {
                "id": item.get("id"),
                "title": item.get("title"),
                "source": item.get("source"),
                "url": item.get("url"),
                "published_at": item.get("published_at"),
                "summary": item.get("summary"),
                "track": item.get("track"),
            }
        )
    return compact


def score_candidates(
    client: OpenAI,
    model: str,
    candidates: list[dict[str, Any]],
    scoring_config: dict[str, Any],
) -> list[dict[str, Any]]:
    prompt = {
        "task": "Score every candidate for a daily AI/deeptech intelligence brief. Return JSON only.",
        "audience": "Tharm, a PhD researcher in AI/surrogate modelling for engineering simulation and future deeptech founder/investor.",
        "score_fields": {
            "phd_relevance": "0-5 relevance to scientific ML, surrogate modelling, engineering AI, PhD research direction.",
            "investment_relevance": "0-5 relevance to AI infrastructure, deeptech markets, capex, supply chain, startup/funding/acquisition signals.",
            "technical_novelty": "0-5 technical novelty or research significance.",
            "moat_implication": "0-5 implication for defensibility, bottlenecks, talent, data, hardware, or commercial moat.",
            "urgency": "0-5 need to read now rather than monitor.",
        },
        "weights": scoring_config.get("weights", {}),
        "rules": scoring_config.get("inclusion_rules", {}),
        "ignore": scoring_config.get("guidance", {}).get("ignore", []),
        "output_schema": {
            "scored_candidates": [
                {
                    "candidate_id": "string, must match input id",
                    "scores": {
                        "phd_relevance": "integer 0-5",
                        "investment_relevance": "integer 0-5",
                        "technical_novelty": "integer 0-5",
                        "moat_implication": "integer 0-5",
                        "urgency": "integer 0-5",
                    },
                    "score_reason": "one concise line",
                    "suggested_section": "market | research | engineering | watchlist | ignore",
                }
            ]
        },
        "candidates": compact_candidates(candidates),
    }
    result = openai_json(client, model, SYSTEM_INSTRUCTION, json.dumps(prompt, ensure_ascii=False))
    scored = result.get("scored_candidates", [])
    if not isinstance(scored, list):
        raise ValueError("OpenAI scoring response did not contain scored_candidates list")
    return scored


def apply_scoring_rules(
    candidates: list[dict[str, Any]],
    model_scores: list[dict[str, Any]],
    scoring_config: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidates_by_id = {str(item.get("id")): item for item in candidates}
    weights = scoring_config.get("weights", {})
    rules = scoring_config.get("inclusion_rules", {})
    min_weighted = float(rules.get("min_weighted_score", 3.0))
    min_raw = int(rules.get("min_raw_score", 15))
    max_selected = int(rules.get("max_selected_items", 5))

    enriched: list[dict[str, Any]] = []
    for scored in model_scores:
        candidate_id = str(scored.get("candidate_id", ""))
        candidate = candidates_by_id.get(candidate_id)
        if not candidate:
            continue
        scores_raw = scored.get("scores", {})
        scores = {field: clamp_score(scores_raw.get(field)) for field in SCORE_FIELDS}
        weighted_score = sum(float(weights.get(field, 0)) * scores[field] for field in SCORE_FIELDS)
        raw_score = sum(scores.values())
        decision = "include" if weighted_score >= min_weighted or raw_score >= min_raw else "ignore"
        enriched.append(
            {
                **candidate,
                "scores": scores,
                "weighted_score": round(weighted_score, 2),
                "raw_score": raw_score,
                "score_reason": str(scored.get("score_reason", "")).strip(),
                "suggested_section": str(scored.get("suggested_section", "watchlist")).strip().lower(),
                "decision": decision,
            }
        )

    enriched.sort(
        key=lambda item: (
            item.get("decision") == "include",
            item.get("weighted_score", 0),
            item.get("raw_score", 0),
            item.get("published_at") or "",
        ),
        reverse=True,
    )
    selected = [item for item in enriched if item["decision"] == "include"][:max_selected]
    for rank, item in enumerate(enriched, start=1):
        item["rank"] = rank
    return enriched, selected


def empty_report(report_date: str, reason: str) -> tuple[str, str]:
    full_report = f"""# Daily AI & Deeptech Brief — {report_date}

## TL;DR
- {reason}

## Market / Investment Signal
No high-quality market or investment signal passed the filter today.

## Research Signal
No high-quality research signal passed the filter today.

## Scientific ML / Engineering Simulation Signal
No high-quality scientific ML or engineering simulation signal passed the filter today.

## Founder Takeaway
There is no need to force a read today. Preserve attention for stronger signals that change infrastructure economics, simulation capability, defensibility, or timing.

## Watchlist
- AI infrastructure capex, supply constraints, and inference economics.
- Neural operators, GNN-based physics models, PDE surrogates, and rollout-stability work.
- Deeptech funding, policy, and acquisition moves in the UK, Thailand, and Asia.

## Scored Candidates
| Rank | Title | Track | PhD | Investment | Novelty | Moat | Urgency | Decision |
|---:|---|---|---:|---:|---:|---:|---:|---|
| - | No candidates | - | - | - | - | - | - | - |
"""
    digest = f"""Daily AI & Deeptech Brief — {report_date}

TL;DR:
1. {reason}

Top Signals:
1. No strong signal passed the filter today.

Founder/Researcher Takeaway:
Do not pad the pipeline with weak news. Monitor infrastructure economics and scientific ML for stronger evidence tomorrow.

Full report saved in GitHub: reports/{report_date}-brief.md"""
    return full_report, digest


def compose_report(
    client: OpenAI,
    model: str,
    report_date: str,
    scored_candidates: list[dict[str, Any]],
    selected: list[dict[str, Any]],
    scoring_config: dict[str, Any],
) -> tuple[str, str]:
    strong_note = ""
    threshold = int(scoring_config.get("inclusion_rules", {}).get("fewer_strong_items_note_threshold", 3))
    if len(selected) < threshold:
        strong_note = "Fewer than 3 high-quality signals passed the threshold today. Do not pad the brief."

    prompt = {
        "task": "Write the full Markdown report and one LINE digest. Return JSON only.",
        "report_date": report_date,
        "style": [
            "English only.",
            "Sharp and concise.",
            "No motivational filler.",
            "No generic hype.",
            "Avoid saying revolutionary unless justified.",
            "Be direct about weak signals.",
            "If selected_items is empty, say there was no high-quality news and do not pad.",
            "Use selected_items only for the main report sections and Top Signals.",
            "Do not promote ignored candidates into narrative sections; ignored items may appear only in the Scored Candidates table.",
        ],
        "strong_note": strong_note,
        "full_report_required_format": """# Daily AI & Deeptech Brief — YYYY-MM-DD

## TL;DR
- Maximum 3 bullets.

## Market / Investment Signal
### [Headline]
- Source:
- Link:
- What happened:
- Why it matters:
- Investment implication:
- Moat implication:
- Action: Read now / Monitor / Ignore

## Research Signal
### [Headline]
- Source:
- Link:
- What happened:
- Technical significance:
- What this may replace or weaken:
- Relevance to scientific ML / engineering AI:
- Action: Read now / Monitor / Ignore

## Scientific ML / Engineering Simulation Signal
### [Headline]
- Source:
- Link:
- What happened:
- Why it matters technically:
- Relevance to Tharm's PhD:
- Risk / limitation:
- Action: Read now / Monitor / Ignore

## Founder Takeaway
One sharp paragraph.

## Watchlist
Three things to monitor next.

## Scored Candidates
| Rank | Title | Track | PhD | Investment | Novelty | Moat | Urgency | Decision |""",
        "line_digest_required_format": f"""Daily AI & Deeptech Brief — {report_date}

TL;DR:
1. ...
2. ...
3. ...

Top Signals:
1. [Headline] — one-line why it matters.

Founder/Researcher Takeaway:
...

Full report saved in GitHub: reports/{report_date}-brief.md""",
        "line_digest_max_chars": LINE_MAX_CHARS,
        "selected_items": selected,
        "scored_candidates": scored_candidates[:30],
        "output_schema": {
            "full_report": "markdown string",
            "line_digest": "plain text string under 4500 characters",
        },
    }
    result = openai_json(client, model, SYSTEM_INSTRUCTION, json.dumps(prompt, ensure_ascii=False))
    full_report = str(result.get("full_report", "")).strip()
    line_digest = str(result.get("line_digest", "")).strip()
    if not full_report.startswith("# Daily AI & Deeptech Brief"):
        raise ValueError("OpenAI composition response did not include a valid full_report")
    if "Full report saved in GitHub:" not in line_digest:
        line_digest = line_digest.rstrip() + f"\n\nFull report saved in GitHub: reports/{report_date}-brief.md"
    if len(selected) < threshold and "Fewer than 3 high-quality signals" not in full_report:
        note = "- Fewer than 3 high-quality signals passed the threshold today; weak items were not included.\n"
        full_report = full_report.replace("## TL;DR\n", f"## TL;DR\n{note}", 1)
    line_digest = graceful_truncate(
        line_digest,
        LINE_MAX_CHARS,
        "\n\n[Truncated to fit LINE. Full report is in GitHub.]",
    )
    return full_report, line_digest


def main() -> int:
    args = parse_args()
    ensure_directories()
    report_date = args.report_date or os.getenv("REPORT_DATE") or london_report_date()
    candidates_payload = read_json(Path(args.candidates), default={"items": []})
    scoring_config = load_yaml(Path(args.scoring))
    candidates = list(candidates_payload.get("items", []))

    if not candidates:
        reason = "No fresh public candidate items were found in the configured lookback window."
        full_report, digest = empty_report(report_date, reason)
        write_text(REPORTS_DIR / f"{report_date}-brief.md", full_report)
        write_text(REPORTS_DIR / "latest_line_digest.txt", digest)
        write_json(
            DATA_DIR / "scored_candidates.json",
            {"generated_at": datetime.now(UTC).isoformat(), "items": []},
        )
        LOGGER.info("No candidates found; wrote empty report")
        return 0

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required to score and summarise candidates")
    model = os.getenv("OPENAI_MODEL") or DEFAULT_MODEL
    client = OpenAI(api_key=api_key)

    LOGGER.info("Scoring %d candidates with model %s", min(len(candidates), 60), model)
    model_scores = score_candidates(client, model, candidates, scoring_config)
    scored_candidates, selected = apply_scoring_rules(candidates, model_scores, scoring_config)
    write_json(
        DATA_DIR / "scored_candidates.json",
        {
            "generated_at": datetime.now(UTC).isoformat(),
            "model": model,
            "selected_count": len(selected),
            "items": scored_candidates,
        },
    )

    if not selected:
        reason = "No candidate passed the quality threshold today; weak or generic items were intentionally excluded."
        full_report, digest = empty_report(report_date, reason)
    else:
        LOGGER.info("Composing report with %d selected items", len(selected))
        full_report, digest = compose_report(client, model, report_date, scored_candidates, selected, scoring_config)

    write_text(REPORTS_DIR / f"{report_date}-brief.md", full_report)
    write_text(REPORTS_DIR / "latest_line_digest.txt", digest)
    LOGGER.info("Wrote reports/%s-brief.md and reports/latest_line_digest.txt", report_date)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
