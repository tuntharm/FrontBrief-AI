# FrontBrief.AI — Posters

Social posters (Instagram, 1080×1350 portrait) that accompany each daily brief in `articles/`.

## How it works

- Codex chooses the single most shareable story from the Brief Five.
- It writes `YYYY-MM-DD-ai-brief.poster.json` with copy, shape, story/source dates, visual
  provenance, and a direct image URL.
- `scripts/validate_newsroom.py` applies the hard freshness, duplicate, source, and channel gates.
- `.github/workflows/commit-poster.yml` runs `scripts/render_poster.py` on GitHub's network and
  commits `YYYY-MM-DD-ai-brief.png`.
- The historical Canva parent (`DAHMpIU_j38`) remains a visual archive/reference, not a production
  dependency.

## Template style (locked)

The current locked geometry follows the approved committed series:

- 1080×1350 RGB PNG.
- Story-specific image from `y=0` to `y=899`.
- Hard `#0A0A0A` editorial panel from `y=900` to the bottom.
- `AI · CATEGORY` at top-left of the panel.
- White FB monogram at top-right of the image.
- Uppercase two- or three-line headline, concise one- or two-line subhead, and the canonical
  FrontBrief.AI pill.

No decorative clutter, generic substitutions, bare-logo backgrounds, or unverified person images.

## Network requirement

The direct image URL in the poster spec must be publicly fetchable from GitHub Actions. A failed
fetch, invalid image, gate failure, or text overflow fails the workflow; it never silently ships a
generic fallback. Legacy Canva `.png.url` pointers remain supported only for migration history.

See `index.md` for the per-day log. The matching Instagram captions live in `../caption/`.
