/**
 * schema.org JSON-LD 物件產生器
 * 用 https://validator.schema.org/ 驗證
 */

export const SITE = 'https://intelliverse.tw';
export const SITE_NAME = '精油能量圖譜';
export const LOGO = `${SITE}/favicon-64.png`;
export const DEFAULT_OG = 'https://cdn.jsdelivr.net/gh/kiolllery8-dev/essential-oil-cdn@main/images/hero-home.png';

/** 站域級 Organization 架構 */
export const organizationSchema = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  '@id': `${SITE}/#organization`,
  name: SITE_NAME,
  alternateName: ['精油能量圖譜', 'Essential Oil Energy Map'],
  url: SITE,
  logo: {
    '@type': 'ImageObject',
    url: LOGO,
    width: 64,
    height: 64,
  },
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
  const buildToday = new Date().toISOString().slice(0, 10);
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
    dateModified: dateModified || buildToday,
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
}) {
  const url = `${SITE}/oil/${oil.id}/`;
  const effectsClean = (oil.effects || '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
  const safetyClean = (oil.safetyText || '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    mainEntityOfPage: { '@type': 'WebPage', '@id': url },
    headline: `${oil.zh}精油完整介紹｜${oil.latin}`,
    name: oil.zh,
    alternateName: oil.latin,
    description: `${oil.zh}（${oil.latin}）：化學分類「${oil.category || '—'}」，主要成分 ${oil.components || ''}。常見芳療應用：${effectsClean}。${safetyClean}`.slice(0, 300),
    author: { '@id': `${SITE}/#organization` },
    publisher: { '@id': `${SITE}/#organization` },
    dateModified: new Date().toISOString().slice(0, 10),
    inLanguage: 'zh-TW',
    about: {
      '@type': 'ChemicalSubstance',
      name: oil.latin,
      alternateName: oil.zh,
      chemicalComposition: oil.components || undefined,
      taxonomicRange: oil.family || undefined,
    },
    keywords: [oil.zh, oil.latin, oil.category, ...(oil.tags || [])].filter(Boolean).join(', '),
  };
}
