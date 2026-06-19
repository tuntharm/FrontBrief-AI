import Link from "next/link";
import { Search, Rss } from "lucide-react";
import { InstagramIcon, GithubIcon } from "@/components/BrandIcons";
import { nav, social } from "@/content/site";

export function Navbar() {
  return (
    <header>
      {/* Masthead */}
      <div className="mx-auto flex w-full max-w-6xl items-end gap-4 px-5 py-6 sm:px-8 sm:py-8">
        <Link href="/" className="font-display text-4xl leading-none text-ink sm:text-6xl">
          FrontBrief<span className="text-accent">.AI</span>
        </Link>
        <span className="mb-1 hidden h-10 w-px bg-line-strong sm:block sm:h-12" aria-hidden />
        <span className="mb-1 hidden text-[0.78rem] font-medium leading-tight text-ink sm:block">
          A Daily Brief
          <br />
          from the
          <br />
          AI Frontier
        </span>
      </div>

      {/* Blue nav bar */}
      <div className="sticky top-0 z-40 bg-accent">
        <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-5 py-2.5 sm:px-8">
          <nav className="flex items-center gap-4 sm:gap-7">
            <Link
              href="/"
              className="flex h-6 w-6 items-center justify-center rounded-[5px] bg-white/20 text-[11px] font-medium text-white"
              aria-label="FrontBrief.AI home"
            >
              FB
            </Link>
            {nav.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="text-[13px] font-medium text-white/85 transition-colors hover:text-white"
              >
                {item.label}
              </Link>
            ))}
          </nav>
          <div className="flex items-center gap-3.5 text-white/85">
            <Link href="/archive" aria-label="Search briefs" className="transition-colors hover:text-white">
              <Search size={16} />
            </Link>
            <a href={social.instagram} target="_blank" rel="noreferrer" aria-label="Instagram" className="transition-colors hover:text-white">
              <InstagramIcon size={16} />
            </a>
            <a href={social.github} target="_blank" rel="noreferrer" aria-label="GitHub" className="transition-colors hover:text-white">
              <GithubIcon size={16} />
            </a>
            <span className="text-white/85" aria-hidden>
              <Rss size={16} />
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
