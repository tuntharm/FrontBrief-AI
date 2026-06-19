import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import { getAllBriefs, getBrief, formatDate, formatDateLong } from "@/lib/briefs";
import { Poster } from "@/components/Poster";
import { site } from "@/content/site";

export function generateStaticParams() {
  return getAllBriefs().map((b) => ({ slug: b.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const brief = await getBrief(slug);
  if (!brief) return { title: "Brief not found" };

  const title = `${formatDate(brief.date)} — ${brief.headline}`;
  const images = brief.posterSrc ? [brief.posterSrc] : undefined;
  return {
    title: `${site.name} · ${formatDate(brief.date)}`,
    description: brief.summary,
    openGraph: { title, description: brief.summary, images, type: "article" },
    twitter: { card: "summary_large_image", title, description: brief.summary, images },
  };
}

export default async function BriefPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const brief = await getBrief(slug);
  if (!brief) notFound();

  return (
    <article>
      <header className="relative overflow-hidden border-b border-line">
        <div className="absolute inset-0 navy-grid" aria-hidden />
        <div className="absolute inset-0 accent-glow" aria-hidden />
        <div className="relative mx-auto w-full max-w-3xl px-5 py-12 sm:px-8 sm:py-16">
          <Link
            href="/archive"
            className="inline-flex items-center gap-1.5 text-sm text-muted transition-colors hover:text-ink"
          >
            <ArrowLeft size={15} /> All briefs
          </Link>

          <div className="mt-7 flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <span className="label-mono">Daily Brief</span>
              <h1 className="mt-3 max-w-2xl text-2xl font-medium leading-tight tracking-tight text-ink sm:text-[2rem]">
                {formatDateLong(brief.date)}
              </h1>
            </div>
            {brief.posterSrc ? (
              <Poster
                src={brief.posterSrc}
                alt={`FrontBrief.AI poster — ${formatDate(brief.date)}`}
                className="aspect-[4/5] w-28 shrink-0 sm:w-32"
              />
            ) : null}
          </div>
        </div>
      </header>

      <div className="mx-auto w-full max-w-3xl px-5 py-12 sm:px-8 sm:py-14">
        <div
          className="prose-brief"
          dangerouslySetInnerHTML={{ __html: brief.bodyHtml }}
        />

        <div className="mt-12 border-t border-line pt-6">
          <Link href="/archive" className="text-sm text-accent-bright hover:underline">
            ← Browse all briefs
          </Link>
        </div>
      </div>
    </article>
  );
}
