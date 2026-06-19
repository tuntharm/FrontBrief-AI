import Link from "next/link";
import { nav, site, social } from "@/content/site";

export function Footer() {
  return (
    <footer className="mt-4 border-t border-line bg-surface">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 px-5 py-8 sm:flex-row sm:items-center sm:justify-between sm:px-8">
        <div>
          <p className="font-display text-lg text-ink">
            FrontBrief<span className="text-accent">.AI</span>
          </p>
          <p className="mt-1 text-xs text-faint">{site.tagline}</p>
        </div>

        <div className="flex flex-wrap items-center gap-x-5 gap-y-2 text-xs text-muted">
          {nav.map((item) => (
            <Link key={item.href} href={item.href} className="hover:text-accent">
              {item.label}
            </Link>
          ))}
          <a href={social.instagram} target="_blank" rel="noreferrer" className="hover:text-accent">
            Instagram
          </a>
          <a href={social.github} target="_blank" rel="noreferrer" className="hover:text-accent">
            GitHub
          </a>
        </div>
      </div>
    </footer>
  );
}
