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

### Imagery priority (Tharm's strong preference — pick for SPECIFICITY, not just "on theme")
1. Story-specific/branded visual: announcement, keynote slide, product, exec on stage/event.
2. If none: a clean LOGO-BASED brand shot (company logo on a phone/screen, like the Anthropic poster).
3. Last resort only: a generic on-theme image.
4. Never: off-topic (e.g. a generic office/circuit board for a person/company story).
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
- **Getting a person photo into Canva (gotcha):** Wikimedia Commons direct URLs FAIL Canva's
  `upload-asset-from-url` (server-side fetch returns non-200 — likely a User-Agent/hotlink block),
  so the MD5-path trick doesn't help. Pexels CDN (`images.pexels.com/photos/<id>/...jpeg`) is
  reliably hotlinkable but is stock (no real named people). For a specific person, find a
  hotlinkable direct CDN image URL (no redirect) of that person; if none can be fetched
  server-side, place the image in Canva manually (as Tharm did) rather than settling for a generic
  image.

## Instagram caption
- File `social/caption/YYYY-MM-DD-ai-brief.txt`, posted verbatim by `post-instagram.yml`.
- Lead with a punchy hook → key fact/number → optional money angle → light CTA ("Full brief in bio").
- Hashtags: AT MOST 5, last line, and the LAST one MUST be `#FrontBriefAI`.

## Gotchas / lessons learned
- Canva background image can be **locked** → `update_fill`/delete refused ("locked element"). Fix:
  unlock the image on the master in Canva. (In the Sakana test the swap worked, so page 1 is unlocked.)
- `copy-design` with `page_numbers` sometimes still reports all pages; edit/export page 1 anyway.
- Canva thumbnails come back through the tool-result channel (work despite egress limits).
- `WebFetch` is blocked (403) on many sites (Unsplash, Sakana). But Canva `upload-asset-from-url`
  fetches **server-side**, so pass a **direct CDN image URL** (no redirects — redirect URLs fail).
- Routine container can't reach the user's local disk (e.g. `/Users/...`) — assets must be in the
  repo or at a public URL.

## Open items / future
- Paste the latest `docs/claude-routine-prompt.md` into the routine config (the config is what runs).
- GitHub Pages for a free "link in bio" site; later buy `frontbrief.ai` and point it at Pages.
- Instagram: create Meta app, add `INSTAGRAM_USER_ID` + `INSTAGRAM_ACCESS_TOKEN` secrets; consider a
  monthly token auto-refresh workflow (60-day token expiry).
- Confirm the `@frontbrief` handle before going public.
