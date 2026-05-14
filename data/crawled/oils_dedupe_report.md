# oils.json 全方位重複／類型一致性檢查報告（2026-05-14）

> 全量 302 支精油  
> 檢測 9 個維度：A 完全重複 / B 同種多名 / C 同名多種 / D 拼字相近 / F 成分高度重疊 / G 同屬類型衝突 / H 分類-檔案對應  

## 統計

| 維度 | 名稱 | 命中 |
|---|---|---:|
| A | 完全重複（同 zh 同 latin） | 5 |
| B | 同 latin 不同 zh（同種多名） | 28 |
| C | 同 zh 不同 latin（同名多種） | 4 |
| D | latin 拼字相近（編輯距離 1-2） | 1 |
| F | components 高度重疊（jaccard ≥ 0.7） | 3 |
| G | 同屬不同種、類型分歧 | 41 |
| H | category 與 catFile 對應不一致 | 0 |

## A. 完全重複（zh + latin 都相同）

| Latin | zh | IDs |
|---|---|---|
| Levisticum officinale | 圓葉當歸 | 26, 89 |
| Citrus limon | 檸檬 | 34, 310 |
| Rosmarinus officinalis ct. cineole | 桉油醇迷迭香 | 47, 87 |
| Curcuma longa | 薑黃 | 59, 204 |
| Eucalyptus smithii | 史密斯尤加利 | 77, 145 |

## B. 同物種、不同俗名／部位（norm latin 相同，zh 不同）

### `fokienia hodginsii`

- #33 藍米柏 | `Fokienia hodginsii`
- #275 暹羅木 | `Fokienia hodginsii`

### `citrus limon`

- #34 檸檬 | `Citrus limon`
- #141 檸檬葉 | `Citrus limon (Petitgrain)`
- #310 檸檬 | `Citrus limon`

### `hyssopus officinalis`

- #37 牛膝草 | `Hyssopus officinalis`
- #80 高地牛膝草 | `Hyssopus officinalis var. decumbens`

### `lavandula stoechas`

- #38 頭狀薰衣草 | `Lavandula stoechas`
- #209 薰衣草 | `Lavandula stoechas`

### `pistacia lentiscus`

- #39 白膠脂 | `Pistacia lentiscus`
- #331 熏陸香 | `Pistacia lentiscus`
- #332 奇歐島熏陸香 | `Pistacia lentiscus var. chia`

### `origanum majorana`

- #40 馬郁蘭 | `Origanum majorana`
- #231 甜馬郁蘭 | `Origanum majorana`

### `rosmarinus officinalis`

- #44 馬鞭草酮迷迭香 | `Rosmarinus officinalis ct. verbenone`
- #47 桉油醇迷迭香 | `Rosmarinus officinalis ct. cineole`
- #87 桉油醇迷迭香 | `Rosmarinus officinalis ct. cineole`

### `angelica archangelica`

- #66 圓葉當歸 | `Angelica archangelica`
- #131 歐白芷 | `Angelica archangelica`
- #298 歐白芷根 | `Angelica archangelica`

### `inula graveolens`

- #64 大花土木香 | `Inula graveolens`
- #277 黏答答土木香 | `Inula graveolens`

### `cinnamomum camphora`

- #70 芳樟葉 | `Cinnamomum camphora ct. linalool`
- #73 桉油醇樟 | `Cinnamomum camphora ct. cineole`
- #217 芳樟 | `Cinnamomum camphora ct. linalool`
- #219 芳樟葉 | `Cinnamomum camphora ct. linalool (leaf)`

### `cinnamomum tamala`

- #81 印度月桂（桂葉） | `Cinnamomum tamala`
- #248 印度肉桂 | `Cinnamomum tamala`

### `melaleuca cajuputi`

- #83 白千層 | `Melaleuca cajuputi`
- #126 鹹亞茶樹 | `Melaleuca cajuputi`

### `melaleuca quinquenervia`

- #84 綠花白千層 | `Melaleuca quinquenervia ct. cineole`
- #280 橙花叔醇綠花白千層 | `Melaleuca quinquenervia ct. Nerolidol`

### `leptospermum scoparium`

- #85 掃帚茶樹 | `Leptospermum scoparium`
- #211 松紅梅 | `Leptospermum scoparium`

### `myrtus communis`

- #86 香桃木 | `Myrtus communis ct. cineole`
- #169 紅香桃木 | `Myrtus communis (ct. myrtenyl acetate)`

### `callitris intratropica`

- #95 澳洲藍絲柏 | `Callitris intratropica`
- #199 澳洲藍絲柏（鑽石級） | `Callitris intratropica`

### `cananga odorata`

- #97 依蘭 | `Cananga odorata`
- #98 大葉依蘭 | `Cananga odorata var. macrophylla`

### `bulnesia sarmientoi`

- #107 古芸香脂 | `Bulnesia sarmientoi`
- #272 玉檀木 | `Bulnesia sarmientoi`

### `juniperus oxycedrus`

- #111 刺檜木 | `Juniperus oxycedrus`
- #321 刺檜漿果 | `Juniperus oxycedrus`

### `citrus hystrix`

- #140 泰國青檸葉 | `Citrus hystrix`
- #307 泰國青檸 | `Citrus hystrix`

### `litsea cubeba`

- #148 山雞椒 | `Litsea cubeba`
- #284 蓽澄茄 | `Litsea cubeba`

### `citrus aurantium`

- #159 苦橙葉 | `Citrus aurantium (leaves)`
- #218 橙花 | `Citrus aurantium (flowers)`
- #306 苦橙 | `Citrus aurantium`

### `citrus reticulata`

- #179 桔葉 | `Citrus reticulata (leaves)`
- #312 桔（紅/綠） | `Citrus reticulata`

### `cistus ladanifer`

- #180 沙漠花 | `Cistus ladanifer`
- #305 岩玫瑰 | `Cistus ladanifer`

### `myroxylon balsamum`

- #187 秘魯香脂 | `Myroxylon balsamum var. pereirae`
- #281 香脂果豆木 | `Myroxylon balsamum`

### `rosa damascena`

- #234 大馬士革玫瑰 | `Rosa damascena`
- #235 苦水玫瑰 | `Rosa damascena var. semperflorens`

### `thymus vulgaris`

- #238 沉香醇百里香 | `Thymus vulgaris ct. linalool`
- #239 側柏醇百里香 | `Thymus vulgaris ct. thujanol`
- #240 牻牛兒醇百里香 | `Thymus vulgaris ct. geraniol`
- #265 百里酚百里香 | `Thymus vulgaris ct. Thymol`

### `juniperus communis`

- #319 高地杜松 | `Juniperus communis var. montana`
- #320 杜松漿果 | `Juniperus communis`

## C. 中文同名但學名不同（zh 衝突）

### `圓葉當歸`

- #26 `Levisticum officinale`
- #66 `Angelica archangelica`
- #89 `Levisticum officinale`

### `胡椒薄荷`

- #42 `Mentha x piperita`
- #226 `Mentha × piperita`

### `芳樟葉`

- #70 `Cinnamomum camphora ct. linalool`
- #219 `Cinnamomum camphora ct. linalool (leaf)`

### `岬角白梅`

- #162 `Baeckea frutescens`
- #313 `Coleonema album / C. pulchellum`

## D. Latin 拼字相近（編輯距離 1-2）

多數為合理屬內近緣，但可檢查是否有打字錯誤。

| Latin A | Latin B | 距離 | A 條目 | B 條目 |
|---|---|---:|---|---|
| `mentha x piperita` | `mentha × piperita` | 1 | #42 胡椒薄荷 | #226 胡椒薄荷 |

## F. components 高度重疊（jaccard ≥ 0.7）

可能是：(1) 同物種不同俗名複製貼上 (2) 真正組成相似的近緣

| ID A | zh A | ID B | zh B | 共有 | Jaccard | 共有成分（前 8） |
|---|---|---|---|---:|---:|---|
| #296 | 西伯利亞冷杉 | #325 | 黑雲杉 | 5 | 1.0 | α-蒎烯, δ--蒈烯, 乙酸龍腦酯, 檸檬烯, 莰烯 |
| #319 | 高地杜松 | #320 | 杜松漿果 | 5 | 1.0 | α-蒎烯, β-蒎烯, 月桂烯, 檸檬烯, 沙賓烯 |
| #326 | 挪威雲杉 | #341 | 加拿大鐵杉 | 5 | 1.0 | α-蒎烯, β-蒎烯, 乙酸龍腦酯, 檸檬烯, 莰烯 |

## G. 同屬不同種、類型分歧

多數合理（同屬不同化學型）但可掃過確保標籤一致。

### `Artemisia` (跨 4 類)

- #25 利古里亞草 `Artemisia ligustica` → **單萜酮/烯類**
- #27 側柏酮白蒿 `Artemisia herba-alba` → **單萜酮/烯類**
- #28 艾葉 `Artemisia argyi` → **單萜酮/烯類**
- #29 艾蒿 `Artemisia vulgaris` → **單萜酮/烯類**
- #30 艾草 `Artemisia princeps` → **單萜酮/烯類**
- #94 樹艾 `Artemisia arborescens` → **倍半萜烯類**
- #123 龍艾 `Artemisia dracunculus` → **醛類**
- #200 印蒿 `Artemisia pallens` → **倍半萜酮類**

### `Levisticum` (跨 2 類)

- #26 圓葉當歸 `Levisticum officinale` → **單萜酮/烯類**
- #89 圓葉當歸 `Levisticum officinale` → **氧化物類**

### `Fokienia` (跨 2 類)

- #33 藍米柏 `Fokienia hodginsii` → **單萜酮/烯類**
- #275 暹羅木 `Fokienia hodginsii` → **倍半萜醇類**

### `Citrus` (跨 6 類)

- #34 檸檬 `Citrus limon` → **單萜酮/烯類**
- #140 泰國青檸葉 `Citrus hystrix` → **酯類**
- #141 檸檬葉 `Citrus limon (Petitgrain)` → **酯類**
- #159 苦橙葉 `Citrus aurantium (leaves)` → **脂類**
- #160 佛手柑 `Citrus bergamia` → **脂類**
- #179 桔葉 `Citrus reticulata (leaves)` → **苯基酯類**
- #218 橙花 `Citrus aurantium (flowers)` → **單萜醇類**
- #306 苦橙 `Citrus aurantium` → **單萜烯類**
- #307 泰國青檸 `Citrus hystrix` → **單萜烯類**
- #308 日本柚子 `Citrus junos` → **單萜烯類**
- #309 萊姆 `Citrus aurantiifolia` → **單萜烯類**
- #310 檸檬 `Citrus limon` → **單萜烯類**
- #311 葡萄柚 `Citrus paradisi` → **單萜烯類**
- #312 桔（紅/綠） `Citrus reticulata` → **單萜烯類**

### `Eucalyptus` (跨 4 類)

- #35 薄荷尤加利 `Eucalyptus dives ct. piperitone` → **單萜酮/烯類**
- #36 多苞葉尤加利 `Eucalyptus polybractea ct. cryptone` → **單萜酮/烯類**
- #76 藍膠尤加利 `Eucalyptus globulus` → **氧化物類**
- #77 史密斯尤加利 `Eucalyptus smithii` → **氧化物類**
- #78 澳洲尤加利 `Eucalyptus radiata` → **氧化物類**
- #145 史密斯尤加利 `Eucalyptus smithii` → **酯類**
- #151 檸檬桉粉 `Eucalyptus staigeriana` → **酯類**
- #163 玫瑰尤加利 `Eucalyptus rhodantha` → **脂類**

### `Hyssopus` (跨 2 類)

- #37 牛膝草 `Hyssopus officinalis` → **單萜酮/烯類**
- #80 高地牛膝草 `Hyssopus officinalis var. decumbens` → **氧化物類**

### `Lavandula` (跨 4 類)

- #38 頭狀薰衣草 `Lavandula stoechas` → **單萜酮/烯類**
- #82 穗花薰衣草 `Lavandula latifolia` → **氧化物類**
- #165 真正薰衣草 `Lavandula angustifolia` → **脂類**
- #166 醒目薰衣草 `Lavandula x intermedia` → **脂類**
- #209 薰衣草 `Lavandula stoechas` → **倍半萜酮類**

### `Pistacia` (跨 2 類)

- #39 白膠脂 `Pistacia lentiscus` → **單萜酮/烯類**
- #331 熏陸香 `Pistacia lentiscus` → **單萜烯類**
- #332 奇歐島熏陸香 `Pistacia lentiscus var. chia` → **單萜烯類**

### `Origanum` (跨 3 類)

- #40 馬郁蘭 `Origanum majorana` → **單萜酮/烯類**
- #231 甜馬郁蘭 `Origanum majorana` → **單萜醇類**
- #255 野馬郁蘭 `Origanum vulgare` → **酚與芳香醛類**
- #257 希臘野馬郁蘭 `Origanum heracleoticum` → **酚與芳香醛類**

### `Mentha` (跨 3 類)

- #41 綠薄荷 `Mentha spicata` → **單萜酮/烯類**
- #42 胡椒薄荷 `Mentha x piperita` → **單萜酮/烯類**
- #167 檸檬薄荷 `Mentha citrata` → **脂類**
- #226 胡椒薄荷 `Mentha × piperita` → **單萜醇類**

### `Cymbopogon` (跨 4 類)

- #43 檸檬草與香茅 `Cymbopogon citratus / C. nardus` → **單萜酮/烯類**
- #142 檸檬香茅 `Cymbopogon citratus` → **酯類**
- #143 爪哇香茅 `Cymbopogon winterianus` → **酯類**
- #222 玫瑰草 `Cymbopogon martinii` → **單萜醇類**
- #316 非洲藍香茅 `Cymbopogon validus` → **單萜烯類**

### `Rosmarinus` (跨 2 類)

- #44 馬鞭草酮迷迭香 `Rosmarinus officinalis ct. verbenone` → **單萜酮/烯類**
- #47 桉油醇迷迭香 `Rosmarinus officinalis ct. cineole` → **單萜酮/烯類**
- #87 桉油醇迷迭香 `Rosmarinus officinalis ct. cineole` → **氧化物類**

### `Salvia` (跨 5 類)

- #45 薰衣草葉鼠尾草 `Salvia lavandulifolia` → **單萜酮/烯類**
- #46 鼠尾草 `Salvia officinalis` → **單萜酮/烯類**
- #88 三葉鼠尾草 `Salvia fruticosa` → **氧化物類**
- #170 水果鼠尾草 `Salvia dorisiana` → **脂類**
- #171 快樂鼠尾草 `Salvia sclarea` → **脂類**
- #236 鳳梨鼠尾草 `Salvia elegans` → **單萜醇類**
- #286 狹長葉鼠尾草 `Salvia stenophylla` → **倍半萜醇類**

### `Tagetes` (跨 2 類)

- #48 芳香萬壽菊 `Tagetes minuta` → **單萜酮/烯類**
- #49 萬壽菊 `Tagetes erecta` → **單萜酮/烯類**
- #137 甜萬壽菊 `Tagetes lucida` → **醛類**

### `Tanacetum` (跨 2 類)

- #50 夏白菊 `Tanacetum parthenium` → **單萜酮/烯類**
- #51 艾菊 `Tanacetum vulgare` → **單萜酮/烯類**
- #118 摩洛哥藍艾菊 `Tanacetum annuum` → **倍半萜烯類**

### `Angelica` (跨 4 類)

- #66 圓葉當歸 `Angelica archangelica` → **單萜酮/烯類**
- #54 中國當歸 `Angelica sinensis` → **香豆素與內酯類**
- #55 印度當歸 `Angelica glauca` → **香豆素與內酯類**
- #131 歐白芷 `Angelica archangelica` → **醛類**
- #298 歐白芷根 `Angelica archangelica` → **單萜烯類**
- #299 白芷 `Angelica dahurica` → **單萜烯類**
- #300 獨活 `Angelica pubescens` → **單萜烯類**

### `Curcuma` (跨 2 類)

- #59 薑黃 `Curcuma longa` → **香豆素與內酯類**
- #204 薑黃 `Curcuma longa` → **倍半萜酮類**
- #205 莪朮 `Curcuma zedoaria` → **倍半萜酮類**

### `Ferula` (跨 2 類)

- #62 阿魏 `Ferula assa-foetida` → **香豆素與內酯類**
- #317 白松香 `Ferula galbaniflua` → **單萜烯類**

### `Inula` (跨 2 類)

- #63 土木香 `Inula helenium` → **香豆素與內酯類**
- #64 大花土木香 `Inula graveolens` → **香豆素與內酯類**
- #277 黏答答土木香 `Inula graveolens` → **倍半萜醇類**

### `Cinnamomum` (跨 4 類)

- #70 芳樟葉 `Cinnamomum camphora ct. linalool` → **氧化物類**
- #73 桉油醇樟 `Cinnamomum camphora ct. cineole` → **氧化物類**
- #81 印度月桂（桂葉） `Cinnamomum tamala` → **氧化物類**
- #178 蘇剛達 `Cinnamomum glaucescens` → **苯基酯類**
- #217 芳樟 `Cinnamomum camphora ct. linalool` → **單萜醇類**
- #219 芳樟葉 `Cinnamomum camphora ct. linalool (leaf)` → **單萜醇類**
- #246 中國肉桂 `Cinnamomum cassia` → **酚與芳香醛類**
- #247 台灣土肉桂 `Cinnamomum osmophloeum` → **酚與芳香醛類**
- #248 印度肉桂 `Cinnamomum tamala` → **酚與芳香醛類**
- #249 錫蘭肉桂 `Cinnamomum verum` → **酚與芳香醛類**

### `Alpinia` (跨 2 類)

- #71 小高良薑 `Alpinia officinarum` → **氧化物類**
- #175 大高良薑 `Alpinia galanga` → **苯基酯類**

### `Melaleuca` (跨 5 類)

- #74 妙嘉白千層 `Melaleuca viridiflora` → **氧化物類**
- #83 白千層 `Melaleuca cajuputi` → **氧化物類**
- #84 綠花白千層 `Melaleuca quinquenervia ct. cineole` → **氧化物類**
- #125 金合歡茶樹 `Melaleuca decora` → **醛類**
- #126 鹹亞茶樹 `Melaleuca cajuputi` → **醛類**
- #149 蜂蜜香桃木 `Melaleuca teretifolia` → **酯類**
- #224 茶樹 `Melaleuca alternifolia` → **單萜醇類**
- #225 沼澤茶樹 `Melaleuca ericifolia` → **單萜醇類**
- #280 橙花叔醇綠花白千層 `Melaleuca quinquenervia ct. Nerolidol` → **倍半萜醇類**

### `Helichrysum` (跨 2 類)

- #79 露兜永久花 `Helichrysum gymnocephalum` → **氧化物類**
- #207 義大利永久花 `Helichrysum italicum` → **倍半萜酮類**

### `Leptospermum` (跨 3 類)

- #85 掃帚茶樹 `Leptospermum scoparium` → **氧化物類**
- #146 檸檬細籽 `Leptospermum petersonii` → **酯類**
- #211 松紅梅 `Leptospermum scoparium` → **倍半萜酮類**

### `Myrtus` (跨 2 類)

- #86 香桃木 `Myrtus communis ct. cineole` → **氧化物類**
- #169 紅香桃木 `Myrtus communis (ct. myrtenyl acetate)` → **脂類**

### `Thymus` (跨 3 類)

- #90 鳳梨香百里香 `Thymus mastichina` → **氧化物類**
- #237 龍腦百里香 `Thymus satureioides` → **單萜醇類**
- #238 沉香醇百里香 `Thymus vulgaris ct. linalool` → **單萜醇類**
- #239 側柏醇百里香 `Thymus vulgaris ct. thujanol` → **單萜醇類**
- #240 牻牛兒醇百里香 `Thymus vulgaris ct. geraniol` → **單萜醇類**
- #265 百里酚百里香 `Thymus vulgaris ct. Thymol` → **酚與芳香醛類**
- #266 野地百里香 `Thymus serpyllum` → **酚與芳香醛類**

### `Callitris` (跨 2 類)

- #95 澳洲藍絲柏 `Callitris intratropica` → **倍半萜烯類**
- #199 澳洲藍絲柏（鑽石級） `Callitris intratropica` → **倍半萜酮類**

### `Bulnesia` (跨 2 類)

- #107 古芸香脂 `Bulnesia sarmientoi` → **倍半萜烯類**
- #272 玉檀木 `Bulnesia sarmientoi` → **倍半萜醇類**

### `Juniperus` (跨 2 類)

- #111 刺檜木 `Juniperus oxycedrus` → **倍半萜烯類**
- #112 維吉尼亞雪松 `Juniperus virginiana` → **倍半萜烯類**
- #319 高地杜松 `Juniperus communis var. montana` → **單萜烯類**
- #320 杜松漿果 `Juniperus communis` → **單萜烯類**
- #321 刺檜漿果 `Juniperus oxycedrus` → **單萜烯類**

### `Cyperus` (跨 2 類)

- #119 印度香附草 `Cyperus scariosus` → **倍半萜烯類**
- #206 莎草 `Cyperus rotundus` → **倍半萜酮類**
