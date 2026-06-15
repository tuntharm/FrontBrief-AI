# FrontBrief.AI

**FrontBrief.AI** — *The AI frontier, briefed daily.*

FrontBrief.AI is a lightweight automation that turns a daily Claude Routine article into a short LINE digest, a social poster, and an Instagram post.

It is designed for people who want a concise, high-signal view of the AI world: frontier models, infrastructure, research, startups, adoption, policy, and selected deeptech angles. The brief can include Tharm's personal deeptech lens, but the core product is broad AI intelligence rather than a PhD-only digest.

## How It Works

```text
Claude Routine, daily 07:00 Europe/London
  -> searches recent high-quality AI sources
  -> writes articles/YYYY-MM-DD-ai-brief.md
  -> commits and pushes the article

GitHub Actions
  -> detects the article push
  -> extracts a short LINE digest
  -> sends one LINE Messaging API message

LINE Official Account
  -> delivers the digest to LINE_TO
```

Claude Routine handles research, writing, scheduling, and committing. GitHub Actions only handles LINE delivery.

## Brief Criteria

The brief should pick the most important 5-7 items across five balanced tracks:

- Global AI / Frontier Models: frontier labs, model releases, agents, multimodal AI, reasoning, safety, regulation, and policy.
- AI Infrastructure / Markets: NVIDIA, AMD, TSMC, Broadcom, hyperscaler capex, data centres, HBM, networking, energy, cooling, and inference economics.
- Research / Technical Signal: important papers and technical releases from high-quality labs, journals, conferences, and research groups.
- Product / Startup / Adoption Signal: enterprise AI, developer tools, robotics, healthcare, finance, legal AI, funding, acquisitions, and adoption signals.
- Tharm's Deeptech Lens: surrogate modelling, neural operators, physics GNNs, FEA/CFD acceleration, aerospace, SHM, robotics, and digital twins.

The deeptech lens is one section, not the whole brief. Niche PhD-relevant items should go there unless they are broadly important to the AI world.

Ignore generic chatbot news, prompt-engineering tips, consumer AI tools, duplicated stories, vague hype, and low-signal opinion pieces.

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

Add these repository secrets under GitHub `Settings` -> `Secrets and variables` -> `Actions`:

```text
LINE_CHANNEL_ACCESS_TOKEN
LINE_TO
```

`LINE_TO` can be a user ID, group ID, or room ID. For a small group of readers, the simplest setup is to add the LINE Official Account to a LINE group and use the group ID as `LINE_TO`.

## Claude Routine Setup

1. Open `https://claude.ai/code/routines`.
2. Create a new routine.
3. Connect/select GitHub repository `tuntharm/DailyAIBrief`.
4. Schedule it daily at `07:00 Europe/London`.
5. Paste the full prompt from `docs/claude-routine-prompt.md` into the Routine Instructions box.
6. Make sure the routine can commit and push to the repository.

Claude should write:

```text
articles/YYYY-MM-DD-ai-brief.md
```

with commit message:

```text
Add daily AI brief YYYY-MM-DD
```

When changing the brief criteria, update both places:

1. Edit `docs/claude-routine-prompt.md` for version control.
2. Paste the same updated prompt into Claude Routine Instructions, because the routine uses the Instructions box at runtime.

## LINE Dispatch

The workflow `.github/workflows/line-dispatch.yml` runs when a Markdown file under `articles/**/*.md` is pushed to `main`.

If Claude Routine opens a pull request instead of pushing directly to `main`, LINE is sent only after the PR is merged. This avoids sending once from the Claude branch and again from the merge commit.

It also supports manual `workflow_dispatch` for testing. Manual dispatch uses the newest Markdown file in `articles/`; the included `articles/sample-ai-brief.md` exists so you can test the LINE path before Claude writes a real article.

LINE quota is based on messages delivered, not word count. This repo sends one LINE message per article push. If `LINE_TO` is a group, quota usage depends on the number of people reached.

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

`send_line.py` sends a real LINE message. For local tests, inspect `reports/latest_line_digest.txt` before running it.

## Article Format

Claude Routine should follow the format in `docs/claude-routine-prompt.md`:

```text
# FrontBrief.AI — YYYY-MM-DD

## TL;DR

## Global AI / Frontier Models

## AI Infrastructure / Markets

## Research / Technical Signal

## Product / Startup / Adoption Signal

## Tharm's Deeptech Lens

## Founder / Investor Takeaway

## Watchlist
```

`scripts/extract_line_digest.py` degrades gracefully if optional sections are missing. `TL;DR` becomes the strategic summary in LINE. The five track sections provide the evidence trail, and the LINE digest includes `Read:` links when the article has `Link:` fields.

## Security

Never commit secrets. Store LINE credentials only as GitHub Actions repository secrets.

If an access token or channel secret is pasted into chat, logs, issues, or commits, rotate it in the LINE Developers console before relying on it.
