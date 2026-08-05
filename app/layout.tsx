import type { Metadata, Viewport } from 'next';
import Script from 'next/script';
import NavSearch from './components/NavSearch';
import JsonLd from './components/JsonLd';
import Analytics from './components/Analytics';
import { organizationSchema, websiteSchema, DEFAULT_OG } from './lib/schema';

export const metadata: Metadata = {
  title: {
    default: '精油能量圖譜｜中文精油百科、芳療應用與安全指南',
    template: '%s | 精油能量圖譜',
  },
  description:
    '精油能量圖譜：400+ 種精油的化學分類、植物來源、芳療應用（助眠、放鬆、空間香氛、肌膚保養）、安全使用與常見精油問題。涵蓋薰衣草、茶樹、尤加利、薄荷、乳香等常見精油，澳洲、黃金海岸等世界產地，建立完整、正確、易懂的精油學習路徑。',
  metadataBase: new URL('https://intelliverse.tw'),
  keywords: [
    '精油', '精油學', '芳療', 'aromatherapy', '精油化學', '化學分類',
    '單萜烯', '倍半萜醇', '薰衣草', '茶樹', '尤加利', '精油功效',
    '精油安全', '精油百科', '精油知識', 'essential oil',
    // 地理 / 品牌關鍵字
    '黃金海岸', '黃金海岸精油', '黃金海岸芳療', 'Gold Coast', 'Gold Coast essential oil',
    '澳洲', '澳洲精油', '澳洲芳療', '澳洲茶樹', '澳洲尤加利',
    'Australia', 'Australian essential oil', 'Australian aromatherapy',
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
        {/* 字型 woff2 實際來源是 fonts.gstatic.com（跨來源需 crossorigin）；
            少這條 preconnect 會在關鍵字型路徑多一次完整 TLS 連線建立 */}
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="preconnect" href="https://cdn.jsdelivr.net" />
        <link
          href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;800&display=swap"
          rel="stylesheet"
        />
        {/* ?v= 版本號：CDN 會長期快取 style.css，改樣式時務必同步 bump，否則新 HTML 配舊 CSS 會破版 */}
        <link rel="stylesheet" href="/assets/css/style.css?v=20260713" />
        {/* 關鍵內嵌樣式：nav 下拉的「預設收合」不能只靠外部 CSS——
            若 CDN 還在送舊版 style.css，子選單會整包攤在導覽列上破版。這段保證不會發生。 */}
        <style dangerouslySetInnerHTML={{ __html: `
nav ul li.has-sub{position:relative}
nav ul li.has-sub>a{display:flex;align-items:center;gap:4px}
.nav-caret{font-size:12px;line-height:1;opacity:.7}
.subnav{position:absolute;top:100%;left:0;min-width:200px;background:#fff;border:1px solid var(--border,#E5D9C0);border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.1);padding:6px;display:none;flex-direction:column;gap:2px;z-index:200}
nav ul li.has-sub:hover>.subnav,nav ul li.has-sub:focus-within>.subnav{display:flex}
.subnav li a{display:block;white-space:nowrap;padding:8px 14px;font-size:15px;font-weight:500;border-radius:6px;color:var(--text-dark,#2C2C2C)}
.subnav li a:hover{background:var(--green-light,#6B8E5A);color:#fff}
@media(max-width:640px){
.subnav{position:static;display:flex;border:none;box-shadow:none;background:transparent;padding:2px 0 6px 12px;min-width:0;border-left:2px solid var(--border,#E5D9C0);margin-left:14px}
.subnav li a{padding:10px 14px;font-size:15px;white-space:normal}
.nav-caret{display:none}
}` }} />
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
                <li><a href="/blend/">調配精油</a></li>
                {/* 生命靈數（計算機本體）拉到第一層，不收在 dropdown 裡 */}
                <li><a href="/numerology/">生命靈數</a></li>
                {/* 人格算命：命理／身心靈自我探索工具與知識（桌機 hover 展開、手機抽屜內直接列出） */}
                <li className="has-sub">
                  <a href="/numerology/" aria-haspopup="true">人格算命<span className="nav-caret" aria-hidden="true">▾</span></a>
                  <ul className="subnav">
                    <li><a href="/numerology/#lp-1">生命靈數 1–9 解析</a></li>
                    <li><a href="/numerology/#compat">生命靈數配對</a></li>
                    <li><a href="/numerology-vs-fortune-telling/">算命 vs 生命靈數</a></li>
                    <li><a href="/article-angel-numbers/">天使數字</a></li>
                    <li><a href="/article-tarot-basics/">塔羅牌入門</a></li>
                    <li><a href="/article-chakra-oils/">七脈輪與精油</a></li>
                    <li><a href="/article-spiritual-aromatherapy/">心靈芳療</a></li>
                    <li><a href="/article-meditation-oils/">冥想入門</a></li>
                  </ul>
                </li>
                <li><a href="/aromatherapy/">芳療應用</a></li>
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
                <li><a href="/references/">引用來源與參考資料</a></li>
                <li><a href="/disclaimer/">免責聲明</a></li>
                <li><a href="/privacy/">隱私政策</a></li>
                <li><a href="/contact/">聯絡我們</a></li>
              </ul>
            </div>
          </div>
          <div className="footer-bottom">
            © 2026 精油能量圖譜 · 精油學 · 網頁設計 by <a
              href="https://show.intelliverse.tw/"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: 'inherit', textDecoration: 'underline' }}
            >靈境智造 Intelliverse</a> · 有更多想法歡迎聯繫我們
          </div>
        </footer>

        <Script src="/assets/js/nav.js" strategy="afterInteractive" />
        <Script src="/assets/js/faq-accordion.js" strategy="afterInteractive" />
        <Script src="https://chat.intelliverse.tw/widget.js" strategy="afterInteractive" />
        <Analytics />
      </body>
    </html>
  );
}
