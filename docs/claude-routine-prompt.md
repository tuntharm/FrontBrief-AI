# Claude Routine Prompt

Every day at 07:00 Europe/London, create an English AI/deeptech intelligence brief.

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

Prioritise:
- AI infrastructure
- NVIDIA, AMD, TSMC, Broadcom
- hyperscaler AI capex
- data centres, memory, networking, energy, cooling
- frontier AI research
- scientific machine learning
- neural operators
- GNNs for physics simulation
- MeshGraphNets successors
- GraphCast-style models
- surrogate modelling
- PDE learning
- FEA/CFD acceleration
- robotics, aerospace, SHM
- deeptech funding, acquisitions, policy, and talent movement
- UK/Thai/Asia deeptech commercialisation when relevant

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

# Daily AI & Deeptech Brief — YYYY-MM-DD

## TL;DR
- Maximum 3 bullets.
- Each bullet should explain the strategic signal, not just the event.

## Top Signals
For each selected item:
### [Headline]
- Source:
- Link:
- What happened:
- Why it matters:
- Research/founder/investor relevance:
- Action: Read now / Monitor / Ignore

## Scientific ML / Engineering Simulation Signal
Include when relevant.

## Market / Investment Signal
Include when relevant.

## Founder Takeaway
One sharp paragraph.

## Watchlist
Three things to monitor next.

Style:
- English only.
- Sharp, concise, technical where useful.
- No hype.
- No motivational filler.
- If fewer than 3 high-quality signals exist, say so.
- Do not pad with weak stories.

After writing the file:
- Commit only the article file.
- Push it to the repository.
- Commit message:
  Add daily AI brief YYYY-MM-DD
