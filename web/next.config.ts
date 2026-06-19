import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Posters and brand art are PNGs synced into /public; no remote images.
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
