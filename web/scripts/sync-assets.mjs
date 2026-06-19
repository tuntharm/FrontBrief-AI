// Copies brand art and daily posters from the automation repo (siblings of web/)
// into web/public so Next.js can serve them. Sources stay the single source of
// truth; these copies are gitignored and regenerated on every dev/build run
// (including on Vercel, where the whole repo is checked out before building).
import { cp, mkdir, readdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const webRoot = dirname(dirname(fileURLToPath(import.meta.url)));
const repoRoot = dirname(webRoot);

const jobs = [
  { from: join(repoRoot, "assets", "brand"), to: join(webRoot, "public", "brand") },
  { from: join(repoRoot, "social", "poster"), to: join(webRoot, "public", "posters") },
];

async function copyPngs({ from, to }) {
  if (!existsSync(from)) {
    console.warn(`[sync-assets] source missing, skipped: ${from}`);
    return 0;
  }
  await mkdir(to, { recursive: true });
  const entries = await readdir(from, { withFileTypes: true });
  let n = 0;
  for (const entry of entries) {
    if (!entry.isFile()) continue;
    if (!/\.(png|jpe?g|webp|svg)$/i.test(entry.name)) continue;
    await cp(join(from, entry.name), join(to, entry.name));
    n += 1;
  }
  return n;
}

let total = 0;
for (const job of jobs) {
  total += await copyPngs(job);
}
console.log(`[sync-assets] copied ${total} asset file(s) into web/public`);
