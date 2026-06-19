# FrontBrief.AI — website

The public site for FrontBrief.AI. It reads the daily briefs the Claude routine
commits to this repo and publishes them as a simple news site:

- **Today** (`/`) — the latest brief, headline + TL;DR, Brief Owl welcome, recent grid.
- **Brief** (`/brief/<date>-ai-brief`) — the full brief (Top 5 / Money Map / Watchlist).
- **Archive** (`/archive`) — every brief, grouped by month, newest first.
- **About** (`/about`) — what FrontBrief.AI is.

## How it works

- Articles are read from `../articles/*.md` at build time (`src/lib/briefs.ts`).
  Both the old category format and the new `## Top 5` format render; the
  channel-specific `## LINE Digest` section is stripped from the web view.
- Brand art (`../assets/brand`) and daily posters (`../social/poster`) are copied
  into `public/` by `scripts/sync-assets.mjs`, which runs automatically before
  `dev` and `build`. Those copies are gitignored — the sources stay canonical.
- A brief with no committed poster falls back to a branded placeholder.

## Develop

```bash
cd web
npm install
npm run dev      # http://localhost:3000
```

## Deploy (Vercel)

- New Vercel project from this GitHub repo.
- **Root Directory = `web`** (framework auto-detected: Next.js).
- Every daily article commit triggers a production redeploy, so the brief
  self-publishes.
- Optional: set `NEXT_PUBLIC_SITE_URL` and attach the `frontbrief.ai` domain.

## Stack

Next.js 16 · React 19 · Tailwind v4 · TypeScript · remark (markdown).
