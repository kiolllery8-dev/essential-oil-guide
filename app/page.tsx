import { loadPage } from './lib/loadHtml';
import type { Metadata } from 'next';
import RawHtml from './components/RawHtml';

const page = loadPage('index.html');

export const metadata: Metadata = {
  title: { absolute: page.title },
  description: page.description,
  openGraph: { images: page.ogImage ? [page.ogImage] : [] },
};

export default function Home() {
  return <RawHtml html={page.bodyHtml} />;
}
