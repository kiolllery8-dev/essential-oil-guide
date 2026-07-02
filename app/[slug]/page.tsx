import { readdirSync } from 'fs';
import { join } from 'path';
import { loadPage } from '../lib/loadHtml';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import ReactDOM from 'react-dom';
import RawHtml from '../components/RawHtml';
import JsonLd from '../components/JsonLd';
import AISummary from '../components/AISummary';
import RelatedLinks from '../components/RelatedLinks';
import { breadcrumbSchema, articleSchema, SITE, DEFAULT_OG } from '../lib/schema';
import { faqSchema, SAFETY_FAQ, BEGINNERS_FAQ } from '../lib/faq';
import { AROMATHERAPY_HOWTOS } from '../lib/howto';
import { getPageSummary } from '../lib/pageSummaries';
import contentDates from '../../data/content-dates.json';

const HTML_DIR = join(process.cwd(), 'html-source');

/** 不進索引的頁：search（純工具）、author-yuling（刻意無入口）。皆已排除於 sitemap。 */
const NOINDEX_SLUGS = new Set(['search', 'author-yuling']);

function listSlugs(): string[] {
  return readdirSync(HTML_DIR)
    .filter((f) => f.endsWith('.html'))
    .map((f) => f.replace(/\.html$/, ''))
    .filter((s) => s !== 'index' && s !== 'oil-detail' && !s.startsWith('googlef'));
}

/** 每個 slug 的中文顯示名稱（麵包屑用） */
const SLUG_NAMES: Record<string, string> = {
  encyclopedia: '大百科',
  oils: '精油化學分子索引',
  blend: '調配精油',
  numerology: '生命靈數',
  'numerology-vs-fortune-telling': '算命 vs 生命靈數對照表',
  aromatherapy: '芳療應用',
  safety: '安全指南',
  search: '搜尋',
  'article-beginners': '新手入門',
  'article-sleep': '助眠精油',
  'article-stress': '紓壓配方',
  'article-dustmites': '塵蟎研究',
  'article-eucalyptus': '尤加利精油指南',
  'article-extraction': '精油萃取方式',
  'article-chamomile-comparison': '羅馬 vs 德國洋甘菊比較',
  'article-children': '兒童芳療指南',
  'article-pregnancy': '孕期芳療指南',
  'article-pets': '寵物芳療指南',
  'article-office': '上班族提神配方',
  'oil-bergamot': '佛手柑精油',
  'oil-rose': '玫瑰精油',
  'oil-geranium': '天竺葵精油',
  'oil-grapefruit': '葡萄柚精油',
  'oil-marjoram': '甜馬鬱蘭精油',
  'oil-ginger': '薑精油',
  'oil-neroli': '橙花精油',
  'oil-vetiver': '岩蘭草精油',
  'oil-clary-sage': '快樂鼠尾草精油',
  'oil-helichrysum': '義大利永久花精油',
  'oil-sandalwood': '檀香精油',
  'oil-jasmine': '茉莉精油',
  'oil-citronella': '香茅精油',
  'oil-clove': '丁香精油',
  'oil-petitgrain': '苦橙葉精油',
  'oil-juniper': '杜松漿果精油',
  'oil-cypress': '絲柏精油',
  'article-conifers': '松柏家族精油比較',
  'article-hydrosols': '純露完整指南',
  'article-newbie-mistakes': '10 大新手錯誤',
  'article-citrus-comparison': '柑橘類精油完整比較',
  'oil-bay': '月桂精油',
  'oil-myrrh': '沒藥精油',
  'oil-patchouli': '廣藿香精油',
  'oil-black-pepper': '黑胡椒精油',
  'oil-ravintsara': '桉油醇樟（Ravintsara）精油',
  'oil-palmarosa': '玫瑰草精油',
  'article-tcm-aromatherapy': '中醫芳療完整指南',
  'article-spiritual-aromatherapy': '心靈芳療：脈輪情緒冥想',
  'oil-lavender': '薰衣草精油',
  'oil-tea-tree': '茶樹精油',
  'oil-peppermint': '薄荷精油',
  'oil-eucalyptus': '尤加利精油',
  'oil-frankincense': '乳香精油',
  'oil-cedarwood': '雪松精油',
  'oil-sweet-orange': '甜橙精油',
  'oil-lemon': '檸檬精油',
  'oil-ylang-ylang': '依蘭精油',
  'oil-rosemary': '迷迭香精油',
  'oil-mandarin': '柑橘精油',
  'oil-german-chamomile': '德國洋甘菊精油',
  'oil-thyme': '百里香精油',
  'oil-melissa': '香蜂草精油',
  'oil-sweet-basil': '甜羅勒精油',
  'oil-sweet-fennel': '甜茴香精油',
  'oil-roman-chamomile': '羅馬洋甘菊精油',
  'oil-spearmint': '綠薄荷精油',
  'oil-spike-lavender': '穗花薰衣草精油',
  'oil-lavandin': '醒目薰衣草精油',
  'oil-yarrow': '西洋蓍草精油',
  'oil-black-spruce': '黑雲杉精油',
  'oil-lemon-eucalyptus': '檸檬尤加利精油',
  'article-insect-repellent': '天然驅蟲完整指南',
  'article-lavender-comparison': '三大薰衣草精油比較',
  'author-yuling': '關於作者：玉玲',
  'references': '引用來源與參考資料',
  'compounds-01': '單萜烯類 I',
  'compounds-02': '香豆素與內酯類',
  'compounds-03': '氧化物類',
  'compounds-04': '倍半萜烯類',
  'compounds-05': '醛類 V',
  'compounds-06': '酯類 VI',
  'compounds-07a': '脂類 VII-1',
  'compounds-07b': '苯基酯類 VII-2',
  'compounds-07c': '芳香醛類 VII-3',
  'compounds-08': '倍半萜酮類',
  'compounds-09': '單萜醇類',
  'compounds-10': '酚與芳香醛類',
  'compounds-11': '倍半萜醇類',
  'compounds-12': '單萜烯類 XII',
};

export async function generateStaticParams() {
  return listSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata(
  { params }: { params: Promise<{ slug: string }> }
): Promise<Metadata> {
  const { slug } = await params;
  const slugs = listSlugs();
  if (!slugs.includes(slug)) return {};
  const page = loadPage(`${slug}.html`);
  const url = `${SITE}/${slug}/`;
  const ogImage = page.ogImage || DEFAULT_OG;
  return {
    title: { absolute: page.title },
    description: page.description,
    alternates: { canonical: url },
    ...(NOINDEX_SLUGS.has(slug) ? { robots: { index: false, follow: true } } : {}),
    openGraph: {
      type: slug.startsWith('article-') ? 'article' : 'website',
      url,
      title: page.title,
      description: page.description,
      images: [{ url: ogImage, width: 1200, height: 630, alt: page.title }],
    },
    twitter: { title: page.title, description: page.description, images: [ogImage] },
  };
}

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const slugs = listSlugs();
  if (!slugs.includes(slug)) notFound();
  const page = loadPage(`${slug}.html`);

  const url = `${SITE}/${slug}/`;
  const niceName = SLUG_NAMES[slug] || slug;
  const image = page.ogImage || DEFAULT_OG;

  // Preload LCP image (每頁 hero)
  ReactDOM.preload(image, { as: 'image', fetchPriority: 'high' });

  const crumbs = breadcrumbSchema([
    { name: '首頁', url: '/' },
    { name: niceName, url: `/${slug}/` },
  ]);

  const isArticle = slug.startsWith('article-');
  const article = articleSchema({
    url,
    headline: page.title.replace(/\s*\|\s*精油能量圖譜\s*$/, ''),
    description: page.description || '',
    image,
    dateModified: (contentDates as Record<string, string>)[slug],
  });

  // FAQ schema：safety / article-beginners 頁
  const faqData =
    slug === 'safety' ? faqSchema(SAFETY_FAQ) :
    slug === 'article-beginners' ? faqSchema(BEGINNERS_FAQ) :
    null;

  const schemas: object[] = [crumbs];
  if (isArticle) schemas.push(article);
  if (faqData) schemas.push(faqData);
  if (slug === 'aromatherapy') schemas.push(...AROMATHERAPY_HOWTOS);

  // Speakable：標示適合語音助理 / AI 朗讀的段落（GEO 訊號）
  schemas.push({
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    '@id': `${url}#speakable`,
    url,
    name: niceName,
    speakable: { '@type': 'SpeakableSpecification', cssSelector: ['h1'] },
    isPartOf: { '@id': `${SITE}/#website` },
  });

  // 取得頁面 AI 摘要（若有手寫版）
  const aiSummary = getPageSummary(slug);

  // 文章類 / 精油類頁面顯示延伸閱讀；首頁與索引頁不顯示
  const showRelated = isArticle || slug.startsWith('oil-') || slug === 'safety' || slug === 'aromatherapy';

  return (
    <>
      <JsonLd data={schemas} />

      {/* AI 友善「快速答案」：純 JSON-LD（不顯示給人，供 AI 引用） */}
      {aiSummary && <AISummary summary={aiSummary} title={`${niceName} 快速答案`} />}

      <RawHtml html={page.bodyHtml} />

      {/* /safety/ 的 FAQPage schema 之 Q&A 必須在頁面可見（Google 規範），
          用原生 <details> 渲染成可見手風琴——內容恆在 DOM，爬蟲與使用者都讀得到。
          （article-beginners 已有頁內可見 FAQ，schema 已對齊該內容，故此處不重複渲染） */}
      {slug === 'safety' && (
        <section
          aria-label="精油安全常見問題"
          style={{ maxWidth: 900, margin: '8px auto 0', padding: '0 20px' }}
        >
          <h2 style={{ fontSize: 22, color: 'var(--green-dark)', borderLeft: '4px solid var(--green-mid)', paddingLeft: 12, margin: '24px 0 16px' }}>
            🛡️ 精油安全常見問題
          </h2>
          {SAFETY_FAQ.map((it, i) => (
            <details
              key={i}
              style={{ background: 'var(--beige-light, #FBF7F1)', border: '1px solid var(--border, #E5D9C0)', borderRadius: 10, padding: '4px 16px', marginBottom: 10 }}
            >
              <summary style={{ cursor: 'pointer', fontWeight: 700, color: '#3D3328', padding: '12px 0', fontSize: 15 }}>
                {it.q}
              </summary>
              <p style={{ fontSize: 14, lineHeight: 1.9, color: '#5D4A28', margin: '0 0 12px' }}>{it.a}</p>
            </details>
          ))}
        </section>
      )}

      {/* 延伸閱讀（強化內部連結 + AI 引用上下文） */}
      {showRelated && <RelatedLinks topic={niceName} max={6} currentPath={`/${slug}/`} />}
    </>
  );
}
