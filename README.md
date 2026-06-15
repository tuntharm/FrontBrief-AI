# FrontBrief.AI

**FrontBrief.AI** — *A daily brief from the AI frontier.*

FrontBrief.AI is a lightweight automation that turns a daily Claude Routine article into a short LINE digest, a social poster, and an Instagram post.

It is designed for people who want a concise, high-signal view of the AI world: frontier models, infrastructure, research, startups, adoption, policy, and selected deeptech angles. The brief can include Tharm's personal deeptech lens, but the core product is broad AI intelligence rather than a PhD-only digest.

## How It Works

```text
Claude Routine, daily 05:00 Europe/London
  -> searches recent high-quality AI sources
  -> writes articles/YYYY-MM-DD-ai-brief.md (with a ## LINE Digest section)
  -> builds the daily Canva poster -> social/poster/YYYY-MM-DD-ai-brief.png.url
  -> writes the IG caption          -> social/caption/YYYY-MM-DD-ai-brief.txt
  -> commits and pushes, then merges to main

GitHub Actions
  -> line-dispatch.yml:   article push  -> sends the LINE digest
  -> commit-poster.yml:   .png.url push -> downloads + commits the poster PNG
  -> post-instagram.yml:  after poster  -> posts the poster + caption to Instagram

Delivery
  -> LINE Official Account delivers the digest to LINE_TO
  -> Instagram posts the poster with the caption
```

Claude Routine handles research, writing, the poster, the caption, scheduling, and committing.
GitHub Actions handles LINE delivery, the poster PNG commit, and Instagram posting.

## Brief Criteria

The brief picks **exactly 5 items, interestingness-first** — lead with the single most "must-know"
story in AI that day, then rank the rest by importance × how interesting/shareable they are. The
five tracks below are a guide for breadth, **not a quota**; never pad with a weak story to fill a
track.

- Global AI / Frontier Models: frontier labs, model releases, agents, multimodal AI, reasoning, safety, regulation, and policy.
- AI Infrastructure / Markets: NVIDIA, AMD, TSMC, Broadcom, hyperscaler capex, data centres, HBM, networking, energy, cooling, and inference economics.
- Research / Technical Signal: important papers and technical releases from high-quality labs, journals, conferences, and research groups.
- Product / Startup / Adoption Signal: enterprise AI, developer tools, robotics, healthcare, finance, legal AI, funding, acquisitions, and adoption signals.
- Tharm's Deeptech Lens: surrogate modelling, neural operators, physics GNNs, FEA/CFD acceleration, aerospace, SHM, robotics, and digital twins.

The deeptech lens is one slot, not the whole brief. Each item carries an investment angle (signal,
not advice) and a Tharm-relevance line, and the brief closes with a Money Map.

Ignore generic chatbot news, prompt-engineering tips, consumer AI tools, duplicated stories, vague hype, and low-signal opinion pieces.

## Repository Layout

```text
.github/workflows/line-dispatch.yml     # sends the LINE digest on article push
.github/workflows/commit-poster.yml      # commits the poster PNG from its .png.url pointer
.github/workflows/post-instagram.yml     # posts poster + caption to Instagram
articles/                                # daily briefs (+ sample-ai-brief.md)
assets/brand/                            # logo + footer brand assets
docs/claude-routine-prompt.md
scripts/extract_line_digest.py
scripts/send_line.py
scripts/post_instagram.py
social/poster/                           # daily posters (PNG + .png.url + index.md)
social/caption/                          # daily Instagram captions
requirements.txt
```

## Required GitHub Secrets

Add these repository secrets under GitHub `Settings` -> `Secrets and variables` -> `Actions`:

```text
LINE_CHANNEL_ACCESS_TOKEN
LINE_TO
INSTAGRAM_USER_ID         # only needed once you enable Instagram auto-posting
INSTAGRAM_ACCESS_TOKEN    # long-lived Instagram Graph API token
```

`LINE_TO` can be a user ID, group ID, or room ID. For a small group of readers, the simplest setup is to add the LINE Official Account to a LINE group and use the group ID as `LINE_TO`. The two `INSTAGRAM_*` secrets are optional until you turn on Instagram posting.

## Claude Routine Setup

1. Open `https://claude.ai/code/routines`.
2. Create a new routine.
3. Connect/select GitHub repository `tuntharm/DailyAIBrief`.
4. Schedule it daily at `05:00 Europe/London`.
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

## LINE Digest     # standalone, punchy; sent to LINE verbatim
## TL;DR           # 3 standalone bullets
## Top 5           # per item: Category / Why interesting / Why it matters /
                   #           Investment angle / Tharm relevance / Action / Link
## Money Map       # where capital + pricing momentum moved
## Watchlist       # three catalysts to monitor next
```

`scripts/extract_line_digest.py` sends the hand-written `## LINE Digest` section verbatim if
present, and otherwise degrades gracefully by building a digest from `TL;DR` and the `Top 5`
links. The `Top 5` is the full evidence trail; each item includes a direct `Link:`.

## Security

Never commit secrets. Store LINE credentials only as GitHub Actions repository secrets.

If an access token or channel secret is pasted into chat, logs, issues, or commits, rotate it in the LINE Developers console before relying on it.
