/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['images.unsplash.com'],
    formats: ['image/avif', 'image/webp'],
    minimumCacheTTL: 60,
  },
  experimental: {
    appDir: true,
  },
  optimizeFonts: true,
};

module.exports = nextConfig;