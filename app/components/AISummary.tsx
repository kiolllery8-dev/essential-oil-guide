/**
 * Quick Answer / AI-friendly summary block
 * 80-120 字摘要，供 Google AI Overview / ChatGPT Search / Perplexity 引用
 *
 * 設計原則：
 *  - 用「常見用途、香氣特色、使用注意」取代「治療、改善疾病」
 *  - 保留必要安全提醒（孕婦、嬰幼兒、稀釋）
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
  return (
    <section
      className="ai-summary"
      itemScope
      itemType="https://schema.org/Question"
      style={{
        background: 'linear-gradient(135deg, #F5F0E6 0%, #EEE7D8 100%)',
        borderLeft: '4px solid #C8A673',
        padding: '20px 24px',
        borderRadius: 12,
        margin: '28px 0',
      }}
    >
      <h2
        itemProp="name"
        style={{
          fontSize: 18,
          fontWeight: 700,
          color: '#8B6F3E',
          margin: '0 0 10px',
          letterSpacing: '0.05em',
        }}
      >
        ✦ {title}
      </h2>
      <div itemScope itemProp="acceptedAnswer" itemType="https://schema.org/Answer">
        <p
          itemProp="text"
          style={{
            fontSize: 15,
            lineHeight: 1.85,
            color: '#3D3328',
            margin: 0,
          }}
        >
          {summary}
        </p>
      </div>
    </section>
  );
}
