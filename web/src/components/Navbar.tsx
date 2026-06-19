import Link from "next/link";
import { nav, social } from "@/content/site";

export function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-line bg-navy/85 backdrop-blur">
      <div className="mx-auto flex w-full max-w-5xl items-center justify-between px-5 py-3.5 sm:px-8">
        <Link href="/" className="flex items-center gap-2.5">
          <span className="flex h-7 w-7 items-center justify-center rounded-[5px] bg-accent text-[13px] font-medium tracking-tighter text-white">
            FB
          </span>
          <span className="text-[15px] font-medium text-ink">
            FrontBrief<span className="text-accent-bright">.AI</span>
          </span>
        </Link>

        <nav className="flex items-center gap-5 text-[13.5px] text-muted sm:gap-7">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="transition-colors hover:text-ink"
            >
              {item.label}
            </Link>
          ))}
          <a
            href={social.instagram}
            target="_blank"
            rel="noreferrer"
            className="hidden text-faint transition-colors hover:text-ink sm:inline"
          >
            Instagram
          </a>
        </nav>
      </div>
    </header>
  );
}
