/**
 * 注入 JSON-LD 結構化資料（schema.org）。
 * 用 <script type="application/ld+json"> 讓 Google/Bing 讀取。
 */
export default function JsonLd({ data }: { data: object | object[] }) {
  return (
    <script
      type="application/ld+json"
      // eslint-disable-next-line react/no-danger
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(Array.isArray(data) ? data : [data]),
      }}
    />
  );
}
