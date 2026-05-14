# intelliverse.tw sitemap.xml 檢查報告

> 產生時間：2026-05-13
> sitemap 來源：`app/sitemap.ts`（Next.js metadata route）
> 輸出位置：`out/sitemap.xml`（build 後）→ 部署為 https://intelliverse.tw/sitemap.xml

## 總計

**342 個 URL**，分布如下：

| 類別 | 數量 | 範例 |
|---|---:|---|
| `/oil/{id}/`（302 支精油 datasheet） | **302** | `https://intelliverse.tw/oil/25/` |
| `/compounds-{nn}/`（化學分類頁） | 14 | `https://intelliverse.tw/compounds-01/` |
| `/oil-{name}/`（10 支單支精油專頁） | 10 | `https://intelliverse.tw/oil-cedarwood/` |
| `/article-{topic}/`（6 篇主題文章） | 6 | `https://intelliverse.tw/article-beginners/` |
| 首頁 | 1 | `https://intelliverse.tw/` |
| `/encyclopedia/`、`/oils/`、`/aromatherapy/`、`/safety/` | 4 | hub 頁 |
| `/about/`、`/contact/`、`/disclaimer/`、`/privacy/` | 4 | 站務頁 |
| `/search/` | 1 | 搜尋頁 |

## ✅ 覆蓋確認

- [x] 首頁
- [x] 所有單支精油頁（`/oil/{id}/` × 302）
- [x] 10 支單支精油命名頁（`/oil-{name}/`）
- [x] `/encyclopedia/` 大百科
- [x] `/oils/` 精油化學分子索引
- [x] `/aromatherapy/` 芳療應用
- [x] `/safety/` 安全指南
- [x] `/about/`、`/contact/`、`/disclaimer/`、`/privacy/`
- [x] 所有 6 篇 article-* 主題文章
- [x] 14 個 compounds-* 化學分類頁
- [x] sitemap 自動產生（`app/sitemap.ts` 從 `data/oils.json` 與 `html-source/*.html` 讀取）

## 重要設定

| 設定 | 值 | 備註 |
|---|---|---|
| `LAST_MOD` | `2026-05-13` | 本次大規模更新後已推進 |
| hub 頁 priority | 0.9 | encyclopedia / oils / aromatherapy / safety |
| 站務頁 priority | 0.4 | about / contact / disclaimer / privacy |
| 精油單品頁 priority | 0.6 | oil/{id} |
| changefreq | weekly / monthly | 視類型不同 |
| og:image | 每頁附帶 | 從 html-source `<meta og:image>` 或 fallback banner |

## ⚠️ 觀察與建議

| 觀察 | 處理建議 |
|---|---|
| `/search/` 進入 sitemap | 建議從 sitemap 排除（搜尋頁屬功能頁，不該被索引）— 可在 `app/sitemap.ts` 增加排除清單 |
| `LAST_MOD` 為全站單一日期 | 中期可改為「每頁個別 lastModified」（讀檔 mtime 或從 `data/oilDates.json`） |
| 部分 article-* / oil-* 頁缺 og:image | 已有 fallback；長期建議補上各自原創圖 |
| 未來新增 `/blog/` 或新文章類型 | 在 `app/sitemap.ts` 的 `readdirSync` filter 中加入；或新增類別陣列 |

## 部署檢查清單

1. **GSC 提交**：`https://intelliverse.tw/sitemap.xml` 在 Google Search Console「Sitemaps」頁面提交
2. **Bing 提交**：同上於 Bing Webmaster Tools
3. **發布後驗證**：
   ```
   curl https://intelliverse.tw/sitemap.xml | head -50
   curl https://intelliverse.tw/robots.txt
   ```
4. **AI bot 抓取確認**：robots.txt 含 GPTBot / OAI-SearchBot / PerplexityBot / ClaudeBot / Claude-User / Applebot-Extended / Google-Extended 等 AI 爬蟲明確 Allow

## robots.txt 配置摘要

| 路徑 | 規則 |
|---|---|
| `/admin/`、`/api/`、`/draft/`、`/private/` | Disallow（內部 / 草稿，不應被索引） |
| 所有其它路徑 | Allow |
| AI 爬蟲（GPTBot / OAI-SearchBot / ChatGPT-User / PerplexityBot / Perplexity-User / Google-Extended / ClaudeBot / Claude-User / Claude-Web / anthropic-ai / Applebot-Extended / CCBot / cohere-ai / Bytespider） | 全部顯式 Allow |
| 傳統搜尋引擎（Googlebot / Bingbot / Applebot） | 顯式 Allow |
| Sitemap 行 | `https://intelliverse.tw/sitemap.xml` |
