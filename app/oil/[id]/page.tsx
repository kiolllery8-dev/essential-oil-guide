import { loadPage } from '../../lib/loadHtml';
import type { Metadata } from 'next';
import oilsData from '../../../data/oils.json';
import RawHtml from '../../components/RawHtml';
import JsonLd from '../../components/JsonLd';
import AISummary from '../../components/AISummary';
import RelatedLinks from '../../components/RelatedLinks';
import { breadcrumbSchema, oilSchema, sanitizeEffects, compBrief, SITE, DEFAULT_OG } from '../../lib/schema';
import { CANONICAL_OVERRIDES } from '../../lib/canonicalOverrides';
import contentDatesJson from '../../../data/content-dates.json';

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
// CANONICAL_OVERRIDES 已抽至 app/lib/canonicalOverrides.ts（sitemap 同步引用以排除非 canonical URL）

export async function generateStaticParams() {
  return oils.map((o) => ({ id: o.id }));
}

export async function generateMetadata(
  { params }: { params: Promise<{ id: string }> }
): Promise<Metadata> {
  const { id } = await params;
  const oil = oils.find((o) => o.id === id);
  if (!oil) return {};
  // SEO title 格式：對齊 GSC 實測最高頻中文查詢意圖「{X}精油功效」
  // （臨門一腳分析：排名 8-12 的 datasheet 多被「XX精油功效」查詢觸發，原 title 無「功效」二字）
  const title = `${oil.zh}精油功效｜成分、香氣、使用與安全`;
  // 描述：用 effects + 化學成分讓 AI 搜尋可索引到完整資訊。
  // 合規：meta 是機器可讀層，effects 原文療效詞（抗菌/消炎/調經…）經 sanitizeEffects 轉中性語氣；
  // 成分用 compBrief 在「、」邊界截斷，避免「香茅醇 (C。」殘缺亂碼。
  const effectsClean = sanitizeEffects((oil.effects || '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim());
  const desc = `${oil.zh}（${oil.latin}）：${oil.category || '芳療'}精油。主要成分 ${compBrief(oil.components || '', 34)}。${effectsClean ? `常見芳療應用：${effectsClean.slice(0, 50)}。` : ''}萃取自${oil.extractPart || '植物'}，使用前請參考安全指南。`.slice(0, 155);

  // ▼ Canonical 重複頁修正：若有對應的完整指南，canonical 指向 /oil-X/
  const dedicatedSlug = CANONICAL_OVERRIDES[id];
  const canonicalUrl = dedicatedSlug ? `${SITE}/${dedicatedSlug}/` : `${SITE}/oil/${id}/`;
  const url = `${SITE}/oil/${id}/`;
  const ogImage = DEFAULT_OG;

  return {
    title: { absolute: title + ' | 精油能量圖譜' },
    description: desc,
    // keywords 過 sanitize（tags 內含「消炎止痛」等療效標籤）＋去重
    keywords: Array.from(new Set(
      ([oil.zh, oil.latin, oil.category, '精油', '芳療', ...(oil.tags || [])].filter(Boolean) as string[]).map((k) => sanitizeEffects(k))
    )),
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

  // ▼ 頁重瘦身（2.66MB → ~250KB）：模板把「全站 302 支精油完整資料（~1.07MB）」內嵌進
  //   每一頁的 window.__oilData，且該 bodyHtml 又被 RSC flight payload 整包鏡像一次（×2）。
  //   client 端實際只用到 data.findIndex(id)、data[idx±1]（上/下一支導覽）與 .find(id)，
  //   所以只注入「當前這支＋前後鄰居」3 筆即可保留全部功能。
  const idx = oils.findIndex((o) => o.id === id);
  const slim = oils.slice(Math.max(0, idx - 1), idx + 2);
  const slimScript = `<script>window.__oilData=${JSON.stringify(slim).replace(/<\//g, '<\\/')}</script>`;
  const patched = page.bodyHtml
    .replace(/<script>window\.__oilData=\[[\s\S]*?<\/script>/, () => slimScript)
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
  // canonical 收編頁：schema url 同步指向 /oil-X/，與 <link rel=canonical> 一致
  const dedicated = CANONICAL_OVERRIDES[id];
  const article = oilSchema(oil, {
    canonicalUrl: dedicated ? `${SITE}/${dedicated}/` : undefined,
    dateModified: (contentDatesJson as Record<string, string>)['data/oils.json'],
  });

  // 相關精油：同化學分類隨機挑 6 支（排除自己）
  const related = oils
    .filter((o) => o.catFile === oil.catFile && o.id !== oil.id)
    .slice(0, 6);

  // 自動產生「快速答案」摘要（為 AI 搜尋引用優化；保留 effects 內既有關鍵詞）
  // 包含：植物學名、化學分類、主成分、常見芳療應用、安全提醒
  // 合規＋截斷修正：AI 摘要（會輸出成 Question/Answer JSON-LD）同樣過 sanitize；成分在「、」邊界截斷
  const compTrim = compBrief(oil.components || '', 34);
  const effectsForAI = sanitizeEffects((oil.effects || '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim());
  const aiSummary = [
    `${oil.zh}（${oil.latin}）為${oil.category || '常見芳療'}精油，`,
    `主要化學成分為 ${compTrim}${(oil.components || '').length > compTrim.length ? ' 等' : ''}。`,
    `植物科屬 ${oil.family || '—'}，萃取自${oil.extractPart || '植物'}。`,
    effectsForAI ? `常見芳療應用：${effectsForAI.slice(0, 60)}。` : '',
    `使用前請參考精油安全指南並做敏感性測試。`,
  ].filter(Boolean).join('').slice(0, 180);

  // ▼ 家族指南連結：同名家族的 datasheet（如玫瑰尤加利、藍膠尤加利）用「X精油功效與完整指南」
  //   精準錨文字指向主指南，把家族查詢的排名訊號集中到對的頁。
  //   （Ahrefs 實測：「尤加利精油功效」vol 2800 排的是 /oil/163/ 玫瑰尤加利 datasheet 而非指南——就是缺這條內鏈）
  //   長詞優先比對，避免「玫瑰尤加利」誤配到玫瑰、「綠薄荷」誤配到薄荷。
  const FAMILY_GUIDE: Array<[string, string, string]> = [
    // [zh 關鍵字, 指南 slug, 指南主詞]
    ['檸檬尤加利', 'oil-lemon-eucalyptus', '檸檬尤加利'], ['尤加利', 'oil-eucalyptus', '尤加利'],
    ['穗花薰衣草', 'oil-spike-lavender', '穗花薰衣草'], ['醒目薰衣草', 'oil-lavandin', '醒目薰衣草'], ['薰衣草', 'oil-lavender', '薰衣草'],
    ['綠薄荷', 'oil-spearmint', '綠薄荷'], ['薄荷', 'oil-peppermint', '薄荷'],
    ['玫瑰草', 'oil-palmarosa', '玫瑰草'], ['玫瑰', 'oil-rose', '玫瑰'],
    ['德國洋甘菊', 'oil-german-chamomile', '德國洋甘菊'], ['羅馬洋甘菊', 'oil-roman-chamomile', '羅馬洋甘菊'],
    ['茶樹', 'oil-tea-tree', '茶樹'], ['雪松', 'oil-cedarwood', '雪松'], ['迷迭香', 'oil-rosemary', '迷迭香'],
    ['乳香', 'oil-frankincense', '乳香'], ['檀香', 'oil-sandalwood', '檀香'], ['茉莉', 'oil-jasmine', '茉莉'],
    ['依蘭', 'oil-ylang-ylang', '依蘭'], ['杜松', 'oil-juniper', '杜松'], ['百里香', 'oil-thyme', '百里香'],
    ['橙花', 'oil-neroli', '橙花'], ['苦橙葉', 'oil-petitgrain', '苦橙葉'], ['甜橙', 'oil-sweet-orange', '甜橙'],
    ['香茅', 'oil-citronella', '香茅'], ['檸檬', 'oil-lemon', '檸檬'],
    ['絲柏', 'oil-cypress', '絲柏'], ['沒藥', 'oil-myrrh', '沒藥'], ['廣藿香', 'oil-patchouli', '廣藿香'],
    ['黑胡椒', 'oil-black-pepper', '黑胡椒'], ['天竺葵', 'oil-geranium', '天竺葵'], ['葡萄柚', 'oil-grapefruit', '葡萄柚'],
    ['佛手柑', 'oil-bergamot', '佛手柑'], ['快樂鼠尾草', 'oil-clary-sage', '快樂鼠尾草'], ['永久花', 'oil-helichrysum', '永久花'],
    ['岩蘭草', 'oil-vetiver', '岩蘭草'], ['香蜂草', 'oil-melissa', '香蜂草'], ['羅勒', 'oil-sweet-basil', '甜羅勒'],
    ['茴香', 'oil-sweet-fennel', '甜茴香'], ['馬鬱蘭', 'oil-marjoram', '甜馬鬱蘭'], ['丁香', 'oil-clove', '丁香'],
    ['月桂', 'oil-bay', '月桂'], ['蓍草', 'oil-yarrow', '西洋蓍草'], ['雲杉', 'oil-black-spruce', '黑雲杉'],
    ['桉油醇樟', 'oil-ravintsara', '桉油醇樟'],
  ];
  const familyHit = FAMILY_GUIDE.find(([kw]) => (oil.zh || '').includes(kw));
  // 自己就是該指南收編對象時交給 dedicatedBanner；家族連結只給「同族但不同種」的頁
  const familyGuide = familyHit && !CANONICAL_OVERRIDES[id] ? { slug: familyHit[1], name: familyHit[2] } : null;

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

      {/* 家族指南連結（同族不同種的 datasheet → 主指南；精準錨文字集中排名訊號） */}
      {familyGuide && (
        <div style={{ maxWidth: 1100, margin: '16px auto 0', padding: '0 20px' }}>
          <a
            href={`/${familyGuide.slug}/`}
            style={{
              display: 'flex', alignItems: 'center', gap: 10,
              background: 'var(--beige-light, #FBF7F1)',
              border: '1px solid var(--border, #E5D9C0)',
              borderRadius: 10, padding: '12px 18px',
              textDecoration: 'none', color: '#5D4A28', fontSize: 14,
            }}
          >
            <span style={{ fontSize: 18 }}>🌿</span>
            <span>
              {oil.zh}屬於{familyGuide.name}家族——想看常見品種的完整介紹？閱讀
              <strong style={{ color: '#8B6F3E' }}>{familyGuide.name}精油功效與完整指南</strong>
            </span>
            <span style={{ marginLeft: 'auto', color: '#C8A673' }}>→</span>
          </a>
        </div>
      )}

      {/* AI 友善「快速答案」：純 JSON-LD（不顯示給人，供 AI 引用） */}
      <AISummary summary={aiSummary} title={`${oil.zh}精油 快速答案`} />

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
              {oil.zh}精油的功效與常見應用方向
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
      <RelatedLinks topic={oil.zh} title={`🌿 與「${oil.zh}」相關的精油知識`} max={6} currentPath={`/oil/${oil.id}/`} />
    </>
  );
}
