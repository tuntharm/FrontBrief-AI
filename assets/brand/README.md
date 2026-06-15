# FrontBrief.AI — Brand Assets

Drop the brand image files here so Canva (and anything else) can fetch them from a stable
public URL. Canva's `upload-asset-from-url` downloads server-side, so the GitHub **raw** URL
works regardless of the routine container's network egress.

## Expected files

| File | Use | Raw URL (once committed) |
|------|-----|--------------------------|
| `frontbrief-logo.png` | FB monogram + wordmark (light bg) | `https://raw.githubusercontent.com/tuntharm/dailyaibrief/main/assets/brand/frontbrief-logo.png` |
| `frontbrief-logo-dark.png` | White logo for dark backgrounds (optional) | `https://raw.githubusercontent.com/tuntharm/dailyaibrief/main/assets/brand/frontbrief-logo-dark.png` |
| `frontbrief-footer.png` | Dark banner / footer ("A Daily Brief from the AI Frontier") | `https://raw.githubusercontent.com/tuntharm/dailyaibrief/main/assets/brand/frontbrief-footer.png` |

## How the routine uses these

1. The FrontBrief.AI logo can replace or sit beside the bottom-right `FrontBrief.AI` text button
   on the poster — add it with Canva `upload-asset-from-url` (pass the raw URL above) then
   `insert_fill`.
2. The **subject company's logo** (the company the lead story is about) is sourced fresh each run
   from that company's official site/press kit as a public URL, then added the same way as a
   small, tasteful mark. Editorial/nominative use only — no logos of unrelated companies.

Keep these as transparent PNGs where possible. The dark footer banner is for posts/stories that
need a header or sign-off strip; the square logo is the primary mark.
