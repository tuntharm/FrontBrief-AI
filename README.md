# Daily AI & Deeptech Brief

This repository supports a Claude Routine that generates a daily AI/deeptech intelligence brief, archives the full report in GitHub, and sends one short digest to LINE through the LINE Messaging API.

It is built for Tharm: a PhD researcher working on AI/surrogate modelling for engineering simulation and a future deeptech founder/investor. The brief filters for infrastructure economics, semiconductor supply chains, scientific ML, engineering simulation, frontier research, robotics/aerospace/SHM, digital twins, and deeptech commercialisation.

This version does **not** use the OpenAI API and does **not** require `OPENAI_API_KEY`. It uses Claude Routine reasoning under your Claude Pro/Routine allowance, so there is no extra OpenAI API billing.

LINE Notify is not used. LINE Notify is discontinued; this repo uses the LINE Messaging API push endpoint only.

## Architecture

```text
Claude Routine at 07:00 Europe/London
  -> fresh clone of tuntharm/DailyAIBrief
  -> python scripts/fetch_news.py
       -> data/news_raw.json
       -> data/news_candidates.json
  -> Claude Routine reads candidates and scoring config
       -> writes data/scored_candidates.json
       -> writes reports/YYYY-MM-DD-brief.md
       -> writes reports/latest_line_digest.txt
  -> commits generated data and reports back to GitHub
  -> python scripts/send_line.py
       -> LINE Messaging API push endpoint
       -> exactly one text message
```

The routine runs on Anthropic-managed cloud infrastructure. It does not depend on your local machine, Mac mini, or an always-on computer.

## Why Claude Routine

The previous GitHub Actions + OpenAI API design was more independent, but it required OpenAI API billing. This version is designed for someone already paying for Claude Pro and wanting to avoid extra model API billing.

Tradeoff: Claude Routines are a Claude product feature and count against Claude/Routine usage limits. They are not the same as the Anthropic API, and this repo does not require a Claude API key.

## Setup

1. Create a LINE Official Account.
2. Create or enable a LINE Messaging API channel for that account.
3. Rotate and issue a fresh Messaging API channel access token.
4. Get the LINE recipient ID for `LINE_TO`. It can be a user ID, group ID, or room ID.
5. In Claude Code on the web, connect GitHub and grant access to this repository:
   `tuntharm/DailyAIBrief`
6. Create a Claude Routine at:
   `https://claude.ai/code/routines`
7. Add this repository to the routine.
8. Use a Claude Routine cloud environment with these environment variables:
   - `LINE_CHANNEL_ACCESS_TOKEN`
   - `LINE_TO`
9. Paste the prompt from `routine/claude-daily-brief.md`.
10. Add a daily schedule for `07:00 Europe/London`.
11. If you want the routine to commit directly to `main`, enable unrestricted branch pushes for this repository in the routine settings. Otherwise, Claude may push to a `claude/` branch and you will need to merge the report branch manually.
12. Click `Run now` once to test.

## Schedule And UK Time

Set the Claude Routine schedule to daily at `07:00` in `Europe/London`.

Claude Routine schedule times are entered in your local zone and converted automatically by Claude's cloud scheduler. Runs may start a few minutes after the scheduled time because routines are staggered.

There is no GitHub Actions cron in this version.

## Required Secrets

Add these to the Claude Routine cloud environment, not to the repository files:

```text
LINE_CHANNEL_ACCESS_TOKEN
LINE_TO
```

Do not add:

```text
OPENAI_API_KEY
ANTHROPIC_API_KEY
```

They are not needed for this version.

## LINE Quota

LINE Messaging API quota is based on sent message count, not word count. The routine prompt instructs Claude to send exactly one text message per successful run.

`scripts/send_line.py` sends one text message only and caps the digest below 4,500 characters.

## Customisation

Edit `config/sources.yml` to add, remove, or disable sources. Sources are grouped by track:

- `ai_infrastructure`
- `markets_investment`
- `frontier_research`
- `scientific_ml`
- `engineering_simulation`
- `aerospace_robotics_shm`
- `deeptech_policy_startups`

Use RSS feeds where possible. Public webpages can be added with `type: url`, but do not scrape paywalled content. Keep paywalled sources such as SemiAnalysis or The Information as disabled placeholders unless you add public/free URLs.

Edit `config/scoring.yml` to adjust weights and thresholds:

```yaml
phd_relevance: 0.30
investment_relevance: 0.25
technical_novelty: 0.20
moat_implication: 0.15
urgency: 0.10
```

Scores are 0-5. Items should be included only when the weighted score is at least `3.0/5` or the raw score is at least `15/25`. The brief selects up to 5 strong items and should not pad weak news.

Edit `routine/claude-daily-brief.md` to tune the analyst style or the routine's run steps.

## Local Testing

Fetch candidates locally:

```bash
python -m pip install -r requirements.txt
python scripts/fetch_news.py
```

Optional no-model fallback report:

```bash
python scripts/summarise.py
```

Send a real LINE message locally:

```bash
LINE_CHANNEL_ACCESS_TOKEN=... LINE_TO=... python scripts/send_line.py
```

On Windows PowerShell:

```powershell
python -m pip install -r requirements.txt
python scripts/fetch_news.py
python scripts/summarise.py
$env:LINE_CHANNEL_ACCESS_TOKEN="..."
$env:LINE_TO="..."
python scripts/send_line.py
```

`send_line.py` sends a real LINE message. Inspect `reports/latest_line_digest.txt` before running it.

## Troubleshooting

No LINE message received:
Check that the bot is allowed to send messages to the recipient, the user has added the bot if using a user ID, and the routine reached the `python scripts/send_line.py` step.

Invalid token:
Regenerate the Messaging API channel access token and update `LINE_CHANNEL_ACCESS_TOKEN`. Do not use a LINE Notify token.

Wrong `LINE_TO`:
Confirm whether the ID is a user ID, group ID, or room ID from a Messaging API webhook event. A display name, phone number, or LINE account name will not work.

Routine does not commit to `main`:
Check the routine repository permissions. By default, Claude may only push to `claude/` branches. Enable unrestricted branch pushes for direct archive commits to `main`, or merge the generated branch manually.

No fresh stories found:
The fetcher prefers the last 48 hours. If no source has fresh public metadata, the report should say there were no high-quality fresh signals instead of padding the brief.

Source failures:
One failing source does not fail the fetcher. If all enabled sources fail, `fetch_news.py` exits with a clear error.

Routine usage limits:
Claude Routines count against Claude/Routine usage limits. If the routine does not run, check `claude.ai/code/routines` and your Claude usage page.

## Security

Never commit secrets. Store only these in the Claude Routine cloud environment:

- `LINE_CHANNEL_ACCESS_TOKEN`
- `LINE_TO`

The LINE Channel ID and Channel secret are not used by this automation. If any access token or channel secret is pasted into chat, logs, issues, or commits, rotate it in the LINE Developers console before relying on it.

The scripts log useful status but never print secret values.
