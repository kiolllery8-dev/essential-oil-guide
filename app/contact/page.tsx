import type { Metadata } from 'next';
import JsonLd from '../components/JsonLd';
import { breadcrumbSchema, SITE, DEFAULT_OG } from '../lib/schema';

const URL = `${SITE}/contact/`;
const TITLE = '聯絡我們 | 精油能量圖譜';
const DESC = '聯絡精油能量圖譜 / 靈境智造 Intelliverse Studio — 合作洽詢、內容指正、授權申請請來信 linsonder6@gmail.com。';

export const metadata: Metadata = {
  title: { absolute: TITLE },
  description: DESC,
  alternates: { canonical: URL },
  openGraph: { type: 'website', url: URL, title: TITLE, description: DESC, images: [{ url: DEFAULT_OG, width: 1200, height: 630 }] },
  twitter: { title: TITLE, description: DESC, images: [DEFAULT_OG] },
};

const contactSchema = {
  '@context': 'https://schema.org',
  '@type': 'ContactPage',
  url: URL,
  mainEntity: {
    '@type': 'Organization',
    '@id': `${SITE}/#organization`,
    name: '靈境智造 Intelliverse Studio',
    email: 'linsonder6@gmail.com',
    telephone: '+886-926-213896',
    url: 'https://show.intelliverse.tw/',
    address: {
      '@type': 'PostalAddress',
      addressLocality: '臺中市北屯區',
      addressRegion: '臺中市',
      addressCountry: 'TW',
    },
  },
};

export default function Contact() {
  const crumbs = breadcrumbSchema([
    { name: '首頁', url: '/' },
    { name: '聯絡我們', url: '/contact/' },
  ]);

  return (
    <>
      <JsonLd data={[crumbs, contactSchema]} />
      <section style={{ maxWidth: 860, margin: '40px auto 80px', padding: '0 24px', lineHeight: 1.85 }}>
        <h1 style={{ fontSize: 38, marginBottom: 20, color: 'var(--green-dark)' }}>💌 聯絡我們</h1>
        <p style={{ color: 'var(--text-mid)', fontSize: 15, marginBottom: 40 }}>歡迎內容指正、合作洽詢、授權申請</p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 20, marginBottom: 40 }}>
          <div style={{ padding: 24, background: 'var(--beige-light)', borderRadius: 16, border: '1px solid var(--border)' }}>
            <div style={{ fontSize: 32, marginBottom: 10 }}>📧</div>
            <h3 style={{ marginBottom: 8, color: 'var(--green-dark)' }}>Email</h3>
            <p style={{ marginBottom: 8 }}>
              <a href="mailto:linsonder6@gmail.com" style={{ color: 'var(--green-dark)', fontSize: 16 }}>linsonder6@gmail.com</a>
            </p>
            <p style={{ fontSize: 13, color: 'var(--text-mid)' }}>一般回覆 3-5 個工作天</p>
          </div>

          <div style={{ padding: 24, background: 'var(--beige-light)', borderRadius: 16, border: '1px solid var(--border)' }}>
            <div style={{ fontSize: 32, marginBottom: 10 }}>🏢</div>
            <h3 style={{ marginBottom: 8, color: 'var(--green-dark)' }}>公司</h3>
            <p style={{ marginBottom: 4, fontWeight: 600 }}>靈境智造 Intelliverse Studio</p>
            <p style={{ fontSize: 14, color: 'var(--text-mid)' }}>臺中市北屯區</p>
            <p style={{ marginTop: 8 }}>
              <a href="https://show.intelliverse.tw/" target="_blank" rel="noopener" style={{ color: 'var(--green-dark)', fontSize: 14 }}>
                🌐 show.intelliverse.tw →
              </a>
            </p>
          </div>

          <div style={{ padding: 24, background: 'var(--beige-light)', borderRadius: 16, border: '1px solid var(--border)' }}>
            <div style={{ fontSize: 32, marginBottom: 10 }}>📱</div>
            <h3 style={{ marginBottom: 8, color: 'var(--green-dark)' }}>電話 / 行動</h3>
            <p style={{ marginBottom: 4 }}>
              <a href="tel:+886926213896" style={{ color: 'var(--green-dark)', fontSize: 16 }}>+886 926 213 896</a>
            </p>
            <p style={{ fontSize: 13, color: 'var(--text-mid)' }}>平日 10:00 – 18:00</p>
          </div>
        </div>

        <h2 style={{ marginTop: 40 }}>✉️ 適合來信的類型</h2>
        <ul>
          <li><strong>內容指正</strong>：發現錯字、學名錯誤、化學成分比例需更新、研究更新等</li>
          <li><strong>內容提議</strong>：希望補充的精油、想看的主題文章、FAQ 補完</li>
          <li><strong>授權洽詢</strong>：商業使用本站內容或 AI 生成圖像的授權申請</li>
          <li><strong>合作提案</strong>：芳療師／芳療品牌願意提供專業內容、提供產品樣本供測試</li>
          <li><strong>技術合作</strong>：Intelliverse 網站設計／AI 內容整合服務洽詢</li>
        </ul>

        <h2 style={{ marginTop: 40 }}>⚠️ 醫療諮詢免責</h2>
        <p style={{ background: '#FFF8E1', padding: 16, borderRadius: 12, borderLeft: '4px solid #E8A838' }}>
          本團隊<strong>不是醫療單位</strong>，無法提供精油的個人健康諮詢、症狀判斷或治療建議。
          若您有健康疑慮，請聯繫您的主治醫師、藥師或合格芳療師。
          相關諮詢請參考 <a href="/safety/" style={{ color: 'var(--green-dark)', fontWeight: 600 }}>精油安全指南</a>。
        </p>

        <h2 style={{ marginTop: 40 }}>🔍 常見問題</h2>
        <ul>
          <li>📖 新手想入門？→ <a href="/article-beginners/" style={{ color: 'var(--green-dark)' }}>新手必備 5 支精油完整指南</a></li>
          <li>🌿 想看全部精油？→ <a href="/oils/" style={{ color: 'var(--green-dark)' }}>精油化學分子索引</a>（400+ 支）</li>
          <li>⚠️ 使用精油前的安全須知？→ <a href="/safety/" style={{ color: 'var(--green-dark)' }}>精油安全指南</a></li>
          <li>🕯️ 怎麼擴香／稀釋？→ <a href="/aromatherapy/" style={{ color: 'var(--green-dark)' }}>芳療應用指南</a></li>
        </ul>
      </section>
    </>
  );
}
