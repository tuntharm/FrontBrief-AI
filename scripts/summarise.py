from __future__ import annotations

import argparse
import os
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

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
    parse_datetime,
    read_json,
    write_json,
    write_text,
)


LOGGER = configure_logging("summarise")
LINE_MAX_CHARS = 4490
SCORE_FIELDS = [
    "phd_relevance",
    "investment_relevance",
    "technical_novelty",
    "moat_implication",
    "urgency",
]

TRACK_BONUSES = {
    "ai_infrastructure": {"investment_relevance": 2, "moat_implication": 1, "urgency": 1},
    "markets_investment": {"investment_relevance": 2, "moat_implication": 1, "urgency": 1},
    "frontier_research": {"phd_relevance": 1, "technical_novelty": 2},
    "scientific_ml": {"phd_relevance": 2, "technical_novelty": 2},
    "engineering_simulation": {"phd_relevance": 2, "technical_novelty": 1, "moat_implication": 1},
    "aerospace_robotics_shm": {"phd_relevance": 1, "technical_novelty": 1, "moat_implication": 1},
    "deeptech_policy_startups": {"investment_relevance": 1, "moat_implication": 1, "urgency": 1},
}

KEYWORDS = {
    "phd_relevance": [
        "scientific machine learning",
        "surrogate",
        "neural operator",
        "fourier neural operator",
        "deeponet",
        "graph neural",
        "gnn",
        "meshgraphnet",
        "graphcast",
        "physics-informed",
        "pde",
        "finite element",
        "fea",
        "cfd",
        "simulation",
        "computational fluid",
        "structural dynamics",
        "structural health",
        "digital twin",
        "aerospace",
        "robotics",
        "rollout",
        "boundary condition",
    ],
    "investment_relevance": [
        "nvidia",
        "amd",
        "tsmc",
        "broadcom",
        "hyperscaler",
        "gpu",
        "accelerator",
        "ai server",
        "data center",
        "datacenter",
        "hbm",
        "memory",
        "networking",
        "ethernet",
        "infiniband",
        "capex",
        "capacity",
        "supply chain",
        "inference",
        "energy",
        "cooling",
        "funding",
        "raises",
        "acquisition",
        "startup",
        "investment",
    ],
    "technical_novelty": [
        "research",
        "paper",
        "arxiv",
        "nature",
        "science",
        "benchmark",
        "dataset",
        "architecture",
        "model",
        "method",
        "open source",
        "open-source",
        "introduces",
        "announces",
        "released",
        "launches",
    ],
    "moat_implication": [
        "capacity",
        "cowos",
        "advanced packaging",
        "foundry",
        "supply chain",
        "proprietary",
        "partnership",
        "exclusive",
        "ecosystem",
        "platform",
        "deployment",
        "customer",
        "talent",
        "acquires",
        "acquisition",
        "infrastructure",
        "energy",
        "cooling",
        "data center",
        "datacenter",
    ],
    "urgency": [
        "announces",
        "launches",
        "released",
        "raises",
        "acquires",
        "acquisition",
        "earnings",
        "guidance",
        "policy",
        "regulation",
        "ban",
        "export control",
        "partnership",
        "contract",
        "deployment",
    ],
}

IGNORE_KEYWORDS = [
    "prompt engineering",
    "consumer app",
    "chatbot",
    "productivity tips",
    "top 10",
    "how to use",
    "opinion",
    "will change everything",
    "social media",
    "image generator",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score AI/deeptech candidates and write reports.")
    parser.add_argument("--candidates", default=str(DATA_DIR / "news_candidates.json"))
    parser.add_argument("--scoring", default=str(CONFIG_DIR / "scoring.yml"))
    parser.add_argument("--report-date", default=None, help="Override YYYY-MM-DD report date.")
    return parser.parse_args()


def text_for_item(item: dict[str, Any]) -> str:
    return " ".join(
        str(item.get(field, ""))
        for field in ("title", "summary", "source", "track")
    ).lower()


def keyword_hits(text: str, keywords: list[str]) -> list[str]:
    return [keyword for keyword in keywords if keyword in text]


def recency_score(item: dict[str, Any]) -> int:
    published_at = parse_datetime(item.get("published_at"))
    if not published_at:
        return 1
    age_hours = (datetime.now(UTC) - published_at).total_seconds() / 3600
    if age_hours <= 24:
        return 2
    if age_hours <= 48:
        return 1
    return 0


def score_item(item: dict[str, Any]) -> dict[str, Any]:
    text = text_for_item(item)
    track = str(item.get("track", ""))
    score_map = {field: 0 for field in SCORE_FIELDS}
    matched_terms: dict[str, list[str]] = {}

    for field, bonus in TRACK_BONUSES.get(track, {}).items():
        score_map[field] += bonus

    for field, keywords in KEYWORDS.items():
        hits = keyword_hits(text, keywords)
        matched_terms[field] = hits[:5]
        score_map[field] += min(3, len(hits))

    score_map["urgency"] += recency_score(item)

    penalty_hits = keyword_hits(text, IGNORE_KEYWORDS)
    if penalty_hits:
        score_map["phd_relevance"] -= 2
        score_map["investment_relevance"] -= 2
        score_map["technical_novelty"] -= 1
        score_map["moat_implication"] -= 1
        score_map["urgency"] -= 1

    scores = {field: clamp_score(value) for field, value in score_map.items()}
    reason_terms = sorted({term for terms in matched_terms.values() for term in terms})[:5]
    if penalty_hits:
        reason = f"Filtered down for low-signal terms: {', '.join(penalty_hits[:3])}."
    elif reason_terms:
        reason = f"Matched {track} signal terms: {', '.join(reason_terms)}."
    else:
        reason = f"Track-level signal from {track}, but limited supporting keywords."

    return {
        "candidate_id": item.get("id"),
        "scores": scores,
        "score_reason": reason,
        "suggested_section": suggested_section(item, scores),
    }


def suggested_section(item: dict[str, Any], scores: dict[str, int]) -> str:
    track = str(item.get("track", ""))
    if track in {"ai_infrastructure", "markets_investment", "deeptech_policy_startups"}:
        return "market"
    if track in {"scientific_ml", "engineering_simulation", "aerospace_robotics_shm"}:
        return "engineering"
    if scores["technical_novelty"] >= scores["investment_relevance"]:
        return "research"
    return "market"


def score_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sorted_candidates = sorted(candidates, key=lambda item: item.get("published_at") or "", reverse=True)
    return [score_item(item) for item in sorted_candidates[:80]]


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
        candidate = candidates_by_id.get(str(scored.get("candidate_id", "")))
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


def first_sentence(text: str, fallback: str, limit: int = 220) -> str:
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    if not text:
        text = fallback
    parts = re.split(r"(?<=[.!?])\s+", text)
    sentence = parts[0] if parts else text
    if len(sentence) > limit:
        sentence = sentence[: limit - 3].rsplit(" ", 1)[0].rstrip() + "..."
    return sentence


def action_for(item: dict[str, Any]) -> str:
    scores = item.get("scores", {})
    if item.get("weighted_score", 0) >= 3.8 or scores.get("urgency", 0) >= 4:
        return "Read now"
    if item.get("decision") == "include":
        return "Monitor"
    return "Ignore"


def why_it_matters(item: dict[str, Any]) -> str:
    section = item.get("suggested_section")
    if section == "market":
        return "Potential signal on AI infrastructure economics, supply constraints, capex, or strategic positioning."
    if section == "engineering":
        return "Potential signal for scientific ML, simulation acceleration, digital twins, or engineering AI workflows."
    return "Potential research signal that may affect model capability, methods, or technical direction."


def escape_table(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def item_block(item: dict[str, Any], section: str) -> str:
    title = item.get("title", "Untitled")
    source = item.get("source", "Unknown")
    link = item.get("url", "")
    summary = first_sentence(item.get("summary"), str(title))
    reason = item.get("score_reason", "")
    action = action_for(item)

    if section == "market":
        return f"""### {title}
- Source: {source}
- Link: {link}
- What happened: {summary}
- Why it matters: {why_it_matters(item)}
- Investment implication: Watch whether this changes compute supply, margins, capex timing, or startup leverage.
- Moat implication: {reason}
- Action: {action}
"""
    if section == "research":
        return f"""### {title}
- Source: {source}
- Link: {link}
- What happened: {summary}
- Technical significance: {why_it_matters(item)}
- What this may replace or weaken: Existing assumptions, toolchains, or benchmarks if the result is validated.
- Relevance to scientific ML / engineering AI: {reason}
- Action: {action}
"""
    return f"""### {title}
- Source: {source}
- Link: {link}
- What happened: {summary}
- Why it matters technically: {why_it_matters(item)}
- Relevance to Tharm's PhD: Check for links to surrogate modelling, PDE learning, FEA/CFD acceleration, rollout stability, or digital twins.
- Risk / limitation: Metadata-only scoring; read the source before treating this as evidence.
- Action: {action}
"""


def empty_report(report_date: str, reason: str) -> tuple[str, str]:
    full_report = f"""# Daily AI & Deeptech Brief - {report_date}

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
    digest = f"""Daily AI & Deeptech Brief - {report_date}

TL;DR:
1. {reason}

Top Signals:
1. No strong signal passed the filter today.

Founder/Researcher Takeaway:
No model API was used. Do not pad the pipeline with weak news; monitor for stronger evidence tomorrow.

Full report saved in GitHub: reports/{report_date}-brief.md"""
    return full_report, digest


def section_text(title: str, selected: list[dict[str, Any]], section: str) -> str:
    items = [item for item in selected if item.get("suggested_section") == section]
    if not items:
        return f"## {title}\nNo high-quality {title.lower()} passed the filter today.\n"
    blocks = "\n".join(item_block(item, section).rstrip() for item in items)
    return f"## {title}\n{blocks}\n"


def tldr_bullets(selected: list[dict[str, Any]]) -> list[str]:
    bullets = []
    for item in selected[:3]:
        bullets.append(f"{item.get('title')} - {why_it_matters(item)}")
    return bullets or ["No high-quality signal passed the filter today; weak items were excluded."]


def founder_takeaway(selected: list[dict[str, Any]]) -> str:
    if not selected:
        return "No strong signal changes the research or founder map today. Keep the pipeline strict and wait for clearer evidence."
    tracks = sorted({str(item.get("track", "unknown")) for item in selected})
    return (
        "Today's selected signals cluster around "
        + ", ".join(tracks)
        + ". Treat this as a monitoring brief, not a final judgement: the no-API scorer preserves cost discipline, but important nuance still requires reading the linked source."
    )


def watchlist(selected: list[dict[str, Any]]) -> list[str]:
    base = [
        "AI infrastructure capex, accelerator supply, memory, networking, energy, and cooling.",
        "Scientific ML methods that improve PDE surrogate accuracy, stability, or boundary-condition generalisation.",
        "Deeptech funding, acquisition, policy, or talent movement that changes defensibility.",
    ]
    if not selected:
        return base
    top_tracks = [str(item.get("track")) for item in selected[:3]]
    return [f"Fresh signals in {track}." for track in top_tracks] + base[: max(0, 3 - len(top_tracks))]


def scored_table(scored_candidates: list[dict[str, Any]]) -> str:
    rows = [
        "| Rank | Title | Track | PhD | Investment | Novelty | Moat | Urgency | Decision |",
        "|---:|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in scored_candidates[:30]:
        scores = item.get("scores", {})
        rows.append(
            "| {rank} | {title} | {track} | {phd} | {investment} | {novelty} | {moat} | {urgency} | {decision} |".format(
                rank=item.get("rank", "-"),
                title=escape_table(item.get("title", "")),
                track=escape_table(item.get("track", "")),
                phd=scores.get("phd_relevance", 0),
                investment=scores.get("investment_relevance", 0),
                novelty=scores.get("technical_novelty", 0),
                moat=scores.get("moat_implication", 0),
                urgency=scores.get("urgency", 0),
                decision=escape_table(item.get("decision", "")),
            )
        )
    return "\n".join(rows)


def compose_report(
    report_date: str,
    scored_candidates: list[dict[str, Any]],
    selected: list[dict[str, Any]],
    scoring_config: dict[str, Any],
) -> tuple[str, str]:
    threshold = int(scoring_config.get("inclusion_rules", {}).get("fewer_strong_items_note_threshold", 3))
    bullets = tldr_bullets(selected)
    fewer_note = []
    if len(selected) < threshold:
        fewer_note.append("Fewer than 3 high-quality signals passed the threshold today; weak items were not included.")

    full_report = "\n".join(
        [
            f"# Daily AI & Deeptech Brief - {report_date}",
            "",
            "## TL;DR",
            *[f"- {bullet}" for bullet in fewer_note + bullets],
            "",
            section_text("Market / Investment Signal", selected, "market").rstrip(),
            "",
            section_text("Research Signal", selected, "research").rstrip(),
            "",
            section_text("Scientific ML / Engineering Simulation Signal", selected, "engineering").rstrip(),
            "",
            "## Founder Takeaway",
            founder_takeaway(selected),
            "",
            "## Watchlist",
            *[f"- {item}" for item in watchlist(selected)[:3]],
            "",
            "## Scored Candidates",
            scored_table(scored_candidates),
        ]
    )

    top_lines = [
        f"{index}. {item.get('title')} - {why_it_matters(item)}"
        for index, item in enumerate(selected[:3], start=1)
    ] or ["1. No strong signal passed the filter today."]
    digest = "\n".join(
        [
            f"Daily AI & Deeptech Brief - {report_date}",
            "",
            "TL;DR:",
            *[f"{index}. {bullet}" for index, bullet in enumerate(bullets[:3], start=1)],
            "",
            "Top Signals:",
            *top_lines,
            "",
            "Founder/Researcher Takeaway:",
            founder_takeaway(selected),
            "",
            f"Full report saved in GitHub: reports/{report_date}-brief.md",
        ]
    )
    digest = graceful_truncate(
        digest,
        LINE_MAX_CHARS,
        "\n\n[Truncated to fit LINE. Full report is in GitHub.]",
    )
    return full_report, digest


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
            {"generated_at": datetime.now(UTC).isoformat(), "scoring_mode": "deterministic_no_api", "items": []},
        )
        LOGGER.info("No candidates found; wrote empty report")
        return 0

    LOGGER.info("Scoring %d candidates with deterministic no-API rules", min(len(candidates), 80))
    candidate_scores = score_candidates(candidates)
    scored_candidates, selected = apply_scoring_rules(candidates, candidate_scores, scoring_config)
    write_json(
        DATA_DIR / "scored_candidates.json",
        {
            "generated_at": datetime.now(UTC).isoformat(),
            "scoring_mode": "deterministic_no_api",
            "selected_count": len(selected),
            "items": scored_candidates,
        },
    )

    if not selected:
        reason = "No candidate passed the quality threshold today; weak or generic items were intentionally excluded."
        full_report, digest = empty_report(report_date, reason)
    else:
        LOGGER.info("Composing no-API report with %d selected items", len(selected))
        full_report, digest = compose_report(report_date, scored_candidates, selected, scoring_config)

    write_text(REPORTS_DIR / f"{report_date}-brief.md", full_report)
    write_text(REPORTS_DIR / "latest_line_digest.txt", digest)
    LOGGER.info("Wrote reports/%s-brief.md and reports/latest_line_digest.txt", report_date)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
