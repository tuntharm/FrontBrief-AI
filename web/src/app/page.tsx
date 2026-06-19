import Link from "next/link";
import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { getAllBriefs, getBrief, formatDate } from "@/lib/briefs";
import { Poster } from "@/components/Poster";
import { BriefCard } from "@/components/BriefCard";

export default async function Home() {
  const all = getAllBriefs();
  const latest = all[0] ? await getBrief(all[0].slug) : null;
  const recent = all.slice(1, 7);

  if (!latest) {
    return (
      <div className="mx-auto max-w-5xl px-5 py-24 text-center sm:px-8">
        <p className="text-muted">No briefs published yet. Check back soon.</p>
      </div>
    );
  }

  return (
    <div>
      {/* Today's Brief hero */}
      <section className="relative overflow-hidden border-b border-line">
        <div className="absolute inset-0 navy-grid" aria-hidden />
        <div className="absolute inset-0 accent-glow" aria-hidden />
        <div className="relative mx-auto w-full max-w-5xl px-5 py-14 sm:px-8 sm:py-20">
          <span className="label-mono">Today&apos;s Brief · {formatDate(latest.date)}</span>
          <div className="mt-5 flex flex-col gap-8 md:flex-row md:items-start md:justify-between">
            <div className="max-w-2xl">
              <h1 className="text-3xl font-medium leading-[1.15] tracking-tight text-ink sm:text-[2.6rem]">
                {latest.headline}
              </h1>
              <p className="mt-5 max-w-xl text-[1.05rem] leading-relaxed text-muted">
                {latest.summary}
              </p>
              <div className="mt-7 flex flex-wrap gap-3">
                <Link
                  href={`/brief/${latest.slug}`}
                  className="inline-flex items-center gap-1.5 rounded-md bg-accent px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-accent-bright"
                >
                  Read full brief <ArrowRight size={15} />
                </Link>
                <Link
                  href="/archive"
                  className="inline-flex items-center rounded-md border border-line-strong px-4 py-2.5 text-sm text-muted transition-colors hover:text-ink"
                >
                  View archive
                </Link>
              </div>
            </div>

            <Link
              href={`/brief/${latest.slug}`}
              className="w-full shrink-0 md:w-[220px]"
              aria-label="Read today's brief"
            >
              <Poster
                src={latest.posterSrc}
                alt={`FrontBrief.AI poster — ${formatDate(latest.date)}`}
                className="aspect-[4/5] w-full"
              />
            </Link>
          </div>

          {/* TL;DR */}
          {latest.tldr.length > 0 ? (
            <div className="mt-10 rounded-xl border border-accent-line bg-accent-tint p-5 sm:p-6">
              <span className="label-mono">TL;DR — the {latest.tldr.length} that matter</span>
              <ol className="mt-3 space-y-2.5">
                {latest.tldr.map((item, i) => (
                  <li key={i} className="flex gap-3 text-[0.95rem] leading-relaxed text-muted">
                    <span className="font-mono text-sm text-accent-bright">{i + 1}</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ol>
            </div>
          ) : null}
        </div>
      </section>

      {/* Brief Owl welcome strip */}
      <section className="mx-auto w-full max-w-5xl px-5 sm:px-8">
        <div className="mt-10 flex items-center gap-4 rounded-2xl border border-line bg-surface p-4 sm:p-5">
          <div className="relative h-14 w-14 shrink-0 overflow-hidden rounded-xl border border-accent-line bg-white sm:h-16 sm:w-16">
            <Image src="/mascot/brief-owl.png" alt="Brief Owl mascot" fill className="object-contain p-1" />
          </div>
          <p className="text-sm leading-relaxed text-muted sm:text-[0.95rem]">
            <span className="font-medium text-ink">Brief Owl clocked in for the night shift.</span>{" "}
            Five signals from the AI frontier, read and ranked before you wake.
          </p>
        </div>
      </section>

      {/* Recent briefs */}
      {recent.length > 0 ? (
        <section className="mx-auto w-full max-w-5xl px-5 py-12 sm:px-8 sm:py-16">
          <div className="mb-6 flex items-center gap-3">
            <span className="label-mono">Recent briefs</span>
            <span className="h-px flex-1 bg-line" aria-hidden />
            <Link href="/archive" className="text-xs text-muted hover:text-ink">
              All briefs →
            </Link>
          </div>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-3">
            {recent.map((brief) => (
              <BriefCard key={brief.slug} brief={brief} />
            ))}
          </div>
        </section>
      ) : null}
    </div>
  );
}
