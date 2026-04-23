/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',          // static export → 可丟 GitHub Pages
  trailingSlash: true,        // /oil/100/ 而不是 /oil/100
  images: { unoptimized: true }, // CDN 圖片無需 Next 優化
  reactStrictMode: true,
};
export default nextConfig;
