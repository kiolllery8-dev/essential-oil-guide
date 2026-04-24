import type { Metadata, Viewport } from 'next';
import Script from 'next/script';
import NavSearch from './components/NavSearch';
import JsonLd from './components/JsonLd';
import { organizationSchema, websiteSchema, DEFAULT_OG } from './lib/schema';

export const metadata: Metadata = {
  title: {
    default: '精油能量圖譜 - 精油學｜從植物到身心靈的完整知識庫',
    template: '%s | 精油能量圖譜',
  },
  description:
    '精油從無到有的生成、運用、醫學、芳療、來源、植物、身心靈——最完整的中文精油能量圖譜，收錄 400+ 種精油化學分類、成分、功效與安全提示。',
  metadataBase: new URL('https://intelliverse.tw'),
  keywords: [
    '精油', '精油學', '芳療', 'aromatherapy', '精油化學', '化學分類',
    '單萜烯', '倍半萜醇', '薰衣草', '茶樹', '尤加利', '精油功效',
    '精油安全', '精油百科', '精油知識', 'essential oil',
  ],
  applicationName: '精油能量圖譜',
  authors: [{ name: '靈境智造 Intelliverse', url: 'https://show.intelliverse.tw/' }],
  publisher: '靈境智造 Intelliverse Studio',
  creator: '靈境智造 Intelliverse Studio',
  openGraph: {
    type: 'website',
    siteName: '精油能量圖譜',
    locale: 'zh_TW',
    url: 'https://intelliverse.tw/',
    images: [{ url: DEFAULT_OG, width: 1200, height: 630, alt: '精油能量圖譜' }],
  },
  twitter: {
    card: 'summary_large_image',
    site: '@intelliverse',
    creator: '@intelliverse',
    images: [DEFAULT_OG],
  },
  icons: {
    icon: [
      { url: '/favicon.ico', sizes: 'any' },
      { url: '/favicon-16.png', sizes: '16x16', type: 'image/png' },
      { url: '/favicon-32.png', sizes: '32x32', type: 'image/png' },
      { url: '/favicon-48.png', sizes: '48x48', type: 'image/png' },
      { url: '/favicon-64.png', sizes: '64x64', type: 'image/png' },
      { url: '/android-chrome-192.png', sizes: '192x192', type: 'image/png' },
      { url: '/android-chrome-512.png', sizes: '512x512', type: 'image/png' },
    ],
    apple: [
      { url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' },
    ],
    shortcut: '/favicon.ico',
  },
  manifest: '/manifest.json',
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, 'max-image-preview': 'large', 'max-snippet': -1 },
  },
  other: {
    'format-detection': 'telephone=no',
  },
  alternates: {
    canonical: '/',
    types: {
      'application/rss+xml': [{ url: '/rss.xml', title: '精油能量圖譜 RSS' }],
    },
  },
};

export const viewport: Viewport = {
  themeColor: '#3D5A3E',
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-TW">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;800&display=swap"
          rel="stylesheet"
        />
        <link rel="stylesheet" href="/assets/css/style.css" />
      </head>
      <body>
        <JsonLd data={[organizationSchema, websiteSchema]} />

        <div className="topbar">🌿 精油能量圖譜 — 用知識療癒您的生活 社會修行</div>

        <header>
          <div className="header-inner">
            <div className="logo-wrap">
              <div className="logo-icon">🌿</div>
              <div className="logo-text">
                <div className="site-title">精油能量圖譜</div>
                <div className="site-sub">精油學 · 從植物到身心靈</div>
              </div>
            </div>
            <nav>
              <ul>
                <li><a href="/">首頁</a></li>
                <li><a href="/encyclopedia/">大百科</a></li>
                <li><a href="/oils/">精油</a></li>
                <li><a href="/aromatherapy/">芳療應用</a></li>
                <li><a href="/safety/">安全指南</a></li>
              </ul>
            </nav>
            <NavSearch />
            <button className="menu-toggle" aria-label="選單">☰</button>
          </div>
        </header>

        {children}

        <footer>
          <div className="footer-inner">
            <div>
              <h4>🌿 精油能量圖譜</h4>
              <p>致力於提供正確、完整、易懂的精油知識，<br />幫助每個人建立安全有效的芳療生活。</p>
              <p style={{ marginTop: 14, fontSize: 12, opacity: 0.6 }}>
                本網站內容僅供教育參考，不構成醫療建議。<br />使用精油前請諮詢專業芳療師或醫師。
              </p>
            </div>
            <div>
              <h4>知識分類</h4>
              <ul>
                <li><a href="/encyclopedia/#chemistry">精油生成原理</a></li>
                <li><a href="/encyclopedia/#regions">植物來源圖鑑</a></li>
                <li><a href="/encyclopedia/">醫學研究摘要</a></li>
                <li><a href="/aromatherapy/">芳療應用教學</a></li>
              </ul>
            </div>
            <div>
              <h4>精油索引</h4>
              <ul>
                <li><a href="/oil-eucalyptus/">尤加利精油</a></li>
                <li><a href="/oil-lavender/">薰衣草精油</a></li>
                <li><a href="/oil-tea-tree/">茶樹精油</a></li>
                <li><a href="/oil-peppermint/">薄荷精油</a></li>
                <li><a href="/oil-frankincense/">乳香精油</a></li>
              </ul>
            </div>
            <div>
              <h4>關於</h4>
              <ul>
                <li><a href="/about/">網站簡介</a></li>
                <li><a href="/disclaimer/">免責聲明</a></li>
                <li><a href="/privacy/">隱私政策</a></li>
                <li><a href="/contact/">聯絡我們</a></li>
              </ul>
            </div>
          </div>
          <div className="footer-bottom">
            © 2026 精油能量圖譜 · 精油學 · 本站內容採 CC BY-NC 4.0 授權
            <br />
            網頁設計 by <a
              href="https://show.intelliverse.tw/"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: 'inherit', textDecoration: 'underline' }}
            >靈境智造 Intelliverse</a> · 讓 AI 幫你賺錢
          </div>
        </footer>

        <Script src="/assets/js/nav.js" strategy="afterInteractive" />
      </body>
    </html>
  );
}
