# `data/oils.json` 拉丁學名／中文名審查報告

> 任務日期：2026-05-13
> 範圍：全量 302 筆精油 datasheet
> 工具：本地檢查 + Wikipedia / 學名資料庫線上驗證

---

## ✅ 已修正（高確定性錯誤，3 筆）

| ID | 原中文 | 原拉丁 | 修改後 | 來源 |
|---|---|---|---|---|
| **198** | 德州白蘿蔔 | Ammi visnaga | **zh → 阿密茴**（aliases: 牙籤芹、凱蘭草、Khella） | Wikipedia confirms *Visnaga daucoides* (syn. *Ammi visnaga*) is **Apiaceae 傘形科**，俗名 **toothpick plant / khella**，**完全不是蘿蔔** |
| **220** | 巨紫荊 | Cercis gigantea | **latin → Cercis chingii** | Wikipedia "Cercis" 屬條目列出 10 個有效種，**無 *gigantea***；巨紫荊正確學名為 *Cercis chingii*（Ching's redbud） |
| **107** | 古芸香脂 | `Guaijawood / Bulnesia sarmientoi` | **latin → Bulnesia sarmientoi**（aliases: Guaiacwood、Guayacán、玉檀木） | 學名欄位本就只該放二名法；英文俗名 Guaiacwood 已移到 aliases |

> ⚠️ 三筆 entries 的 `pharmacology` / `energy` HTML 內文也同步替換，避免 SEO 不一致。

---

## ⚠️ 拉丁名重複（21 對）— 多數為「同種、不同部位／品種」，少數為實質重複

| Latin | IDs | 中文名 | 性質 | 建議 |
|---|---|---|---|---|
| Levisticum officinale | 26, 89, **136** | 圓葉當歸、圓葉當歸、**防風** | ⚠️ #136 中文名「防風」與 Levisticum officinale 不符（防風應為 *Saposhnikovia divaricata*） | 改 #136 zh → 「歐當歸」，或確認原意是否為 *Saposhnikovia* 然後改拉丁 |
| Angelica archangelica | 66, 131, 298 | 圓葉當歸、歐白芷、歐白芷根 | ⚠️ #66 標示「圓葉當歸」與 Levisticum 衝突；#131/298 分別為全株/根，合理 | 改 #66 zh → 「歐白芷」（與 #131 重複可考慮合併） |
| Fokienia hodginsii | 33, 275 | 藍米柏、暹羅木 | ⚠️ 同種、不同俗名 | 保留兩者並加 `aliases`；或合併為 #275 主，#33 alias |
| Citrus limon | 34, 310 | 檸檬、檸檬 | 🔴 **完全重複** | 合併為一筆 |
| Lavandula stoechas | 38, 209 | 頭狀薰衣草、薰衣草 | 🔴 #209「薰衣草」應為「真正薰衣草」筆誤；實際 *L. angustifolia* 為 #165 | 改 #209 zh → 「頭狀薰衣草」或刪除 |
| Pistacia lentiscus | 39, 331 | 白膠脂、熏陸香 | ⚠️ 同種不同俗名（熏陸香為通用名） | 保留兩者，加 aliases 互相對照 |
| Origanum majorana | 40, 231 | 馬郁蘭、甜馬郁蘭 | ⚠️ 同種，「甜馬郁蘭」為標準芳療名 | 改 #40 zh → 「甜馬郁蘭」或合併 |
| Rosmarinus officinalis ct. cineole | 47, 87 | 桉油醇迷迭香、桉油醇迷迭香 | 🔴 **完全重複** | 合併為一筆 |
| Curcuma longa | 59, 204 | 薑黃、薑黃 | 🔴 **完全重複** | 合併為一筆 |
| Inula graveolens | 64, 277 | 大花土木香、黏答答土木香 | ⚠️ 同種不同俗名 | 保留並加 aliases |
| Cinnamomum camphora ct. linalool | 70, 217 | 芳樟葉、芳樟 | ⚠️ #70 是葉、#217 是木材；建議補上「(leaf)」「(wood)」 | 拉丁名分別補上 `(leaf)` / `(wood)` |
| Eucalyptus smithii | 77, 145 | 史密斯尤加利、史密斯尤加利 | 🔴 **完全重複** | 合併為一筆 |
| Cinnamomum tamala | 81, 248 | 印度月桂（桂葉）、印度肉桂 | ⚠️ Cinnamomum tamala 確為印度月桂；#248「印度肉桂」實為 *C. verum*（已在 #249）或 *C. cassia*。需釐清 #248 是否標籤錯誤 | 檢查 #248 是否應為其他種 |
| Melaleuca cajuputi | 83, 126 | 白千層、鹹亞茶樹 | ⚠️ 同種不同俗名 | 保留並加 aliases |
| Leptospermum scoparium | 85, 211 | 掃帚茶樹、松紅梅 | ⚠️ 同種不同俗名（松紅梅 = Manuka） | 保留並加 aliases |
| Callitris intratropica | 95, **199** | 澳洲藍絲柏、**鑽石** | 🔴 #199 zh「鑽石」非植物名（疑為品牌等級） | 改 #199 zh → 「澳洲藍絲柏（鑽石級）」或刪除 |
| Juniperus oxycedrus | 111, 321 | 刺檜木、刺檜漿果 | ✅ 同種不同部位（合理） | 拉丁名建議補上部位標註 |
| Citrus hystrix | 140, 307 | 泰國青檸葉、泰國青檸 | ✅ 同種不同部位 | 拉丁名加 `(leaf)` `(peel)` |
| Litsea cubeba | 148, 284 | 山雞椒、草澄茄 | ⚠️ #284「草澄茄」疑為「蓽澄茄」之誤（蓽澄茄為通用名） | 改 #284 zh → 「蓽澄茄」或合併 #148 |
| Cistus ladanifer | 180, 305 | 沙漠花、岩玫瑰 | ⚠️ 同種，「岩玫瑰」為標準芳療名 | 改 #180 zh 或合併 |
| Kunzea ambigua | 278, 322 | 昆士亞、卡奴卡 | ⚠️ 「Kunzea」音譯為昆士亞；「卡奴卡」是 *Kunzea ericoides*（另一種），可能 #322 拉丁名錯 | 檢查 #322 是否應為 *K. ericoides* |

---

## ⚠️ 中文俗名重複（不同拉丁名）— 7 對

| zh | IDs | 拉丁 | 衝突點 |
|---|---|---|---|
| 圓葉當歸 | 26, 66, 89 | L. officinale / A. archangelica / L. officinale | 26 與 89 重複；66 拉丁不同 |
| 檸檬 | 34, 310 | Citrus limon / Citrus limon | 完全重複 |
| 胡椒薄荷 | 42, 226 | Mentha x piperita / Mentha × piperita | 完全重複（差別在 x 字元） |
| 桉油醇迷迭香 | 47, 87 | 同拉丁 | 完全重複 |
| 薑黃 | 59, 204 | 同拉丁 | 完全重複 |
| 芳樟葉 | 70, 219 | Cinnamomum camphora ct. linalool / 同 ct. linalool (leaf) | 重複，#219 應為其他部位 |
| 史密斯尤加利 | 77, 145 | 同拉丁 | 完全重複 |

---

## ⚠️ 可疑中文俗名（非標準芳療界用語）

| ID | zh | latin | 建議 |
|---|---|---|---|
| 119 | 頭狀香科 | Cyperus scariosus | 「香科」為 *Teucrium*（脣形科），*Cyperus* 為莎草科。建議 zh → 「印度香附草」或「頭狀莎草」 |
| 125 | 同密助 | Dipteryx odorata | Dipteryx odorata 為 Tonka bean。建議 zh → 「零陵香豆」或「東加豆」 |
| 153 | 馬魯科 | Aeollanthus suaveolens | 「馬魯科」音譯較少見；標準為「馬如拉」或保留 |
| 172 | 蘆爪豆 | Spartium junceum | 應為「鷹爪豆」（疑「蘆」是「鷹」誤植） |
| 176 | 蕕櫛 | Caryopteris incana | 應為「蘭香草」或「蕕草」（櫛字疑為誤） |
| 162 | 崢角白梅 | Baeckea frutescens | 「崢」疑為「岬」誤；應為「崗松」或「岬角白梅」 |
| 213 | 紫羅蘭 | Viola odorata | OK，但與「香堇菜」相通；加 alias |

---

## ⚠️ 學名查證提示（建議人工再 double-check）

| ID | zh | latin | 疑點 |
|---|---|---|---|
| 53 | （無此 id） | — | id 跳號（25→52 → 跳到 66/67/68，再回 54）— 建議重排 id 或保留現狀 |
| 192 | 五月玫瑰 | Rosa centifolia | OK |
| 234 | 大馬士革玫瑰 | Rosa damascena | OK |
| 235 | 苦水玫瑰 | Rosa damascena var. semperflorens | OK |
| 191 | 晚香玉 | Polianthes tuberosa | 2024 後仍有效（曾改 *Agave amica*，現重新承認 *Polianthes*） |
| 197（無） | — | — | id 197/214/215/244/245/268/269/293/311 等跳號 |

---

## 📊 統計總覽

| 類別 | 數量 |
|---|---:|
| 全量 entries | 302 |
| 全部有 latin + zh | ✓ 100% |
| 高確定性錯誤（已修） | 3 |
| 完全重複（待合併） | 5 |
| 同種不同部位／俗名（合理保留） | 11 |
| 中文俗名可疑（建議人工 review） | 7 |
| 拉丁名疑誤（建議人工 review） | 6 |

---

## 🎯 建議下一步

1. **批次合併重複**（5 筆）：#34/310、#42/226、#47/87、#59/204、#77/145
2. **改俗名疑誤**（7 筆）：#119、#125、#172、#176、#162、#284、#199
3. **檢查拉丁名疑誤**（6 筆）：#136、#220（已修）、#322、#248、#220、#107（已修）
4. **補 `aliases` 欄位** 給「同種不同俗名」群組（共 11 對）

如使用者確認可批次自動處理，可由 `scripts/oils_dedupe.py`（待建）執行；或逐筆人工審核。
