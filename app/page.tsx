import { loadPage } from './lib/loadHtml';
import type { Metadata } from 'next';
import ReactDOM from 'react-dom';
import RawHtml from './components/RawHtml';
import JsonLd from './components/JsonLd';
import { breadcrumbSchema, SITE, DEFAULT_OG } from './lib/schema';

const page = loadPage('index.html');
const ogImage = page.ogImage || DEFAULT_OG;

export const metadata: Metadata = {
  title: { absolute: page.title },
  description: page.description,
  alternates: { canonical: '/' },
  openGraph: {
    type: 'website',
    url: SITE,
    title: page.title,
    description: page.description,
    images: [{ url: ogImage, width: 1200, height: 630, alt: '精油能量圖譜' }],
  },
  twitter: { title: page.title, description: page.description, images: [ogImage] },
};

export default function Home() {
  // Preload LCP image（首頁 hero）
  ReactDOM.preload(ogImage, { as: 'image', fetchPriority: 'high' });

  const crumbs = breadcrumbSchema([{ name: '首頁', url: '/' }]);
  return (
    <>
      <JsonLd data={crumbs} />
      <RawHtml html={page.bodyHtml} />
    </>
  );
}
