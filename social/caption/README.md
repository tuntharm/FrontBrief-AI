# FrontBrief.AI — Instagram Captions

One caption file per day, written by the routine right after the poster:
`social/caption/YYYY-MM-DD-ai-brief.txt`.

The `post-instagram.yml` workflow reads this file and posts it verbatim as the Instagram caption
for that day's poster (`social/poster/YYYY-MM-DD-ai-brief.png`). If the file is missing, the
posting script falls back to building a caption from the article.

## Caption rules

- Plain text, English, lead with the news hook (same #1 Must-Know story as the poster).
- 1–3 short lines: headline hook → the key fact/number → optional money/investment angle.
- A light call to action is fine (e.g. "Full brief in bio").
- **Hashtags: at most 5, on the last line, and the LAST one must be `#FrontBriefAI`.**
  Example: `#AI #Anthropic #AINews #TechNews #FrontBriefAI`

## Shape

    <hook headline>
    <one line with the key fact/number>
    <optional one-line money/investment angle — signal, not advice>

    #Tag1 #Tag2 #Tag3 #Tag4 #FrontBriefAI
