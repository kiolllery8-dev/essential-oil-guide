/**
 * RelatedLinks — 文章末尾「延伸閱讀」區塊
 *
 * 用法：
 *   <RelatedLinks topic="薰衣草" title="延伸閱讀" max={6} />
 *
 *  - 用 `app/lib/internalLinks.ts` 的對應表，找出與 topic 最相關的站內連結
 *  - 自動加上 schema.org 的 SiteNavigationElement microdata
 *  - 提升站內連結深度（SEO）與 AI 引用時的上下文（GEO）
 */
import { getRelatedLinks } from '../lib/internalLinks';

export default function RelatedLinks({
  topic,
  title = '🌿 延伸閱讀',
  max = 6,
  currentPath = '',
}: {
  topic?: string;
  title?: string;
  max?: number;
  /** 當前頁路徑（如 '/oil-lavender/'）— 排除自連、決定補位輪替 */
  currentPath?: string;
}) {
  const links = getRelatedLinks(topic || '', max, currentPath);
  if (!links.length) return null;

  return (
    <nav
      className="related-links"
      aria-labelledby="related-links-heading"
      itemScope
      itemType="https://schema.org/SiteNavigationElement"
      style={{
        maxWidth: 1100,
        margin: '40px auto 30px',
        padding: '24px 28px',
        background: '#F5F0E6',
        borderRadius: 12,
        border: '1px solid #E5D9C0',
      }}
    >
      <h2
        id="related-links-heading"
        itemProp="name"
        style={{
          fontSize: 18,
          fontWeight: 700,
          color: '#8B6F3E',
          marginTop: 0,
          marginBottom: 14,
          letterSpacing: '0.05em',
        }}
      >
        {title}
      </h2>
      <ul
        style={{
          listStyle: 'none',
          padding: 0,
          margin: 0,
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: 10,
        }}
      >
        {links.map((l) => (
          <li key={l.href + l.keyword}>
            <a
              href={l.href}
              title={l.title}
              itemProp="url"
              style={{
                display: 'block',
                padding: '10px 14px',
                background: '#FFFDF8',
                borderRadius: 8,
                border: '1px solid #E5D9C0',
                textDecoration: 'none',
                color: '#3D3328',
                fontSize: 14,
                transition: 'transform .15s, box-shadow .15s',
              }}
            >
              <span itemProp="name">→ {l.keyword}</span>
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
