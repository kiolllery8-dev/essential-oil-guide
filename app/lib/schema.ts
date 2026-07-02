/**
 * schema.org JSON-LD 物件產生器
 * 用 https://validator.schema.org/ 驗證
 */

export const SITE = 'https://intelliverse.tw';
export const SITE_NAME = '精油能量圖譜';
export const LOGO = `${SITE}/android-chrome-192.png`; // Google 要求 Organization logo ≥112×112
// og:image 用 JPEG（98KB；部分社群平台不吃 WebP，原 611KB PNG 太肥）
export const DEFAULT_OG = 'https://cdn.jsdelivr.net/gh/kiolllery8-dev/essential-oil-cdn@main/images/hero-home-og.jpg';
// 首頁 hero 背景實際載入的檔（style.css .hero 同步引用；LCP preload 要對準這張）
export const HERO_WEBP = 'https://cdn.jsdelivr.net/gh/kiolllery8-dev/essential-oil-cdn@main/images/hero-home.webp';

/** 療效詞 → 中性香氛/保養語氣（合規：機器可讀層 meta/schema/AI摘要 不得帶醫療宣稱）
 *  詞表與 scripts/build_kb.py 的 SANITIZE 同步；長詞優先，避免「消炎止痛」被拆開替換。
 *  只用於自動生成的摘要層——內文（pharmacology 引用文獻）不經過此函式。 */
const EFFECT_SANITIZE: Array<[string, string]> = [
  // 中醫／傳統療效詞（長詞先於短詞，避免被子字串搶先替換）
  ['強效化瘀消腫', '舒緩放鬆'], ['化瘀消腫', '舒緩放鬆'], ['活血化瘀', '循環按摩'], ['行氣活血', '循環按摩'],
  ['化瘀', '舒緩'], ['活血', '循環暢快'], ['止血收斂', '緊緻收斂'], ['止血', '緊緻'],
  ['開竅醒神', '提神清新'], ['消積散結', '日常保養'], ['補氣強身', '日常保養'], ['補氣', '日常保養'],
  ['護肝', '日常保養'], ['美白護膚', '亮澤保養'], ['美白', '亮澤'], ['通竅', '呼吸清新'],
  ['促進傷口癒合', '肌膚修護感'], ['傷口癒合', '肌膚修護感'], ['促進細胞再生', '肌膚煥活'], ['細胞再生', '肌膚煥活'],
  ['溫腎壯陽', '溫暖活力'], ['消炎止痛', '舒緩放鬆'], ['抗菌消炎', '清新淨化'],
  ['呼吸道感染', '呼吸道保養'], ['皮膚感染', '肌膚呵護'], ['促進呼吸道暢通', '帶來呼吸清新感'],
  ['調理經期', '經期前後香氛陪伴'], ['緩解更年期不適', '更年期身心陪伴'],
  ['增強免疫', '日常保養'], ['提升免疫', '日常保養'], ['免疫刺激', '日常保養'], ['免疫調節', '日常保養'],
  ['抗病毒', '清新淨化'], ['抗真菌', '清新淨化'], ['抗微生物', '清新淨化'], ['抗菌', '清新淨化'], ['殺菌', '清新淨化'],
  ['抗發炎', '舒緩'], ['抗炎', '舒緩'], ['消炎', '舒緩'],
  ['化解黏液', '呼吸清新'], ['化痰', '呼吸清新'], ['祛痰', '呼吸清新'], ['止咳', '呼吸放鬆'],
  ['改善痤瘡', '肌膚保養'], ['抗痘', '肌膚保養'], ['止癢', '肌膚舒緩'],
  ['調經', '經期前後香氛陪伴'], ['通經', '經期前後香氛陪伴'],
  ['止痛', '放鬆'], ['鎮痛', '放鬆'], ['退燒', '清涼舒適'], ['退熱', '清涼舒適'],
  ['抗憂鬱', '情緒放鬆'], ['降血壓', '放鬆'], ['抗風濕', '溫暖舒緩'],
  ['抗腫瘤', '日常保養'], ['抗癌', '日常保養'], ['抗增生', '日常保養'],
  ['壯陽', '活力提升'], ['催情', '浪漫氛圍'],
  ['利尿', '循環暢快'], ['排毒', '淨化清爽'], ['消水腫', '循環按摩'], ['抗痙攣', '安撫放鬆'],
  ['治療', '護理'], ['治癒', '呵護'], ['根治', '呵護'], ['感染', '不適'],
];
export function sanitizeEffects(s: string): string {
  let out = String(s || '');
  for (const [bad, good] of EFFECT_SANITIZE) out = out.split(bad).join(good);
  // 多個相鄰（或以「、」分隔）療效詞轉成同一中性詞時會重複（如「清新淨化、清新淨化、清新淨化」）。
  // 單次 replace 對「A、A、A」只會收成「A、A」（\1 無法跨「、」連續比對），故迴圈到收斂為止。
  let prev = '';
  while (prev !== out) { prev = out; out = out.replace(/([一-鿿]{2,4})、?\1/g, '$1'); }
  return out;
}

/** 成分摘要截斷：在「、」分隔邊界截斷，避免固定字數硬切把「香茅醇 (Citronellol…」
 *  切成殘缺的「香茅醇 (C。」出現在 meta/FAQ schema。 */
export function compBrief(s: string, limit = 40): string {
  const full = String(s || '').trim();
  if (full.length <= limit) return full;
  const parts = full.split('、');
  let out = '';
  for (const p of parts) {
    const candidate = out ? `${out}、${p}` : p;
    if (candidate.length > limit) break;
    out = candidate;
  }
  // 首個成分就超長：硬切但把切在括號內的殘尾清掉
  return out || full.slice(0, limit).replace(/[（(][^）)]*$/, '').trim();
}

/** 站域級 Organization 架構 */
export const organizationSchema = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  '@id': `${SITE}/#organization`,
  name: SITE_NAME,
  alternateName: ['精油能量圖譜', 'Essential Oil Energy Map', '靈境智造 Intelliverse Studio'],
  url: SITE,
  logo: {
    '@type': 'ImageObject',
    url: LOGO,
    width: 192,
    height: 192,
  },
  sameAs: ['https://show.intelliverse.tw/'],
  description:
    '最完整的中文精油知識庫——化學分子、芳療應用、安全指南、400+ 種精油資料庫；深入介紹澳洲（黃金海岸）等世界各地精油產區。',
  keywords: [
    '精油','精油百科','芳療','aromatherapy','澳洲精油','黃金海岸','Gold Coast',
    'Australia','澳洲','Australian essential oil','薰衣草','茶樹','尤加利',
  ].join(', '),
  inLanguage: 'zh-TW',
};

/** 站域級 WebSite 架構（含 Sitelinks 搜尋） */
export const websiteSchema = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  '@id': `${SITE}/#website`,
  name: SITE_NAME,
  url: SITE,
  inLanguage: 'zh-TW',
  publisher: { '@id': `${SITE}/#organization` },
  potentialAction: {
    '@type': 'SearchAction',
    target: {
      '@type': 'EntryPoint',
      urlTemplate: `${SITE}/search/?q={search_term_string}`,
    },
    'query-input': 'required name=search_term_string',
  },
};

/** 麵包屑 */
export function breadcrumbSchema(items: Array<{ name: string; url: string }>) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: item.name,
      item: item.url.startsWith('http') ? item.url : `${SITE}${item.url}`,
    })),
  };
}

/** 一般文章（article-* 頁用）
 *  注意：datePublished/dateModified 不再硬編碼預設值，避免假日期誤導 Google。
 *  - 若 opts 沒提供 datePublished，schema 不會輸出該欄位（schema.org 允許 optional）。
 *  - dateModified 預設用「build 當下日期」作為網站更新訊號，這是合理的。
 *  - 未來建立 articleMeta 資料表後可逐篇補上正式日期。
 */
export function articleSchema(opts: {
  url: string;
  headline: string;
  description: string;
  image: string;
  datePublished?: string;
  dateModified?: string;
  keywords?: string[];
  articleSection?: string;
}) {
  const { url, headline, description, image, datePublished, dateModified, keywords, articleSection } = opts;
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    mainEntityOfPage: { '@type': 'WebPage', '@id': url },
    headline,
    description,
    image: [image],
    author: { '@id': `${SITE}/#organization` },
    publisher: { '@id': `${SITE}/#organization` },
    ...(datePublished ? { datePublished } : {}),
    // 沒有真實日期就不輸出，避免每次 build 全站「假更新」讓 Google 不信任日期
    ...(dateModified ? { dateModified } : {}),
    inLanguage: 'zh-TW',
    ...(articleSection ? { articleSection } : {}),
    ...(keywords?.length ? { keywords: keywords.join(', ') } : {}),
  };
}

/** 精油頁：用 MedicalSubstance 更貼合化學資訊+藥用屬性 */
export function oilSchema(oil: {
  id: string;
  zh: string;
  latin: string;
  family?: string;
  components?: string;
  extractPart?: string;
  effects?: string;
  safetyText?: string;
  category?: string;
  tags?: string[];
  aliases?: string[];
}, opts?: { canonicalUrl?: string; dateModified?: string }) {
  // canonical 收編頁（/oil/N → /oil-X/）的 schema url 對齊 canonical，避免訊號互相矛盾
  const url = opts?.canonicalUrl || `${SITE}/oil/${oil.id}/`;
  // 合規：schema 是機器可讀層，effects 原文的療效詞（抗菌/消炎/調經…）一律轉中性語氣
  const effectsClean = sanitizeEffects((oil.effects || '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim());
  const safetyClean = (oil.safetyText || '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
  // alternateName 含拉丁學名 + Wikipedia 植物學名別名（幫 AI/搜尋連結實體）
  const altNames = [oil.latin, ...(oil.aliases || [])].filter(Boolean);
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    mainEntityOfPage: { '@type': 'WebPage', '@id': url },
    headline: `${oil.zh}精油完整介紹｜${oil.latin}`,
    name: oil.zh,
    alternateName: altNames.length > 1 ? altNames : oil.latin,
    // safetyClean 也過 sanitize（安全警語尾段可能提到「活血/通經/消炎」等作為禁忌說明，schema 為機器可讀層須中性化；
    // 頁面上的可見安全提醒框用 oil.safetyText 原文，不受影響）
    description: `${oil.zh}（${oil.latin}）：化學分類「${oil.category || '—'}」，主要成分 ${compBrief(oil.components || '', 60)}。常見芳療應用：${effectsClean}。${sanitizeEffects(safetyClean)}`.slice(0, 300),
    author: { '@id': `${SITE}/#organization` },
    publisher: { '@id': `${SITE}/#organization` },
    image: [DEFAULT_OG], // Article 結構化資料必要欄位
    ...(opts?.dateModified ? { dateModified: opts.dateModified } : {}),
    inLanguage: 'zh-TW',
    about: {
      '@type': 'ChemicalSubstance',
      name: oil.latin,
      alternateName: oil.zh,
      chemicalComposition: oil.components || undefined,
      taxonomicRange: oil.family || undefined,
    },
    // keywords 也過 sanitize（tags 內含「消炎止痛」等療效標籤）＋去重
    keywords: Array.from(new Set(
      [oil.zh, oil.latin, oil.category, ...(oil.tags || [])].filter(Boolean).map((k) => sanitizeEffects(String(k)))
    )).join(', '),
  };
}
