import Link from "next/link";
import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { getAllBriefs, formatDateLong } from "@/lib/briefs";
import { BriefRow } from "@/components/BriefRow";

export default function Home() {
  const all = getAllBriefs();
  const latest = all[0];

  // "Today" shows only the last 7 days, anchored to the latest brief's date.
  const cutoff = latest ? new Date(`${latest.date}T00:00:00Z`) : new Date();
  cutoff.setUTCDate(cutoff.getUTCDate() - 6);
  const rest = all
    .slice(1)
    .filter((b) => new Date(`${b.date}T00:00:00Z`) >= cutoff);

  if (!latest) {
    return (
      <div className="mx-auto max-w-6xl px-5 py-24 text-center sm:px-8">
        <p className="text-muted">No briefs published yet. Check back soon.</p>
      </div>
    );
  }

  return (
    <div>
      {/* Hero banner */}
      <section className="bg-navy">
        <div className="mx-auto w-full max-w-6xl px-5 sm:px-8">
          <div className="flex flex-col items-center gap-6 py-10 sm:flex-row sm:justify-between sm:py-12">
            <div className="order-2 max-w-xl text-center sm:order-1 sm:text-left">
              <span className="font-mono text-[0.72rem] uppercase tracking-[0.15em] text-owl-blue">
                Today&apos;s Edition
              </span>
              <h1 className="mt-3 font-display text-3xl leading-[1.05] text-navy-text sm:text-5xl">
                AI Brief — {formatDateLong(latest.date)}
              </h1>
              <p className="mx-auto mt-4 max-w-md text-[0.98rem] leading-relaxed text-navy-muted sm:mx-0">
                Five must-know signals from the AI frontier — models, money, and deeptech, read and
                ranked before you wake.
              </p>
              <Link
                href={`/brief/${latest.slug}`}
                className="mt-6 inline-flex items-center gap-1.5 rounded-md bg-white px-5 py-2.5 text-sm font-medium text-navy transition-colors hover:bg-accent hover:text-white"
              >
                Read the full brief <ArrowRight size={15} />
              </Link>
            </div>

            <div className="relative order-1 shrink-0 sm:order-2">
              <div
                className="absolute inset-0 -z-0 rounded-full bg-[radial-gradient(circle,rgba(43,70,201,0.55),transparent_68%)] blur-2xl"
                aria-hidden
              />
              <Image
                src="/mascot/owl-flying.png"
                alt="Brief Owl mascot"
                width={340}
                height={306}
                priority
                className="relative h-52 w-auto object-contain sm:h-72"
              />
            </div>
          </div>
        </div>

        {/* Top-story ticker */}
        <Link href={`/brief/${latest.slug}`} className="block bg-accent">
          <div className="mx-auto flex w-full max-w-6xl items-center gap-3 px-5 py-2.5 sm:px-8">
            <span className="shrink-0 rounded-sm bg-white px-2 py-0.5 text-[0.62rem] font-semibold uppercase tracking-wide text-accent">
              Top story
            </span>
            <span className="truncate text-sm text-white">{latest.headline}</span>
          </div>
        </Link>
      </section>

      {/* Latest briefs feed */}
      <section className="mx-auto w-full max-w-6xl px-5 py-10 sm:px-8 sm:py-12">
        <div className="mb-2 flex items-end justify-between">
          <h2 className="font-display text-2xl text-accent">Latest Briefs</h2>
          <Link href="/archive" className="text-sm text-muted hover:text-accent">
            View archive →
          </Link>
        </div>
        <div>
          {rest.length > 0 ? (
            rest.map((brief) => <BriefRow key={brief.slug} brief={brief} />)
          ) : (
            <p className="py-8 text-muted">More briefs coming soon.</p>
          )}
        </div>
      </section>

      {/* About strip */}
      <section className="mx-auto w-full max-w-6xl px-5 pb-14 sm:px-8">
        <div className="flex flex-col overflow-hidden rounded-xl border border-line sm:flex-row">
          <div className="flex items-center justify-center bg-accent-soft px-8 py-8 sm:w-64 sm:shrink-0">
            <Image
              src="/mascot/owl-standing.png"
              alt="Brief Owl mascot"
              width={200}
              height={280}
              className="h-40 w-auto object-contain sm:h-52"
            />
          </div>
          <div className="p-6 sm:p-8">
            <span className="rounded-sm bg-accent px-2 py-0.5 text-[0.62rem] font-semibold uppercase tracking-wide text-white">
              About
            </span>
            <h3 className="mt-3 font-display text-2xl leading-tight text-accent">
              Quality AI signal, every morning
            </h3>
            <p className="mt-3 max-w-xl text-[0.95rem] leading-relaxed text-muted">
              Meet Brief Owl. It works the night shift — reading, ranking, and writing the day&apos;s
              five signals across frontier models, infrastructure, markets, adoption, and deeptech,
              so the brief is ready before you wake. Interestingness-first, signal not advice.
            </p>
            <Link
              href="/about"
              className="mt-4 inline-flex items-center gap-1 text-[0.85rem] font-medium text-accent hover:text-accent-dark"
            >
              More about FrontBrief.AI <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
