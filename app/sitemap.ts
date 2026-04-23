import type { MetadataRoute } from 'next';
import { readdirSync } from 'fs';
import { join } from 'path';
import oilsData from '../data/oils.json';

const SITE = 'https://intelliverse.tw';
const HTML_DIR = join(process.cwd(), 'html-source');

export default function sitemap(): MetadataRoute.Sitemap {
  const urls: MetadataRoute.Sitemap = [{ url: `${SITE}/`, changeFrequency: 'weekly', priority: 1.0 }];

  // 35 static pages
  readdirSync(HTML_DIR)
    .filter((f) => f.endsWith('.html'))
    .map((f) => f.replace(/\.html$/, ''))
    .filter((s) => s !== 'index' && s !== 'oil-detail' && !s.startsWith('googlef'))
    .forEach((slug) => {
      urls.push({ url: `${SITE}/${slug}/`, changeFrequency: 'weekly', priority: 0.7 });
    });

  // 302 oil detail pages
  (oilsData as Array<{ id: string }>).forEach((o) => {
    urls.push({ url: `${SITE}/oil/${o.id}/`, changeFrequency: 'monthly', priority: 0.6 });
  });

  return urls;
}
