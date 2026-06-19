import Link from "next/link";
import type { BriefMeta } from "@/lib/briefs";
import { formatDate } from "@/lib/briefs";
import { Poster } from "@/components/Poster";

export function BriefCard({ brief }: { brief: BriefMeta }) {
  return (
    <Link
      href={`/brief/${brief.slug}`}
      className="group flex flex-col overflow-hidden rounded-xl border border-line bg-surface transition-colors hover:border-accent-line"
    >
      <Poster
        src={brief.posterSrc}
        alt={`FrontBrief.AI — ${formatDate(brief.date)}`}
        rounded="rounded-none"
        className="aspect-[4/3] w-full"
      />
      <div className="flex flex-1 flex-col p-4">
        <span className="label-mono">{formatDate(brief.date)}</span>
        <p className="mt-2 text-[0.95rem] font-medium leading-snug text-ink group-hover:text-accent-bright">
          {brief.headline}
        </p>
      </div>
    </Link>
  );
}
