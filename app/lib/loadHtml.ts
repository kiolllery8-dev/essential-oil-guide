import { readFileSync } from 'fs';
import { join } from 'path';

export interface LoadedPage {
  title: string;
  description: string;
  ogImage: string;
  bodyHtml: string;
}

const HTML_DIR = join(process.cwd(), 'html-source');

const pick = (re: RegExp, src: string, dflt = '') => {
  const m = src.match(re);
  return m ? m[1].trim() : dflt;
};

/** Extract main content: everything inside <body> except <header> and <footer>.
 *  Keeps any trailing <script> tags (e.g. oil-detail.html embeds large JSON
 *  + render scripts AFTER </footer>). */
function extractMain(html: string): string {
  // Get content inside <body>
  const bodyMatch = html.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  let body = bodyMatch ? bodyMatch[1] : html;
  // Strip <header>...</header>
  body = body.replace(/<header[\s\S]*?<\/header>/i, '');
  // Strip <footer>...</footer>
  body = body.replace(/<footer[\s\S]*?<\/footer>/i, '');
  // Strip leading topbar div if present (we have our own in Layout)
  body = body.replace(/<div\s+class=["']topbar["'][^>]*>[\s\S]*?<\/div>\s*/i, '');
  return body.trim();
}

/** Rewrite legacy URLs:
 *  - oil-detail.html?id=N  → /oil/N/
 *  - foo.html#anchor       → /foo/#anchor
 *  - foo.html              → /foo/
 *  - index.html            → /
 */
function rewriteLinks(html: string): string {
  return html
    .replace(/(["'])oil-detail\.html\?id=(\d+)\1/g, (_, q, id) => `${q}/oil/${id}/${q}`)
    .replace(/(["'])index\.html(?:#([\w-]+))?\1/g, (_, q, h) => `${q}/${h ? '#' + h : ''}${q}`)
    .replace(/(["'])([a-z][a-z0-9-]+)\.html(?:#([\w-]+))?\1/g,
      (_, q, slug, h) => `${q}/${slug}/${h ? '#' + h : ''}${q}`);
}

/** Extract all <style>...</style> blocks from <head> (page-specific CSS).
 *  Many pages (compounds-*, oil-detail, search) define their own classes in <head>. */
function extractHeadStyles(html: string): string {
  const headMatch = html.match(/<head[^>]*>([\s\S]*?)<\/head>/i);
  if (!headMatch) return '';
  const head = headMatch[1];
  const styles: string[] = [];
  const re = /<style\b[^>]*>([\s\S]*?)<\/style>/gi;
  let m: RegExpExecArray | null;
  while ((m = re.exec(head)) !== null) styles.push(m[0]);
  return styles.join('\n');
}

export function loadPage(filename: string): LoadedPage {
  const file = join(HTML_DIR, filename);
  const raw = readFileSync(file, 'utf-8');
  const headStyles = extractHeadStyles(raw);
  const body = rewriteLinks(extractMain(raw));
  // Prepend page-specific <style> so its rules apply to the body content
  const bodyHtml = headStyles ? `${headStyles}\n${body}` : body;
  return {
    title: pick(/<title>([^<]*)<\/title>/, raw, '精油能量圖譜'),
    description: pick(/<meta\s+name="description"\s+content="([^"]*)"/, raw),
    ogImage: pick(/<meta\s+property="og:image"\s+content="([^"]*)"/, raw),
    bodyHtml,
  };
}
