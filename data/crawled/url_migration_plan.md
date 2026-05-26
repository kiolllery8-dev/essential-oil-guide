# URL 語意化遷移計畫

共 **48 個 URL** 需要 301 redirect 從 `/oil/N/` 收編到 `/oil-X/`

## 對照表

| ID | 中文名 | 舊 URL | → | 新 URL |
|----|--------|--------|---|--------|
| 34 | 檸檬 | `/oil/34/` | → | `/oil-lemon/` |
| 41 | 綠薄荷 | `/oil/41/` | → | `/oil-spearmint/` |
| 42 | 胡椒薄荷 | `/oil/42/` | → | `/oil-peppermint/` |
| 47 | 桉油醇迷迭香 | `/oil/47/` | → | `/oil-rosemary/` |
| 72 | 月桂 | `/oil/72/` | → | `/oil-bay/` |
| 73 | 桉油醇樟 | `/oil/73/` | → | `/oil-ravintsara/` |
| 76 | 藍膠尤加利 | `/oil/76/` | → | `/oil-eucalyptus/` |
| 82 | 穗花薰衣草 | `/oil/82/` | → | `/oil-spike-lavender/` |
| 87 | 桉油醇迷迭香 | `/oil/87/` | → | `/oil-rosemary/` |
| 92 | 西洋蓍草 | `/oil/92/` | → | `/oil-yarrow/` |
| 97 | 依蘭 | `/oil/97/` | → | `/oil-ylang-ylang/` |
| 102 | 沒藥 | `/oil/102/` | → | `/oil-myrrh/` |
| 108 | 德國洋甘菊 | `/oil/108/` | → | `/oil-german-chamomile/` |
| 120 | 薑 | `/oil/120/` | → | `/oil-ginger/` |
| 124 | 茴香 | `/oil/124/` | → | `/oil-sweet-fennel/` |
| 143 | 爪哇香茅 | `/oil/143/` | → | `/oil-citronella/` |
| 144 | 檸檬尤加利 | `/oil/144/` | → | `/oil-lemon-eucalyptus/` |
| 150 | 香蜂草 | `/oil/150/` | → | `/oil-melissa/` |
| 157 | 羅馬洋甘菊 | `/oil/157/` | → | `/oil-roman-chamomile/` |
| 159 | 苦橙葉 | `/oil/159/` | → | `/oil-petitgrain/` |
| 160 | 佛手柑 | `/oil/160/` | → | `/oil-bergamot/` |
| 165 | 真正薰衣草 | `/oil/165/` | → | `/oil-lavender/` |
| 166 | 醒目薰衣草 | `/oil/166/` | → | `/oil-lavandin/` |
| 171 | 快樂鼠尾草 | `/oil/171/` | → | `/oil-clary-sage/` |
| 182 | 大花茉莉 | `/oil/182/` | → | `/oil-jasmine/` |
| 192 | 五月玫瑰 | `/oil/192/` | → | `/oil-rose/` |
| 201 | 大西洋雪松 | `/oil/201/` | → | `/oil-cedarwood/` |
| 207 | 義大利永久花 | `/oil/207/` | → | `/oil-helichrysum/` |
| 209 | 薰衣草 | `/oil/209/` | → | `/oil-lavender/` |
| 218 | 橙花 | `/oil/218/` | → | `/oil-neroli/` |
| 222 | 玫瑰草 | `/oil/222/` | → | `/oil-palmarosa/` |
| 224 | 茶樹 | `/oil/224/` | → | `/oil-tea-tree/` |
| 226 | 胡椒薄荷 | `/oil/226/` | → | `/oil-peppermint/` |
| 230 | 甜羅勒 | `/oil/230/` | → | `/oil-sweet-basil/` |
| 233 | 天竺葵 | `/oil/233/` | → | `/oil-geranium/` |
| 234 | 大馬士革玫瑰 | `/oil/234/` | → | `/oil-rose/` |
| 238 | 沉香醇百里香 | `/oil/238/` | → | `/oil-thyme/` |
| 252 | 丁香花苞 | `/oil/252/` | → | `/oil-clove/` |
| 285 | 廣藿香 | `/oil/285/` | → | `/oil-patchouli/` |
| 287 | 檀香 | `/oil/287/` | → | `/oil-sandalwood/` |
| 292 | 岩蘭草 | `/oil/292/` | → | `/oil-vetiver/` |
| 301 | 乳香 | `/oil/301/` | → | `/oil-frankincense/` |
| 310 | 檸檬 | `/oil/310/` | → | `/oil-lemon/` |
| 311 | 葡萄柚 | `/oil/311/` | → | `/oil-grapefruit/` |
| 315 | 絲柏 | `/oil/315/` | → | `/oil-cypress/` |
| 320 | 杜松漿果 | `/oil/320/` | → | `/oil-juniper/` |
| 325 | 黑雲杉 | `/oil/325/` | → | `/oil-black-spruce/` |
| 330 | 黑胡椒 | `/oil/330/` | → | `/oil-black-pepper/` |

## 部署方式（擇一）

### 方法 A：Cloudflare Bulk Redirects（推薦）
1. 登入 Cloudflare Dashboard
2. 進入 `intelliverse.tw` zone
3. **Rules** → **URL Forwarding** → **Bulk Redirects**
4. Create new list，上傳 `data/crawled/cloudflare_bulk_redirects.json`
5. 啟用 list

### 方法 B：Nginx (備用)
把 `nginx_redirects.conf` 內容貼到 server 區塊內，重啟 nginx

### 方法 C：Apache (備用)
把 `htaccess_redirects.conf` 內容貼到網站根目錄 `.htaccess`

## 為什麼只遷移這 48 個

oils.json 共 302 個精油 datasheet，但只有 48 個有對應的完整指南頁面（`/oil-X/`）。
其餘 ~256 個 datasheet 為獨特物種（非重複內容），保留 `/oil/N/` 不需 redirect。
已透過 `app/oil/[id]/page.tsx` 的 `CANONICAL_OVERRIDES` map 處理 canonical 標籤。