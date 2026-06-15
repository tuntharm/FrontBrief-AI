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
`FrontBrief.AI` button bottom-right. Imagery is AI-generated and on-theme — no real photos of
identifiable people and no third-party brand logos.

## Network requirement

Exporting/downloading the PNG needs these hosts on the environment's network egress allowlist:
`export-download.canva.com`, `design.canva.ai`, `*.canva.com`. If they are not allowlisted the
routine still appends the Canva page and records links in `index.md`, but cannot commit the PNG.

See `index.md` for the per-day log.
