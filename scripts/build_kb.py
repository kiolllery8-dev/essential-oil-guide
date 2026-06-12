# -*- coding: utf-8 -*-
"""從網站結構化資料建知識庫 kb.json（給 chat 線上詢問 AI 用 RAG 檢索）。
來源：data/oils.json（302 支精油事實）＋ app/lib/pageSummaries.ts（75 篇頁面摘要）。
只取「事實／本站原創摘要」，不放書本原文。輸出 → ../chat-intelliverse/data/kb.json
（既有由後台手動新增/訓練的條目 source=='admin' 會保留，不被覆蓋）"""
import json, re, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'C:\Users\User\Desktop\essential-oil-guide'
OUT = r'C:\Users\User\Desktop\chat-intelliverse\data\kb.json'
SITE = 'https://intelliverse.tw'

# 精油中文名 → oil-* slug（有完整指南頁的 46 支）
SLUG = {
 '薰衣草':'oil-lavender','真正薰衣草':'oil-lavender','茶樹':'oil-tea-tree','尤加利':'oil-eucalyptus',
 '薄荷':'oil-peppermint','胡椒薄荷':'oil-peppermint','甜橙':'oil-sweet-orange','乳香':'oil-frankincense',
 '佛手柑':'oil-bergamot','玫瑰':'oil-rose','大馬士革玫瑰':'oil-rose','天竺葵':'oil-geranium',
 '葡萄柚':'oil-grapefruit','甜馬鬱蘭':'oil-marjoram','薑':'oil-ginger','橙花':'oil-neroli',
 '岩蘭草':'oil-vetiver','快樂鼠尾草':'oil-clary-sage','永久花':'oil-helichrysum','義大利永久花':'oil-helichrysum',
 '檀香':'oil-sandalwood','茉莉':'oil-jasmine','香茅':'oil-citronella','丁香':'oil-clove',
 '苦橙葉':'oil-petitgrain','杜松':'oil-juniper','杜松漿果':'oil-juniper','絲柏':'oil-cypress',
 '月桂':'oil-bay','沒藥':'oil-myrrh','廣藿香':'oil-patchouli','黑胡椒':'oil-black-pepper',
 '桉油醇樟':'oil-ravintsara','玫瑰草':'oil-palmarosa','檸檬':'oil-lemon','依蘭':'oil-ylang-ylang',
 '迷迭香':'oil-rosemary','德國洋甘菊':'oil-german-chamomile','羅馬洋甘菊':'oil-roman-chamomile',
 '百里香':'oil-thyme','香蜂草':'oil-melissa','甜羅勒':'oil-sweet-basil','甜茴香':'oil-sweet-fennel',
 '綠薄荷':'oil-spearmint','穗花薰衣草':'oil-spike-lavender','醒目薰衣草':'oil-lavandin',
 '西洋蓍草':'oil-yarrow','黑雲杉':'oil-black-spruce','檸檬尤加利':'oil-lemon-eucalyptus','雪松':'oil-cedarwood',
}
SLUGNAME = {
 'index':'精油基礎','numerology':'生命靈數','numerology-vs-fortune-telling':'算命 vs 生命靈數',
 'safety':'精油安全','blend':'調配精油','aromatherapy':'芳療應用','encyclopedia':'精油大百科',
}

# 療效詞 → 中性香氛/保養語氣（資料層去醫療宣稱，比只靠 prompt 可靠）
SANITIZE = [
    ('抗病毒', '清新淨化'), ('抗菌消炎', '清新淨化'), ('抗菌', '清新淨化'), ('殺菌', '清新淨化'),
    ('抗真菌', '清新淨化'), ('抗發炎', '舒緩'), ('消炎', '舒緩'),
    ('化解黏液', '呼吸清新'), ('化痰', '呼吸清新'), ('祛痰', '呼吸清新'), ('止咳', '呼吸放鬆'),
    ('促進呼吸道暢通', '帶來呼吸清新感'), ('改善痤瘡', '肌膚保養'), ('抗痘', '肌膚保養'),
    ('調經', '經期前後香氛陪伴'), ('通經', '經期前後香氛陪伴'),
    ('止痛', '放鬆'), ('鎮痛', '放鬆'), ('退燒', '清涼舒適'), ('抗憂鬱', '情緒放鬆'),
    ('降血壓', '放鬆'), ('治療', '護理'), ('治癒', '呵護'), ('根治', '呵護'),
]
def sanitize(s):
    for bad, good in SANITIZE:
        s = s.replace(bad, good)
    return s

# slug → 中文名（canonical，第一個出現者）；給頁面摘要的 oil-* 條目用中文當問法
REV_SLUG = {}
for _zh, _s in SLUG.items():
    REV_SLUG.setdefault(_s, _zh)

kb = []
seen = set()
def add(q, a, url, tags, source='site'):
    a = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', a)).strip()
    a = sanitize(a)
    if not a or len(a) < 8: return
    key = q + '|' + url
    if key in seen: return
    seen.add(key)
    kb.append({'id': 'kb%03d' % len(kb), 'q': q, 'a': a, 'url': url, 'tags': tags, 'source': source})

# 1) 精油事實（有完整指南頁的優先）
oils = json.load(open(os.path.join(ROOT, 'data', 'oils.json'), encoding='utf-8'))
for o in oils:
    zh = o.get('zh', '')
    slug = SLUG.get(zh)
    url = f'{SITE}/{slug}/' if slug else f'{SITE}/oil/{o["id"]}/'
    safety = (o.get('safetyText') or '').strip()
    a = f'{zh}（{o.get("latin","")}）屬{o.get("family","")}，主要成分：{o.get("components","")}。常見芳療應用：{o.get("effects","")}。'
    if safety: a += f'安全提醒：{safety}'
    # 有完整指南頁的 46 支＝常見精油（site，正常權重）；其餘 300 支冷門品種＝datasheet（檢索降權，避免霸佔）
    src = 'site' if slug else 'datasheet'
    add(f'{zh}精油', a, url, [zh, o.get('family', ''), '精油'] + (o.get('tags') or []), source=src)
    if slug:  # 完整指南頁再給一條別名問法
        add(f'{zh}精油的功效與用法', a, url, [zh, '功效', '用法'], source='site')

# 2) 頁面摘要（本站原創 definition-first）
ps = open(os.path.join(ROOT, 'app', 'lib', 'pageSummaries.ts'), encoding='utf-8').read()
for m in re.finditer(r"'([a-z0-9-]+)':\s*\n?\s*'([^']+)'", ps):
    slug, summ = m.group(1), m.group(2)
    name = SLUGNAME.get(slug) or SLUG and None
    if slug in SLUGNAME:
        url = f'{SITE}/{slug}/'; q = f'{SLUGNAME[slug]}是什麼'
    elif slug.startswith('oil-'):
        url = f'{SITE}/{slug}/'; q = f'{REV_SLUG.get(slug, slug[4:])}精油'
    elif slug.startswith('article-'):
        url = f'{SITE}/{slug}/'; q = summ[:14]
    else:
        url = f'{SITE}/{slug}/'; q = summ[:14]
    add(q, summ, url, [slug], source='site-summary')

# 2.5) 確保 46 支常見精油（有完整指南頁）都有「中文名」kb 條目
#      （oils.json 可能缺某些常見油，如甜橙；補一條保底，讓客服 AI 找得到）
by_zh = {o.get('zh'): o for o in oils}
for zh, slug in SLUG.items():
    url = f'{SITE}/{slug}/'
    if (f'{zh}精油' + '|' + url) in seen:
        continue
    o = by_zh.get(zh)
    if o:
        a = f'{zh}（{o.get("latin","")}）屬{o.get("family","")}，主要成分：{o.get("components","")}。常見芳療應用：{o.get("effects","")}。'
    else:
        a = f'{zh}精油是常見的芳療精油，可作為香氛陪伴與肌膚保養使用。完整成分、香氣與用法請見頁面。'
    add(f'{zh}精油', a, url, [zh, '精油'], source='site')

# 3) 文章 FAQ（reference/*_faq.json，客服 QA 對）
import glob
FAQ_URL = {'rose': f'{SITE}/oil-rose/'}
for fp in glob.glob(os.path.join(ROOT, 'reference', '*_faq.json')):
    base = os.path.basename(fp)
    url = next((u for k, u in FAQ_URL.items() if k in base), '')
    try:
        for f in json.load(open(fp, encoding='utf-8')):
            add(f.get('q', ''), f.get('a', ''), url, [f.get('cat', ''), 'FAQ'], source='site-faq')
    except Exception as e:
        print('FAQ 讀取失敗', base, e)

# 4) 保留後台手動新增/訓練的條目
if os.path.exists(OUT):
    try:
        old = json.load(open(OUT, encoding='utf-8'))
        for e in old:
            if e.get('source') == 'admin' and (e.get('q','') + '|' + e.get('url','')) not in seen:
                e['id'] = 'kb%03d' % len(kb); kb.append(e)
    except Exception: pass

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(kb, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'kb 條目：{len(kb)} → {OUT}')
print('範例:', json.dumps(kb[0], ensure_ascii=False)[:160])
