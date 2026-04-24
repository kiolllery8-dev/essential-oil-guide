import { loadPage } from '../lib/loadHtml';

export const dynamic = 'force-static';

const SITE = 'https://intelliverse.tw';
const SITE_NAME = '精油能量圖譜';
const BUILD_DATE = new Date('2026-04-24').toUTCString();

/** RSS items: 專題文章 + 精選精油頁 */
const FEED_ITEMS = [
  // 5 專題文章
  { slug: 'article-beginners', date: '2026-03-15' },
  { slug: 'article-sleep',     date: '2026-03-20' },
  { slug: 'article-stress',    date: '2026-03-25' },
  { slug: 'article-dustmites', date: '2026-04-01' },
  { slug: 'article-eucalyptus',date: '2026-04-10' },
  // 10 精選精油頁
  { slug: 'oil-lavender',      date: '2026-04-12' },
  { slug: 'oil-tea-tree',      date: '2026-04-12' },
  { slug: 'oil-peppermint',    date: '2026-04-13' },
  { slug: 'oil-eucalyptus',    date: '2026-04-13' },
  { slug: 'oil-frankincense',  date: '2026-04-14' },
  { slug: 'oil-cedarwood',     date: '2026-04-14' },
  { slug: 'oil-sweet-orange',  date: '2026-04-15' },
  { slug: 'oil-lemon',         date: '2026-04-15' },
  { slug: 'oil-ylang-ylang',   date: '2026-04-16' },
  { slug: 'oil-rosemary',      date: '2026-04-16' },
];

function esc(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

export function GET() {
  const items = FEED_ITEMS.map(({ slug, date }) => {
    let title = slug, description = '';
    try {
      const page = loadPage(`${slug}.html`);
      title = page.title.replace(/\s*\|\s*精油能量圖譜\s*$/, '');
      description = page.description || '';
    } catch {}
    const url = `${SITE}/${slug}/`;
    return `    <item>
      <title>${esc(title)}</title>
      <link>${url}</link>
      <guid isPermaLink="true">${url}</guid>
      <description>${esc(description)}</description>
      <pubDate>${new Date(date).toUTCString()}</pubDate>
    </item>`;
  }).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${SITE_NAME}</title>
    <link>${SITE}/</link>
    <atom:link href="${SITE}/rss.xml" rel="self" type="application/rss+xml" />
    <description>最完整的中文精油知識庫——化學分子、芳療應用、安全指南、400+ 精油。</description>
    <language>zh-TW</language>
    <copyright>© 2026 靈境智造 Intelliverse Studio</copyright>
    <lastBuildDate>${BUILD_DATE}</lastBuildDate>
    <generator>Next.js 15</generator>
${items}
  </channel>
</rss>
`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}
