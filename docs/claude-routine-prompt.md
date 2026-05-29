# Claude Routine Prompt

Every day at 07:00 Europe/London, create an English AI-world intelligence brief.

Search recent high-quality sources from the last 24-48 hours.

Important repository rules:
- Do not rebuild this repository.
- Do not restore the old GitHub Actions + OpenAI API pipeline.
- Do not create or edit `scripts/fetch_news.py`, `scripts/summarise.py`, `scripts/utils.py`, `config/sources.yml`, `config/scoring.yml`, or `routine/claude-daily-brief.md`.
- Do not write the brief to `reports/`.
- Only create or update one article file under `articles/`.
- GitHub Actions will handle LINE dispatch after the article is pushed.
- Do not send LINE from Claude Routine.
- Do not use OpenAI API, Anthropic API, or any model API key.
- Every selected item must include a direct public source link.
- Prefer primary sources and high-quality reporting. Do not cite paywalled pages unless the public metadata alone is sufficient.

Audience:
- Tharm is a PhD researcher in AI/surrogate modelling for engineering simulation and a future deeptech founder/investor.
- The PhD/deeptech lens is useful, but it must be one section only. Do not let it dominate the brief.

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

After writing the file:
- Commit only the article file.
- Push it to the repository.
- Commit message:
  Add daily AI brief YYYY-MM-DD
