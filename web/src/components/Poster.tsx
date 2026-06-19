import Image from "next/image";

/**
 * Daily poster thumbnail. Falls back to a branded placeholder when the routine
 * hasn't committed a poster for that day (older briefs have none).
 */
export function Poster({
  src,
  alt,
  className = "",
  rounded = "rounded-lg",
}: {
  src: string | null;
  alt: string;
  className?: string;
  rounded?: string;
}) {
  if (!src) {
    return (
      <div
        className={`flex items-center justify-center border border-accent-line bg-surface ${rounded} ${className}`}
        aria-label={`${alt} (no poster)`}
      >
        <span className="flex h-9 w-9 items-center justify-center rounded-[5px] bg-accent text-[13px] font-medium tracking-tighter text-white">
          FB
        </span>
      </div>
    );
  }

  return (
    <div className={`relative overflow-hidden border border-line ${rounded} ${className}`}>
      <Image src={src} alt={alt} fill sizes="(max-width: 768px) 40vw, 220px" className="object-cover" />
    </div>
  );
}
