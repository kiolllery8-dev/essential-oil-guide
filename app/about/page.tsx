import type { Metadata } from 'next';
import JsonLd from '../components/JsonLd';
import { breadcrumbSchema, SITE, DEFAULT_OG } from '../lib/schema';

const URL = `${SITE}/about/`;
const TITLE = '網站簡介 | 精油能量圖譜';
const DESC = '精油能量圖譜是由靈境智造 Intelliverse Studio 打造的中文精油知識庫，收錄 400+ 支精油的化學分類、芳療應用與安全資訊，以科學方法整理並以視覺化方式呈現。';

export const metadata: Metadata = {
  title: { absolute: TITLE },
  description: DESC,
  alternates: { canonical: URL },
  openGraph: { type: 'article', url: URL, title: TITLE, description: DESC, images: [{ url: DEFAULT_OG, width: 1200, height: 630 }] },
  twitter: { title: TITLE, description: DESC, images: [DEFAULT_OG] },
};

export default function About() {
  const crumbs = breadcrumbSchema([
    { name: '首頁', url: '/' },
    { name: '網站簡介', url: '/about/' },
  ]);

  return (
    <>
      <JsonLd data={crumbs} />
      <section style={{ maxWidth: 860, margin: '40px auto 80px', padding: '0 24px', lineHeight: 1.85 }}>
        <h1 style={{ fontSize: 38, marginBottom: 20, color: 'var(--green-dark)' }}>🌿 關於精油能量圖譜</h1>
        <p style={{ color: 'var(--text-mid)', fontSize: 15, marginBottom: 40 }}>最完整的中文精油知識庫 · 收錄 400+ 精油 · 12 大化學分類</p>

        <h2 style={{ marginTop: 32 }}>📖 我們在做什麼</h2>
        <p>
          精油能量圖譜是一個以<strong>科學化學分類</strong>為骨幹、整合<strong>芳療實務應用</strong>與<strong>安全使用指南</strong>的中文精油知識平台。
          我們將 400 多種精油按 12 大化學族群（單萜烯、氧化物、醛類、酯類、酚類、單萜醇、倍半萜醇等）系統整理，
          並為每支精油標註拉丁學名、植物科屬、萃取部位、主要成分、適用症候與安全注意。
        </p>

        <h2 style={{ marginTop: 32 }}>✨ 我們的理念</h2>
        <ul>
          <li><strong>科學優先</strong>：以化學分子為基礎理解精油療效，而非行銷話術。</li>
          <li><strong>安全為本</strong>：每支精油均附使用禁忌、稀釋比例、特殊族群提醒。</li>
          <li><strong>教育性質</strong>：本站內容為知識整理與教育參考，不構成醫療建議。</li>
          <li><strong>開放共享</strong>：內容以 CC BY-NC 4.0 授權，歡迎非商業引用。</li>
        </ul>

        <h2 style={{ marginTop: 32 }}>📚 資料來源</h2>
        <p>
          本站內容整理自以下公開來源與資料庫：
        </p>
        <ul>
          <li>國際芳療師協會（IFA、NAHA、AIA）教材與白皮書</li>
          <li>Aesop、Florihana、Aus Garden、Puressentiel 等品牌官網技術資料</li>
          <li>PubMed / Google Scholar 精油相關醫學期刊論文</li>
          <li>TopView AI 視覺工具（植物與場景圖示意生成）</li>
        </ul>
        <p style={{ color: 'var(--text-mid)', fontSize: 14 }}>
          資料僅供教育參考；精油使用時請依照產品標示、諮詢合格芳療師或醫師。
        </p>

        <h2 style={{ marginTop: 32 }}>🏢 關於靈境智造 Intelliverse Studio</h2>
        <p>
          <a href="https://show.intelliverse.tw/" target="_blank" rel="noopener" style={{ color: 'var(--green-dark)' }}>靈境智造 Intelliverse Studio</a>{' '}
          是位於臺中的品牌企劃與 AI 整合工作室，專注於：
        </p>
        <ul>
          <li>品牌設計與電商落地頁</li>
          <li>AI 圖像／影音素材生成</li>
          <li>精油、香氛、保養品牌知識網站</li>
          <li>軟硬整合產品設計</li>
        </ul>
        <p>
          本站為 Intelliverse 自主開發的精油知識專案，實驗「AI + 傳統出版品 + 靜態網站」的知識體系建構路徑。
        </p>

        <h2 style={{ marginTop: 32 }}>💌 聯絡我們</h2>
        <p>有任何建議、指正或合作洽詢，歡迎透過 <a href="/contact/" style={{ color: 'var(--green-dark)' }}>聯絡頁面</a>與我們聯繫。</p>
      </section>
    </>
  );
}
