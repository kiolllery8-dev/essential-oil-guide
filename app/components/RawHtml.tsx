/**
 * 將 raw HTML 注入 DOM。靜態匯出的網站全用 <a> 完整頁面載入，
 * 瀏覽器解析時內嵌 <script> 會自動執行，不需 useEffect 重跑。
 * suppressHydrationWarning 避免 script 提前修改 DOM 造成 hydration warning。
 */
export default function RawHtml({ html }: { html: string }) {
  return (
    <div
      suppressHydrationWarning
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
