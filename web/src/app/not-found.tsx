import Image from "next/image";
import Link from "next/link";

export default function NotFound() {
  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col items-center px-5 py-24 text-center sm:px-8">
      <Image
        src="/mascot/brief-owl.png"
        alt="Brief Owl mascot"
        width={180}
        height={180}
        className="h-40 w-40 object-contain"
      />
      <h1 className="mt-6 font-display text-3xl text-ink">Nothing here on this shift</h1>
      <p className="mt-2 text-muted">Brief Owl couldn&apos;t find that page.</p>
      <Link
        href="/"
        className="mt-6 inline-flex items-center rounded-md bg-accent px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-accent-dark"
      >
        Back to today&apos;s brief
      </Link>
    </div>
  );
}
