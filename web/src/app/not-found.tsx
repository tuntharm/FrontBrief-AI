import Image from "next/image";
import Link from "next/link";

export default function NotFound() {
  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col items-center px-5 py-24 text-center sm:px-8">
      <div className="relative h-24 w-24 overflow-hidden rounded-2xl border border-accent-line bg-white">
        <Image src="/mascot/brief-owl.png" alt="Brief Owl mascot" fill className="object-contain p-2" />
      </div>
      <h1 className="mt-6 text-2xl font-medium text-ink">Nothing here on this shift</h1>
      <p className="mt-2 text-muted">
        Brief Owl couldn&apos;t find that page.
      </p>
      <Link
        href="/"
        className="mt-6 inline-flex items-center rounded-md bg-accent px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-accent-bright"
      >
        Back to today&apos;s brief
      </Link>
    </div>
  );
}
