import { readdirSync } from 'fs';
import { join } from 'path';
import { loadPage } from '../lib/loadHtml';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import RawHtml from '../components/RawHtml';

const HTML_DIR = join(process.cwd(), 'html-source');

function listSlugs(): string[] {
  return readdirSync(HTML_DIR)
    .filter((f) => f.endsWith('.html'))
    .map((f) => f.replace(/\.html$/, ''))
    .filter((s) => s !== 'index' && s !== 'oil-detail' && !s.startsWith('googlef'));
}

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
  return {
    title: { absolute: page.title },
    description: page.description,
    openGraph: { images: page.ogImage ? [page.ogImage] : [] },
  };
}

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const slugs = listSlugs();
  if (!slugs.includes(slug)) notFound();
  const page = loadPage(`${slug}.html`);
  return <RawHtml html={page.bodyHtml} />;
}
