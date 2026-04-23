import type { MetadataRoute } from 'next';
import { readdirSync } from 'fs';
import { join } from 'path';
import oilsData from '../data/oils.json';

export const dynamic = 'force-static';

const SITE = 'https://intelliverse.tw';
const HTML_DIR = join(process.cwd(), 'html-source');
const LAST_MOD = new Date('2026-04-23');

export default function sitemap(): MetadataRoute.Sitemap {
  const urls: MetadataRoute.Sitemap = [
    { url: `${SITE}/`, changeFrequency: 'weekly', priority: 1.0, lastModified: LAST_MOD },
  ];

  // 35 個靜態頁面
  const hubs = new Set(['encyclopedia', 'oils', 'aromatherapy', 'safety']);
  readdirSync(HTML_DIR)
    .filter((f) => f.endsWith('.html'))
    .map((f) => f.replace(/\.html$/, ''))
    .filter((s) => s !== 'index' && s !== 'oil-detail' && !s.startsWith('googlef'))
    .forEach((slug) => {
      urls.push({
        url: `${SITE}/${slug}/`,
        changeFrequency: 'weekly',
        priority: hubs.has(slug) ? 0.9 : 0.7,
        lastModified: LAST_MOD,
      });
    });

  // 302 個精油靜態頁
  (oilsData as Array<{ id: string }>).forEach((o) => {
    urls.push({
      url: `${SITE}/oil/${o.id}/`,
      changeFrequency: 'monthly',
      priority: 0.6,
      lastModified: LAST_MOD,
    });
  });

  return urls;
}
