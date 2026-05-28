"""
build_knowledge_wiki.py — 把 5 本 IFA 芳療書的知識建成 Karpathy-pattern wiki

供 understand-anything:/understand-knowledge 分析，產出互動知識圖譜。

產出結構（knowledge-wiki/）：
  CLAUDE.md         schema/config
  index.md          分類目錄（8 大類）
  log.md            操作紀錄
  raw/              5 本書來源（輕量參照）
  *.md              ~140 篇文章，用 [[wikilink]] 互連

知識來源：
  - data/oils.json（302 精油）
  - 46 個完整指南頁的化學/分類資料
  - 5 本書萃取的概念（化學分類、技法、安全、芳療史、學派）
"""
import sys
import json
import re
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

WIKI = Path(r'C:\Users\User\Desktop\essential-oil-guide\knowledge-wiki')
OILS_JSON = Path(r'C:\Users\User\Desktop\essential-oil-guide\data\oils.json')


def slugify(name):
    """安全檔名（保留中文，移除特殊符號）"""
    return re.sub(r'[\\/:*?"<>|]', '', name).strip()


def write_article(filename, frontmatter, body):
    """寫一篇 wiki 文章（YAML frontmatter + markdown body）"""
    fm_lines = ['---']
    for k, v in frontmatter.items():
        if isinstance(v, list):
            fm_lines.append(f'{k}: [{", ".join(v)}]')
        else:
            fm_lines.append(f'{k}: {v}')
    fm_lines.append('---')
    content = '\n'.join(fm_lines) + '\n\n' + body + '\n'
    (WIKI / filename).write_text(content, encoding='utf-8')


# ═══════════════════════════════════════════════════════════
# 46 主要精油（含豐富 wikilink）
# (slug, zh, latin, family, chem_class, key_molecules, uses, history, safety, school)
# ═══════════════════════════════════════════════════════════
OILS = [
    ('真正薰衣草', 'Lavandula angustifolia', '唇形科', ['酯類', '單萜醇類'],
     ['沉香醇', '乙酸沉香酯'], ['助眠', '抗焦慮', '皮膚修復'],
     'René-Maurice Gattefossé 1910 年燒傷實驗奠定現代芳療', '孕初期謹慎；幾乎無禁忌', '英系芳療'),
    ('穗花薰衣草', 'Lavandula latifolia', '唇形科', ['氧化物類', '單萜醇類'],
     ['1,8-桉油醇', '沉香醇', '樟腦'], ['呼吸保健', '肌肉舒緩', '蚊蟲叮咬'],
     '法系傳統用於燒燙傷與蛇咬', '含樟腦；孕婦/6歲以下/癲癇避用', '法系芳療'),
    ('醒目薰衣草', 'Lavandula intermedia', '唇形科', ['酯類', '單萜醇類'],
     ['沉香醇', '乙酸沉香酯', '樟腦'], ['居家清潔', '空間擴香'],
     '1920 年代發現的真正薰衣草與穗花薰衣草天然雜交種', '含樟腦；孕婦/6歲以下避用', '商業用途'),
    ('茶樹', 'Melaleuca alternifolia', '桃金孃科', ['單萜醇類'],
     ['萜品烯-4-醇'], ['抗菌', '皮膚保養'], '澳洲原住民 Bundjalung 族傳統用藥', '貓咪嚴禁；稀釋 1-2%', '英系芳療'),
    ('尤加利', 'Eucalyptus globulus', '桃金孃科', ['氧化物類'],
     ['1,8-桉油醇'], ['呼吸保健', '空間清新'], '澳洲原生，19 世紀引入歐洲', '6歲以下/蠶豆症/孕婦避用', '英系芳療'),
    ('胡椒薄荷', 'Mentha piperita', '唇形科', ['單萜醇類', '單萜酮類'],
     ['薄荷腦', '薄荷酮'], ['提神', '止痛', '消化'], '希臘神話寧芙 Minthe 的化身', '孕婦/嬰幼兒/低血壓避用', '英系芳療'),
    ('綠薄荷', 'Mentha spicata', '唇形科', ['單萜酮類'],
     ['香芹酮'], ['兒童消化', '口氣清新', '溫和提神'], '古希臘羅馬廣泛使用', '3歲以上可用；最溫和的薄荷', '英系芳療'),
    ('甜橙', 'Citrus sinensis', '芸香科', ['單萜烯類'],
     ['檸檬烯'], ['情緒提振', '兒童安撫'], '原產中國南方，16 世紀葡萄牙人帶入歐洲', '輕微光敏；兒童可用', '英系芳療'),
    ('柑橘', 'Citrus reticulata', '芸香科', ['單萜烯類'],
     ['檸檬烯'], ['兒童助眠', '情緒安撫'], '柑橘類中最溫和', '兒童夜哭安撫首選；輕微光敏', '英系芳療'),
    ('檸檬', 'Citrus limon', '芸香科', ['單萜烯類'],
     ['檸檬烯'], ['淨化', '提神', '抗菌'], 'James Lind 1747 年壞血病實驗', '光敏；12 小時內避日曬', '英系芳療'),
    ('葡萄柚', 'Citrus paradisi', '芸香科', ['單萜烯類'],
     ['檸檬烯', '圓柚酮'], ['循環', '控油', '提神'], '18 世紀加勒比海雜交種「禁果」', '光敏；藥物交互作用', '英系芳療'),
    ('佛手柑', 'Citrus bergamia', '芸香科', ['酯類', '單萜烯類'],
     ['乙酸沉香酯', '檸檬烯', '佛手柑素'], ['抗焦慮', '情緒平衡'], '伯爵紅茶香氣來源；古龍水主成分', '光敏；可選 FCF 版', '英系芳療'),
    ('橙花', 'Citrus aurantium', '芸香科', ['單萜醇類'],
     ['沉香醇'], ['安神助眠', '肌膚再生'], '17 世紀 Nerola 公主愛用而得名 Neroli', '最溫和花朵精油；孕婦可低劑量', '英系芳療'),
    ('苦橙葉', 'Citrus aurantium', '芸香科', ['酯類'],
     ['乙酸沉香酯', '沉香醇'], ['抗壓', '平衡自律神經'], '苦橙樹三兄弟之一（與橙花、苦橙同樹）', '無光敏；性價比高', '英系芳療'),
    ('玫瑰', 'Rosa damascena', '薔薇科', ['單萜醇類', '苯基酯類'],
     ['香茅醇', '牻牛兒醇', '苯乙醇'], ['深層情緒療癒', '抗老化'], '保加利亞玫瑰谷；3000 朵花釀 1ml', '孕期謹慎；高單價', '英系芳療'),
    ('茉莉', 'Jasminum grandiflorum', '木犀科', ['苯基酯類'],
     ['乙酸苄酯', '吲哚'], ['情緒沉澱', '香水基底'], '8000 朵夜花僅產 1ml 原精', '原精需稀釋；孕期避用', '法系芳療'),
    ('依蘭', 'Cananga odorata', '番荔枝科', ['倍半萜烯類', '酯類'],
     ['大根老鸛草烯', '乙酸苄酯'], ['情緒平衡', '護髮'], '菲律賓「花中之花」', '分餾等級差異大；低血壓慎用', '英系芳療'),
    ('義大利永久花', 'Helichrysum italicum', '菊科', ['倍半萜酮類'],
     ['義大利雙酮', '橙花酯'], ['化瘀', '疤痕修護'], '科西嘉島「不凋花」', '菊科過敏先測試；高單價', '法系芳療'),
    ('羅馬洋甘菊', 'Chamaemelum nobile', '菊科', ['酯類'],
     ['歐白芷酸酯'], ['兒童安撫', '深度助眠', '抗痙攣'], 'Saxons 九神聖草之一', '嬰幼兒/孕婦可用；菊科過敏測試', '英系芳療'),
    ('德國洋甘菊', 'Matricaria chamomilla', '菊科', ['倍半萜烯類', '氧化物類'],
     ['母菊天藍烴', 'α-沒藥醇'], ['敏感肌舒緩', '抗炎'], '蒸餾後轉化出藍色母菊天藍烴', '菊科過敏測試；深藍色', '英系芳療'),
    ('西洋蓍草', 'Achillea millefolium', '菊科', ['倍半萜烯類', '單萜酮類'],
     ['母菊天藍烴', '樟腦'], ['皮膚修護', '女性週期'], '希臘英雄阿基里斯的傷藥', '孕期避用；菊科過敏測試', '英系芳療'),
    ('迷迭香', 'Salvia rosmarinus', '唇形科', ['氧化物類', '單萜酮類'],
     ['1,8-桉油醇', '樟腦'], ['記憶力', '頭皮循環', '提神'], '「海洋的露珠」；地中海聖草', '高血壓/孕婦/癲癇依化學型謹慎', '英系芳療'),
    ('甜馬鬱蘭', 'Origanum majorana', '唇形科', ['單萜醇類'],
     ['萜品烯-4-醇'], ['鎮靜', '肌肉舒緩', '自律神經'], '希臘愛神阿芙蘿黛蒂的香草', '低血壓慎用；孕期避免', '英系芳療'),
    ('快樂鼠尾草', 'Salvia sclarea', '唇形科', ['酯類'],
     ['乙酸沉香酯', '香紫蘇醇'], ['PMS', '女性週期', '助眠'], '中世紀「清澈之眼」明目草', '孕期全程避用；勿與酒精併用', '英系芳療'),
    ('甜羅勒', 'Ocimum basilicum', '唇形科', ['單萜醇類'],
     ['沉香醇'], ['提神', '消化', '神經養護'], '希臘「香草之王」；印度聖草圖西', '需確認 ct.linalool 化學型', '英系芳療'),
    ('百里香', 'Thymus vulgaris', '唇形科', ['酚類', '單萜醇類'],
     ['百里酚', '沉香醇'], ['抗菌', '免疫支持'], '古埃及防腐；古希臘勇氣象徵', '化學型差異大；thymol 型強刺激', '法系芳療'),
    ('香蜂草', 'Melissa officinalis', '唇形科', ['醛類'],
     ['橙花醛', '香葉醛'], ['情緒急救', '助眠'], 'Paracelsus 稱「生命靈藥」', '精油界最貴；孕初期避用', '英系芳療'),
    ('天竺葵', 'Pelargonium graveolens', '牻牛兒苗科', ['單萜醇類'],
     ['香茅醇', '牻牛兒醇'], ['女性週期', '皮膚平衡', '驅蚊'], '南非原生；波旁島為頂級產地', '糖尿病慎用；貓家庭避擴香', '英系芳療'),
    ('玫瑰草', 'Cymbopogon martinii', '禾本科', ['單萜醇類'],
     ['牻牛兒醇'], ['保濕', '抗菌'], '禾本科卻有玫瑰香的「平價玫瑰」', '產前可助產；非臨產孕婦避用', '英系芳療'),
    ('桉油醇樟', 'Cinnamomum camphora', '樟科', ['氧化物類'],
     ['1,8-桉油醇'], ['呼吸保健', '免疫'], '馬達加斯加「好葉子」Ravintsara', '嬰幼兒/癲癇避用；勿與羅文莎葉混淆', '法系芳療'),
    ('檸檬尤加利', 'Corymbia citriodora', '桃金孃科', ['醛類'],
     ['香茅醛'], ['驅蚊', '空間清新'], '美國 CDC 認證天然驅蚊成分 OLE', '敏感肌 1-2%；3歲以下避用', '英系芳療'),
    ('月桂', 'Laurus nobilis', '樟科', ['氧化物類'],
     ['1,8-桉油醇'], ['淋巴循環', '消化'], '希臘羅馬勝利桂冠；德爾菲神諭', '微量丁香酚；貼膚測試', '英系芳療'),
    ('大西洋雪松', 'Cedrus atlantica', '松科', ['倍半萜烯類', '倍半萜醇類'],
     ['喜馬雪松烯', '雪松醇'], ['助眠', '頭皮養護'], '黎巴嫩雪松；所羅門聖殿建材', '孕婦避免；多種雪松易混淆', '英系芳療'),
    ('檀香', 'Santalum album', '檀香科', ['倍半萜醇類'],
     ['檀香醇'], ['冥想', '肌膚保養'], '3000 年東方木質；CITES 管制', '印度產偽品多；孕婦可用', '英系芳療'),
    ('杜松漿果', 'Juniperus communis', '柏科', ['單萜烯類'],
     ['α-蒎烯'], ['利尿排毒', '淨化'], '琴酒香料來源；中世紀驅瘟疫', '腎臟疾病/孕婦避用；勿長期', '英系芳療'),
    ('絲柏', 'Cupressus sempervirens', '柏科', ['單萜烯類'],
     ['α-蒎烯'], ['收斂', '靜脈循環'], '地中海「死亡之樹」象徵轉化', '含 manool 類雌激素；孕婦避用', '英系芳療'),
    ('黑雲杉', 'Picea mariana', '松科', ['酯類', '單萜烯類'],
     ['乙酸龍腦酯', 'α-蒎烯'], ['腎上腺疲勞', '森林浴'], '加拿大原住民汗屋儀式用', '一般安全；松柏類易氧化需冷藏', '法系芳療'),
    ('廣藿香', 'Pogostemon cablin', '唇形科', ['倍半萜醇類'],
     ['廣藿香醇'], ['皮膚修護', '定香'], '1960 嬉皮代表香；喀什米爾披肩防蟲', '安全性高；陳年越香', '英系芳療'),
    ('岩蘭草', 'Chrysopogon zizanioides', '禾本科', ['倍半萜醇類'],
     ['岩蘭草醇'], ['深層助眠', '冥想接地'], '印度 Khus；海地頂級香水原料', '安全性極高；黏稠需溫熱', '英系芳療'),
    ('薑', 'Zingiber officinale', '薑科', ['倍半萜烯類'],
     ['薑烯'], ['暖身循環', '消化', '暈車'], '阿育吠陀與中醫千年藥材', 'CO2 萃取較刺激；敏感肌 1%', '英系芳療'),
    ('黑胡椒', 'Piper nigrum', '胡椒科', ['單萜烯類', '倍半萜烯類'],
     ['β-石竹烯'], ['循環', '肌肉', '消化'], '「東方香料之王」比黃金貴', '高濃度刺激；外用 1%', '英系芳療'),
    ('丁香', 'Syzygium aromaticum', '桃金孃科', ['酚類'],
     ['丁香酚'], ['牙痛應急', '辛香'], '摩鹿加群島香料貿易爭奪', '黏膜刺激極強；≤0.5%；孕婦避用', '英系芳療'),
    ('香茅', 'Cymbopogon winterianus', '禾本科', ['醛類', '單萜醇類'],
     ['香茅醛', '牻牛兒醇'], ['驅蚊', '空間清新'], '爪哇 vs 錫蘭兩大品系', '皮膚敏感 ≤1%；貓家庭注意', '英系芳療'),
    ('乳香', 'Boswellia carterii', '橄欖科', ['單萜烯類'],
     ['α-蒎烯'], ['冥想', '抗老化', '皮膚'], '聖經三禮物之一；古埃及聖香', '孕初期諮詢；稀釋 1-3%', '英系芳療'),
    ('沒藥', 'Commiphora myrrha', '橄欖科', ['倍半萜烯類'],
     ['呋喃桉烷二烯'], ['皮膚修復', '口腔保健', '冥想'], '聖經三禮物；古埃及木乃伊防腐', '孕婦避免；糖尿病慎用', '英系芳療'),
    ('甜茴香', 'Foeniculum vulgare', '傘形科', ['醚類'],
     ['反式茴香腦'], ['消化', '女性週期'], 'Prometheus 用茴香莖藏神火', '孕婦/5歲以下/癲癇禁用；≤2.5%', '法系芳療'),
]

# ═══════════════════════════════════════════════════════════
# 14 化學分類
# ═══════════════════════════════════════════════════════════
CHEM_CLASSES = [
    ('單萜烯類', 'Monoterpenes', ['檸檬烯', 'α-蒎烯'], '10 碳揮發性烴；柑橘松柏；明亮輕快、易氧化', ['甜橙', '檸檬', '葡萄柚', '杜松漿果', '絲柏', '乳香']),
    ('單萜醇類', 'Monoterpenols', ['沉香醇', '牻牛兒醇', '香茅醇', '萜品烯-4-醇'], '含羥基；化學最溫和；適合敏感族群與兒童', ['真正薰衣草', '玫瑰', '天竺葵', '茶樹', '甜馬鬱蘭', '橙花']),
    ('倍半萜醇類', 'Sesquiterpenols', ['檀香醇', '岩蘭草醇', '廣藿香醇'], '15 碳醇類；深沉木質；揮發極慢；優質定香劑', ['檀香', '岩蘭草', '廣藿香']),
    ('倍半萜烯類', 'Sesquiterpenes', ['β-石竹烯', '母菊天藍烴'], '15 碳不飽和烴；溫和抗炎', ['依蘭', '薑', '德國洋甘菊', '沒藥', '黑胡椒']),
    ('單萜酮類', 'Monoterpenones', ['薄荷酮', '樟腦', '香芹酮'], '含羰基；強神經作用；孕婦嬰幼兒癲癇避用', ['胡椒薄荷', '綠薄荷', '迷迭香']),
    ('倍半萜酮類', 'Sesquiterpenones', ['義大利雙酮'], '15 碳酮類；神經毒性極低卻能化瘀消腫', ['義大利永久花']),
    ('氧化物類', 'Oxides', ['1,8-桉油醇'], '含氧雜環；呼吸系統保健代表', ['尤加利', '桉油醇樟', '迷迭香', '月桂', '穗花薰衣草']),
    ('醛類', 'Aldehydes', ['檸檬醛', '橙花醛', '香葉醛', '香茅醛'], '含醛基；香氣強烈帶柑橘；可能刺激皮膚', ['香蜂草', '檸檬尤加利', '香茅']),
    ('酯類', 'Esters', ['乙酸沉香酯', '歐白芷酸酯'], '酸醇結合；最溫和鎮靜的化學族群', ['佛手柑', '快樂鼠尾草', '羅馬洋甘菊', '苦橙葉', '真正薰衣草']),
    ('苯基酯類', 'Benzyl Esters', ['乙酸苄酯', '苯乙醇'], '苯環酯類；香氣甜美持久；高級香水基底', ['茉莉', '玫瑰', '依蘭']),
    ('芳香醛類', 'Aromatic Aldehydes', ['肉桂醛', '水楊酸甲酯'], '帶苯環醛類；刺激性強需嚴格稀釋', []),
    ('酚類', 'Phenols', ['丁香酚', '百里酚'], '帶羥基苯環；抗菌最強但黏膜刺激最強', ['丁香', '百里香']),
    ('香豆素與內酯類', 'Coumarins', ['佛手柑素'], '苯並吡喃；柑橘果皮光敏成分', ['佛手柑']),
    ('醚類', 'Phenolic Ethers', ['反式茴香腦', '甲基醚蒟醬'], '苯醚類；類雌激素活性；需注意劑量', ['甜茴香']),
]

# ═══════════════════════════════════════════════════════════
# 植物科屬
# ═══════════════════════════════════════════════════════════
FAMILIES = [
    ('唇形科', 'Lamiaceae', '芳療最重要的科；多酯類與單萜醇；鎮靜放鬆代表',
     ['真正薰衣草', '穗花薰衣草', '醒目薰衣草', '胡椒薄荷', '綠薄荷', '迷迭香', '甜馬鬱蘭', '快樂鼠尾草', '甜羅勒', '百里香', '香蜂草', '廣藿香']),
    ('芸香科', 'Rutaceae', '柑橘類；果皮冷壓富含檸檬烯；多有光敏性',
     ['甜橙', '柑橘', '檸檬', '葡萄柚', '佛手柑', '橙花', '苦橙葉']),
    ('桃金孃科', 'Myrtaceae', '澳洲為主；多氧化物與酚類；呼吸與抗菌代表',
     ['茶樹', '尤加利', '檸檬尤加利', '丁香']),
    ('菊科', 'Asteraceae', '多藍色精油與倍半萜；抗炎與皮膚修復；過敏者注意',
     ['義大利永久花', '羅馬洋甘菊', '德國洋甘菊', '西洋蓍草']),
    ('禾本科', 'Poaceae', '香茅家族；多醛類與單萜醇；驅蟲與保濕',
     ['玫瑰草', '香茅', '岩蘭草']),
    ('柏科', 'Cupressaceae', '針葉樹；多單萜烯；收斂與淨化',
     ['杜松漿果', '絲柏']),
    ('松科', 'Pinaceae', '針葉樹；森林浴與能量提振',
     ['大西洋雪松', '黑雲杉']),
    ('橄欖科', 'Burseraceae', '樹脂類；冥想與皮膚修復；聖經香料',
     ['乳香', '沒藥']),
    ('樟科', 'Lauraceae', '多氧化物；呼吸保健',
     ['桉油醇樟', '月桂']),
    ('傘形科', 'Apiaceae', '種子類；消化與荷爾蒙；多醚類需謹慎',
     ['甜茴香']),
    ('薔薇科', 'Rosaceae', '玫瑰所屬；高單價花朵',
     ['玫瑰']),
    ('木犀科', 'Oleaceae', '茉莉所屬；夜開花原精',
     ['茉莉']),
    ('番荔枝科', 'Annonaceae', '依蘭所屬；濃郁熱帶花香',
     ['依蘭']),
    ('牻牛兒苗科', 'Geraniaceae', '天竺葵所屬；玫瑰般花香的平衡精油',
     ['天竺葵']),
    ('檀香科', 'Santalaceae', '檀香所屬；半寄生植物；深沉木質',
     ['檀香']),
    ('薑科', 'Zingiberaceae', '薑所屬；根莖類；溫暖辛香',
     ['薑']),
    ('胡椒科', 'Piperaceae', '黑胡椒所屬；辛香料；循環溫暖',
     ['黑胡椒']),
]

# ═══════════════════════════════════════════════════════════
# 芳療技法
# ═══════════════════════════════════════════════════════════
TECHNIQUES = [
    ('擴香', '透過擴香儀或水氧機讓精油分子散布空間；最安全的入門用法', ['嗅吸', '稀釋']),
    ('嗅吸', '直接從瓶口或嗅吸棒吸聞；最快作用於[[邊緣系統]]', ['擴香', '情緒急救']),
    ('按摩', '精油用[[基底油]]稀釋後塗抹按摩；結合觸覺與嗅覺', ['稀釋', '基底油']),
    ('稀釋', '精油用基底油/純露稀釋至安全濃度（臉部 0.5-1%、身體 2-3%）', ['基底油', '按摩', '精油安全']),
    ('沐浴', '精油先用基底油或全脂牛奶乳化再入浴；勿直接滴入水中', ['稀釋', '基底油']),
    ('蒸氣蒸餾', '最常見萃取法；蒸氣帶出植物揮發油再冷凝分離', ['萃取方式', '純露']),
    ('冷壓榨', '柑橘果皮機械擠壓萃取；保留完整香氣但有光敏成分', ['萃取方式']),
    ('溶劑萃取', '用溶劑萃取脆弱花朵得到原精；香氣濃郁', ['萃取方式', '茉莉']),
    ('CO2超臨界萃取', '低溫高壓二氧化碳萃取；保留更完整成分', ['萃取方式', '薑']),
    ('基底油', '植物油作精油載體（甜杏仁、荷荷巴、玫瑰果）；延長香氣並安全稀釋', ['稀釋', '按摩']),
    ('純露', '蒸餾過程的水相產物；含微量水溶性成分；溫和適合嬰幼兒', ['蒸氣蒸餾']),
    ('萃取方式', '蒸氣蒸餾、冷壓、溶劑、CO2 四大法；決定成分輪廓與香氣', ['蒸氣蒸餾', '冷壓榨', '溶劑萃取', 'CO2超臨界萃取']),
]

# ═══════════════════════════════════════════════════════════
# 安全知識
# ═══════════════════════════════════════════════════════════
SAFETY = [
    ('精油安全', '芳療核心原則：稀釋、避光敏、認清禁忌族群；天然不等於安全', ['稀釋', '光敏性', '孕期芳療', '兒童芳療', '寵物芳療']),
    ('光敏性', '柑橘類含[[香豆素與內酯類]]；塗抹後 12 小時內避免日曬', ['佛手柑', '檸檬', '葡萄柚']),
    ('孕期芳療', '初期完全避免；中後期可低劑量用溫和精油；多種精油全程禁用', ['快樂鼠尾草', '甜茴香', '精油安全']),
    ('兒童芳療', '0-6 月避免；2 歲以上低劑量；避用薄荷腦樟腦類', ['綠薄荷', '羅馬洋甘菊', '柑橘', '精油安全']),
    ('寵物芳療', '貓缺乏葡萄糖醛酸轉移酶無法代謝多種成分；茶樹柑橘類高危', ['茶樹', '精油安全']),
    ('化學型', '同種植物因產地氣候有不同主成分（如百里香 ct.thymol vs ct.linalool）；購買須確認', ['百里香', '迷迭香']),
]

# ═══════════════════════════════════════════════════════════
# 芳療史 / 人物
# ═══════════════════════════════════════════════════════════
PEOPLE = [
    ('René-Maurice Gattefossé', '法國化學家；1910 年燒傷後用薰衣草處理；創造 aromathérapie 一詞', ['真正薰衣草', '法系芳療']),
    ('Marguerite Maury', '奧地利生化學家；將芳療帶入美容與身心領域；個人配方概念', ['英系芳療']),
    ('Robert Tisserand', '英國芳療先驅；著《The Art of Aromatherapy》與《Essential Oil Safety》', ['英系芳療', '精油安全']),
    ('Pierre Franchomme', '法系芳療代表；化學型 chemotype 概念奠基；著《L\'aromathérapie exactement》', ['法系芳療', '化學型']),
    ('Jean Valnet', '法國軍醫；用精油治療傷兵；推動醫療芳療', ['法系芳療']),
    ('Avicenna', '波斯醫師（980-1037）；相傳改良蒸氣蒸餾技術', ['蒸氣蒸餾']),
]

# ═══════════════════════════════════════════════════════════
# 芳療學派
# ═══════════════════════════════════════════════════════════
SCHOOLS = [
    ('英系芳療', 'IFA/IFPA 代表；強調按摩、稀釋、整體療癒；溫和保守', ['Robert Tisserand', 'Marguerite Maury', '按摩', 'IFA']),
    ('法系芳療', 'Franchomme/Valnet 代表；強調化學分子、高濃度、口服（醫療監督）', ['Pierre Franchomme', 'Jean Valnet', '化學型']),
    ('IFA', 'International Federation of Aromatherapists；1985 成立的國際芳療師組織', ['英系芳療']),
    ('中醫芳療', '結合精油與經絡、五行、寒熱屬性；東西方融合', ['五行', '經絡']),
    ('五行', '金木水火土；對應精油的能量屬性與臟腑', ['中醫芳療']),
    ('經絡', '中醫十二經絡；精油可依歸經選用', ['中醫芳療']),
    ('邊緣系統', '大腦情緒中樞；嗅覺神經直接連結；芳療作用情緒的生理基礎', ['嗅吸']),
]

# ═══════════════════════════════════════════════════════════
# 應用情境
# ═══════════════════════════════════════════════════════════
USE_CASES = [
    ('助眠', '睡前放鬆香氛；改善入睡與睡眠品質', ['真正薰衣草', '羅馬洋甘菊', '岩蘭草', '大西洋雪松']),
    ('抗焦慮', '日常情緒支持；緩解壓力與緊繃', ['佛手柑', '香蜂草', '橙花', '真正薰衣草']),
    ('皮膚修復', '促進肌膚再生與修護；疤痕淡化', ['真正薰衣草', '義大利永久花', '廣藿香']),
    ('呼吸保健', '空間清新與呼吸道日常保養', ['尤加利', '桉油醇樟', '穗花薰衣草', '茶樹']),
    ('消化', '腹部按摩支持消化舒適', ['薑', '甜茴香', '胡椒薄荷', '甜羅勒']),
    ('女性週期', 'PMS 與更年期的情緒與身體芳香支持', ['快樂鼠尾草', '天竺葵', '玫瑰', '甜茴香']),
    ('驅蚊', '天然驅蟲驅蚊配方', ['檸檬尤加利', '香茅', '天竺葵']),
    ('冥想', '靜心與靈性練習的香氛陪伴', ['乳香', '沒藥', '檀香', '岩蘭草']),
    ('提神', '提升注意力與工作精神', ['迷迭香', '胡椒薄荷', '檸檬', '甜羅勒']),
    ('肌肉舒緩', '運動後與緊繃肌肉的按摩支持', ['甜馬鬱蘭', '黑胡椒', '薑', '穗花薰衣草']),
    ('化瘀', '瘀傷腫脹的芳香護理', ['義大利永久花', '西洋蓍草']),
    ('情緒急救', '突發情緒衝擊時的即時嗅吸支持', ['香蜂草', '佛手柑', '真正薰衣草']),
    ('抗菌', '日常環境與肌膚的抗菌香氛應用', ['茶樹', '百里香', '丁香', '玫瑰草']),
    ('空間清新', '淨化與清新室內空氣的擴香', ['檸檬', '尤加利', '香茅', '檸檬尤加利']),
    ('淨化', '空間與能量的淨化（薩滿傳統）', ['杜松漿果', '乳香', '大西洋雪松']),
    ('循環', '促進血液與淋巴循環的按摩支持', ['黑胡椒', '薑', '絲柏', '葡萄柚']),
    ('抗老化', '熟齡肌膚的抗氧化與緊緻保養', ['乳香', '玫瑰', '檀香', '義大利永久花']),
    ('情緒平衡', '穩定情緒高低起伏', ['天竺葵', '依蘭', '佛手柑']),
    ('皮膚保養', '日常肌膚保濕與護理', ['橙花', '檀香', '玫瑰草', '廣藿香']),
    ('兒童安撫', '兒童情緒安撫與睡前放鬆（2 歲以上低劑量）', ['柑橘', '羅馬洋甘菊', '甜橙', '真正薰衣草']),
    ('護髮', '頭皮與髮絲的養護', ['迷迭香', '依蘭', '大西洋雪松']),
    ('暖身循環', '寒冷季節的溫暖循環支持', ['薑', '黑胡椒', '甜馬鬱蘭']),
]


def link(name):
    """產生 wikilink"""
    return f'[[{name}]]'


def build_oils():
    count = 0
    for zh, latin, family, chem_classes, molecules, uses, history, safety, school in OILS:
        chem_links = ' · '.join(link(c) for c in chem_classes)
        mol_links = ' · '.join(link(m) for m in molecules)
        use_links = ' · '.join(link(u) for u in uses)
        body = f"""# {zh}

**{zh}精油** · 學名 *{latin}*
**植物科**：{link(family)}
**化學分類**：{chem_links}
**主要分子**：{mol_links}
**芳療學派**：{link(school)}

## 簡介

{zh}（*{latin}*）屬於{link(family)}，化學上歸類為{chem_links}。主要活性分子包括 {mol_links}。

## 歷史與文化

{history}。

## 主要應用

常見於 {use_links} 等芳香應用。

## 安全須知

{safety}。詳見 {link('精油安全')}。

## 相關連結

- 植物科：{link(family)}
- 化學分類：{chem_links}
- 應用：{use_links}
- 學派：{link(school)}
"""
        write_article(
            f'{slugify(zh)}.md',
            {'type': 'oil', 'latin': latin, 'family': family, 'tags': [f'"{c}"' for c in chem_classes]},
            body,
        )
        count += 1
    return count


def build_chem():
    count = 0
    for zh, en, molecules, desc, oils in CHEM_CLASSES:
        mol_links = ' · '.join(link(m) for m in molecules)
        oil_links = ' · '.join(link(o) for o in oils) if oils else '（多種精油）'
        body = f"""# {zh}

**{zh}（{en}）** — 精油化學分類
**代表分子**：{mol_links}

## 定義

{desc}。

## 代表分子

{mol_links}

## 代表精油

{oil_links}

## 相關連結

- 分子：{mol_links}
- 精油：{oil_links}
"""
        write_article(
            f'{slugify(zh)}.md',
            {'type': 'chemistry', 'english': en, 'tags': ['"化學分類"']},
            body,
        )
        count += 1
    return count


def build_molecules():
    """從化學分類抽取所有分子，建立分子文章"""
    mol_to_classes = {}
    mol_to_oils = {}
    for zh, en, molecules, desc, oils in CHEM_CLASSES:
        for m in molecules:
            mol_to_classes.setdefault(m, []).append(zh)
    for oil_zh, latin, family, chem_classes, molecules, *_ in OILS:
        for m in molecules:
            mol_to_oils.setdefault(m, []).append(oil_zh)

    count = 0
    all_mols = set(mol_to_classes) | set(mol_to_oils)
    for mol in sorted(all_mols):
        classes = mol_to_classes.get(mol, [])
        oils = mol_to_oils.get(mol, [])
        class_links = ' · '.join(link(c) for c in classes) if classes else '—'
        oil_links = ' · '.join(link(o) for o in oils) if oils else '—'
        body = f"""# {mol}

精油化學分子。

## 所屬化學分類

{class_links}

## 含此分子的精油

{oil_links}

## 相關連結

- 化學分類：{class_links}
- 精油：{oil_links}
"""
        write_article(
            f'{slugify(mol)}.md',
            {'type': 'molecule', 'tags': ['"化學分子"']},
            body,
        )
        count += 1
    return count


def build_families():
    """植物科專屬（4 元素結構：中文、英文、描述、精油清單）"""
    count = 0
    for zh, en, desc, oils in FAMILIES:
        oil_links = ' · '.join(link(o) for o in oils) if oils else '—'
        body = f"""# {zh}

**{zh}（{en}）** — 植物科

{desc}。

## 此科精油

{oil_links}

## 相關連結

{oil_links}
"""
        write_article(
            f'{slugify(zh)}.md',
            {'type': 'family', 'english': en, 'tags': ['"植物科屬"']},
            body,
        )
        count += 1
    return count


def build_generic(items, type_name, tag, count_box):
    for entry in items:
        name = entry[0]
        desc = entry[1]
        related = entry[2] if len(entry) > 2 else []
        rel_links = ' · '.join(link(r) for r in related) if related else '—'
        body = f"""# {name}

{desc}。

## 相關連結

{rel_links}
"""
        write_article(
            f'{slugify(name)}.md',
            {'type': type_name, 'tags': [f'"{tag}"']},
            body,
        )
        count_box[0] += 1


def build_index():
    """產生 index.md 分類目錄"""
    def section(title, items, get_name=lambda x: x[0]):
        lines = [f'## {title}', '']
        for it in items:
            name = get_name(it)
            lines.append(f'- [[{slugify(name)}]]')
        lines.append('')
        return '\n'.join(lines)

    # 分子
    all_mols = set()
    for _, _, molecules, _, _ in CHEM_CLASSES:
        all_mols |= set(molecules)
    for oil_zh, latin, family, chem_classes, molecules, *_ in OILS:
        all_mols |= set(molecules)

    body = f"""# 精油能量圖譜知識庫

整合 5 本 IFA 芳療經典（IFA 芳療課程、破解精油、天然驅蟲配方手冊、方療應用全書等）的知識圖譜。
由 [[英系芳療]] 與 [[法系芳療]] 兩大學派整合，涵蓋 {len(OILS)} 支精油、{len(CHEM_CLASSES)} 大化學分類、{len(FAMILIES)} 個植物科。

{section('精油單品', OILS)}
{section('化學分類', CHEM_CLASSES)}
{section('化學分子', sorted(all_mols), get_name=lambda x: x)}
{section('植物科屬', FAMILIES)}
{section('芳療技法', TECHNIQUES)}
{section('安全知識', SAFETY)}
{section('芳療史與人物', PEOPLE)}
{section('芳療學派與概念', SCHOOLS)}
{section('應用情境', USE_CASES)}
"""
    (WIKI / 'index.md').write_text(body, encoding='utf-8')


def build_schema():
    body = """# 精油能量圖譜知識庫 — Schema

這是一個 Karpathy-pattern LLM wiki，整合 5 本 IFA 芳療經典書籍的知識。

## 知識來源（raw/）

1. IFA 芳療課程 - Joanna Hoare（英系 IFA 標準教材）
2. 破解精油 - Essential Oils Handbook（英法系整合）
3. 天然驅蟲配方手冊 - Naturally Bug Free（75 配方）
4. 方療應用全書 - 呂秀齡（應用實務）
5. 綜合 IFA 芳療聖經教材

## 節點類型

- `oil` — 精油單品（學名、科屬、化學分類、應用）
- `chemistry` — 化學分類（14 大類）
- `molecule` — 化學分子（沉香醇、檸檬烯等）
- `family` — 植物科屬
- `technique` — 芳療技法
- `safety` — 安全知識
- `person` — 芳療史人物
- `school` — 芳療學派與概念
- `usecase` — 應用情境

## 連結語意

- 精油 → 化學分類 / 分子 / 植物科 / 應用 / 學派
- 化學分類 → 分子 / 精油
- 應用情境 → 推薦精油
- 安全知識 → 相關精油
"""
    (WIKI / 'CLAUDE.md').write_text(body, encoding='utf-8')


def build_log():
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    body = f"""# 操作紀錄

- {today} — 從 5 本 IFA 芳療書建立知識 wiki（build_knowledge_wiki.py）
"""
    (WIKI / 'log.md').write_text(body, encoding='utf-8')


def build_raw_refs():
    """raw/ 放 5 本書的輕量參照（不放 PDF，只放說明）"""
    books = [
        ('01-IFA芳療課程-Joanna-Hoare.md', 'IFA 芳療課程', 'Joanna Hoare', '英系 IFA 標準教材，131 頁，涵蓋芳療史、精油 profile、安全'),
        ('02-破解精油.md', '破解精油 Essential Oils Handbook', '—', '英法系整合，170 頁，中高階調配與科學實證'),
        ('03-天然驅蟲配方手冊.md', 'Naturally Bug Free 天然驅蟲配方手冊', 'Stephanie L. Tourles', '75 個無毒驅蟲配方，99 頁'),
        ('04-方療應用全書.md', '方療應用全書', '呂秀齡', '應用實務，125 頁，全方位健康照護'),
        ('05-IFA芳療聖經.md', 'IFA 芳療聖經（綜合教材）', '—', '254 頁綜合教材，芳療史、化學、精油 profile'),
    ]
    for fn, title, author, desc in books:
        body = f"# {title}\n\n**作者**：{author}\n\n{desc}\n"
        (WIKI / 'raw' / fn).write_text(body, encoding='utf-8')


def main():
    print('建立 Karpathy-pattern 知識 wiki...')
    build_schema()
    build_log()
    build_raw_refs()
    n_oils = build_oils()
    n_chem = build_chem()
    n_mol = build_molecules()
    n_fam = build_families()
    box = [0]; build_generic(TECHNIQUES, 'technique', '芳療技法', box); n_tech = box[0]
    box = [0]; build_generic(SAFETY, 'safety', '安全知識', box); n_safe = box[0]
    box = [0]; build_generic(PEOPLE, 'person', '芳療史', box); n_ppl = box[0]
    box = [0]; build_generic(SCHOOLS, 'school', '芳療學派', box); n_sch = box[0]
    box = [0]; build_generic(USE_CASES, 'usecase', '應用情境', box); n_uc = box[0]
    build_index()

    total = n_oils + n_chem + n_mol + n_fam + n_tech + n_safe + n_ppl + n_sch + n_uc
    print(f'''
✓ Wiki 建立完成於 {WIKI}
  精油單品:   {n_oils}
  化學分類:   {n_chem}
  化學分子:   {n_mol}
  植物科屬:   {n_fam}
  芳療技法:   {n_tech}
  安全知識:   {n_safe}
  芳療史人物: {n_ppl}
  學派概念:   {n_sch}
  應用情境:   {n_uc}
  ─────────────────
  總文章數:   {total}
  + index.md + CLAUDE.md + log.md + raw/ (5 本書)
''')


if __name__ == '__main__':
    main()
