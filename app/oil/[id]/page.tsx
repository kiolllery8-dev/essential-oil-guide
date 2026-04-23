import { loadPage } from '../../lib/loadHtml';
import type { Metadata } from 'next';
import oilsData from '../../../data/oils.json';
import RawHtml from '../../components/RawHtml';

const oils = oilsData as Array<{
  id: string; zh: string; latin: string; category?: string;
  extractPart?: string; family?: string; safetyText?: string;
  components?: string;
}>;

export async function generateStaticParams() {
  return oils.map((o) => ({ id: o.id }));
}

export async function generateMetadata(
  { params }: { params: Promise<{ id: string }> }
): Promise<Metadata> {
  const { id } = await params;
  const oil = oils.find((o) => o.id === id);
  if (!oil) return {};
  const desc = `${oil.zh}（${oil.latin}）：化學分類「${oil.category || '—'}」，主要成分 ${oil.components || ''}。${oil.safetyText || ''}`.slice(0, 155);
  return {
    title: { absolute: `${oil.zh} ${oil.latin} | 精油能量圖譜` },
    description: desc,
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

  return <RawHtml html={patched} />;
}
