# Claude Routine Prompt

The product is **FrontBrief.AI** — slogan: *"A daily brief from the AI frontier."* Use "FrontBrief.AI"
as the brand name on every public surface (article H1, LINE Digest header, poster mark/button,
Instagram caption). The internal file slug `YYYY-MM-DD-ai-brief.md/.png` stays as-is.

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

Selection rules (interestingness-first — pick exactly 5):
- Lead slot (#1) is the single most "must-know" story in AI today — the thing the field is
  actually talking about: a frontier model launch / ban / retirement, a dramatic capability jump,
  a regulatory shock with teeth, a major funding round, or a big-name "next winner" call.
- Rank the rest by importance x how interesting and shareable they are across the whole AI world.
- Breadth is a tiebreaker, NOT a quota. Use the five slots below as a guide, but only include an
  item if it is genuinely interesting — never add an analyst report or a procedural legal update
  just to fill a track.
- Favor: hot funding rounds and valuations, the buzzy startup everyone is watching, model
  launches/bans/big benchmark jumps, influential-people calls (e.g. Jensen/Altman naming a
  winner), surprising acquisitions or strategy pivots.
- Downweight: routine capex/analyst forecasts (unless the number is shocking), regulatory
  procedure (unless immediately material), incremental papers (keep only landmark, named-system,
  real-world ones).
- Suggested five slots: 1) Must-Know  2) Interesting Company / Startup  3) Money / Market /
  NVIDIA / Compute  4) Product / Model / Adoption  5) Deeptech / Research Lens.
- Every item must include a direct public source link.
- If fewer than 5 high-quality signals exist, say so and do not pad with weak stories.

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

# FrontBrief.AI — YYYY-MM-DD

## LINE Digest
This section is sent to LINE verbatim, so it must be standalone and punchy — every sentence must
make sense on its own with NO reference to "yesterday" or prior context. Keep it well under 4490
characters. Write it as plain text (no code fences), in exactly this shape:

    FrontBrief.AI — YYYY-MM-DD

    TL;DR:
    1. Biggest thing.
    2. Most interesting company / money move.
    3. One technical / deeptech thing worth knowing.

    1. <Headline>
    Why interesting: <one standalone sentence>
    Investment angle: <one standalone sentence — signal, not advice; no live prices>
    Action: Read / Track / Ignore
    Link: <direct public URL>

    2. ... (same shape, five items total)

    Money view:
    <2-3 sentences on where capital and pricing momentum moved + names/themes to watch.
    Signal, not advice.>

    Full report: articles/YYYY-MM-DD-ai-brief.md

## TL;DR
- 3 bullets: (1) most important thing, (2) most interesting company/startup/money move,
  (3) one technical/deeptech thing worth knowing. Each bullet stands alone.

## Top 5
For each of the five items use this per-item format:
### N. [Headline]
- Category: (Must-Know / Interesting Company / Money-Market-NVIDIA-Compute / Product-Model-Adoption / Deeptech-Research)
- Why it's interesting:
- Why it matters:
- Investment angle: (who's moving / what to watch — a public ticker, a private round, or a theme;
  directional only. Signal, not advice; no live prices.)
- Tharm relevance:
- Action: Read / Track / Ignore
- Link: direct public URL

## Money Map
One tight paragraph: where capital + pricing momentum moved this period and the names/themes worth
watching. Slightly fuller than the LINE "Money view". Signal, not advice; built from public
funding, pricing and news flow.

## Watchlist
Three catalysts to monitor next.

Style:
- English only.
- Sharp, concise, technical where useful. No hype, no motivational filler.
- Interestingness-first: lead with what matters most, not track coverage.
- Investment framing is signal, not advice — no price targets, no buy/sell calls, no live prices.
- The LINE Digest is the send surface (standalone); the Top 5 is the full evidence trail with links.

Daily social poster (after the article is written):

A single Canva "parent" file holds the whole series; each run appends one new page (one day =
one page) and exports that page as the committed PNG.

- Parent Canva design: "FrontBrief.AI — Poster Series", design ID `DAHMpIU_j38`
  (edit: https://www.canva.com/d/bMWYO56xKFXmTz6).
- Locked template style: Instagram post, 1080×1350 portrait, editorial tech-news look —
  full-bleed on-theme image; "AI · [category]" pill top-left; "FRONTBRIEF.AI · DD MON YYYY"
  mark top-right; bottom gradient scrim with a bold news HEADLINE, one-line SUBHEAD, and a small
  kicker (`metric · Source`); a "FrontBrief.AI" button bottom-right. Keep it clean and
  professional — NO decorative dot/circle patterns or clutter over the image.
- Subject company logo: include the logo of the company the lead story is about (Anthropic,
  NVIDIA, Cognition, etc.) as a small, tasteful mark — editorial/nominative use. Source the
  official logo as a public URL and add it via Canva `upload-asset-from-url`. Don't add logos of
  companies the story isn't about, and never imply endorsement.
- Imagery: AI-generated and on-theme only. No real photos of identifiable people. Third-party
  logos allowed ONLY for the subject company of the story.
- Steps:
  1. Use the brief's #1 Must-Know story as the poster story.
  2. Reframe it as marketing content — a short news headline + a one-line subhead with the key
     fact/number. Lead with the news, not a floating stat.
  3. Build the page by DUPLICATING page 1 of the parent series (the locked master — it already has
     the two FrontBrief.AI logos placed: FB monogram top-right, wordmark in the bottom-right pill).
     Change ONLY four things: category pill, headline, subhead, background image. Do NOT move,
     swap, recolor, or re-place the logos — they carry over. Do NOT regenerate from scratch.
  4. Append the page to `DAHMpIU_j38` via Canva `merge-designs` (insert at end).
  5. Export the page as a `pro` PNG to get its Canva export URL, and write that URL (one line) to
     `posters/YYYY-MM-DD-ai-brief.png.url`.
  6. Append a row to `posters/index.md` (date, headline, Canva view link).
- English only. The `commit-poster.yml` workflow downloads the PNG on GitHub's network and commits
  `posters/YYYY-MM-DD-ai-brief.png`, so the routine does NOT need Canva on its egress allowlist.

After writing the files:
- Commit the article file, the `posters/YYYY-MM-DD-ai-brief.png.url` pointer, and `posters/index.md`.
- Push it to the repository.
- Commit message:
  Add daily AI brief YYYY-MM-DD
