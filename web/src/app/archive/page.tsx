import type { Metadata } from "next";
import { getAllBriefs, formatDate } from "@/lib/briefs";
import { BriefRow } from "@/components/BriefRow";

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
    <div className="mx-auto w-full max-w-6xl px-5 py-10 sm:px-8 sm:py-12">
      <h1 className="font-display text-3xl text-accent sm:text-4xl">All Briefs</h1>
      <p className="mt-3 max-w-xl text-[0.975rem] leading-relaxed text-muted">
        {all.length} daily {all.length === 1 ? "brief" : "briefs"} from the AI frontier.
        Latest published {all[0] ? formatDate(all[0].date) : "—"}.
      </p>

      <div className="mt-8 space-y-10">
        {groups.map((group) => (
          <section key={group.month}>
            <div className="mb-1 flex items-center gap-3">
              <h2 className="font-display text-lg text-ink">{group.month}</h2>
              <span className="h-px flex-1 bg-line" aria-hidden />
            </div>
            <div>
              {group.briefs.map((brief) => (
                <BriefRow key={brief.slug} brief={brief} />
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}
