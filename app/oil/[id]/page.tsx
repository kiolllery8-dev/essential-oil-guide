import { loadPage } from '../../lib/loadHtml';
import type { Metadata } from 'next';
import oilsData from '../../../data/oils.json';
import RawHtml from '../../components/RawHtml';
import JsonLd from '../../components/JsonLd';
import { breadcrumbSchema, oilSchema, SITE, DEFAULT_OG } from '../../lib/schema';

interface Oil {
  id: string; zh: string; latin: string; category?: string;
  extractPart?: string; family?: string; safetyText?: string;
  components?: string; effects?: string; tags?: string[];
  catFile?: string;
}
const oils = oilsData as Oil[];

/** 精油 → 化學分類 slug 對應，用於麵包屑 */
const CAT_SLUG_MAP: Record<string, string> = {
  'compounds-01.html': 'compounds-01',
  'compounds-02.html': 'compounds-02',
  'compounds-03.html': 'compounds-03',
  'compounds-04.html': 'compounds-04',
  'compounds-05.html': 'compounds-05',
  'compounds-06.html': 'compounds-06',
  'compounds-07a.html': 'compounds-07a',
  'compounds-07b.html': 'compounds-07b',
  'compounds-07c.html': 'compounds-07c',
  'compounds-08.html': 'compounds-08',
  'compounds-09.html': 'compounds-09',
  'compounds-10.html': 'compounds-10',
  'compounds-11.html': 'compounds-11',
  'compounds-12.html': 'compounds-12',
};

export async function generateStaticParams() {
  return oils.map((o) => ({ id: o.id }));
}

export async function generateMetadata(
  { params }: { params: Promise<{ id: string }> }
): Promise<Metadata> {
  const { id } = await params;
  const oil = oils.find((o) => o.id === id);
  if (!oil) return {};
  const title = `${oil.zh}精油完整介紹｜${oil.latin}`;
  const desc = `${oil.zh}（${oil.latin}）：化學分類「${oil.category || '—'}」，主要成分 ${oil.components || ''}。${oil.safetyText || ''}`.slice(0, 155);
  const url = `${SITE}/oil/${id}/`;
  const ogImage = DEFAULT_OG;

  return {
    title: { absolute: title + ' | 精油能量圖譜' },
    description: desc,
    keywords: [oil.zh, oil.latin, oil.category, '精油', '芳療', ...(oil.tags || [])].filter(Boolean) as string[],
    alternates: { canonical: url },
    openGraph: {
      type: 'article',
      url,
      title,
      description: desc,
      images: [{ url: ogImage, width: 1200, height: 630, alt: `${oil.zh} ${oil.latin}` }],
    },
    twitter: { title, description: desc, images: [ogImage] },
  };
}

export default async function OilDetail({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const oil = oils.find((o) => o.id === id);
  if (!oil) return <div>404 Not Found</div>;

  // Reuse the original oil-detail.html body. Patch the JS so it picks up the id
  // from our static path instead of the (missing) ?id= query string.
  const page = loadPage('oil-detail.html');
  const patched = page.bodyHtml
    .replace(/var\s+id\s*=\s*params\.get\(['"]id['"]\)\s*;/g, `var id = ${JSON.stringify(id)};`)
    .replace(/var\s+oid\s*=\s*params\.get\(['"]id['"]\)\s*;/g, `var oid = ${JSON.stringify(id)};`);

  // 麵包屑：首頁 › 精油化學分子索引 › [化學分類] › [該精油]
  const catSlug = CAT_SLUG_MAP[oil.catFile || ''];
  const crumbList = [
    { name: '首頁', url: '/' },
    { name: '精油化學分子索引', url: '/oils/' },
  ];
  if (catSlug && oil.category) {
    crumbList.push({ name: oil.category, url: `/${catSlug}/` });
  }
  crumbList.push({ name: oil.zh, url: `/oil/${id}/` });

  const crumbs = breadcrumbSchema(crumbList);
  const article = oilSchema(oil);

  return (
    <>
      <JsonLd data={[crumbs, article]} />
      <RawHtml html={patched} />
    </>
  );
}
