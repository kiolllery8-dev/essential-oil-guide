import type { MetadataRoute } from 'next';
import { readdirSync, readFileSync } from 'fs';
import { join } from 'path';
import oilsData from '../data/oils.json';

export const dynamic = 'force-static';

const SITE = 'https://intelliverse.tw';
const CDN = 'https://cdn.jsdelivr.net/gh/kiolllery8-dev/essential-oil-cdn@main/images/';
const HTML_DIR = join(process.cwd(), 'html-source');
const LAST_MOD = new Date('2026-04-24');

/** 從原 HTML 抓 og:image（已是 CDN 絕對路徑）*/
function ogImageOf(filename: string): string | undefined {
  try {
    const raw = readFileSync(join(HTML_DIR, filename), 'utf-8');
    const m = raw.match(/<meta\s+property="og:image"\s+content="([^"]+)"/);
    return m ? m[1] : undefined;
  } catch { return undefined; }
}

export default function sitemap(): MetadataRoute.Sitemap {
  const urls: MetadataRoute.Sitemap = [
    {
      url: `${SITE}/`,
      changeFrequency: 'weekly',
      priority: 1.0,
      lastModified: LAST_MOD,
      images: [`${CDN}hero-home.png`],
    },
  ];

  // 直接用 app/ 路由手寫的頁面（非 html-source）
  ['about', 'disclaimer', 'privacy', 'contact'].forEach((slug) => {
    urls.push({
      url: `${SITE}/${slug}/`,
      changeFrequency: 'monthly',
      priority: 0.4,
      lastModified: LAST_MOD,
    });
  });

  // 35 個靜態頁面
  const hubs = new Set(['encyclopedia', 'oils', 'aromatherapy', 'safety']);
  readdirSync(HTML_DIR)
    .filter((f) => f.endsWith('.html'))
    .map((f) => f.replace(/\.html$/, ''))
    .filter((s) => s !== 'index' && s !== 'oil-detail' && !s.startsWith('googlef'))
    .forEach((slug) => {
      const og = ogImageOf(`${slug}.html`);
      urls.push({
        url: `${SITE}/${slug}/`,
        changeFrequency: 'weekly',
        priority: hubs.has(slug) ? 0.9 : 0.7,
        lastModified: LAST_MOD,
        ...(og ? { images: [og] } : {}),
      });
    });

  // 302 個精油靜態頁（都帶 fallback banner，未來可加 idBannerMap 對應）
  const oilBanner = `${CDN}oil-detail-banner-herbs.jpg`;
  (oilsData as Array<{ id: string }>).forEach((o) => {
    urls.push({
      url: `${SITE}/oil/${o.id}/`,
      changeFrequency: 'monthly',
      priority: 0.6,
      lastModified: LAST_MOD,
      images: [oilBanner],
    });
  });

  return urls;
}
