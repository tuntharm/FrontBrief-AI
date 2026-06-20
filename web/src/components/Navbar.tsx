import Link from "next/link";
import Image from "next/image";
import { Search, Rss, Mail } from "lucide-react";
import { InstagramIcon } from "@/components/BrandIcons";
import { nav, social } from "@/content/site";

export function Navbar() {
  return (
    <header>
      {/* Masthead */}
      <div className="mx-auto flex w-full max-w-6xl items-end gap-3 px-5 py-6 sm:gap-4 sm:px-8 sm:py-8">
        <Link href="/" className="flex items-end gap-3">
          <Image
            src="/fb-black.png"
            alt=""
            width={56}
            height={56}
            className="h-10 w-10 sm:h-14 sm:w-14"
          />
          <span className="font-display text-4xl leading-none text-ink sm:text-6xl">
            FrontBrief<span className="text-accent">.AI</span>
          </span>
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
            <Link href="/" aria-label="FrontBrief.AI home" className="flex items-center">
              <Image src="/fb-white.png" alt="FrontBrief.AI" width={28} height={28} className="h-7 w-7" />
            </Link>
            {nav.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="text-[15px] font-medium text-white/85 transition-colors hover:text-white sm:text-base"
              >
                {item.label}
              </Link>
            ))}
          </nav>
          <div className="flex items-center gap-3.5 text-white/85">
            <Link href="/archive" aria-label="Search briefs" className="transition-colors hover:text-white">
              <Search size={17} />
            </Link>
            <a href={social.instagram} target="_blank" rel="noreferrer" aria-label="Instagram" className="transition-colors hover:text-white">
              <InstagramIcon size={17} />
            </a>
            <a href={`mailto:${social.email}`} aria-label="Email" className="transition-colors hover:text-white">
              <Mail size={17} />
            </a>
            <span className="text-white/85" aria-hidden>
              <Rss size={17} />
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
