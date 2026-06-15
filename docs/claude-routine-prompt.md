# Claude Routine Prompt

Every day at 07:00 Europe/London, create an English AI-world intelligence brief.

Search recent high-quality sources from the last 24-48 hours.

Important repository rules:
- Do not rebuild this repository.
- Do not restore the old GitHub Actions + OpenAI API pipeline.
- Do not create or edit `scripts/fetch_news.py`, `scripts/summarise.py`, `scripts/utils.py`, `config/sources.yml`, `config/scoring.yml`, or `routine/claude-daily-brief.md`.
- Do not write the brief to `reports/`.
- Create or update one article file under `articles/`, plus that day's poster under `posters/`.
- GitHub Actions will handle LINE dispatch after the article is pushed.
- Do not send LINE from Claude Routine.
- Do not use OpenAI API, Anthropic API, or any model API key.
- Every selected item must include a direct public source link.
- Prefer primary sources and high-quality reporting. Do not cite paywalled pages unless the public metadata alone is sufficient.

Audience:
- Write for technically curious AI readers, builders, researchers, founders, investors, and operators who want a concise view of what changed in the AI world.
- Include Tharm's personal deeptech lens as one useful section, especially around AI for engineering simulation and deeptech commercialisation, but do not let it dominate the brief.

Selection rules:
- Pick the most important 5-7 items across the whole AI world.
- Do not select more than 2 items from Tharm's Deeptech Lens unless the day is unusually relevant.
- Usually include at least 1 Global AI / Frontier Models or AI policy/regulation item.
- Usually include at least 1 AI Infrastructure / Markets item.
- Usually include at least 1 Research / Technical Signal item.
- If a PhD-relevant item is interesting but niche, put it in `Tharm's Deeptech Lens` rather than the TL;DR.
- If fewer than 3 high-quality signals exist, say so and do not pad with weak stories.

Track definitions:

1. Global AI / Frontier Models
   OpenAI, Anthropic, Google DeepMind, Meta, Mistral, xAI, model releases, agent systems, multimodal AI, reasoning, safety, regulation.

2. AI Infrastructure / Markets
   NVIDIA, AMD, TSMC, Broadcom, hyperscaler capex, data centres, HBM, networking, energy, cooling, inference economics.

3. Research / Technical Signal
   Important papers from Nature Machine Intelligence, Nature, Science, arXiv, OpenReview, DeepMind, Microsoft Research, Google Research, NVIDIA Research. Include scientific ML when important, but do not over-weight surrogate modelling.

4. Product / Startup / Adoption Signal
   Enterprise AI, agent platforms, developer tools, robotics, healthcare AI, finance AI, legal AI, major funding rounds, acquisitions, notable product launches.

5. Tharm's Deeptech Lens
   Surrogate modelling, neural operators, GNNs for physics simulation, FEA/CFD acceleration, aerospace, SHM, robotics, digital twins. Include this section only when there is genuinely strong signal.

Ignore:
- generic chatbot launches
- prompt-engineering content
- consumer AI tools
- vague AI hype
- duplicated stories
- low-signal VC thought leadership
- old news unless newly strategically relevant

Output file:
articles/YYYY-MM-DD-ai-brief.md

Format:

# Daily AI Brief — YYYY-MM-DD

## TL;DR
- Exactly 3 bullets covering the broad AI world, not only engineering simulation.
- Each bullet should explain the strategic signal, not just the event.
- No links are needed here; this section is for the compressed strategic readout.

## Global AI / Frontier Models
For each selected item in this track:
### [Headline]
- Source: publication or organisation name
- Link: direct public URL to read the source
- What happened:
- Why it matters:
- Founder/investor relevance:
- Action: Read now / Monitor / Ignore

## AI Infrastructure / Markets
Use the same per-item format.

## Research / Technical Signal
Use the same per-item format.

## Product / Startup / Adoption Signal
Use the same per-item format.

## Tharm's Deeptech Lens
Include only when there is genuinely strong signal. Use the same per-item format.

## Founder / Investor Takeaway
One sharp paragraph.

## Watchlist
Three things to monitor next.

Style:
- English only.
- Sharp, concise, technical where useful.
- No hype.
- No motivational filler.
- Broad AI-world coverage first; Tharm's PhD lens is one section only.
- Do not pad with weak stories.
- TL;DR is the strategic summary.
- The five track sections are the clickable evidence trail with source links.

Daily social poster (after the article is written):

A single Canva "parent" file holds the whole series; each run appends one new page (one day =
one page) and exports that page as the committed PNG.

- Parent Canva design: "Daily AI Brief — Poster Series", design ID `DAHMpIU_j38`
  (edit: https://www.canva.com/d/bMWYO56xKFXmTz6).
- Locked template style: Instagram post, 1080×1350 portrait, editorial tech-news look —
  full-bleed on-theme image; "AI · [category]" pill top-left; "DAILY AI BRIEF · DD MON YYYY"
  mark top-right; bottom gradient scrim with a bold news HEADLINE, one-line SUBHEAD, and a small
  kicker (`metric · Source`); an "AI Brief" button bottom-right.
- Imagery: AI-generated and on-theme only. No real photos of identifiable people, no third-party
  brand logos.
- Steps:
  1. Pick the single most shareable lead story from the brief (usually a top "Read now" item).
  2. Reframe it as marketing content — a short news headline + a one-line subhead with the key
     fact/number. Lead with the news, not a floating stat.
  3. Generate the poster in the locked style, then append it as a new page to `DAHMpIU_j38`
     via Canva `merge-designs`.
  4. Export that page as a `pro` PNG and save it to `posters/YYYY-MM-DD-ai-brief.png`.
  5. Append a row to `posters/index.md` (date, headline, Canva view link).
- English only. If Canva hosts are not on the egress allowlist and the PNG download fails, still
  append the Canva page and record the links in `posters/index.md`; do not fail the run.

After writing the files:
- Commit only the article file, that day's poster PNG, and `posters/index.md`.
- Push it to the repository.
- Commit message:
  Add daily AI brief YYYY-MM-DD
