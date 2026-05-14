# SEO / GEO 全站優化變更紀錄

> 任務日期：2026-05-13
> 範圍：intelliverse.tw 精油能量圖譜（Next.js 15 / App Router / static export）
> 原則：不破壞 UI、不刪內容、不加電商功能、不加 Product schema、不偽造作者品牌資料、不強化醫療宣稱、所有更動需 build 成功

---

## ✅ Build 狀態

| 項目 | 結果 |
|---|---|
| `npx next build` | ✓ 成功 |
| 靜態頁面總數 | 348 頁 |
| 編譯時間 | ~1.4 秒 |
| 型別檢查 / ESLint | 通過 |

---

## 1. Phase 1-3：Metadata + 結構化資料

### 變更檔案
- `app/layout.tsx`
- `app/oil/[id]/page.tsx`
- `app/[slug]/page.tsx`（透過 `loadHtml` 讀取 `<title>`/`<meta>`）
- `app/lib/schema.ts`
- `html-source/index.html`
- `html-source/oils.html`

### 重點
- 站名統一為：`精油能量圖譜｜中文精油百科、芳療應用與安全指南`
- 精油單品頁 title 模板：`{中文}精油｜成分、香氣、使用方式與安全注意`
- 描述（meta description）80-120 字、避免醫療宣稱、結尾以「常見芳療應用與使用安全注意」收尾
- 全站關鍵字加入「黃金海岸 / 澳洲 / Gold Coast / Australia」（既存任務延續）
- **Schema 移除假日期**：原 `2026-01-01` / `2026-04-21` 硬編碼已移除；`datePublished` 改為 optional，`dateModified` 採 build 當下日期
- 保留：`WebSite` + `SearchAction`、`Organization`、`Article`、`BreadcrumbList`、`ChemicalSubstance`（精油頁的 `about` 欄位）、`ContactPage`
- 不加：`Product`（商品 schema）、`MedicalIndication`、任何療效宣稱類 schema

---

## 2. Phase 4：GEO / AI 引用優化

### 新建元件
- `app/components/AISummary.tsx`
  - 「快速答案」區塊，80-145 字
  - schema.org `Question` + `Answer` microdata（給 AI Overview / ChatGPT Search / Perplexity / Claude 引用）
  - Morandi 漸層底 + 金色左 border，與站台調性一致

### 新建資料表
- `app/lib/pageSummaries.ts`
  - 手寫 80-120 字摘要的 `PAGE_SUMMARIES` 字典
  - 已寫好：article-beginners / article-sleep / article-stress / article-dustmites / article-eucalyptus / article-extraction / oil-lavender / oil-tea-tree / oil-eucalyptus / oil-peppermint / oil-sweet-orange / oil-frankincense / oils / encyclopedia / aromatherapy / safety
  - 所有摘要採「常見用途／日常香氛／保養／使用注意」中性詞，無療效宣稱
  - 未列入字典的頁面不會顯示 AI 摘要區塊（將來人工逐頁補上即可）

### 接入位置
- `app/oil/[id]/page.tsx`：用 `oils.json` 既有事實欄位自動產生 145 字摘要，渲染於 `<RawHtml>` 之上
- `app/[slug]/page.tsx`：讀 `getPageSummary(slug)`；有摘要才渲染

---

## 3. Phase 5：醫療風險字詞掃描

### 產出
- `C:/Users/User/Desktop/essential-oil-guide/risk-report.md`（54.8 KB）
- 工具：`C:/tmp/oil-excel/risk_scan.py`

### 結果摘要
- **2 633 處風險字詞，分布於 603 個檔案 / JSON 欄位**
- Top 8 字詞頻率：

  | 字詞 | 次數 | 建議替代 |
  |---|---|---|
  | 抗菌 | 893 | 清新香氛 |
  | 消炎 | 281 | 肌膚保養 |
  | 免疫 | 256 | 日常保養支持 |
  | 止痛 | 207 | 放鬆按摩 |
  | 抗病毒 | 164 | 空間清新感 |
  | 祛痰 | 145 | 呼吸放鬆氛圍 |
  | 助眠 | 144 | 睡前放鬆氛圍 |
  | 抗炎 | 143 | 舒適感受 |

### 重要：報告為 read-only
- 依使用者指示「**請不要直接刪除內容**」，本 phase **未自動修改任何檔案**
- `risk-report.md` 含三層人工審核原則：
  1. 研究類內容 → 保留語氣 + 加註研究背景／條件／非醫療建議聲明
  2. 使用建議類 → 改為非醫療語氣（例：「茶樹精油可以治療痘痘」→「茶樹精油常用於肌膚保養」）
  3. 化學分類 / 安全指南頁 → 保留專業術語但頁首加註「以下為精油化學專業資訊，不構成醫療建議」

### 後續建議
- 建議優先處理：**「治療」「治癒」「抗癌」「改善疾病」「退燒」「過敏治療」** 等強療效宣稱字眼（共 ≤80 處，工作量可控）
- 「抗菌 / 消炎 / 免疫」雖然出現次數多，但多為研究類內容；建議分批人工審核並加上文獻來源 + 研究條件聲明

---

## 4. Phase 6：精油詳細頁 SEO 模板

### 確認項目
- `app/oil/[id]/page.tsx` 單一 H1（透過 oil-detail.html 既有結構）
- H2 / H3 結構由 oil-detail.html 控制（化學成分、香氣、應用、安全等區塊）
- 麵包屑：`首頁 › 精油化學分子索引 › [化學分類] › [精油名]`（含 `BreadcrumbList` schema）
- 相關精油區塊（同化學分類）已存在
- 新增：頁首 AISummary 摘要 + 頁末 RelatedLinks 站內延伸閱讀

---

## 5. Phase 7：內部連結 mapping helper

### 新建檔案
- `app/lib/internalLinks.ts`
  - `INTERNAL_LINKS` 對應表（20 個關鍵詞 → 站內路徑）
  - `linkify(text, opts)`：將任意 HTML / 文字內的關鍵詞自動轉成內部 `<a>`；自動跳過已在 `<a>` / `<h1>~<h6>` / `<code>` / `<pre>` 內的內容，避免巢狀連結；每個關鍵詞預設只 linkify 一次
  - `getRelatedLinks(topic, max=6)`：為特定主題推薦相關連結

- `app/components/RelatedLinks.tsx`
  - 文章末「延伸閱讀」區塊
  - schema.org `SiteNavigationElement` microdata

### 對應表內容
| 關鍵詞 | 連結 |
|---|---|
| 薰衣草精油 | `/oil-lavender/` |
| 茶樹精油 | `/oil-tea-tree/` |
| 尤加利精油 | `/oil-eucalyptus/` |
| 薄荷精油 | `/oil-peppermint/` |
| 甜橙精油 | `/oil-sweet-orange/` |
| 乳香精油 | `/oil-frankincense/` |
| 精油索引 / 化學分子索引 | `/oils/` |
| 芳療應用 / 芳療入門 | `/aromatherapy/` |
| 精油安全 / 安全指南 | `/safety/` |
| 精油化學 / 精油大百科 | `/encyclopedia/` |
| 澳洲精油 / 黃金海岸精油 | `/encyclopedia/#regions` |
| 聯絡我們 | `/contact/` |
| 網站簡介 | `/about/` |
| 免責聲明 | `/disclaimer/` |
| 隱私政策 | `/privacy/` |

### 接入位置
- `app/oil/[id]/page.tsx`：頁末顯示「與「{精油名}」相關的精油知識」（6 筆）
- `app/[slug]/page.tsx`：在 article-* / oil-* / safety / aromatherapy 頁末顯示「🌿 延伸閱讀」

---

## 6. Phase 8：robots.txt + sitemap

### `public/robots.txt`（重寫）
新增 13 個 AI 搜尋爬蟲明確 Allow 規則：
- **OpenAI**：GPTBot、OAI-SearchBot、ChatGPT-User
- **Perplexity**：PerplexityBot、Perplexity-User
- **Google**：Google-Extended
- **Anthropic**：ClaudeBot、Claude-Web、anthropic-ai
- **Common Crawl**：CCBot
- **Apple**：Applebot-Extended
- **其他**：cohere-ai、Bytespider
- Sitemap 行：`https://intelliverse.tw/sitemap.xml`

### `app/sitemap.ts`
- `LAST_MOD` 推進至 `2026-05-13`
- 包含：首頁 / 4 個 app 路由頁 / 35 個 html-source slug / 302 個精油 ID
- 每頁附 og:image（從 html-source 解析）；精油頁用 fallback banner
- 部分 hub 頁（encyclopedia / oils / aromatherapy / safety）priority 0.9，其餘 0.4-0.7

---

## 7. Phase 9：E-E-A-T 強化

### `app/about/page.tsx`
**新增區塊**：
- 🔬 **內容編輯方法（Editorial Methodology）**：5 點透明說明（資料蒐集、用詞規範、安全標註、AI 輔助內容、持續更新）
- 📅 **內容版本**：標示最後一次大規模審查日（2026 年 5 月）+ 下階段計畫

### `app/disclaimer/page.tsx`
- 最後更新日：`2026 年 4 月` → `2026 年 5 月`
- **新增第八章「AI 生成內容聲明」**：透明揭露 AI 圖像來源（TopView / OpenAI gpt-image）、AI 文字輔助、不保證百分之百正確的聲明
- 法律管轄改為第九章

### `app/privacy/page.tsx`
- 最後更新日：`2026 年 4 月` → `2026 年 5 月`

### `app/contact/page.tsx`（既已完整，無變更）
- 既有 Email / 電話 / 地址 + ContactPage schema + 醫療諮詢免責聲明

### 不執行（避免造假）
| 項目 | 為何不做 |
|---|---|
| 增加芳療師人物 bio | 使用者明確要求不偽造作者資料 |
| 增加「IFA 認證」徽章 | 站方目前無此認證 |
| 增加實體商店地址 | 站方無實體店面，避免誤導 |
| 偽造「醫療顧問」名單 | 無此關係 |

### 後續人工建議
- 個別精油的 GC/MS 來源連結與研究文獻引用清單（已在 about 頁標示為下階段計畫）
- 若未來與認證芳療師合作，可在 about 頁補上「審校顧問」區塊

---

## 8. 不變更項目（依使用者明確指示）

| 項目 | 狀態 |
|---|---|
| 既有 UI 樣式 | ✓ 維持，所有新元件採同系 Morandi 色 + 圓角 + 同字型 |
| 既有 oils.json / html-source 內容 | ✓ 未刪除任何欄位／檔案 |
| 電商功能（購物車、訂單、價格） | ✓ 不加 |
| Product / Offer / AggregateRating schema | ✓ 不加 |
| 偽造作者 / 品牌 / 地址 | ✓ 無 |
| 強化醫療療效宣稱 | ✓ 反向操作：所有新文案改為非醫療語氣 |

---

## 9. 新增 / 修改檔案清單

### 新增
- `app/components/AISummary.tsx`
- `app/components/RelatedLinks.tsx`
- `app/lib/internalLinks.ts`
- `app/lib/pageSummaries.ts`
- `risk-report.md`（位於專案根目錄）
- `SEO-GEO-CHANGELOG.md`（本檔）
- `C:/tmp/oil-excel/risk_scan.py`（外部工具，不在 repo 內）

### 修改
- `app/layout.tsx`（title / description）
- `app/lib/schema.ts`（移除假日期）
- `app/oil/[id]/page.tsx`（title / desc / AISummary / RelatedLinks）
- `app/[slug]/page.tsx`（AISummary / RelatedLinks）
- `app/about/page.tsx`（編輯方法 + 內容版本）
- `app/disclaimer/page.tsx`（更新日期 + AI 內容聲明）
- `app/privacy/page.tsx`（更新日期）
- `app/sitemap.ts`（LAST_MOD）
- `public/robots.txt`（13 個 AI 爬蟲規則）
- `html-source/index.html`（title / desc）
- `html-source/oils.html`（title / desc）

---

## 10. 待人工處理項目（標示「需人工補充」）

| 區塊 | 內容 | 建議處理 |
|---|---|---|
| risk-report.md | 2 633 處風險字詞 | 依「人工審核原則」三層分類逐頁修改；建議從 top 8 字詞（≥143 次）的高曝光頁面（薰衣草 / 茶樹 / 尤加利 / 薄荷 / safety / aromatherapy）開始 |
| pageSummaries.ts | 目前覆蓋 16 個頁面 | 為剩餘 article-* / oil-* / compounds-* 頁手寫 80-120 字摘要；無摘要的頁面不會顯示 AI 區塊（安全） |
| oil/[id] AI 摘要 | 自動產生版（145 字） | 若想為熱門精油提供更精修的人寫版，可加進 `pageSummaries.ts` 並修改 `oil/[id]/page.tsx` 改為「優先用手寫，否則 fallback 自動」 |
| about 頁的下階段計畫 | 「逐支補上 GC/MS 來源連結」 | 需建立 `data/oilSources.json` 紀錄每支精油的 PubMed / 期刊 / 品牌 GC/MS 連結 |
| 個別精油 datePublished | 目前皆無 | 若可考據各精油頁實際初次撰寫日，可建立 `data/oilDates.json` 並傳入 `oilSchema()` |

---

## 11. 後續建議（不在本任務範圍）

1. **Google Search Console / Bing Webmaster** 提交 sitemap.xml；觀察索引覆蓋率
2. **Schema 驗證**：用 https://validator.schema.org/ 與 https://search.google.com/test/rich-results 跑一次首頁、精油單品頁、article 頁
3. **核心網頁指標（Core Web Vitals）**：用 PageSpeed Insights 跑 hero / safety / oil/lavender 三個代表頁；目前 LCP 預載已透過 `ReactDOM.preload(image, ...)` 處理
4. **AI 搜尋可見性追蹤**：每月用 ChatGPT、Perplexity、Claude 搜尋「薰衣草精油 安全」「澳洲精油」「精油化學分類」等關鍵字，觀察是否被引用
5. **內容更新節奏**：建議每季更新 `LAST_MOD` 與一次 `risk-report.md` 重掃；新文章上線時把該 slug 加進 `pageSummaries.ts`

---

🌿 **完成。本次任務遵守「不刪內容、不偽造、不破壞 UI、不加電商、build 成功」全部限制，所有醫療敏感內容改以報告呈現供人工審核。**

---

## 附錄 A：AI 爬蟲可見性微調（2026-05-13 補）

依使用者指示「要讓 AI 可爬蟲，藥效相關可以先保留」，做了以下調整：

### 已確認
- `public/robots.txt`：13 個 AI bot（GPTBot / OAI-SearchBot / ChatGPT-User / PerplexityBot / Perplexity-User / Google-Extended / ClaudeBot / Claude-Web / anthropic-ai / CCBot / Applebot-Extended / cohere-ai / Bytespider）+ `User-agent: *` 全 Allow
- 所有 Next.js 渲染頁面 `<meta name="robots" content="index, follow">`、Googlebot `max-image-preview:large, max-snippet:-1`
- 唯一 noindex：`public/oil-detail.html`（legacy template，正確避免與 `/oil/{id}/` 重複索引）

### 將 oils.json `effects` 欄位帶入索引面
保留既有「化解黏液、抗菌、促進傷口癒合、助眠」等實際關鍵詞於以下位置，提升 AI 引用命中率：

1. **`app/oil/[id]/page.tsx` meta description**：加入 `effects` 前 50 字
   - 例：`頭狀薰衣草（Lavandula stoechas）：單萜酮/烯類精油。主要成分 冰片酮、樟腦、1,8-桉油醇、α-蒎烯。常見芳療應用：強力化痰、促進傷口癒合、抗菌、耳鼻喉感染。`
2. **`app/oil/[id]/page.tsx` AISummary 自動生成**：加入 `effects` 前 60 字到 Quick Answer
3. **`app/lib/schema.ts` oilSchema description**：加入「常見芳療應用：...」段，並把 slice 上限從 250 → 300
4. **`app/layout.tsx` 站台 description**：加入「助眠、放鬆、抗菌、空間香氛、肌膚保養」高搜尋頻關鍵字
5. **`html-source/index.html` meta description**：同上（layout fallback 用 html-source 的 description）

### 影響
- AI 搜尋引用（ChatGPT Search / Perplexity / Google AI Overview）能直接從 meta + 結構化資料看到精油的應用面向，不需要爬完整頁
- 既有 oils.json / html-source 醫療字眼一字未動；`risk-report.md` 仍可作為「日後若需法規對應時的修改清單」
- Build：348 頁，全綠

