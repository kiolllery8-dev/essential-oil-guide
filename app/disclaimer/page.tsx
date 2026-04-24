import type { Metadata } from 'next';
import JsonLd from '../components/JsonLd';
import { breadcrumbSchema, SITE, DEFAULT_OG } from '../lib/schema';

const URL = `${SITE}/disclaimer/`;
const TITLE = '免責聲明 | 精油能量圖譜';
const DESC = '精油能量圖譜的內容為教育性知識整理，不構成醫療、診斷或治療建議。精油使用前請諮詢合格芳療師、醫師或藥師。';

export const metadata: Metadata = {
  title: { absolute: TITLE },
  description: DESC,
  alternates: { canonical: URL },
  openGraph: { type: 'article', url: URL, title: TITLE, description: DESC, images: [{ url: DEFAULT_OG, width: 1200, height: 630 }] },
  twitter: { title: TITLE, description: DESC, images: [DEFAULT_OG] },
};

export default function Disclaimer() {
  const crumbs = breadcrumbSchema([
    { name: '首頁', url: '/' },
    { name: '免責聲明', url: '/disclaimer/' },
  ]);

  return (
    <>
      <JsonLd data={crumbs} />
      <section style={{ maxWidth: 860, margin: '40px auto 80px', padding: '0 24px', lineHeight: 1.85 }}>
        <h1 style={{ fontSize: 38, marginBottom: 20, color: 'var(--green-dark)' }}>⚠️ 免責聲明</h1>
        <p style={{ color: 'var(--text-mid)', fontSize: 15, marginBottom: 40 }}>最後更新：2026 年 4 月 · 請在使用精油前完整閱讀</p>

        <h2>一、內容性質</h2>
        <p>
          精油能量圖譜（<a href="https://intelliverse.tw/">https://intelliverse.tw</a>）上的所有內容——包含文字、圖片、影音、圖表、資料庫——
          皆為<strong>教育與參考目的</strong>之知識整理，<strong>不構成醫療建議、疾病診斷或治療處方</strong>。
        </p>

        <h2>二、醫療聲明</h2>
        <ul>
          <li>本站內容<strong>不得取代</strong>專業醫師、芳療師、藥師、護理師的診斷或建議。</li>
          <li>任何健康狀況疑慮、慢性病、急性症狀，請立即就醫，<strong>不可延誤治療</strong>而僅依賴精油。</li>
          <li>使用精油前，建議先諮詢您的主治醫師，尤其是<strong>孕婦、哺乳婦女、幼兒、老年人、癲癇患者、心血管疾病者、腎臟疾病者、正在服藥者</strong>。</li>
        </ul>

        <h2>三、使用風險</h2>
        <ul>
          <li>精油為高濃度植物萃取物，<strong>不當使用可能造成皮膚灼傷、過敏、光敏、神經毒性、肝腎負擔、胎兒影響</strong>等嚴重後果。</li>
          <li>本站標示的稀釋比例、劑量、使用方式僅供參考；實際使用請根據<strong>個人體質、年齡、健康狀況</strong>調整。</li>
          <li>首次使用新精油請先進行<strong>貼膚測試</strong>（基底油稀釋 1% 塗抹手肘內側 24 小時觀察）。</li>
          <li>請將精油存放於<strong>兒童、寵物無法觸及的位置</strong>。誤食請立即以植物油或牛奶漱口、大量飲水並緊急就醫。</li>
        </ul>

        <h2>四、資料準確性</h2>
        <p>
          本站收錄之精油資訊（化學成分比例、學名、產地、功效）係整理自國際芳療機構、品牌官網、醫學期刊與 GC/MS 報告等公開資料。
          我們盡力確保資訊準確，但：
        </p>
        <ul>
          <li>植物成分會因<strong>產地、氣候、採收季節、萃取批次</strong>而顯著不同；</li>
          <li>品牌配方、產品資訊可能隨時更新，請以<strong>產品實際標籤</strong>為準；</li>
          <li>醫學研究持續進展，部分舊觀點可能被新研究推翻。</li>
        </ul>
        <p>如發現錯誤或過時資訊，歡迎 <a href="/contact/" style={{ color: 'var(--green-dark)' }}>聯繫我們</a> 指正。</p>

        <h2>五、責任限制</h2>
        <p>
          使用本站資訊所產生之任何直接或間接損害（包含但不限於：皮膚反應、健康狀況變化、經濟損失），
          本站作者、靈境智造 Intelliverse Studio 及其合作單位<strong>概不負責</strong>。
          使用者自行評估風險並承擔使用後果。
        </p>

        <h2>六、品牌與商標</h2>
        <p>
          本站提及之精油品牌（Aesop、Florihana、Aus Garden、Puressentiel 等）之名稱、商標、產品資訊皆歸其各自所有者所有，
          本站引用為提供消費者參考比較之用，<strong>與品牌方並無隸屬、贊助或授權關係</strong>（除非另行聲明）。
        </p>

        <h2>七、著作權與授權</h2>
        <ul>
          <li>本站原創內容採用 <strong>CC BY-NC 4.0</strong>（創用授權 - 姓名標示 - 非商業）授權。</li>
          <li>非商業使用可自由引用，請標註來源「精油能量圖譜 https://intelliverse.tw/」。</li>
          <li>商業使用（包含轉載至付費媒體、用於產品銷售、嵌入付費服務）請來信洽詢授權。</li>
          <li>AI 生成之植物示意圖像版權屬於本站；商業使用需授權。</li>
        </ul>

        <h2>八、法律管轄</h2>
        <p>
          本聲明適用<strong>中華民國法律</strong>。如因本站內容衍生爭議，雙方同意以<strong>臺灣臺中地方法院</strong>為第一審管轄法院。
        </p>

        <p style={{ marginTop: 48, color: 'var(--text-mid)', fontSize: 14 }}>
          若您無法接受本聲明任何一項條款，請立即停止使用本站。繼續使用視為同意本聲明全部內容。
        </p>
      </section>
    </>
  );
}
