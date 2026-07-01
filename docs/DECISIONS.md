# FrontBrief.AI — Decisions & Feedback Log

Running record of key decisions, Tharm's feedback, rationale, and gotchas. New Claude sessions
should read this for *context* (the "why"); `CLAUDE.md` + `docs/claude-routine-prompt.md` hold the
authoritative *rules*. Append to this file as new decisions are made; don't rewrite history.

## Brand
- Name: **FrontBrief.AI**. Slogan: **"A daily brief from the AI frontier."**
- Naming journey: AI Brief → considered The Signal / Morning Inference / Frontier Signal →
  landed on **FrontBrief** ("Frontier" + "Brief"). One name across all surfaces (LINE, article,
  poster, IG) on purpose — don't split brand recognition.
- File slug `YYYY-MM-DD-ai-brief.md/.png` stays as a path identifier (not a brand surface) to
  avoid breaking the pipeline/history.
- Brand assets in `assets/brand/`: `whitebg.png`, `blackbg.png`, `footer.png` (uploaded by Tharm).

## Architecture
- Routine writes: article + poster (`.png.url` pointer) + IG caption; commits + merges to main.
- GitHub Actions: `line-dispatch.yml` (LINE), `commit-poster.yml` (downloads/commits poster PNG),
  `post-instagram.yml` (posts poster + caption once IG secrets exist).
- Schedule: **05:00 Europe/London** (moved from 07:00 for token-budget reasons). Model: Opus 4.8.

## Content / selection
- **Interestingness-first, exactly 5 items.** Lead with the single most must-know story. Breadth
  is a guide, NOT a quota. Tharm disliked niche/quota-filled briefs (dry capex forecasts, procedural
  legal updates). Favor hot rounds, model launches/bans, influential-people calls, big valuations.
- Each item: investment angle (signal, not advice; no live prices) + Tharm-relevance. Brief closes
  with Money Map. LINE Digest is a dedicated, standalone section (sent verbatim).

## No repeats — scan before you write (Tharm, 2026-06-18)
- **Hard rule: do not repeat a recent lead/poster story.** On 2026-06-18 the routine led with (and
  postered) "SpaceX buys Cursor for $60B" — but that exact story had already been the poster lead on
  the two prior runs (series pages 6 & 7), making it **three SpaceX/Cursor posters in a row**. Tharm
  was (rightly) annoyed.
- **Before selecting the #1 / poster story, SCAN recent coverage first:**
  1. Read the last ~5–7 `articles/YYYY-MM-DD-ai-brief.md` `### 1.` leads.
  2. Read the recent poster headlines from the Canva series via
     `get-design-content(DAHMpIU_j38, content_types=["richtexts"], pages=[last several])`.
  3. If your would-be #1 (or its poster) was already used in the last few days, **pick the next
     fresh item** instead. Same company/deal twice in a row on the poster = not allowed; lead with
     genuinely new news (a story from the last 24–48h that has not been covered).
- The freshest item, not just the biggest, should lead when the biggest is a day-old repeat.
- **Freshness window = 5 days max (Tharm, 2026-06-18).** The poster's lead story may be up to 5 days
  old at most (prefer 24–48h). Don't poster news older than that, and don't reuse a story already
  postered within that window.

## Poster image: no bare logos (Tharm, 2026-06-18)
- The first DeepSeek poster used the flat lobehub logo PNG stretched full-frame — Tharm said that's
  "just a logo as the background"; he wants depth: a real branded photo, or a designed background
  with the logo composed in the MIDDLE (transparency around it), like the app-on-phone / founder +
  backers examples he sent.
- **Rule:** never use a bare logo as the whole background. Prefer a real branded photo (the
  company's app on a phone/screen, an event/press photo, a product shot). Pexels has free,
  no-attribution AI-app photos that Canva can fetch — e.g. the DeepSeek app shots
  `images.pexels.com/photos/30530404|30530422/...jpeg` (used for the fixed 2026-06-18 poster).
  If compositing, place the logo centred over a designed background, not edge-to-edge.

## Poster (Canva)
- Parent series design `DAHMpIU_j38` ("FrontBrief.AI — Poster Series"). One page per day, appended.
- **Page 1 is the locked master** with logos already placed: FB monogram top-right
  (asset `MAHMrGzahno`), FrontBrief.AI wordmark in the bottom-right pill (asset `MAHMrIzveUk`).
- Daily flow: COPY page 1 → change ONLY category pill, headline, subhead, background image
  (`update_fill`) → balance-check → append to parent → export → `.png.url` pointer.
- **Never** move/recolor/re-place the logos; never regenerate from scratch (drifts off-template);
  no decorative dot/circle patterns (Thark had these removed).
- Headline ~2 lines (3 lines overflow into the subhead). Subhead concise (~2 lines) sitting just
  above the button — Tharm nudged it up ~16px when it sank too low; do a balance check before export.
- **HARD RULE — subhead must be ≤2 lines and vertically aligned with the FrontBrief.AI button
  (Tharm, 2026-07-01).** The FrontBrief.AI button (bottom-right) is centred on a TWO-line subhead;
  a 3-line subhead drops its 3rd line BELOW the button and breaks the symmetry (Tharm has had to fix
  this by hand repeatedly). So: if the subhead wraps to 3 lines, SHORTEN THE COPY until it's 2 lines —
  do not ship a 3-line subhead. **Always** pull the page thumbnail and eyeball the symmetry (headline
  ≤2 lines, subhead ≤2 lines and level with the button, both logos placed, nothing sinking to the very
  bottom) BEFORE committing/exporting/submitting — every poster, every time, no exceptions.

### Imagery priority (Tharm's strong preference — pick for SPECIFICITY, not just "on theme")
1. Story-specific/branded visual: announcement, keynote slide, product, exec on stage/event.
2. If none: a clean LOGO-BASED brand shot (logo IN CONTEXT — app on a phone/screen — NOT a bare
   logo stretched full-frame).
3. Last resort only: a generic on-theme image.
4. Never: off-topic (e.g. a generic office/circuit board for a person/company story); never a bare
   flat logo as the whole background.
- Real photos of identifiable people ARE allowed for editorial news use (this REVERSED an earlier
  "no real people / no logos" rule). Prefer official press-kit / company announcement visuals /
  Creative Commons / licensed sources; credit where appropriate; subject company's logo is fine.
- **Person-centric stories → use a real photo OF that person (Tharm, 2026-06-16).** When the #1
  story is about a named individual (e.g. "Bezos raises $12B"), the poster image should be a good,
  recognisable photo of that person, not a generic on-theme image (a humanoid-robot stock photo for
  a Bezos story is wrong). Pick a clean, well-composed shot (ideally with a company logo/context in
  frame, like the Bezos-at-Amazon photo Tharm sent) and crop it to fit the poster's image area: the
  background fill is the top region (1080×900, landscape-ish), and the bottom ~450px is covered by
  the gradient scrim + headline/subhead — so frame the face/subject in the UPPER portion so it isn't
  hidden by the text. On 2026-06-16 the routine first shipped a generic robot image for the Bezos
  story; Tharm re-edited the Canva by hand to a proper Bezos photo and asked us to make this a rule.
- **Getting a photo into Canva (gotcha):** Wikimedia Commons direct URLs FAIL Canva's
  `upload-asset-from-url` (server-side fetch returns non-200 — likely a User-Agent/hotlink block).
  Pexels CDN (`images.pexels.com/photos/<id>/...jpeg`) is reliably hotlinkable and has free
  no-attribution AI-app shots (used for the DeepSeek poster). lobehub jsDelivr brand PNGs also fetch
  but are bare logos — only use composited, not full-frame. For a specific person with no fetchable
  photo, place the image in Canva manually rather than settling for a generic image.

### Sci-fi / futuristic stories → GENERATED conceptual image (Tharm, 2026-06-19)
- On 2026-06-19 the poster story was **Midjourney's full-body "Ultrasonic CT" scanner** — a futuristic
  product that *doesn't physically exist yet* (a person lowered into a pool/pod of light, ~8,960
  transducers, "MRI at ~100x speed"). The routine shipped a **real stock MRI photo** (Pexels
  `7088479`, a patient in a hospital MRI tube). It satisfied "on-theme / real photo," but Tharm felt
  it was too **literal and clinical** — it read as today's MRI, not the sci-fi thing the story is about.
- Tharm re-did it by hand with a **generated (Canva Magic Media) conceptual image**: a person standing
  in a glowing scan **cylinder** with golden scan rings, in a sleek futurist clinic, with the
  **Midjourney sailboat logo** (the subject company — allowed) placed tastefully top-right. Far more
  feed-worthy than the stock MRI.
- **Rule:** when the lead/poster story is **futuristic / sci-fi / a product or capability that doesn't
  physically exist yet** (this scanner, "physical AI," novel robotics, brain-computer, etc.), the
  image priority **flips** — prefer a **generated conceptual image** over a too-literal stock photo.
  (For grounded stories — a named person, a real company event/product — the existing "real photo /
  branded visual" priority still wins. This exception is only for not-yet-real subjects.)
- **Capability gotcha:** there is **no DALL·E-style text-to-image MCP tool** wired into the routine.
  Canva `generate-design` exists but produces a whole new *design candidate* (drifts off-template) —
  not a clean background asset for the locked master. So generating the image is currently a **manual
  Magic Media step** in the Canva editor (what Tharm did). Until a real image-gen tool exists, the
  routine should **auto-draft the image-gen prompt** in the daily output (editorial, photoreal, framed
  for the upper region so the scrim/headline doesn't cover the subject) so the marketing team can
  paste it straight into Magic Media. Keep the subject company's logo (tastefully placed) when fitting.

## Instagram caption
- File `social/caption/YYYY-MM-DD-ai-brief.txt`, posted verbatim by `post-instagram.yml`.
- Lead with a punchy hook → key fact/number → optional money angle, then the CTA.
- **End with a "Full brief in bio" CTA (Tharm, 2026-06-20).** The public site is now live at
  https://frontbrief-ai.vercel.app (Next.js app in `web/`, auto-deployed from `main` via Vercel),
  and the Instagram bio links to it. This reverses the earlier 2026-06-19 "no CTA, no website yet"
  rule — there is now a real link to send people to.
- Hashtags: AT MOST 5, last line, and the LAST one MUST be `#FrontBriefAI`.

## Public website
- **Live at https://frontbrief-ai.vercel.app** — Next.js app in `web/`, auto-deployed from `main` by
  Vercel (Root Directory = `web`, "include files outside root" ON so it can read `../articles`). Every
  daily routine commit triggers a rebuild, so the brief self-publishes.
- **Public article = a narrative `## Web Edition` (Tharm, 2026-06-20).** The website renders the
  `## Web Edition` section — a journalist-voice blog post (standfirst + per-story prose under `### `
  subheads + inline links + money/watch close), NOT the internal bullet brief. The Producer (Stage 4)
  writes it in the same pass; the team stays at 7 agents (no new "web" agent — dedup is already the
  Assignment Editor's job, publishing is already automatic via Vercel).
- **`Tharm relevance` + `Action` are internal-only, hidden on the web.** They stay in `## Top 5`
  (for Tharm / archive / evidence), but the site never shows them: it renders `## Web Edition` when
  present, otherwise strips `Tharm relevance:` / `Action:` lines (and the LINE Digest) from the brief.
  Supersedes the earlier implicit "web = raw brief" behaviour.

## Gotchas / lessons learned
- Canva background image can be **locked** → `update_fill`/delete refused ("locked element"). Fix:
  unlock the image on the master in Canva. (In the Sakana test the swap worked, so page 1 is unlocked.)
- `copy-design` with `page_numbers` sometimes still reports all pages; edit/export page 1 anyway.
- Canva thumbnails come back through the tool-result channel (work despite egress limits).
- `WebFetch` is blocked (403) on many sites (Unsplash, Sakana). But Canva `upload-asset-from-url`
  fetches **server-side**, so pass a **direct CDN image URL** (no redirects — redirect URLs fail).
- Routine container can't reach the user's local disk (e.g. `/Users/...`) — assets must be in the
  repo or at a public URL.
- **Pushing to `main` can 503 on the git transport** (2026-06-18): the routine's `git push` to
  `main` failed repeatedly with HTTP 503 while the session-branch push and the GitHub API both
  worked. Fallback: push files to `main` via the GitHub API (`push_files`) to update `main` and
  fire the `line-dispatch` / `commit-poster` workflows.

## Open items / future
- Paste the latest `docs/claude-routine-prompt.md` into the routine config (the config is what runs).
- Public site is live on Vercel (see "Public website" above); later buy `frontbrief.ai` and point
  it at the Vercel project, then set `NEXT_PUBLIC_SITE_URL` for correct OG/canonical links.
- Instagram: create Meta app, add `INSTAGRAM_USER_ID` + `INSTAGRAM_ACCESS_TOKEN` secrets; consider a
  monthly token auto-refresh workflow (60-day token expiry).
- Confirm the `@frontbrief` handle before going public.
