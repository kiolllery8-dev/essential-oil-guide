/**
 * 站內連結對應表
 *
 * 用途：在任何文章 / 精油頁 / FAQ 中，若出現以下「關鍵詞」，可以自動轉換成站內連結。
 * 這對 SEO（內部連結深度）與 GEO（AI 引用時更容易理解站點結構）都很重要。
 *
 * 使用方式：
 *   import { linkify, INTERNAL_LINKS } from '@/app/lib/internalLinks';
 *   const html = linkify('薰衣草精油是常見的助眠香氛');
 *   // → '<a href="/oil-lavender/">薰衣草精油</a>是常見的助眠香氛'
 *
 * 維護原則：
 *  - 「越具體」的詞放越前面（先 match 長詞，避免「精油」蓋掉「薰衣草精油」）
 *  - 每個關鍵詞只連到一個最相關的站內頁
 *  - 不要過度連結，同篇文章每個關鍵詞最多 linkify 一次
 */

export type InternalLink = {
  /** 顯示在文章內的關鍵詞 */
  keyword: string;
  /** 連結目標（絕對路徑，trailing slash） */
  href: string;
  /** title 屬性說明 */
  title?: string;
  /** 是否為「精油單品頁」（用於樣式區分） */
  isOil?: boolean;
};

/** 順序很重要：長詞 / 具體詞要在前 */
export const INTERNAL_LINKS: InternalLink[] = [
  // ─── 精油單品（最具體） ───
  { keyword: '薰衣草精油', href: '/oil-lavender/', title: '薰衣草精油完整介紹', isOil: true },
  { keyword: '茶樹精油', href: '/oil-tea-tree/', title: '茶樹精油完整介紹', isOil: true },
  { keyword: '尤加利精油', href: '/oil-eucalyptus/', title: '尤加利精油完整介紹', isOil: true },
  { keyword: '薄荷精油', href: '/oil-peppermint/', title: '薄荷精油完整介紹', isOil: true },
  { keyword: '甜橙精油', href: '/oil-sweet-orange/', title: '甜橙精油完整介紹', isOil: true },
  { keyword: '乳香精油', href: '/oil-frankincense/', title: '乳香精油完整介紹', isOil: true },
  { keyword: '佛手柑精油', href: '/oil-bergamot/', title: '佛手柑精油完整指南', isOil: true },
  { keyword: '佛手柑', href: '/oil-bergamot/', title: '佛手柑精油完整指南', isOil: true },
  { keyword: '玫瑰精油', href: '/oil-rose/', title: '玫瑰精油完整指南', isOil: true },
  { keyword: '大馬士革玫瑰', href: '/oil-rose/', title: '玫瑰精油完整指南：三大品種比較', isOil: true },
  { keyword: '五月玫瑰', href: '/oil-rose/', title: '玫瑰精油完整指南：三大品種比較', isOil: true },
  { keyword: '玫瑰原精', href: '/oil-rose/#三奧圖vs原精兩種萃取的差異', title: '玫瑰原精 vs 奧圖比較' },
  { keyword: '奧圖玫瑰', href: '/oil-rose/#三奧圖vs原精兩種萃取的差異', title: '玫瑰奧圖 vs 原精比較' },
  { keyword: '天竺葵精油', href: '/oil-geranium/', title: '天竺葵精油完整指南', isOil: true },
  { keyword: '玫瑰天竺葵', href: '/oil-geranium/', title: '天竺葵精油完整指南', isOil: true },
  { keyword: '波旁島天竺葵', href: '/oil-geranium/#二三大產地比較', title: '天竺葵三大產地比較' },
  { keyword: '葡萄柚精油', href: '/oil-grapefruit/', title: '葡萄柚精油完整指南', isOil: true },
  { keyword: '圓柚酮', href: '/oil-grapefruit/#二化學成分輪廓', title: '葡萄柚特徵分子' },
  { keyword: '葡萄柚效應', href: '/oil-grapefruit/#四藥物交互作用葡萄柚效應', title: '葡萄柚與藥物交互作用' },
  { keyword: '松柏類', href: '/article-conifers/', title: '松柏家族精油完整比較' },
  { keyword: '松精油', href: '/article-conifers/', title: '松柏家族精油完整比較' },
  { keyword: '雲杉', href: '/article-conifers/', title: '松柏家族精油完整比較' },
  { keyword: '冷杉', href: '/article-conifers/', title: '松柏家族精油完整比較' },
  { keyword: '杜松', href: '/article-conifers/', title: '松柏家族精油完整比較' },
  { keyword: '絲柏', href: '/article-conifers/', title: '松柏家族精油完整比較' },
  { keyword: '森林浴', href: '/article-conifers/#五適用情境快速對照', title: '松柏類森林浴擴香配方' },
  { keyword: 'α-蒎烯', href: '/article-conifers/#三化學成分輪廓比較', title: 'α-蒎烯精油比較' },
  { keyword: '甜馬鬱蘭', href: '/oil-marjoram/', title: '甜馬鬱蘭精油完整指南', isOil: true },
  { keyword: '馬鬱蘭', href: '/oil-marjoram/', title: '甜馬鬱蘭精油完整指南', isOil: true },
  { keyword: '薑精油', href: '/oil-ginger/', title: '薑精油完整指南', isOil: true },
  { keyword: '橙花精油', href: '/oil-neroli/', title: '橙花精油完整指南', isOil: true },
  { keyword: '橙花', href: '/oil-neroli/', title: '橙花精油完整指南', isOil: true },
  { keyword: 'Neroli', href: '/oil-neroli/', title: '橙花精油完整指南', isOil: true },
  { keyword: '岩蘭草', href: '/oil-vetiver/', title: '岩蘭草精油完整指南', isOil: true },
  { keyword: 'Vetiver', href: '/oil-vetiver/', title: '岩蘭草精油完整指南', isOil: true },
  { keyword: '快樂鼠尾草', href: '/oil-clary-sage/', title: '快樂鼠尾草精油完整指南', isOil: true },
  { keyword: 'Clary Sage', href: '/oil-clary-sage/', title: '快樂鼠尾草精油完整指南', isOil: true },

  // ─── 第三波 oil-* ───
  { keyword: '永久花', href: '/oil-helichrysum/', title: '義大利永久花完整指南', isOil: true },
  { keyword: '義大利永久花', href: '/oil-helichrysum/', title: '義大利永久花完整指南', isOil: true },
  { keyword: 'Helichrysum', href: '/oil-helichrysum/', title: '義大利永久花完整指南', isOil: true },
  { keyword: '檀香', href: '/oil-sandalwood/', title: '檀香精油完整指南', isOil: true },
  { keyword: 'Santalum', href: '/oil-sandalwood/', title: '檀香精油完整指南', isOil: true },
  { keyword: '茉莉', href: '/oil-jasmine/', title: '茉莉精油完整指南', isOil: true },
  { keyword: '大花茉莉', href: '/oil-jasmine/', title: '茉莉精油完整指南', isOil: true },
  { keyword: '小花茉莉', href: '/oil-jasmine/', title: '茉莉精油完整指南', isOil: true },
  { keyword: 'Jasmine', href: '/oil-jasmine/', title: '茉莉精油完整指南', isOil: true },
  { keyword: '香茅', href: '/oil-citronella/', title: '香茅精油完整指南', isOil: true },
  { keyword: '爪哇香茅', href: '/oil-citronella/', title: '香茅精油完整指南', isOil: true },
  { keyword: 'Citronella', href: '/oil-citronella/', title: '香茅精油完整指南', isOil: true },
  { keyword: '丁香', href: '/oil-clove/', title: '丁香精油完整指南', isOil: true },
  { keyword: '丁香花苞', href: '/oil-clove/', title: '丁香精油完整指南', isOil: true },
  { keyword: 'Clove', href: '/oil-clove/', title: '丁香精油完整指南', isOil: true },
  { keyword: '苦橙葉', href: '/oil-petitgrain/', title: '苦橙葉精油完整指南', isOil: true },
  { keyword: 'Petitgrain', href: '/oil-petitgrain/', title: '苦橙葉精油完整指南', isOil: true },
  { keyword: '杜松漿果', href: '/oil-juniper/', title: '杜松漿果精油完整指南', isOil: true },
  { keyword: 'Juniper', href: '/oil-juniper/', title: '杜松漿果精油完整指南', isOil: true },
  { keyword: '絲柏精油', href: '/oil-cypress/', title: '絲柏精油完整指南', isOil: true },
  { keyword: 'Cypress', href: '/oil-cypress/', title: '絲柏精油完整指南', isOil: true },

  // ─── 第三波 article-* ───
  { keyword: '純露', href: '/article-hydrosols/', title: '純露完整指南' },
  { keyword: 'hydrosol', href: '/article-hydrosols/', title: '純露完整指南' },
  { keyword: '玫瑰純露', href: '/article-hydrosols/#三5-大主流純露推薦', title: '玫瑰純露' },
  { keyword: '橙花純露', href: '/article-hydrosols/#三5-大主流純露推薦', title: '橙花純露' },
  { keyword: '新手錯誤', href: '/article-newbie-mistakes/', title: '10 大新手錯誤' },
  { keyword: '柑橘類', href: '/article-citrus-comparison/', title: '柑橘類精油完整比較' },
  { keyword: '柑橘精油', href: '/article-citrus-comparison/', title: '柑橘類精油完整比較' },

  // ─── 第五波 oil-* ───
  { keyword: '月桂精油', href: '/oil-bay/', title: '月桂精油完整指南', isOil: true },
  { keyword: '月桂', href: '/oil-bay/', title: '月桂精油完整指南', isOil: true },
  { keyword: 'Bay Laurel', href: '/oil-bay/', title: '月桂精油完整指南', isOil: true },
  { keyword: '沒藥精油', href: '/oil-myrrh/', title: '沒藥精油完整指南', isOil: true },
  { keyword: '沒藥', href: '/oil-myrrh/', title: '沒藥精油完整指南', isOil: true },
  { keyword: '紅沒藥', href: '/oil-myrrh/#二紅沒藥-vs-沒藥', title: '紅沒藥比較' },
  { keyword: 'Myrrh', href: '/oil-myrrh/', title: '沒藥精油完整指南', isOil: true },
  { keyword: '廣藿香', href: '/oil-patchouli/', title: '廣藿香精油完整指南', isOil: true },
  { keyword: 'Patchouli', href: '/oil-patchouli/', title: '廣藿香精油完整指南', isOil: true },
  { keyword: '黑胡椒', href: '/oil-black-pepper/', title: '黑胡椒精油完整指南', isOil: true },
  { keyword: 'Black Pepper', href: '/oil-black-pepper/', title: '黑胡椒精油完整指南', isOil: true },
  { keyword: '桉油醇樟', href: '/oil-ravintsara/', title: 'Ravintsara 完整指南', isOil: true },
  { keyword: 'Ravintsara', href: '/oil-ravintsara/', title: 'Ravintsara 完整指南', isOil: true },
  { keyword: '玫瑰草', href: '/oil-palmarosa/', title: '玫瑰草精油完整指南', isOil: true },
  { keyword: 'Palmarosa', href: '/oil-palmarosa/', title: '玫瑰草精油完整指南', isOil: true },

  // ─── 第五波 大主題 article-* ───
  { keyword: '中醫芳療', href: '/article-tcm-aromatherapy/', title: '中醫芳療完整指南' },
  { keyword: '12 經絡', href: '/article-tcm-aromatherapy/#二十二經絡與對應精油', title: '經絡精油對應' },
  { keyword: '五行精油', href: '/article-tcm-aromatherapy/#三五行金木水火土與精油五大類', title: '五行精油對應' },
  { keyword: '寒熱屬性', href: '/article-tcm-aromatherapy/#四寒熱屬性對照表', title: '精油寒熱屬性' },
  { keyword: '心靈芳療', href: '/article-spiritual-aromatherapy/', title: '心靈芳療完整指南' },
  { keyword: '脈輪', href: '/article-spiritual-aromatherapy/#二七個脈輪與精油對應表', title: '脈輪精油對應' },
  { keyword: '冥想精油', href: '/article-spiritual-aromatherapy/#四冥想擴香配方', title: '冥想擴香配方' },
  { keyword: '羅馬洋甘菊', href: '/article-chamomile-comparison/', title: '羅馬 vs 德國洋甘菊比較' },
  { keyword: '德國洋甘菊', href: '/article-chamomile-comparison/', title: '羅馬 vs 德國洋甘菊比較' },
  { keyword: '洋甘菊比較', href: '/article-chamomile-comparison/', title: '羅馬 vs 德國洋甘菊比較' },
  { keyword: '光敏性', href: '/oil-bergamot/#四光敏性與12小時避光原則', title: '佛手柑光敏性說明' },

  // ─── 高優先主題文章 ───
  { keyword: '兒童芳療', href: '/article-children/', title: '兒童芳療 0-12 歲分段安全' },
  { keyword: '嬰幼兒精油', href: '/article-children/', title: '兒童芳療 0-12 歲分段安全' },
  { keyword: '兒童精油', href: '/article-children/', title: '兒童芳療 0-12 歲分段安全' },
  { keyword: '孕期芳療', href: '/article-pregnancy/', title: '孕期芳療完整指南' },
  { keyword: '孕婦精油', href: '/article-pregnancy/', title: '孕期芳療完整指南' },
  { keyword: '寵物芳療', href: '/article-pets/', title: '寵物芳療：貓狗安全 vs 危險精油' },
  { keyword: '寵物精油', href: '/article-pets/', title: '寵物芳療：貓狗安全 vs 危險精油' },
  { keyword: '貓咪精油', href: '/article-pets/', title: '寵物芳療：貓狗安全 vs 危險精油' },
  { keyword: '辦公室擴香', href: '/article-office/', title: '上班族 5 支提神精油' },
  { keyword: '提神精油', href: '/article-office/', title: '上班族 5 支提神精油' },

  // ─── 分類索引頁 ───
  { keyword: '精油化學分類', href: '/oils/', title: '依化學分子分類的精油索引' },
  { keyword: '化學分子索引', href: '/oils/', title: '依化學分子分類的精油索引' },
  { keyword: '精油索引', href: '/oils/', title: '完整精油索引' },
  { keyword: '芳療應用', href: '/aromatherapy/', title: '芳療應用教學' },
  { keyword: '芳療入門', href: '/aromatherapy/', title: '芳療應用教學' },
  { keyword: '精油安全', href: '/safety/', title: '精油安全使用指南' },
  { keyword: '安全指南', href: '/safety/', title: '精油安全使用指南' },
  { keyword: '精油化學', href: '/encyclopedia/', title: '精油生成原理與化學知識' },
  { keyword: '精油大百科', href: '/encyclopedia/', title: '精油大百科' },
  { keyword: '澳洲精油', href: '/encyclopedia/#regions', title: '澳洲精油產區介紹' },
  { keyword: '黃金海岸精油', href: '/encyclopedia/#regions', title: '黃金海岸精油' },

  // ─── 關於 / 客服 ───
  { keyword: '聯絡我們', href: '/contact/', title: '聯絡精油能量圖譜' },
  { keyword: '網站簡介', href: '/about/', title: '關於精油能量圖譜' },
  { keyword: '免責聲明', href: '/disclaimer/', title: '免責聲明與資訊使用準則' },
  { keyword: '隱私政策', href: '/privacy/', title: '隱私政策' },
];

/**
 * 將純文字 / HTML 字串中的關鍵詞轉成站內連結。
 *
 *  - 已經在 <a>...</a> 內的字會跳過（避免巢狀連結）
 *  - 已經是 <h1>~<h6> 標題裡的字也跳過（避免標題被改）
 *  - 每個關鍵詞最多 linkify 一次
 *
 * @param text  原始文字或 HTML 片段
 * @param opts  選項
 *   - maxPerKeyword：每個關鍵詞最多連結次數（預設 1）
 *   - skipAnchors：是否跳過已在 <a> 內的字（預設 true）
 *   - skipHeadings：是否跳過 <h1>~<h6> 內的字（預設 true）
 */
export function linkify(
  text: string,
  opts: { maxPerKeyword?: number; skipAnchors?: boolean; skipHeadings?: boolean } = {}
): string {
  const { maxPerKeyword = 1, skipAnchors = true, skipHeadings = true } = opts;

  if (!text) return text;

  // 1. 先把要保護的區段（已在 <a>、<h1>~<h6>、<code>、<pre> 內）抽出來
  const protectedSegments: string[] = [];
  let working = text;
  const protectRegexes: RegExp[] = [];
  if (skipAnchors) protectRegexes.push(/<a\s[^>]*>[\s\S]*?<\/a>/gi);
  if (skipHeadings) protectRegexes.push(/<h[1-6]\s*[^>]*>[\s\S]*?<\/h[1-6]>/gi);
  protectRegexes.push(/<code\b[^>]*>[\s\S]*?<\/code>/gi);
  protectRegexes.push(/<pre\b[^>]*>[\s\S]*?<\/pre>/gi);

  protectRegexes.forEach((re) => {
    working = working.replace(re, (m) => {
      protectedSegments.push(m);
      return ` PROTECTED_${protectedSegments.length - 1} `;
    });
  });

  // 2. 對每個關鍵詞做替換
  for (const link of INTERNAL_LINKS) {
    let count = 0;
    const re = new RegExp(escapeRegex(link.keyword), 'g');
    working = working.replace(re, (m) => {
      if (count >= maxPerKeyword) return m;
      count++;
      const titleAttr = link.title ? ` title="${escapeAttr(link.title)}"` : '';
      const classAttr = link.isOil ? ' class="internal-link internal-link--oil"' : ' class="internal-link"';
      return `<a href="${link.href}"${classAttr}${titleAttr}>${m}</a>`;
    });
  }

  // 3. 把保護區段塞回去
  working = working.replace(/ PROTECTED_(\d+) /g, (_, i) => protectedSegments[Number(i)] || '');

  return working;
}

function escapeRegex(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
function escapeAttr(s: string): string {
  return s.replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/**
 * 取得「相關連結」清單（給文章末尾 / 側欄使用）
 *
 * @param topic 主題關鍵字（例如「薰衣草」、「澳洲」、「化學」）
 * @param max   最多回傳幾筆（預設 6）
 */
export function getRelatedLinks(topic: string, max = 6): InternalLink[] {
  if (!topic) return INTERNAL_LINKS.slice(0, max);
  const lower = topic.toLowerCase();
  // 先抓「關鍵詞包含 topic」的條目，再用其他熱門條目補滿
  const direct = INTERNAL_LINKS.filter((l) => l.keyword.toLowerCase().includes(lower) || lower.includes(l.keyword.toLowerCase()));
  const others = INTERNAL_LINKS.filter((l) => !direct.includes(l));
  return [...direct, ...others].slice(0, max);
}
