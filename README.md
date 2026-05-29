# Daily AI Brief

This repository is a Claude Routine plus GitHub Actions LINE-dispatch pipeline.

Claude Routine does the intelligence work: it searches, writes, and commits a Markdown article. GitHub Actions does only the delivery work: when an article is pushed, it extracts a short digest and sends exactly one LINE Messaging API message.

This version does **not** use the OpenAI API. `OPENAI_API_KEY` is no longer required, and no OpenAI API billing is needed for this version. Claude Routine uses your Claude account/routine quota.

The brief is broad AI-world intelligence, not a PhD-only or deeptech-only digest. Tharm's PhD lens appears as one optional section: `Tharm's Deeptech Lens`.

This repo uses the LINE Messaging API only.

## Architecture

```text
Claude Routine, daily 07:00 Europe/London
  -> searches broad AI-world news
  -> writes articles/YYYY-MM-DD-ai-brief.md
  -> commits and pushes the article

GitHub Actions
  -> triggers on article push
  -> python scripts/extract_line_digest.py
  -> python scripts/send_line.py

LINE Official Account
  -> receives one text message
```

## Repository Layout

```text
.github/workflows/line-dispatch.yml
articles/sample-ai-brief.md
docs/claude-routine-prompt.md
scripts/extract_line_digest.py
scripts/send_line.py
requirements.txt
```

## Required GitHub Secrets

Add only these repository secrets under GitHub `Settings` -> `Secrets and variables` -> `Actions`:

```text
LINE_CHANNEL_ACCESS_TOKEN
LINE_TO
```

Do not add `OPENAI_API_KEY`; it is not used. Do not add `ANTHROPIC_API_KEY`; Claude Routine does not need an API key for this setup.

## Claude Routine Setup

1. Open `https://claude.ai/code/routines`.
2. Create a new routine.
3. Connect/select GitHub repository `tuntharm/DailyAIBrief`.
4. Schedule it daily at `07:00 Europe/London`.
5. Paste the full prompt from `docs/claude-routine-prompt.md`.
6. Make sure the routine can commit and push to the repository.
7. If Claude pushes to `claude/daily-ai-brief` or another `claude/**` branch, the LINE workflow is already configured to trigger on `claude/**` article pushes. If you want archive files on `main`, merge that branch or allow the routine to push directly to `main`.

Claude should write:

```text
articles/YYYY-MM-DD-ai-brief.md
```

with commit message:

```text
Add daily AI brief YYYY-MM-DD
```

When you change the news context, update both places:

1. Edit `docs/claude-routine-prompt.md` in GitHub for version control.
2. Paste the same updated prompt into Claude Routine Instructions, because the scheduler uses the Instructions box directly.

## LINE Dispatch

The workflow `.github/workflows/line-dispatch.yml` runs when a Markdown file under `articles/**/*.md` is pushed to `main` or `claude/**`.

It also supports manual `workflow_dispatch` for testing. Manual dispatch uses the newest Markdown file in `articles/`; the included `articles/sample-ai-brief.md` exists so you can test the LINE path before Claude writes a real article.

The LINE quota is based on message count, not word count. This repo sends one LINE message per article push.

`scripts/send_line.py` sends one text message only and caps the message below 4,500 characters.

## Manual LINE Test

From GitHub:

1. Add repository secrets `LINE_CHANNEL_ACCESS_TOKEN` and `LINE_TO`.
2. Open `Actions`.
3. Select `LINE Article Dispatch`.
4. Click `Run workflow`.
5. Confirm LINE receives one message generated from `articles/sample-ai-brief.md` or the newest article.

From local PowerShell:

```powershell
python -m pip install -r requirements.txt
python scripts/extract_line_digest.py
$env:LINE_CHANNEL_ACCESS_TOKEN="..."
$env:LINE_TO="..."
python scripts/send_line.py
```

`send_line.py` sends a real LINE message. For local tests, `scripts/extract_line_digest.py` creates `reports/latest_line_digest.txt`; inspect that generated file before running `send_line.py`.

## Article Format

Claude Routine should follow the format in `docs/claude-routine-prompt.md`:

```text
# Daily AI Brief — YYYY-MM-DD

## TL;DR

## Global AI / Frontier Models

## AI Infrastructure / Markets

## Research / Technical Signal

## Product / Startup / Adoption Signal

## Tharm's Deeptech Lens

## Founder / Investor Takeaway

## Watchlist
```

`scripts/extract_line_digest.py` degrades gracefully if optional sections are missing. `TL;DR` becomes the strategic summary in LINE. The five track sections provide the evidence trail, and the LINE digest includes `Read:` links when Claude writes `Link:` fields in the article.

## Security

Never commit secrets. Store only these as GitHub Actions repository secrets:

- `LINE_CHANNEL_ACCESS_TOKEN`
- `LINE_TO`

The LINE Channel ID and Channel secret are not used by this automation. If any access token or channel secret is pasted into chat, logs, issues, or commits, rotate it in the LINE Developers console before relying on it.
