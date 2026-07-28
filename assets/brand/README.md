# FrontBrief.AI — Brand Assets

Canonical brand images used locally by the deterministic poster renderer and public website.

## Files

| File | Use | Raw URL |
|------|-----|---------|
| `whitebg.png` | FB monogram + wordmark on a light/white background | `https://raw.githubusercontent.com/tuntharm/FrontBrief-AI/main/assets/brand/whitebg.png` |
| `blackbg.png` | FB monogram + wordmark on a dark/black background | `https://raw.githubusercontent.com/tuntharm/FrontBrief-AI/main/assets/brand/blackbg.png` |
| `footer.png` | Dark banner / footer ("A daily brief from the AI frontier") | `https://raw.githubusercontent.com/tuntharm/FrontBrief-AI/main/assets/brand/footer.png` |

## How these are used

1. `scripts/render_poster.py` composes the transparent monogram from `web/public/fb-white.png` and
   crops the canonical wordmark from `whitebg.png`.
2. Use `whitebg.png` on light layouts, `blackbg.png` on dark ones, and `footer.png` for any post
   header/sign-off strip.
3. The poster background must be a story-specific photo, branded scene, or conceptual image. Never
   stretch a bare company logo across the background.
