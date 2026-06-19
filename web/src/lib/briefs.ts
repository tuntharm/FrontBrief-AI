/**
 * Reads the daily briefs from the repo's ../articles directory at build time
 * and turns them into typed objects the website can render.
 *
 * Articles come in two historical shapes:
 *   - new (>= 2026-06-15): "## LINE Digest" -> "## TL;DR" -> "## Top 5" ...
 *   - old (<= 2026-06-14): "## TL;DR" -> category sections ...
 * So parsing stays format-agnostic: we strip the channel-specific LINE Digest,
 * derive the headline from the first "###" story, and render the rest generically.
 */
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { remark } from "remark";
import remarkGfm from "remark-gfm";
import remarkHtml from "remark-html";

const ARTICLES_DIR = join(process.cwd(), "..", "articles");
const FILE_RE = /^(\d{4}-\d{2}-\d{2})-ai-brief\.md$/;

export type BriefMeta = {
  slug: string;
  date: string; // YYYY-MM-DD
  headline: string; // the day's lead story
  summary: string; // short hook (first TL;DR line)
  topHeadlines: string[]; // the day's top story headlines (for digest excerpts)
};

export type Brief = BriefMeta & {
  tldr: string[];
  /** Article body rendered to HTML, with the LINE Digest section removed. */
  bodyHtml: string;
};

function stripFrontmatter(md: string): string {
  if (md.startsWith("---")) {
    const end = md.indexOf("\n---", 3);
    if (end !== -1) return md.slice(md.indexOf("\n", end + 1) + 1);
  }
  return md;
}

/** Remove a "## <name>" section (up to the next "## " heading). */
function removeSection(md: string, name: string): string {
  const re = new RegExp(`(^|\\n)##\\s+${name}\\b[\\s\\S]*?(?=\\n##\\s|$)`, "i");
  return md.replace(re, "");
}

/** Body text of a "## <name>" section (between it and the next "## "). */
function getSection(md: string, name: string): string {
  const re = new RegExp(`(?:^|\\n)##\\s+${name}\\b[ \\t]*\\n([\\s\\S]*?)(?=\\n##\\s|$)`, "i");
  return md.match(re)?.[1]?.trim() ?? "";
}

/** Strip inline markdown so a string is safe to show as plain text. */
function plain(text: string): string {
  return text
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1") // links -> text
    .replace(/[*_`]+/g, "") // emphasis/code marks
    .replace(/^\s*[-*]\s+/, "") // leading bullet
    .replace(/^\s*\d+[.)]\s*/, "") // leading "1. " / "1) "
    .replace(/\s+/g, " ")
    .trim();
}

function deriveHeadline(md: string): string {
  return deriveTopHeadlines(md, 1)[0] ?? "Daily AI brief";
}

function deriveTopHeadlines(md: string, n: number): string[] {
  return md
    .split("\n")
    .filter((l) => /^###\s+/.test(l))
    .map((l) => plain(l.replace(/^###\s+/, "")))
    .filter(Boolean)
    .slice(0, n);
}

function deriveTldr(md: string): string[] {
  const section = getSection(md, "TL;DR");
  if (!section) return [];
  return section
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => /^(\d+[.)]|[-*])\s+/.test(l))
    .map(plain)
    .filter(Boolean);
}

function findRawByDate(): { slug: string; date: string; raw: string }[] {
  if (!existsSync(ARTICLES_DIR)) return [];
  return readdirSync(ARTICLES_DIR)
    .map((file) => {
      const m = file.match(FILE_RE);
      if (!m) return null;
      const slug = file.replace(/\.md$/, "");
      return { slug, date: m[1], raw: readFileSync(join(ARTICLES_DIR, file), "utf8") };
    })
    .filter((x): x is { slug: string; date: string; raw: string } => x !== null)
    .sort((a, b) => (a.date < b.date ? 1 : -1)); // newest first
}

function toMeta({ slug, date, raw }: { slug: string; date: string; raw: string }): BriefMeta {
  const md = stripFrontmatter(raw);
  const tldr = deriveTldr(md);
  return {
    slug,
    date,
    headline: deriveHeadline(md),
    summary: tldr[0] ?? site_fallback_summary,
    topHeadlines: deriveTopHeadlines(md, 4),
  };
}

const site_fallback_summary =
  "Five must-know signals from the AI frontier — models, money, and deeptech.";

export function getAllBriefs(): BriefMeta[] {
  return findRawByDate().map(toMeta);
}

export function getLatestBrief(): BriefMeta | null {
  return getAllBriefs()[0] ?? null;
}

export async function getBrief(slug: string): Promise<Brief | null> {
  const entry = findRawByDate().find((e) => e.slug === slug);
  if (!entry) return null;

  const md = stripFrontmatter(entry.raw);
  // Drop the H1 (we render our own header) and the channel-specific LINE Digest.
  let body = md.replace(/^#\s+.*\n/, "");
  body = removeSection(body, "LINE Digest").trim();

  const bodyHtml = String(await remark().use(remarkGfm).use(remarkHtml, { sanitize: false }).process(body));

  return { ...toMeta(entry), tldr: deriveTldr(md), bodyHtml };
}

/** Human-readable date, e.g. "Thu 19 Jun 2026". */
export function formatDate(date: string): string {
  const d = new Date(`${date}T00:00:00Z`);
  return d.toLocaleDateString("en-GB", {
    weekday: "short",
    day: "numeric",
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  });
}

/** Long edition title, e.g. "Friday, 19 June 2026". */
export function formatDateLong(date: string): string {
  const d = new Date(`${date}T00:00:00Z`);
  return d.toLocaleDateString("en-GB", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  });
}
