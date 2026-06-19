import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { site, social } from "@/content/site";

export const metadata: Metadata = {
  title: "About",
  description: site.description,
};

const principles = [
  {
    title: "Interestingness-first",
    body: "Five items a day, chosen because they are worth reading — not to fill a quota. No padding with weak stories.",
  },
  {
    title: "Signal, not advice",
    body: "Every item carries why it's interesting, why it matters, and where capital and attention are moving. Market-aware, never hype.",
  },
  {
    title: "Broad, not niche",
    body: "Frontier models, infrastructure, markets, product adoption, policy, and one deeptech lens — the AI world distilled, not a narrow reading list.",
  },
];

export default function AboutPage() {
  return (
    <div className="mx-auto w-full max-w-3xl px-5 py-10 sm:px-8 sm:py-12">
      <h1 className="font-display text-3xl text-accent sm:text-4xl">{site.tagline}</h1>
      <p className="mt-5 text-[1.05rem] leading-relaxed text-muted">
        FrontBrief.AI distills the AI world into a handful of must-know signals every day —
        for builders, founders, investors, and the AI-curious who want to know what matters
        across frontier models, infrastructure, research, startups, adoption, and deeptech.
      </p>

      <div className="mt-10 flex flex-col items-center gap-6 rounded-xl border border-line bg-accent-soft p-6 sm:flex-row sm:p-8">
        <Image
          src="/mascot/brief-owl.png"
          alt="Brief Owl mascot"
          width={160}
          height={160}
          className="h-32 w-32 shrink-0 object-contain sm:h-40 sm:w-40"
        />
        <p className="text-[0.975rem] leading-relaxed text-muted">
          <span className="font-semibold text-ink">Meet Brief Owl.</span> It works the night
          shift — reading, ranking, and writing the brief so it&apos;s ready before you wake.
        </p>
      </div>

      <div className="mt-10 space-y-6">
        {principles.map((p) => (
          <div key={p.title}>
            <h2 className="font-display text-lg text-ink">{p.title}</h2>
            <p className="mt-1.5 text-[0.975rem] leading-relaxed text-muted">{p.body}</p>
          </div>
        ))}
      </div>

      <div className="mt-12 border-t border-line pt-6">
        <p className="text-sm text-muted">
          Read it daily on{" "}
          <a href={social.instagram} target="_blank" rel="noreferrer" className="font-medium text-accent hover:text-accent-dark">
            Instagram
          </a>
          , or browse the{" "}
          <Link href="/archive" className="font-medium text-accent hover:text-accent-dark">
            full archive
          </Link>
          .
        </p>
      </div>
    </div>
  );
}
