import { readdirSync } from 'fs';
import { join } from 'path';
import { loadPage } from '../lib/loadHtml';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import RawHtml from '../components/RawHtml';
import JsonLd from '../components/JsonLd';
import { breadcrumbSchema, articleSchema, SITE, DEFAULT_OG } from '../lib/schema';
import { faqSchema, SAFETY_FAQ, BEGINNERS_FAQ } from '../lib/faq';

const HTML_DIR = join(process.cwd(), 'html-source');

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
  aromatherapy: '芳療應用',
  safety: '安全指南',
  search: '搜尋',
  'article-beginners': '新手入門',
  'article-sleep': '助眠精油',
  'article-stress': '紓壓配方',
  'article-dustmites': '塵蟎研究',
  'article-eucalyptus': '尤加利精油指南',
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
  });

  // FAQ schema：safety / article-beginners 頁
  const faqData =
    slug === 'safety' ? faqSchema(SAFETY_FAQ) :
    slug === 'article-beginners' ? faqSchema(BEGINNERS_FAQ) :
    null;

  const schemas: object[] = [crumbs];
  if (isArticle) schemas.push(article);
  if (faqData) schemas.push(faqData);

  return (
    <>
      <JsonLd data={schemas} />
      <RawHtml html={page.bodyHtml} />
    </>
  );
}
