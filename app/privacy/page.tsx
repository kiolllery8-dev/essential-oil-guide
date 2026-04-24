import type { Metadata } from 'next';
import JsonLd from '../components/JsonLd';
import { breadcrumbSchema, SITE, DEFAULT_OG } from '../lib/schema';

const URL = `${SITE}/privacy/`;
const TITLE = '隱私政策 | 精油能量圖譜';
const DESC = '精油能量圖譜隱私政策：本站為靜態內容網站，不主動收集個人識別資訊。Google Analytics（若啟用）僅用於網站匿名流量統計。';

export const metadata: Metadata = {
  title: { absolute: TITLE },
  description: DESC,
  alternates: { canonical: URL },
  openGraph: { type: 'article', url: URL, title: TITLE, description: DESC, images: [{ url: DEFAULT_OG, width: 1200, height: 630 }] },
  twitter: { title: TITLE, description: DESC, images: [DEFAULT_OG] },
};

export default function Privacy() {
  const crumbs = breadcrumbSchema([
    { name: '首頁', url: '/' },
    { name: '隱私政策', url: '/privacy/' },
  ]);

  return (
    <>
      <JsonLd data={crumbs} />
      <section style={{ maxWidth: 860, margin: '40px auto 80px', padding: '0 24px', lineHeight: 1.85 }}>
        <h1 style={{ fontSize: 38, marginBottom: 20, color: 'var(--green-dark)' }}>🔒 隱私政策</h1>
        <p style={{ color: 'var(--text-mid)', fontSize: 15, marginBottom: 40 }}>最後更新：2026 年 4 月</p>

        <h2>一、政策宣言</h2>
        <p>
          靈境智造 Intelliverse Studio（以下簡稱「本站」）非常重視您的個人隱私。本政策說明本站如何處理您訪問時可能產生的資料。
        </p>

        <h2>二、本站收集哪些資料</h2>
        <p>本站為<strong>純靜態教育內容網站</strong>，<strong>不設註冊、登入、訂閱、購物功能</strong>，因此：</p>
        <ul>
          <li>✅ 本站<strong>不主動</strong>收集您的姓名、Email、電話、地址等個人識別資訊</li>
          <li>✅ 本站<strong>不要求</strong>您填寫任何表單</li>
          <li>✅ 本站<strong>不販售</strong>任何商品或服務</li>
        </ul>

        <h2>三、自動化技術資料</h2>
        <p>當您訪問本站時，以下資料可能被自動記錄（主要由 GitHub Pages 託管平台與 CDN 服務商處理）：</p>
        <ul>
          <li>IP 位址（用於路由，會在服務商日誌保留短期）</li>
          <li>瀏覽器類型與版本</li>
          <li>作業系統</li>
          <li>訪問時間、訪問頁面</li>
          <li>來源網址（referrer）</li>
        </ul>
        <p>這些資料<strong>匿名且彙總</strong>使用，不會被本站儲存或識別為個人身份。</p>

        <h2>四、Cookies 與第三方分析</h2>
        <p>本站目前的第三方服務：</p>
        <ul>
          <li>
            <strong>Google Fonts</strong>：載入 Noto Sans TC 字型。Google 依其
            <a href="https://policies.google.com/privacy" target="_blank" rel="noopener" style={{ color: 'var(--green-dark)' }}> 隱私政策 </a>
            處理字型請求。
          </li>
          <li>
            <strong>jsDelivr CDN</strong>：提供圖片資源加速。
          </li>
          <li>
            <strong>Google Analytics / Search Console</strong>：<strong>若啟用</strong>，僅用於匿名流量統計與 SEO 優化，
            不會收集個人識別資訊。您可透過瀏覽器擴充（如 uBlock Origin）封鎖追蹤。
          </li>
        </ul>

        <h2>五、資料共享</h2>
        <p>本站<strong>不販售、不出租、不交換</strong>任何訪客資料給第三方。</p>

        <h2>六、資料安全</h2>
        <p>
          本站以 HTTPS 加密連線，由 GitHub Pages 提供基礎安全防護。但網路傳輸無法 100% 保證絕對安全，您承擔使用網路服務固有的風險。
        </p>

        <h2>七、兒童隱私</h2>
        <p>
          本站內容為一般教育資訊，不針對 13 歲以下兒童。我們不刻意收集兒童資料。
          若您為兒童監護人並發現本站意外收集兒童資料，請聯繫我們立即刪除。
        </p>

        <h2>八、您的權利</h2>
        <p>若您認為本站處理您的資料有違本政策，您可：</p>
        <ul>
          <li>寄信至 <a href="mailto:linsonder6@gmail.com" style={{ color: 'var(--green-dark)' }}>linsonder6@gmail.com</a> 要求查詢、更正或刪除。</li>
          <li>使用瀏覽器「不追蹤」設定與廣告封鎖擴充。</li>
          <li>停止使用本站。</li>
        </ul>

        <h2>九、政策變更</h2>
        <p>
          本政策可能依法規或服務內容調整而更新，最新版本將張貼於本頁。
          建議您定期回顧。重大變更時會於首頁公告。
        </p>

        <h2>十、聯絡我們</h2>
        <p>
          對本政策有任何疑問，請至 <a href="/contact/" style={{ color: 'var(--green-dark)' }}>聯絡頁面</a> 或來信
          <a href="mailto:linsonder6@gmail.com" style={{ color: 'var(--green-dark)' }}> linsonder6@gmail.com</a>。
        </p>
      </section>
    </>
  );
}
