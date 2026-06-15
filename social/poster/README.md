# FrontBrief.AI — Posters

Social posters (Instagram, 1080×1350 portrait) that accompany each daily brief in `articles/`.

## How it works

- A single Canva **parent** file holds the whole series — one page per day.
  - Design: **"FrontBrief.AI — Poster Series"**, design ID `DAHMpIU_j38`
  - Edit: https://www.canva.com/d/bMWYO56xKFXmTz6
  - View: https://www.canva.com/d/3cUi9X-xizO5rGJ
- Each routine run picks the single most shareable story from that day's brief, reframes it as
  an editorial news headline + subhead, generates a poster in the locked template style, appends
  it as a new page to the parent file, exports that page, and commits it here as
  `YYYY-MM-DD-ai-brief.png`.

## Template style (locked)

Editorial tech-news look: full-bleed on-theme image; an `AI · [category]` pill top-left; a
`FRONTBRIEF.AI · DD MON YYYY` mark top-right; a dark gradient scrim across the bottom carrying a
bold news headline, a one-line subhead, and a small kicker (`metric · Source`); and a
`FrontBrief.AI` button bottom-right. Keep it clean and professional — no decorative dot/circle
patterns over the image. Include the **subject company's logo** (the company the story is about)
as a small, tasteful mark (editorial use); imagery is otherwise AI-generated and on-theme — no
real photos of identifiable people and no logos of companies the story isn't about.

## Network requirement

The routine does NOT need Canva on its egress allowlist. It writes a one-line pointer file
`YYYY-MM-DD-ai-brief.png.url` (the Canva export URL); the `commit-poster.yml` workflow downloads
the PNG on GitHub's network and commits `YYYY-MM-DD-ai-brief.png` here. (If the routine container
does have egress, it may download and commit the PNG itself and skip the pointer.)

See `index.md` for the per-day log. The matching Instagram captions live in `../caption/`.
