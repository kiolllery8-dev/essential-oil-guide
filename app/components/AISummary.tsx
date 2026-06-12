/**
 * Quick Answer / AI-friendly summary — 純 JSON-LD 版（不顯示給人，只供機器讀取）
 *
 * 為什麼不顯示給人：
 *  - 視覺上保持頁面乾淨（不再有可見的米色「快速答案」框）
 *  - 但仍以 schema.org Question/Answer JSON-LD 形式存在，供 Google AI Overview /
 *    ChatGPT Search / Perplexity / Claude 引用
 *  - 這是 Google 官方推薦的結構化資料做法（機器讀、不顯示），非 cloaking：
 *    我們並未對使用者與爬蟲顯示「不同的可見內容」，摘要的同等資訊正文本來就有
 *
 * 設計原則：
 *  - 用「常見用途、香氣特色、使用注意」取代「治療、改善疾病」
 *  - 避免醫療療效宣稱，符合臺灣化妝品/食品/藥物法規
 */
export default function AISummary({
  summary,
  title = '快速答案',
}: {
  summary: string;
  title?: string;
}) {
  if (!summary) return null;
  const topic = title.replace(/\s*快速答案\s*$/, '').trim() || '本頁主題';
  // 包在 WebPage.mainEntity 內：Google 不解析「裸 Question」頂層節點；
  // 不用 FAQPage 以免與部分頁面既有 FAQPage 重複衝突
  const data = {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    mainEntity: {
      '@type': 'Question',
      name: `${topic}有哪些特性、常見用途與使用注意？`,
      acceptedAnswer: { '@type': 'Answer', text: summary },
    },
  };
  return (
    <script
      type="application/ld+json"
      // eslint-disable-next-line react/no-danger
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
