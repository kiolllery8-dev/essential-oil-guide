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

  // 相關精油：同化學分類隨機挑 6 支（排除自己）
  const related = oils
    .filter((o) => o.catFile === oil.catFile && o.id !== oil.id)
    .slice(0, 6);

  return (
    <>
      <JsonLd data={[crumbs, article]} />
      <RawHtml html={patched} />

      {related.length > 0 && (
        <section
          style={{
            maxWidth: 1100,
            margin: '40px auto 60px',
            padding: '0 20px',
          }}
          aria-labelledby="related-oils-heading"
        >
          <h2
            id="related-oils-heading"
            style={{
              fontSize: 22,
              marginBottom: 20,
              color: 'var(--green-dark)',
              borderLeft: '4px solid var(--green-mid)',
              paddingLeft: 12,
            }}
          >
            🌿 同「{oil.category}」相關精油
          </h2>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: 14,
            }}
          >
            {related.map((r) => (
              <a
                key={r.id}
                href={`/oil/${r.id}/`}
                style={{
                  display: 'block',
                  padding: '16px 18px',
                  background: 'var(--beige-light)',
                  borderRadius: 12,
                  border: '1px solid var(--border)',
                  textDecoration: 'none',
                  color: 'inherit',
                  transition: 'transform .15s, box-shadow .15s',
                }}
              >
                <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 4 }}>{r.zh}</div>
                <div style={{ fontSize: 12, fontStyle: 'italic', color: 'var(--text-mid)', marginBottom: 8 }}>
                  {r.latin}
                </div>
                {r.components && (
                  <div style={{ fontSize: 12, color: 'var(--text-mid)', lineHeight: 1.5 }}>
                    {String(r.components).slice(0, 45)}
                    {String(r.components).length > 45 ? '…' : ''}
                  </div>
                )}
              </a>
            ))}
          </div>
        </section>
      )}
    </>
  );
}
