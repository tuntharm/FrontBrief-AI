import Link from "next/link";
import Image from "next/image";
import { ArrowRight } from "lucide-react";
import type { BriefMeta } from "@/lib/briefs";
import { formatDate, formatDateLong } from "@/lib/briefs";

/** Short date for the branded tile, e.g. "18 JUN". */
function tileDate(date: string): string {
  return new Date(`${date}T00:00:00Z`)
    .toLocaleDateString("en-GB", { day: "numeric", month: "short", timeZone: "UTC" })
    .toUpperCase();
}

export function BriefRow({ brief }: { brief: BriefMeta }) {
  const excerpt = brief.topHeadlines.join("  ·  ");
  return (
    <article className="flex gap-4 border-b border-line py-6 sm:gap-6">
      <Link
        href={`/brief/${brief.slug}`}
        className="relative flex h-[104px] w-[130px] shrink-0 flex-col items-center justify-center overflow-hidden rounded-md bg-navy sm:h-[120px] sm:w-[170px]"
        aria-label={`AI Brief — ${formatDateLong(brief.date)}`}
      >
        <div className="flex h-11 w-11 items-center justify-center rounded-full bg-white sm:h-12 sm:w-12">
          <Image
            src="/mascot/brief-owl.png"
            alt=""
            width={44}
            height={44}
            className="h-8 w-8 object-contain sm:h-9 sm:w-9"
          />
        </div>
        <span className="mt-2 font-mono text-[0.6rem] tracking-[0.15em] text-owl-blue">
          AI BRIEF
        </span>
        <span className="font-mono text-[0.7rem] font-medium tracking-[0.1em] text-navy-text">
          {tileDate(brief.date)}
        </span>
      </Link>

      <div className="min-w-0 flex-1">
        <p className="text-[0.78rem] text-faint">
          FrontBrief.AI · {formatDate(brief.date)} · {brief.topHeadlines.length} signals
        </p>
        <h3 className="mt-1">
          <Link
            href={`/brief/${brief.slug}`}
            className="text-lg font-semibold leading-snug text-ink transition-colors hover:text-accent sm:text-xl"
          >
            AI Brief — {formatDateLong(brief.date)}
          </Link>
        </h3>
        {excerpt ? (
          <p className="mt-2 line-clamp-3 text-[0.92rem] leading-relaxed text-muted">{excerpt}</p>
        ) : null}
        <Link
          href={`/brief/${brief.slug}`}
          className="mt-3 inline-flex items-center gap-1 text-[0.85rem] font-medium text-accent hover:text-accent-dark"
        >
          Read the full brief <ArrowRight size={14} />
        </Link>
      </div>
    </article>
  );
}
