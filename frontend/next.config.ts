import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
  // (The old `eslint.ignoreDuringBuilds` key was removed: Next 16 no longer lints during
  // `next build` and rejects that option in NextConfig.)
  async rewrites() {
    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://web-production-c40ef4.up.railway.app';
    return [
      {
        source: '/api/backend/:path*',
        destination: `${backendUrl.replace(/\/+$/, '')}/:path*`,
      },
    ];
  },
};

export default nextConfig;
