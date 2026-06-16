# Claude Routine Prompt

The product is **FrontBrief.AI** — slogan: *"A daily brief from the AI frontier."* Use
"FrontBrief.AI" as the brand name on every public surface (article H1, LINE Digest header, poster
mark/button, Instagram caption). The internal file slug `YYYY-MM-DD-ai-brief.md/.png` stays as-is.

Every day at 05:00 Europe/London, create an English AI-world intelligence brief.
Search recent high-quality sources from the last 24-48 hours.

Repository rules:
- Do not rebuild this repo or restore the old GitHub Actions + OpenAI pipeline.
- Do not create/edit scripts/fetch_news.py, scripts/summarise.py, scripts/utils.py,
  config/sources.yml, config/scoring.yml, routine/claude-daily-brief.md, or
  .github/workflows/daily-brief.yml.
- Do not write to reports/. Do not send LINE. Do not use any model API key.
- Every item must include a direct public source link; prefer primary/high-quality sources.

Audience: Tharm — PhD in AI/surrogate modelling, future deeptech founder/investor. Deeptech is one
slot only; lead with the broad AI world.

Selection (interestingness-first, pick EXACTLY 5):
- #1 is the single most must-know story in AI today: a frontier model launch/ban/retirement, a big
  capability jump, a regulatory shock with teeth, a major funding round, or a big-name "next
  winner" call.
- Rank the rest by importance x how interesting/shareable across the whole AI world.
- Breadth is a guide, NOT a quota. Include an item only if genuinely interesting — never add an
  analyst report or procedural legal update just to fill a slot.
- Favor: hot funding rounds/valuations, the buzzy startup everyone's watching, model
  launches/bans/benchmark jumps, influential-people calls, surprising M&A or strategy pivots.
- Downweight: routine capex/analyst forecasts (unless shocking), regulatory procedure (unless
  immediately material), incremental papers (keep only landmark, named-system, real-world ones).
- Slots: 1) Must-Know 2) Interesting Company/Startup 3) Money/Market/NVIDIA/Compute
  4) Product/Model/Adoption 5) Deeptech/Research Lens.
- If fewer than 5 strong signals exist, say so; do not pad.

Output file: articles/YYYY-MM-DD-ai-brief.md

Format:

# FrontBrief.AI — YYYY-MM-DD

## LINE Digest
(Sent to LINE verbatim — standalone & punchy, every sentence makes sense alone with NO "yesterday"
references, under 4490 chars, plain text, no code fences. Shape:)

    FrontBrief.AI — YYYY-MM-DD

    TL;DR:
    1. Biggest thing.
    2. Most interesting company / money move.
    3. One technical / deeptech thing worth knowing.

    1. <Headline>
    Why interesting: <one standalone sentence>
    Investment angle: <one sentence — signal, not advice; no live prices>
    Action: Read / Track / Ignore
    Link: <direct public URL>

    2. ... (five items total)

    Money view:
    <2-3 sentences: where capital + pricing momentum moved + names/themes to watch. Signal, not advice.>

    Full report: articles/YYYY-MM-DD-ai-brief.md

## TL;DR
3 standalone bullets: (1) most important, (2) most interesting company/money move, (3) one tech/deeptech thing.

## Top 5
For each item:
### N. [Headline]
- Category: (Must-Know / Interesting Company / Money-Market-NVIDIA-Compute / Product-Model-Adoption / Deeptech-Research)
- Why it's interesting:
- Why it matters:
- Investment angle: (who's moving / what to watch — public ticker, private round, or theme; directional only. Signal, not advice; no live prices.)
- Tharm relevance:
- Action: Read / Track / Ignore
- Link: direct public URL

## Money Map
One tight paragraph — where capital + pricing momentum moved + names/themes to watch. Signal, not advice.

## Watchlist
Three catalysts to monitor next.

Style: English only. Sharp, concise, no hype, no filler. Interestingness-first. Investment framing
is signal, not advice (no price targets/buy-sell calls/live prices). LINE Digest is the send
surface; Top 5 is the full evidence trail with links.

Daily social poster (after the article):
- Single Canva parent file holds the series; append one new page per day. Parent design ID:
  DAHMpIU_j38 (edit: https://www.canva.com/d/bMWYO56xKFXmTz6).
- AI-write the copy from the #1 Must-Know story: a short news HEADLINE (keep ~2 lines — long ones
  overflow into the subhead) + a one-line SUBHEAD with the key fact/number. Lead with the news.
- AI-pick the image (most important — pick for SPECIFICITY, not just "on theme"): choose the image
  that visually ties to THIS exact story — it should carry the company's identity or announcement
  context (its logo, a launch/keynote slide, the product, the exec on stage, the venue). A branded
  announcement visual or a real press/event photo of the actual people/company beats a generic
  AI/robot/office/circuit stock photo every time, even a nice-looking one. Real photos of
  identifiable people ARE allowed for editorial news use. Prefer official press-kit / the company's
  own announcement visual / Creative Commons / properly-licensed sources; credit where appropriate.
  Image priority: (1) story-specific/branded visual (announcement, keynote slide, product, exec on
  stage); (2) if none, a clean LOGO-BASED brand shot — the company's logo on a phone/screen, like
  the Anthropic poster — a strong fallback; (3) only then a generic on-theme image. Off-topic is
  never acceptable. Upload via Canva upload-asset-from-url.
- PERSON-CENTRIC stories MUST use a real photo of that person (e.g. "Bezos raises $12B" → a good
  Bezos photo, NOT a generic robot/office image). Prefer a clean, recognisable shot, ideally with
  company logo/context in frame (e.g. Bezos before the Amazon logo). Crop for the image area: the
  background fill is the TOP region (1080×900, landscape-ish) and the bottom ~450px is hidden by the
  scrim + headline/subhead, so keep the face/subject in the UPPER part of the photo. Note: Wikimedia
  direct URLs FAIL upload-asset-from-url (server-side fetch blocked) — use a hotlinkable direct CDN
  URL (no redirect); if none can be fetched, place the person photo into the Canva page manually
  rather than shipping a generic fallback.
- COPY page 1 of the parent series (the master — the two FrontBrief.AI logos are already placed: FB
  monogram top-right, wordmark in the bottom-right pill). Change ONLY: category pill, headline,
  subhead, and background image (update_fill the background — it is now UNLOCKED, so the swap is
  clean and the logos stay put). Do NOT move, recolor, or re-place the logos. Do NOT regenerate.
- Locked style: IG 1080x1350 portrait; "AI · [category]" pill top-left; "FRONTBRIEF.AI · DD MON YYYY"
  mark top-right; bottom gradient scrim with bold HEADLINE + one-line SUBHEAD; FrontBrief.AI wordmark
  in the bottom-right pill. Clean and professional — NO decorative dot/circle patterns or clutter.
- Balance check before finishing: view the page thumbnail and confirm it's balanced — headline ~2
  lines, subhead concise (~2 lines) sitting just above the button (not sinking to the bottom), both
  logos visible, nothing cramped or off-centre. Nudge element positions (e.g. subhead top) if needed.
- Append the finished page to DAHMpIU_j38 (Canva merge-designs, insert at end).
- Export the page as a pro PNG to get the Canva export URL, and write that URL (one line) to
  social/poster/YYYY-MM-DD-ai-brief.png.url. Add a row to social/poster/index.md (date, headline, Canva view link).
  The commit-poster.yml workflow downloads the PNG on GitHub's network and commits the .png — the
  routine does NOT need Canva on its egress allowlist.

Daily Instagram caption (after the poster):
- Write the caption for the same #1 story to social/caption/YYYY-MM-DD-ai-brief.txt. The
  post-instagram.yml workflow posts it verbatim with the day's poster (falls back to the article
  if missing).
- Plain text, English, lead with the news hook. 1–3 short lines: headline hook → key fact/number →
  optional money/investment angle (signal, not advice). A light CTA is fine ("Full brief in bio").
- Hashtags: AT MOST 5, on the last line, and the LAST one MUST be #FrontBriefAI.
  Example: #AI #Anthropic #AINews #TechNews #FrontBriefAI

After writing the files:
- Commit the article file, social/poster/YYYY-MM-DD-ai-brief.png.url, social/poster/index.md, and
  social/caption/YYYY-MM-DD-ai-brief.txt.
- Push to the repo, then merge into main and push main.
- Commit message: Add daily AI brief YYYY-MM-DD
