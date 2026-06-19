import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import { getAllBriefs, getBrief, formatDate, formatDateLong } from "@/lib/briefs";
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

  const title = `AI Brief — ${formatDateLong(brief.date)}`;
  return {
    title: `${site.name} · ${formatDate(brief.date)}`,
    description: brief.summary,
    openGraph: { title, description: brief.summary, type: "article" },
    twitter: { card: "summary_large_image", title, description: brief.summary },
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
      <header className="bg-navy">
        <div className="mx-auto w-full max-w-3xl px-5 py-10 sm:px-8 sm:py-12">
          <Link
            href="/archive"
            className="inline-flex items-center gap-1.5 text-sm text-navy-muted transition-colors hover:text-navy-text"
          >
            <ArrowLeft size={15} /> All briefs
          </Link>
          <p className="mt-6 font-mono text-[0.72rem] uppercase tracking-[0.15em] text-owl-blue">
            Daily Brief · {brief.topHeadlines.length} signals
          </p>
          <h1 className="mt-3 font-display text-3xl leading-tight text-navy-text sm:text-[2.4rem]">
            AI Brief — {formatDateLong(brief.date)}
          </h1>
        </div>
      </header>

      <div className="mx-auto w-full max-w-3xl px-5 py-10 sm:px-8 sm:py-12">
        <div className="prose-brief" dangerouslySetInnerHTML={{ __html: brief.bodyHtml }} />

        <div className="mt-12 border-t border-line pt-6">
          <Link href="/archive" className="text-sm font-medium text-accent hover:text-accent-dark">
            ← Browse all briefs
          </Link>
        </div>
      </div>
    </article>
  );
}
