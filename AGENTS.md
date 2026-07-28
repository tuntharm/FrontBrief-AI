# FrontBrief.AI — Codex Repository Instructions

Codex is the active Editor-in-Chief and automation orchestrator for this repository.

Before a newsroom run, read:

1. `docs/codex-routine-prompt.md` — active operating procedure and output contract.
2. `docs/DECISIONS.md` — editorial decisions, brand feedback, and historical gotchas.
3. `social/poster/ledger.json` and the latest seven dated articles — deterministic archive inputs.

`CLAUDE.md` and `docs/claude-routine-prompt.md` are retained as migration history. They are not the
active Codex instructions.

Hard operational rules:

- If `articles/YYYY-MM-DD-ai-brief.md` or `social/poster/YYYY-MM-DD-ai-brief.png` already exists for
  the London run date, stop without publishing. Report that the edition is already present.
- Never send LINE or Instagram directly. Publishing is triggered only by a validated push to
  `main`.
- Before committing, run `scripts/validate_newsroom.py` against the article, caption, poster spec,
  ledger, and archive.
- Canva design `DAHMpIU_j38` is the production poster parent. Duplicate its latest page, change only
  category/headline/subhead/background, preserve both logos and all typography/layout, then export
  only the new page as a 1080×1350 RGB PNG.
- `social/poster/YYYY-MM-DD-ai-brief.poster.json` is deterministic editorial metadata only. Never
  use `scripts/render_poster.py` for a production poster.
- Commit only the day’s article, caption, poster metadata, Canva-exported PNG, poster index update,
  and ledger update.
  Preserve unrelated local changes and never commit credentials.
- Treat any missing source, stale story, duplicate, failed validation, unavailable visual, dirty
  checkout, or push failure as a failed run. Do not publish a partial edition.
