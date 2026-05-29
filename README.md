# Daily AI & Deeptech Brief

This repository runs a daily GitHub Actions pipeline that fetches public AI/deeptech signals, uses the OpenAI API to score and summarise them, archives a full Markdown report in `reports/`, and sends one short digest to LINE through the LINE Messaging API.

It is built for Tharm: a PhD researcher working on AI/surrogate modelling for engineering simulation and a future deeptech founder/investor. The brief filters for infrastructure economics, semiconductor supply chains, scientific ML, engineering simulation, frontier research, robotics/aerospace/SHM, digital twins, and deeptech commercialisation. It intentionally ignores generic chatbot/product news and low-signal commentary.

LINE Notify is not used. LINE Notify is discontinued; this repo uses the LINE Messaging API push endpoint only.

## Architecture

```text
GitHub Actions scheduler
  -> scripts/fetch_news.py
       -> data/news_raw.json
       -> data/news_candidates.json
  -> scripts/summarise.py
       -> OpenAI API scoring and report generation
       -> data/scored_candidates.json
       -> reports/YYYY-MM-DD-brief.md
       -> reports/latest_line_digest.txt
  -> scripts/send_line.py
       -> LINE Messaging API push endpoint
       -> exactly one text message
  -> git commit generated data and reports
```

The workflow runs fully on GitHub Actions. It does not depend on Claude Routine, a local machine, a Mac mini, or any always-on computer.

## Setup

1. Create a LINE Official Account.
2. Create or enable a LINE Messaging API channel for that account.
3. Issue a channel access token for the Messaging API channel.
4. Get the LINE recipient ID for `LINE_TO`. It can be a user ID, group ID, or room ID. For a user ID, the user normally needs to add the bot as a friend and you can capture the ID from a webhook event.
5. Add these GitHub Actions secrets in the repository settings:
   - `OPENAI_API_KEY`
   - `LINE_CHANNEL_ACCESS_TOKEN`
   - `LINE_TO`
6. Open the `Daily AI Deeptech Brief` workflow in GitHub Actions and run it manually with `workflow_dispatch`.

Optional: set a repository variable named `OPENAI_MODEL` to override the default model used by `scripts/summarise.py`.

## Schedule And UK Time

GitHub Actions cron uses UTC. The workflow has two cron triggers:

```yaml
- cron: "0 6 * * *"
- cron: "0 7 * * *"
```

Inside the workflow, it checks the actual current hour in `Europe/London`. Scheduled runs continue only when the London hour is `07`; otherwise they exit cleanly. This handles UK daylight saving safely:

- During British Summer Time, `06:00 UTC` is `07:00 Europe/London`.
- During Greenwich Mean Time, `07:00 UTC` is `07:00 Europe/London`.

The workflow also compares the cron expression that triggered the run against the current London UTC offset. This prevents a delayed inactive cron trigger from sending a duplicate digest during the 07:00 hour.

Manual `workflow_dispatch` runs ignore the hour check and run immediately.

## LINE Quota

LINE Messaging API quota is based on sent message count, not word count. This repo sends exactly one text message per run, and the scheduled hour gate is designed so only one scheduled run sends per day.

The digest is capped below 4,500 characters and is truncated gracefully if necessary. The script never splits the digest into multiple LINE messages.

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

Scores are 0-5. Items are included only when the weighted score is at least `3.0/5` or the raw score is at least `15/25`. The brief selects up to 5 strong items and does not pad weak news.

Set `OPENAI_MODEL` as a GitHub repository variable or environment variable to change the model without editing code.

## Manual Testing

From the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/fetch_news.py
OPENAI_API_KEY=... python scripts/summarise.py
LINE_CHANNEL_ACCESS_TOKEN=... LINE_TO=... python scripts/send_line.py
```

On Windows PowerShell:

```powershell
python -m pip install -r requirements.txt
python scripts/fetch_news.py
$env:OPENAI_API_KEY="..."
python scripts/summarise.py
$env:LINE_CHANNEL_ACCESS_TOKEN="..."
$env:LINE_TO="..."
python scripts/send_line.py
```

`send_line.py` sends a real LINE message. Test fetch and summarise first, inspect `reports/latest_line_digest.txt`, then run the send step.

Manual `workflow_dispatch` also sends a real LINE message because it is intended for end-to-end testing and backfills.

## Troubleshooting

No LINE message received:
Check that the bot is allowed to send messages to the recipient, the user has added the bot if using a user ID, and the workflow reached the `Send LINE digest` step.

Invalid token:
Regenerate the Messaging API channel access token and update `LINE_CHANNEL_ACCESS_TOKEN`. Do not use a LINE Notify token.

Wrong `LINE_TO`:
Confirm whether the ID is a user ID, group ID, or room ID from a Messaging API webhook event. A display name, phone number, or LINE account name will not work.

GitHub Actions cron delay:
GitHub scheduled workflows may start late. The workflow checks the actual `Europe/London` hour and exits if it is not `07`. If GitHub delays the active run beyond the 07:00 London hour, it exits rather than sending late.

No fresh stories found:
The fetcher prefers the last 48 hours. If no source has fresh public metadata, the report will say there were no high-quality fresh signals instead of padding the brief.

OpenAI API error:
Check `OPENAI_API_KEY`, billing/access for the selected model, and optionally set `OPENAI_MODEL` to a model available to your account.

Source failures:
One failing source does not fail the pipeline. If all enabled sources fail, `fetch_news.py` exits with a clear error.

## Security

Never commit secrets. Use GitHub Actions secrets for:

- `OPENAI_API_KEY`
- `LINE_CHANNEL_ACCESS_TOKEN`
- `LINE_TO`

The LINE Channel ID and Channel secret are not used by this automation. If any access token or channel secret is pasted into chat, logs, issues, or commits, rotate it in the LINE Developers console before relying on it.

The scripts log useful status but never print secret values.
