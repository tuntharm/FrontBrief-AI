/**
 * Site-wide identity, navigation, and external links.
 * Edit this first when personalising the FrontBrief.AI website.
 */
export const site = {
  name: "FrontBrief.AI",
  tagline: "A daily brief from the AI frontier.",
  description:
    "FrontBrief.AI distills the AI world into five must-know signals a day — frontier models, infrastructure, markets, adoption, and deeptech. Sharp, concise, interestingness-first.",
  // Override with NEXT_PUBLIC_SITE_URL on a staging/preview deploy.
  url: process.env.NEXT_PUBLIC_SITE_URL ?? "https://frontbrief.ai",
};

export const nav = [
  { label: "Today", href: "/" },
  { label: "Archive", href: "/archive" },
  { label: "About", href: "/about" },
];

export const social = {
  instagram: "https://www.instagram.com/frontbrief.ai/",
  email: "contact@tharmlab.com",
};
