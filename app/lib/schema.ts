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
    '最完整的中文精油知識庫——化學分子、芳療應用、安全指南、400+ 種精油資料庫。',
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

/** 一般文章（article-* 頁用） */
export function articleSchema(opts: {
  url: string;
  headline: string;
  description: string;
  image: string;
  datePublished?: string;
  dateModified?: string;
  keywords?: string[];
}) {
  const { url, headline, description, image, datePublished, dateModified, keywords } = opts;
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    mainEntityOfPage: { '@type': 'WebPage', '@id': url },
    headline,
    description,
    image: [image],
    author: { '@id': `${SITE}/#organization` },
    publisher: { '@id': `${SITE}/#organization` },
    datePublished: datePublished || '2026-01-01',
    dateModified: dateModified || '2026-04-21',
    inLanguage: 'zh-TW',
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
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    mainEntityOfPage: { '@type': 'WebPage', '@id': url },
    headline: `${oil.zh}精油完整介紹｜${oil.latin}`,
    name: oil.zh,
    alternateName: oil.latin,
    description: `${oil.zh}（${oil.latin}）：化學分類「${oil.category || '—'}」，主要成分 ${oil.components || ''}。${oil.safetyText || ''}`.slice(0, 250),
    author: { '@id': `${SITE}/#organization` },
    publisher: { '@id': `${SITE}/#organization` },
    datePublished: '2026-01-01',
    dateModified: '2026-04-21',
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
