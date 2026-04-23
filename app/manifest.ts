import type { MetadataRoute } from 'next';

export const dynamic = 'force-static';

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: '精油能量圖譜',
    short_name: '精油能量圖譜',
    description: '最完整的中文精油知識庫——化學分子、芳療應用、安全指南、400+ 種精油資料庫。',
    start_url: '/',
    display: 'standalone',
    background_color: '#FAFAF8',
    theme_color: '#3D5A3E',
    lang: 'zh-TW',
    icons: [
      { src: '/android-chrome-192.png', sizes: '192x192', type: 'image/png' },
      { src: '/android-chrome-512.png', sizes: '512x512', type: 'image/png' },
      { src: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' },
    ],
  };
}
