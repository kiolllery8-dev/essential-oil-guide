# oils.json 全量驗證報告（Wikipedia + SearxNG + crawl4ai）

> 驗證日期：2026-05-14  
> 工具：Wikipedia API + SearxNG `http://192.168.1.236:8080` + crawl4ai `http://192.168.1.236:11235`  

## 統計

- 已驗證精油：**303**
- ✅ 拉丁學名存在於 Wikipedia 或權威來源：**274** (90%)
- Family ✓ 131 / ⚠️ 4 / ❓ 168
- Category ✓ 164 / ⚠️ 114 / ❓ 25

## ❌ 找不到 Wikipedia 或權威來源（29 支，建議人工查證）

| ID | 中文 | Latin | Wikipedia fuzzy 建議 | 備註 |
|---|---|---|---|---|
| 25 | 利古里亞草 | Artemisia ligustica | — |  |
| 25 | 利古里亞草 | Artemisia ligustica | — |  |
| 35 | 薄荷尤加利 | Eucalyptus dives ct. piperitone | — |  |
| 43 | 檸檬草與香茅 | Cymbopogon citratus / C. nardus | — | skip: latin slash/empty: 'Cymbopogon citratus / C. |
| 44 | 馬鞭草酮迷迭香 | Rosmarinus officinalis ct. verbenone | — |  |
| 47 | 桉油醇迷迭香 | Rosmarinus officinalis ct. cineole | — |  |
| 73 | 桉油醇樟 | Cinnamomum camphora ct. cineole | — |  |
| 84 | 綠花白千層 | Melaleuca quinquenervia ct. cineole | — |  |
| 87 | 桉油醇迷迭香 | Rosmarinus officinalis ct. cineole | — |  |
| 129 | 熱帶羅勒 | Ocimum basilicum ct. methyl chavicol | — |  |
| 135 | 洋茴香蘿文莎葉 | Ravensara anisata | — |  |
| 141 | 檸檬葉 | Citrus limon (Petitgrain) | — |  |
| 179 | 桔葉 | Citrus reticulata (leaves) | — |  |
| 218 | 橙花 | Citrus aurantium (flowers) | — |  |
| 219 | 芳樟葉 | Cinnamomum camphora ct. linalool (leaf) | — |  |
| 230 | 甜羅勒 | Ocimum basilicum ct. linalool | — |  |
| 233 | 天竺葵 | Pelargonium × asperum | — |  |
| 235 | 苦水玫瑰 | Rosa damascena var. semperflorens | — |  |
| 238 | 沉香醇百里香 | Thymus vulgaris ct. linalool | — |  |
| 239 | 側柏醇百里香 | Thymus vulgaris ct. thujanol | — |  |
| 240 | 牻牛兒醇百里香 | Thymus vulgaris ct. geraniol | — |  |
| 257 | 希臘野馬郁蘭 | Origanum heracleoticum | — |  |
| 261 | 重味過江藤 | Lippia origanoides | — |  |
| 265 | 百里酚百里香 | Thymus vulgaris ct. Thymol | — |  |
| 280 | 橙花叔醇綠花白千層 | Melaleuca quinquenervia ct. Nerolidol | — |  |
| 301 | 乳香 | Boswellia sacra / B. carterii | — | skip: latin slash/empty: 'Boswellia sacra / B. car |
| 313 | 岬角白梅 | Coleonema album / C. pulchellum | — | skip: latin slash/empty: 'Coleonema album / C. pul |
| 319 | 高地杜松 | Juniperus communis var. montana | — |  |
| 337 | 馬達加斯加鹽膚木 | Rhus taratana | — |  |

## ⚠️ Family 不一致（4 支）

| ID | 中文 | Latin | intelliverse | Wikipedia |
|---|---|---|---|---|
| 93 | 樹蘭 | Aglaia odorata | 楝科 | Meliaceae |
| 122 | 菖蒲 | Acorus calamus | 天南星科 (Araceae) | Acoraceae |
| 212 | 桂花 | Osmanthus fragrans | 木樨科 | Oleaceae |
| 290 | 纈草 | Valeriana officinalis | 敗醬科 Valerianaceae | Caprifoliaceae |

## ⚠️ Category 與 components 反推不符（114 支）

| ID | 中文 | components 第一個成分對應 | 標示 category |
|---|---|---|---|
| 34 | 檸檬 | 單萜烯類 | 單萜酮/烯類 |
| 36 | 多苞葉尤加利 | 單萜烯類 | 單萜酮/烯類 |
| 37 | 牛膝草 | 單萜烯類 | 單萜酮/烯類 |
| 38 | 頭狀薰衣草 | 單萜醇類 | 單萜酮/烯類 |
| 39 | 白膠脂 | 單萜烯類 | 單萜酮/烯類 |
| 40 | 馬郁蘭 | 單萜醇類 | 單萜酮/烯類 |
| 42 | 胡椒薄荷 | 單萜醇類 | 單萜酮/烯類 |
| 44 | 馬鞭草酮迷迭香 | 單萜烯類 | 單萜酮/烯類 |
| 45 | 薰衣草葉鼠尾草 | 氧化物類 | 單萜酮/烯類 |
| 47 | 桉油醇迷迭香 | 氧化物類 | 單萜酮/烯類 |
| 66 | 圓葉當歸 | 單萜烯類 | 單萜酮/烯類 |
| 67 | 歐防風 | 單萜烯類 | 單萜酮/烯類 |
| 54 | 中國當歸 | 單萜烯類 | 香豆素與內酯類 |
| 56 | 芹菜籽 | 單萜烯類 | 香豆素與內酯類 |
| 59 | 薑黃 | 倍半萜酮類 | 香豆素與內酯類 |
| 63 | 土木香 | 單萜烯類 | 香豆素與內酯類 |
| 64 | 大花土木香 | 單萜酮/烯類 | 香豆素與內酯類 |
| 93 | 樹蘭 | 單萜醇類 | 倍半萜烯類 |
| 96 | 大麻 | 單萜烯類 | 倍半萜烯類 |
| 97 | 依蘭 | 單萜醇類 | 倍半萜烯類 |
| 98 | 大葉依蘭 | 苯基酯類 | 倍半萜烯類 |
| 103 | 紅沒藥 | 倍半萜醇類 | 倍半萜烯類 |
| 107 | 古芸香脂 | 倍半萜醇類 | 倍半萜烯類 |
| 109 | 蛇麻草 | 單萜烯類 | 倍半萜烯類 |
| 110 | 聖約翰草 | 單萜烯類 | 倍半萜烯類 |
| 112 | 維吉尼亞雪松 | 單萜烯類 | 倍半萜烯類 |
| 113 | 穗甘松 | 倍半萜醇類 | 倍半萜烯類 |
| 114 | 中國甘松 | 倍半萜醇類 | 倍半萜烯類 |
| 115 | 番石榴葉 | 氧化物類 | 倍半萜烯類 |
| 117 | 一枝黃花 | 單萜烯類 | 倍半萜烯類 |
| 123 | 龍艾 | 單萜烯類 | 醛類 |
| 124 | 茴香 | 單萜烯類 | 醛類 |
| 125 | 金合歡茶樹 | 酚與芳香醛類 | 醛類 |
| 126 | 鹹亞茶樹 | 氧化物類 | 醛類 |
| 127 | 肉豆蔻 | 單萜烯類 | 醛類 |
| 128 | 粉紅蓮花 | 單萜醇類 | 醛類 |
| 129 | 熱帶羅勒 | 單萜醇類 | 醛類 |
| 130 | 露兜花 | 苯基酯類 | 醛類 |
| 131 | 歐白芷 | 單萜烯類 | 醛類 |
| 132 | 平葉歐芹 | 單萜烯類 | 醛類 |
| 133 | 洋茴香 | 單萜醇類 | 醛類 |
| 134 | 西部黃松 | 單萜烯類 | 醛類 |
| 135 | 洋茴香蘿文莎葉 | 單萜醇類 | 醛類 |
| 136 | 防風 | 單萜烯類 | 醛類 |
| 137 | 甜萬壽菊 | 香豆素與內酯類 | 醛類 |
| 139 | 檸檬香桃木 | 醛類 | 酯類 |
| 140 | 泰國青檸葉 | 醛類 | 酯類 |
| 141 | 檸檬葉 | 單萜烯類 | 酯類 |
| 142 | 檸檬香茅 | 醛類 | 酯類 |
| 143 | 爪哇香茅 | 醛類 | 酯類 |
| 144 | 檸檬尤加利 | 醛類 | 酯類 |
| 145 | 史密斯尤加利 | 氧化物類 | 酯類 |
| 146 | 檸檬細籽 | 醛類 | 酯類 |
| 147 | 檸檬馬鞭草 | 醛類 | 酯類 |
| 148 | 山雞椒 | 醛類 | 酯類 |
| 149 | 蜂蜜香桃木 | 醛類 | 酯類 |
| 150 | 香蜂草 | 醛類 | 酯類 |
| 151 | 檸檬桉粉 | 單萜烯類 | 酯類 |
| 152 | 紫蘇 | 倍半萜烯類 | 酯類 |
| 153 | 馬魯科 | 單萜醇類 | 酯類 |
| 156 | 零陵香豆 | 香豆素與內酯類 | 脂類 |
| 157 | 羅馬洋甘菊 | 酯類 | 脂類 |
| 158 | 墨西哥沉香 | 單萜醇類 | 脂類 |
| 159 | 苦橙葉 | 酯類 | 脂類 |
| 160 | 佛手柑 | 單萜烯類 | 脂類 |
| 161 | 小飛蓬 | 單萜烯類 | 脂類 |
| 162 | 岬角白梅 | 單萜烯類 | 脂類 |
| 163 | 玫瑰尤加利 | 氧化物類 | 脂類 |
| 164 | 黃葵 | 倍半萜醇類 | 脂類 |
| 165 | 真正薰衣草 | 酯類 | 脂類 |
| 166 | 醒目薰衣草 | 單萜醇類 | 脂類 |
| 167 | 檸檬薄荷 | 酯類 | 脂類 |
| 168 | 含笑 | 苯基酯類 | 脂類 |
| 169 | 紅香桃木 | 氧化物類 | 脂類 |
| 170 | 水果鼠尾草 | 單萜醇類 | 脂類 |
| 171 | 快樂鼠尾草 | 酯類 | 脂類 |
| 172 | 鷹爪豆 | 單萜醇類 | 脂類 |
| 175 | 大高良薑 | 氧化物類 | 苯基酯類 |
| 176 | 蘭香草 | 單萜醇類 | 苯基酯類 |
| 177 | 波羅尼花 | 單萜醇類 | 苯基酯類 |
| 178 | 蘇剛達 | 氧化物類 | 苯基酯類 |
| 182 | 大花茉莉 | 單萜醇類 | 苯基酯類 |
| 185 | 白玉蘭 | 單萜醇類 | 苯基酯類 |
| 186 | 滇玉蘭 | 單萜酮/烯類 | 苯基酯類 |
| 189 | 牡丹花 | 單萜醇類 | 苯基酯類 |
| 195 | 暹羅安息香 | 苯基酯類 | 芳香醛與芳香酯 |
| 196 | 香草 | 酚與芳香醛類 | 芳香醛與芳香酯 |
| 198 | 阿密茴 | 單萜醇類 | 倍半萜酮類 |
| 199 | 澳洲藍絲柏（鑽石級） | 倍半萜醇類 | 倍半萜酮類 |
| 200 | 印蒿 | 單萜醇類 | 倍半萜酮類 |
| 203 | 杭白菊 | 單萜酮/烯類 | 倍半萜酮類 |
| 207 | 義大利永久花 | 單萜醇類 | 倍半萜酮類 |
| 209 | 薰衣草 | 單萜酮/烯類 | 倍半萜酮類 |
| 210 | 馬纓丹 | 倍半萜烯類 | 倍半萜酮類 |
| 211 | 松紅梅 | 倍半萜烯類 | 倍半萜酮類 |
| 212 | 桂花 | 單萜醇類 | 倍半萜酮類 |
| 229 | 檸檬荊芥 | 醛類 | 單萜醇類 |
| 242 | 食茱萸 | 單萜烯類 | 單萜醇類 |
| 251 | 小茴香 | 單萜烯類 | 酚與芳香醛類 |
| 262 | 黑種草 | 單萜烯類 | 酚與芳香醛類 |
| 271 | 沉香樹 | 單萜醇類 | 倍半萜醇類 |
| 274 | 胡蘿蔔籽 | 倍半萜烯類 | 倍半萜醇類 |
| 276 | 白草果 | 氧化物類 | 倍半萜醇類 |
| 277 | 黏答答土木香 | 氧化物類 | 倍半萜醇類 |
| 278 | 昆士亞 | 單萜烯類 | 倍半萜醇類 |
| 279 | 厚朴 | 倍半萜烯類 | 倍半萜醇類 |
| 281 | 香脂果豆木 | 苯基酯類 | 倍半萜醇類 |
| 284 | 蓽澄茄 | 醛類 | 倍半萜醇類 |
| 286 | 狹長葉鼠尾草 | 單萜醇類 | 倍半萜醇類 |
| 289 | 塔斯馬尼亞胡椒 | 單萜烯類 | 倍半萜醇類 |
| 316 | 非洲藍香茅 | 醛類 | 單萜烯類 |
| 330 | 黑胡椒 | 倍半萜烯類 | 單萜烯類 |
| 335 | 雅麗菊 | 酚與芳香醛類 | 單萜烯類 |
| 342 | 貞節樹 | 氧化物類 | 單萜烯類 |

## ℹ️ Wikipedia redirect（舊學名→新學名，83 支）

| ID | 中文 | intelliverse Latin | Wikipedia 新標題 |
|---|---|---|---|
| 26 | 圓葉當歸 | Levisticum officinale | Lovage |
| 31 | 假剪股穎風輪菜 | Calamintha nepeta | Clinopodium nepeta |
| 32 | 藏茴香 | Carum carvi | Caraway |
| 33 | 藍米柏 | Fokienia hodginsii | Fokienia |
| 34 | 檸檬 | Citrus limon | Lemon |
| 40 | 馬郁蘭 | Origanum majorana | Marjoram |
| 41 | 綠薄荷 | Mentha spicata | Spearmint |
| 42 | 胡椒薄荷 | Mentha x piperita | Peppermint |
| 45 | 薰衣草葉鼠尾草 | Salvia lavandulifolia | Salvia officinalis subsp. lavandulifolia |
| 51 | 艾菊 | Tanacetum vulgare | Tansy |
| 67 | 歐防風 | Pastinaca sativa | Parsnip |
| 68 | 木香 | Saussurea costus | Dolomiaea costus |
| 57 | 辣根 | Armoracia rusticana | Horseradish |
| 59 | 薑黃 | Curcuma longa | Turmeric |
| 63 | 土木香 | Inula helenium | Elecampane |
| 64 | 大花土木香 | Inula graveolens | Dittrichia graveolens |
| 65 | 川芎 | Ligusticum chuanxiong | Conioselinum anthriscoides |
| 85 | 掃帚茶樹 | Leptospermum scoparium | Mānuka |
| 89 | 圓葉當歸 | Levisticum officinale | Lovage |
| 95 | 澳洲藍絲柏 | Callitris intratropica | Callitris columellaris |
| 113 | 穗甘松 | Nardostachys jatamansi | Nardostachys |
| 114 | 中國甘松 | Nardostachys chinensis | Nardostachys |
| 120 | 薑 | Zingiber officinale | Ginger |
| 123 | 龍艾 | Artemisia dracunculus | Tarragon |
| 124 | 茴香 | Foeniculum vulgare | Fennel |
| 130 | 露兜花 | Pandanus odoratissimus | Pandanus odorifer |
| 132 | 平葉歐芹 | Petroselinum crispum | Parsley |
| 133 | 洋茴香 | Pimpinella anisum | Anise |
| 136 | 防風 | Saposhnikovia divaricata | Saposhnikovia |
| 140 | 泰國青檸葉 | Citrus hystrix | Kaffir lime |
| 150 | 香蜂草 | Melissa officinalis | Lemon balm |
| 160 | 佛手柑 | Citrus bergamia | Bergamot orange |
| 166 | 醒目薰衣草 | Lavandula x intermedia | Lavandula |
| 167 | 檸檬薄荷 | Mentha citrata | Eau de Cologne mint |
| 168 | 含笑 | Michelia figo | Magnolia figo |
| 172 | 鷹爪豆 | Spartium junceum | Spartium |
| 178 | 蘇剛達 | Cinnamomum glaucescens | Camphora glaucescens |
| 185 | 白玉蘭 | Michelia x alba | Magnolia × alba |
| 186 | 滇玉蘭 | Michelia yunnanensis | Magnolia laevifolia |
| 187 | 秘魯香脂 | Myroxylon balsamum var. pereirae | Myroxylon balsamum |
| 189 | 牡丹花 | Paeonia suffruticosa | Paeonia × suffruticosa |
| 192 | 五月玫瑰 | Rosa centifolia | Rosa × centifolia |
| 198 | 阿密茴 | Ammi visnaga | Visnaga daucoides |
| 199 | 澳洲藍絲柏（鑽石級） | Callitris intratropica | Callitris columellaris |
| 203 | 杭白菊 | Chrysanthemum morifolium | Chrysanthemum × morifolium |
| 204 | 薑黃 | Curcuma longa | Turmeric |
| 211 | 松紅梅 | Leptospermum scoparium | Mānuka |
| 226 | 胡椒薄荷 | Mentha × piperita | Peppermint |
| 228 | 可因氏月橘 | Murraya koenigii | Curry tree |
| 231 | 甜馬郁蘭 | Origanum majorana | Marjoram |
| 232 | 野洋甘菊 | Ormenis mixta | Cladanthus mixtus |
| 234 | 大馬士革玫瑰 | Rosa damascena | Rosa × damascena |
| 250 | 頭狀百里香 | Thymbra capitata | Thymus capitatus |
| 251 | 小茴香 | Cuminum cyminum | Cumin |
| 252 | 丁香花苞 | Syzygium aromaticum | Clove |
| 255 | 野馬郁蘭 | Origanum vulgare | Oregano |
| 256 | 嚴愛草 | Satureja hortensis | Summer savory |
| 258 | 多香果 | Pimenta dioica | Allspice |
| 260 | 到手香 | Plectranthus amboinicus | Coleus amboinicus |
| 263 | 冬季香薄荷 | Satureja montana | Winter savory |
| 267 | 印度藏茴香 | Trachyspermum ammi | Ajwain |
| 275 | 暹羅木 | Fokienia hodginsii | Fokienia |
| 277 | 黏答答土木香 | Inula graveolens | Dittrichia graveolens |
| 282 | 新喀里多尼亞松 | Neocallitropsis pancheri | Callitris pancheri |
| 283 | 羌活 | Notopterygium incisum | Hansenia weberbaueriana |
| 285 | 廣藿香 | Pogostemon cablin | Patchouli |
| 290 | 纈草 | Valeriana officinalis | Valerian (herb) |
| 292 | 岩蘭草 | Vetiveria zizanioides | Chrysopogon zizanioides |
| 297 | 蒔蘿（全株） | Anethum graveolens | Dill |
| 306 | 苦橙 | Citrus aurantium | Bitter orange |
| 307 | 泰國青檸 | Citrus hystrix | Kaffir lime |
| 308 | 日本柚子 | Citrus junos | Yuzu |
| 309 | 萊姆 | Citrus aurantiifolia | Key lime |
| 310 | 檸檬 | Citrus limon | Lemon |
| 311 | 葡萄柚 | Citrus paradisi | Grapefruit |
| 312 | 桔（紅/綠） | Citrus reticulata | Mandarin orange |
| 314 | 海茴香 | Crithmum maritimum | Crithmum |
| 317 | 白松香 | Ferula galbaniflua | Ferula |
| 324 | 格陵蘭喇叭茶 | Ledum groenlandicum | Rhododendron groenlandicum |
| 330 | 黑胡椒 | Piper nigrum | Black pepper |
| 332 | 奇歐島熏陸香 | Pistacia lentiscus var. chia | Pistacia lentiscus |
| 334 | 道格拉斯杉 | Pseudotsuga menziesii | Douglas fir |
| 339 | 巴西胡椒 | Schinus terebinthifolius | Schinus terebinthifolia |
