import type { Metadata } from "next";
import { getAllBriefs, formatDate } from "@/lib/briefs";
import { BriefCard } from "@/components/BriefCard";

export const metadata: Metadata = {
  title: "Archive",
  description: "Every FrontBrief.AI daily brief, newest first.",
};

function monthKey(date: string): string {
  return new Date(`${date}T00:00:00Z`).toLocaleDateString("en-GB", {
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  });
}

export default function ArchivePage() {
  const all = getAllBriefs();

  const groups: { month: string; briefs: typeof all }[] = [];
  for (const brief of all) {
    const month = monthKey(brief.date);
    const last = groups[groups.length - 1];
    if (last && last.month === month) last.briefs.push(brief);
    else groups.push({ month, briefs: [brief] });
  }

  return (
    <div className="mx-auto w-full max-w-5xl px-5 py-12 sm:px-8 sm:py-16">
      <span className="label-mono">Archive</span>
      <h1 className="mt-3 text-2xl font-medium tracking-tight text-ink sm:text-3xl">
        Every brief, newest first
      </h1>
      <p className="mt-3 max-w-xl text-[0.975rem] leading-relaxed text-muted">
        {all.length} daily {all.length === 1 ? "brief" : "briefs"} from the AI frontier.
        Latest published {all[0] ? formatDate(all[0].date) : "—"}.
      </p>

      <div className="mt-10 space-y-12">
        {groups.map((group) => (
          <section key={group.month}>
            <div className="mb-5 flex items-center gap-3">
              <h2 className="text-sm font-medium text-muted">{group.month}</h2>
              <span className="h-px flex-1 bg-line" aria-hidden />
            </div>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
              {group.briefs.map((brief) => (
                <BriefCard key={brief.slug} brief={brief} />
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}
