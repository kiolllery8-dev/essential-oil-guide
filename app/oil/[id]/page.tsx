import { loadPage } from '../../lib/loadHtml';
import type { Metadata } from 'next';
import oilsData from '../../../data/oils.json';
import RawHtml from '../../components/RawHtml';
import JsonLd from '../../components/JsonLd';
import AISummary from '../../components/AISummary';
import RelatedLinks from '../../components/RelatedLinks';
import { breadcrumbSchema, oilSchema, SITE, DEFAULT_OG } from '../../lib/schema';

interface Oil {
  id: string; zh: string; latin: string; category?: string;
  extractPart?: string; family?: string; safetyText?: string;
  components?: string; effects?: string; tags?: string[];
  catFile?: string; pharmacology?: string; aliases?: string[];
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

/**
 * Canonical 重複頁修正：oils.json id → 對應的完整指南 slug
 *
 * 修復 SEO 災難：23+ 個精油同時存在 /oil-X/ 和 /oil/N/ 兩個 URL，
 * 造成 Google 視為重複內容、稀釋排名。
 *
 * 規則：
 *  - 如果 oil.id 在這個 map 裡，則 canonical → /oil-X/
 *  - 並在頁面顯眼處放「更完整指南 →」按鈕引導用戶 + 爬蟲
 *  - 麵包屑也指向完整指南
 *
 * 來源：手動對照 oils.json 與 46 個 oil-*.html 完整指南
 */
const CANONICAL_OVERRIDES: Record<string, string> = {
  // 柑橘類
  '34': 'oil-lemon', '310': 'oil-lemon',
  '144': 'oil-lemon-eucalyptus',
  '159': 'oil-petitgrain',
  '160': 'oil-bergamot',
  '218': 'oil-neroli',
  '311': 'oil-grapefruit',
  // 花朵類
  '182': 'oil-jasmine',
  '192': 'oil-rose', '234': 'oil-rose',
  '207': 'oil-helichrysum',
  // 菊科
  '92': 'oil-yarrow',
  '108': 'oil-german-chamomile',
  '157': 'oil-roman-chamomile',
  // 薰衣草系
  '82': 'oil-spike-lavender',
  '165': 'oil-lavender', '209': 'oil-lavender',
  '166': 'oil-lavandin',
  // 香草類
  '47': 'oil-rosemary', '87': 'oil-rosemary',
  '150': 'oil-melissa',
  '171': 'oil-clary-sage',
  '222': 'oil-palmarosa',
  '230': 'oil-sweet-basil',
  '233': 'oil-geranium',
  '238': 'oil-thyme',
  // 薄荷類
  '41': 'oil-spearmint',
  '42': 'oil-peppermint', '226': 'oil-peppermint',
  // 呼吸類
  '72': 'oil-bay',
  '73': 'oil-ravintsara',
  '76': 'oil-eucalyptus',
  '224': 'oil-tea-tree',
  // 木質/松柏
  '102': 'oil-myrrh',
  '201': 'oil-cedarwood',
  '285': 'oil-patchouli',
  '287': 'oil-sandalwood',
  '292': 'oil-vetiver',
  '315': 'oil-cypress',
  '320': 'oil-juniper',
  '325': 'oil-black-spruce',
  // 辛香類
  '120': 'oil-ginger',
  '143': 'oil-citronella',
  '252': 'oil-clove',
  '330': 'oil-black-pepper',
  // 樹脂・其他
  '124': 'oil-sweet-fennel',
  '301': 'oil-frankincense',
  // 柑橘類
  '97': 'oil-ylang-ylang',
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
  // SEO title 格式：{中文}精油｜成分、香氣、使用方式與安全注意
  const title = `${oil.zh}精油｜成分、香氣、使用方式與安全注意`;
  // 描述：用 effects（已有的「化解黏液、抗菌、消炎」等實際關鍵詞）+ 化學成分
  // 讓 AI 搜尋（ChatGPT Search / Perplexity / Google AI Overview）可索引到完整資訊
  const effectsClean = (oil.effects || '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
  const desc = `${oil.zh}（${oil.latin}）：${oil.category || '芳療'}精油。主要成分 ${(oil.components || '').slice(0, 32)}。${effectsClean ? `常見芳療應用：${effectsClean.slice(0, 50)}。` : ''}萃取自${oil.extractPart || '植物'}，使用前請參考安全指南。`.slice(0, 155);

  // ▼ Canonical 重複頁修正：若有對應的完整指南，canonical 指向 /oil-X/
  const dedicatedSlug = CANONICAL_OVERRIDES[id];
  const canonicalUrl = dedicatedSlug ? `${SITE}/${dedicatedSlug}/` : `${SITE}/oil/${id}/`;
  const url = `${SITE}/oil/${id}/`;
  const ogImage = DEFAULT_OG;

  return {
    title: { absolute: title + ' | 精油能量圖譜' },
    description: desc,
    keywords: [oil.zh, oil.latin, oil.category, '精油', '芳療', ...(oil.tags || [])].filter(Boolean) as string[],
    alternates: { canonical: canonicalUrl },
    openGraph: {
      type: 'article',
      url: canonicalUrl,
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

  // 自動產生「快速答案」摘要（為 AI 搜尋引用優化；保留 effects 內既有關鍵詞）
  // 包含：植物學名、化學分類、主成分、常見芳療應用、安全提醒
  const compTrim = (oil.components || '').slice(0, 32);
  const effectsForAI = (oil.effects || '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
  const aiSummary = [
    `${oil.zh}（${oil.latin}）為${oil.category || '常見芳療'}精油，`,
    `主要化學成分為 ${compTrim}${(oil.components || '').length > 32 ? '…' : ''}。`,
    `植物科屬 ${oil.family || '—'}，萃取自${oil.extractPart || '植物'}。`,
    effectsForAI ? `常見芳療應用：${effectsForAI.slice(0, 60)}。` : '',
    `使用前請參考精油安全指南並做敏感性測試。`,
  ].filter(Boolean).join('').slice(0, 180);

  // ▼ 若有對應的完整指南，顯示醒目導引橫幅（同時做 canonical 收編）
  const dedicatedSlug = CANONICAL_OVERRIDES[id];
  const dedicatedBanner = dedicatedSlug ? (
    <div style={{ maxWidth: 1100, margin: '20px auto 0', padding: '0 20px' }}>
      <a
        href={`/${dedicatedSlug}/`}
        style={{
          display: 'block',
          background: 'linear-gradient(135deg,#FBF7F1 0%,#F4EDE4 100%)',
          border: '2px solid #C8A673',
          borderRadius: 14,
          padding: '20px 26px',
          textDecoration: 'none',
          color: '#5D4A28',
          transition: 'transform .15s, box-shadow .2s',
          boxShadow: '0 2px 8px rgba(200,166,115,0.15)',
        }}
        rel="canonical"
      >
        <div style={{ display: 'flex', gap: 14, alignItems: 'center' }}>
          <div style={{ fontSize: 32, flexShrink: 0 }}>📖</div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 13, color: '#8B6F3E', fontWeight: 600, marginBottom: 4, letterSpacing: '0.05em' }}>
              ✦ 推薦閱讀完整指南
            </div>
            <div style={{ fontSize: 18, fontWeight: 700, marginBottom: 4 }}>
              {oil.zh}精油 5000+ 字 IFA 標準完整指南 →
            </div>
            <div style={{ fontSize: 13, lineHeight: 1.7, color: '#7A6852' }}>
              包含：化學成分詳解、IFA + 中醫雙觀點、6 大功效、DIY 配方、安全須知、心靈能量、研究文獻、芳療師筆記、FAQ。
              本頁（化學分子 datasheet）為簡要版。
            </div>
          </div>
          <div style={{ fontSize: 24, color: '#C8A673', flexShrink: 0 }}>→</div>
        </div>
      </a>
    </div>
  ) : null;

  return (
    <>
      <JsonLd data={[crumbs, article]} />

      {dedicatedBanner}

      {/* AI 友善「快速答案」區塊（Google AI Overview / ChatGPT Search / Perplexity 引用優化） */}
      <div style={{ maxWidth: 1100, margin: '0 auto', padding: '0 20px' }}>
        <AISummary summary={aiSummary} title={`${oil.zh}精油 快速答案`} />
      </div>

      {/* ▼ Server-rendered 核心內容（讓非 JS 爬蟲 GPTBot/Perplexity 也看得到 pharmacology）
          oil-detail.html 是 client-side innerHTML 渲染，AI 爬蟲看不到；這裡把 oils.json 的
          pharmacology + 結構化資料直接 SSR 進靜態 HTML，解決 thin-content 與 AI 引用問題 */}
      <section style={{ maxWidth: 1100, margin: '0 auto', padding: '0 20px' }} aria-label={`${oil.zh}精油核心資訊`}>
        {/* 結構化速覽事實 */}
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
          gap: 12, margin: '24px 0',
        }}>
          {[
            ['🌿 植物科屬', oil.family],
            ['⚗️ 化學分類', oil.category],
            ['🧪 主要成分', oil.components],
            ['💧 萃取方式', oil.extractPart],
            ['📚 別名／學名', (oil.aliases && oil.aliases.length) ? oil.aliases.join('、') : ''],
          ].filter(([, v]) => v).map(([label, value]) => (
            <div key={label} style={{
              background: 'var(--beige-light, #FBF7F1)', border: '1px solid var(--border, #E5D9C0)',
              borderRadius: 10, padding: '12px 16px',
            }}>
              <div style={{ fontSize: 12, color: 'var(--text-light, #8B6F3E)', marginBottom: 4 }}>{label}</div>
              <div style={{ fontSize: 14, fontWeight: 600, color: '#3D3328', lineHeight: 1.5 }}>{value}</div>
            </div>
          ))}
        </div>

        {/* 藥學屬性主文（pharmacology，~900字 SSR） */}
        {oil.pharmacology && (
          <div style={{ fontSize: 15, lineHeight: 1.9, color: '#2C2C2C', margin: '8px 0 24px' }}
               dangerouslySetInnerHTML={{ __html: oil.pharmacology }} />
        )}

        {/* 常見芳療應用 */}
        {effectsForAI && (
          <div style={{ margin: '16px 0' }}>
            <h2 style={{ fontSize: 18, fontWeight: 700, color: 'var(--green-dark, #3a5a40)', margin: '0 0 8px' }}>
              {oil.zh}精油的常見應用方向
            </h2>
            <p style={{ fontSize: 15, lineHeight: 1.9, color: '#2C2C2C', margin: 0 }}>
              {oil.zh}（{oil.latin}）在日常芳療中常見於：{effectsForAI}。
              建議稀釋後使用，並依個人膚質與狀況斟酌。
            </p>
          </div>
        )}

        {/* 安全提醒 */}
        {oil.safetyText && (
          <div style={{
            background: '#FFF4E6', borderLeft: '4px solid #E8A04B', borderRadius: 8,
            padding: '14px 18px', margin: '16px 0',
          }}>
            <strong style={{ color: '#B5701A', fontSize: 14 }}>⚠️ 安全使用提醒</strong>
            <p style={{ fontSize: 14, lineHeight: 1.8, color: '#5D4A28', margin: '6px 0 0' }}>
              {(oil.safetyText || '').replace(/<[^>]+>/g, '')}　使用前請參考
              <a href="/safety/" style={{ color: '#B5701A', fontWeight: 600 }}>精油安全指南</a>。
            </p>
          </div>
        )}
      </section>

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

      {/* 站內延伸閱讀：強化內部連結深度與 AI 引用上下文 */}
      <RelatedLinks topic={oil.zh} title={`🌿 與「${oil.zh}」相關的精油知識`} max={6} />
    </>
  );
}
