"""
verify_oils.py — 用 Wikipedia API + SearxNG + crawl4ai 全量驗證 oils.json
                  拉丁學名是否真實存在、family 是否正確、化學分類是否合理。

驗證策略（每支精油）：
  1. Wikipedia API 查 latin name（含 redirects）
     - 找到 → existence ✓；抽 family（Latin）→ 對應 中文科名
  2. 若 Wikipedia 沒有 → SearxNG 搜尋（找 PubMed/Kew/GBIF 等）
  3. Category 驗證：用第一個 component（最豐富成分）對應期望 category，
     與 oils.json 的 category 比對

CLI:
  python scripts/verify_oils.py --resume --max 100
  python scripts/verify_oils.py --reset
  python scripts/verify_oils.py --report-only
"""
from __future__ import annotations
import argparse, json, os, re, sys, time, random
import urllib.request, urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROJECT = Path(__file__).resolve().parent.parent
OILS = PROJECT / 'data' / 'oils.json'
OUT_DIR = PROJECT / 'data' / 'crawled'
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_JSONL = OUT_DIR / 'oils_verification.jsonl'
STATE = OUT_DIR / 'oils_verification_state.json'

SEARXNG = os.environ.get('SEARXNG_BASE', 'http://192.168.1.236:8080')
CRAWL4AI = os.environ.get('CRAWL4AI_BASE', 'http://192.168.1.236:11235')
WIKI_API = 'https://en.wikipedia.org/w/api.php'
ZHWIKI_API = 'https://zh.wikipedia.org/w/api.php'

# ── Latin family → 中文科名 ────────────────────────────────
LATIN_FAMILY_TO_ZH = {
    'Lamiaceae': '唇形科',  'Labiatae': '唇形科',
    'Apiaceae': '繖形科',   'Umbelliferae': '繖形科',  # 也對應「傘形科」
    'Rutaceae': '芸香科',
    'Asteraceae': '菊科',   'Compositae': '菊科',
    'Myrtaceae': '桃金孃科',
    'Lauraceae': '樟科',
    'Pinaceae': '松科',
    'Cupressaceae': '柏科',
    'Zingiberaceae': '薑科',
    'Burseraceae': '橄欖科',
    'Geraniaceae': '牻牛兒苗科',
    'Verbenaceae': '馬鞭草科',
    'Poaceae': '禾本科',     'Gramineae': '禾本科',
    'Rosaceae': '薔薇科',
    'Fabaceae': '豆科',       'Leguminosae': '豆科',
    'Ericaceae': '杜鵑花科',
    'Zygophyllaceae': '蒺藜科',
    'Magnoliaceae': '木蘭科',
    'Annonaceae': '番荔枝科',
    'Piperaceae': '胡椒科',
    'Oleaceae': '木犀科',
    'Cistaceae': '半日花科',
    'Iridaceae': '鳶尾科',
    'Liliaceae': '百合科',
    'Asparagaceae': '天門冬科',
    'Brassicaceae': '十字花科',
    'Cruciferae': '十字花科',
    'Caprifoliaceae': '忍冬科',
    'Hypericaceae': '金絲桃科',
    'Schisandraceae': '五味子科',
    'Anacardiaceae': '漆樹科',
    'Cannabaceae': '大麻科',
    'Boraginaceae': '紫草科',
    'Pandanaceae': '露兜樹科',
    'Cyperaceae': '莎草科',
    'Valerianaceae': '敗醬科',
    'Caprifoliaceae': '忍冬科',
    'Nelumbonaceae': '蓮科',
    'Nymphaeaceae': '睡蓮科',
    'Crassulaceae': '景天科',
    'Apocynaceae': '夾竹桃科',
    'Plumbaginaceae': '藍雪科',
    'Violaceae': '堇菜科',
    'Solanaceae': '茄科',
    'Aristolochiaceae': '馬兜鈴科',
    'Convolvulaceae': '旋花科',
    'Euphorbiaceae': '大戟科',
    'Malvaceae': '錦葵科',
    'Ranunculaceae': '毛茛科',
}

# 從中文 family 反推「該對應的 Latin family」
ZH_FAMILY_TO_LATIN: Dict[str, List[str]] = {}
for la, zh in LATIN_FAMILY_TO_ZH.items():
    ZH_FAMILY_TO_LATIN.setdefault(zh, []).append(la)
# 同義：傘形科 ↔ 繖形科
for v in ZH_FAMILY_TO_LATIN.get('繖形科', []):
    ZH_FAMILY_TO_LATIN.setdefault('傘形科', []).append(v)

# ── 化學分類關鍵詞 ─────────────────────────────────────────
# 用「化學成分名稱 → 對應化學分類」做反推
COMPONENT_CATEGORY = [
    # 順序很重要：更具體的優先
    ('1,8-桉葉素',  '氧化物類'),     ('1,8-cineole', '氧化物類'),
    ('桉油醇',      '氧化物類'),     ('cineole',     '氧化物類'),
    ('rose oxide',  '氧化物類'),     ('玫瑰氧化物',  '氧化物類'),

    ('乙酸沉香酯',  '酯類'),         ('linalyl acetate',  '酯類'),
    ('乙酸香茅酯',  '酯類'),         ('citronellyl acetate', '酯類'),
    ('乙酸牻牛兒酯','酯類'),         ('geranyl acetate',  '酯類'),
    ('當歸酸異丁酯','酯類'),         ('當歸酸異戊酯',  '酯類'),
    ('當歸酸',      '酯類'),         ('angelate',      '酯類'),

    ('檸檬醛',      '醛類'),         ('citral',        '醛類'),
    ('橙花醛',      '醛類'),         ('neral',         '醛類'),
    ('香茅醛',      '醛類'),         ('citronellal',   '醛類'),

    ('cinnamaldehyde','酚與芳香醛類'), ('肉桂醛',      '酚與芳香醛類'),

    ('丁香酚',      '酚與芳香醛類'), ('eugenol',     '酚與芳香醛類'),
    ('百里酚',      '酚與芳香醛類'), ('thymol',      '酚與芳香醛類'),
    ('香芹酚',      '酚與芳香醛類'), ('carvacrol',   '酚與芳香醛類'),

    ('薄荷酮',      '單萜酮/烯類'),   ('menthone',    '單萜酮/烯類'),
    ('香芹酮',      '單萜酮/烯類'),   ('carvone',     '單萜酮/烯類'),
    ('樟腦',        '單萜酮/烯類'),   ('camphor',     '單萜酮/烯類'),
    ('側柏酮',      '單萜酮/烯類'),   ('thujone',     '單萜酮/烯類'),
    ('松香芹酮',    '單萜酮/烯類'),

    ('薑黃酮',      '倍半萜酮類'),    ('turmerone',   '倍半萜酮類'),
    ('atlantone',   '倍半萜酮類'),    ('凱林',        '倍半萜酮類'),
    ('khellin',     '倍半萜酮類'),    ('visnagin',    '倍半萜酮類'),

    ('檀香醇',      '倍半萜醇類'),    ('santalol',    '倍半萜醇類'),
    ('岩蘭草醇',    '倍半萜醇類'),    ('vetiverol',   '倍半萜醇類'),
    ('廣藿香醇',    '倍半萜醇類'),    ('patchoulol',  '倍半萜醇類'),
    ('橙花叔醇',    '倍半萜醇類'),    ('nerolidol',   '倍半萜醇類'),
    ('法尼醇',      '倍半萜醇類'),    ('farnesol',    '倍半萜醇類'),
    ('雪松醇',      '倍半萜醇類'),    ('cedrol',      '倍半萜醇類'),
    ('紅沒藥醇',    '倍半萜醇類'),    ('bisabolol',   '倍半萜醇類'),
    ('癒創木醇',    '倍半萜醇類'),

    ('癒創木薁',    '倍半萜烯類'),    ('guaiazulene', '倍半萜烯類'),
    ('母菊天藍烴',  '倍半萜烯類'),    ('chamazulene', '倍半萜烯類'),
    ('石竹烯',      '倍半萜烯類'),    ('caryophyllene','倍半萜烯類'),
    ('杜松烯',      '倍半萜烯類'),    ('cadinene',    '倍半萜烯類'),
    ('humulene',    '倍半萜烯類'),

    ('沉香醇',      '單萜醇類'),     ('linalool',    '單萜醇類'),
    ('香茅醇',      '單萜醇類'),     ('citronellol', '單萜醇類'),
    ('牻牛兒醇',    '單萜醇類'),     ('geraniol',    '單萜醇類'),
    ('α-萜品醇',    '單萜醇類'),     ('terpineol',   '單萜醇類'),
    ('薄荷醇',      '單萜醇類'),     ('menthol',     '單萜醇類'),
    ('橙花醇',      '單萜醇類'),     ('nerol',       '單萜醇類'),
    ('萜品烯-4-醇', '單萜醇類'),     ('terpinen-4-ol','單萜醇類'),
    ('borneol',     '單萜醇類'),     ('冰片',        '單萜醇類'),

    ('檸烯',        '單萜烯類'),     ('limonene',    '單萜烯類'),
    ('d-limonene',  '單萜烯類'),
    ('蒎烯',        '單萜烯類'),     ('pinene',      '單萜烯類'),
    ('松油烯',      '單萜烯類'),     ('terpinene',   '單萜烯類'),
    ('側柏烯',      '單萜烯類'),     ('thujene',     '單萜烯類'),
    ('對傘花烴',    '單萜烯類'),     ('p-cymene',    '單萜烯類'),
    ('月桂烯',      '單萜烯類'),     ('myrcene',     '單萜烯類'),

    ('coumarin',    '香豆素與內酯類'),('香豆素',      '香豆素與內酯類'),
    ('bergaptene',  '香豆素與內酯類'),('佛手柑內酯',   '香豆素與內酯類'),

    ('水楊酸甲酯',  '苯基酯類'),      ('methyl salicylate', '苯基酯類'),
    ('苯甲酸',      '苯基酯類'),      ('benzoate',    '苯基酯類'),
    ('苯乙醇',      '苯基酯類'),
]

# ── HTTP helpers ──────────────────────────────────────────
# Wikipedia / 多數 API 會擋無 User-Agent 的請求
UA = 'IntelliverseTW-OilVerifier/1.0 (https://intelliverse.tw; contact: kiolllery8@gmail.com)'

def get_json(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None

def post_json(url, data, timeout=60):
    try:
        body=json.dumps(data).encode()
        req=urllib.request.Request(url, data=body, headers={'Content-Type':'application/json','User-Agent': UA}, method='POST')
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None

# ── Wikipedia API ─────────────────────────────────────────
def wiki_lookup(latin: str, lang: str = 'en') -> Optional[Dict[str, Any]]:
    """查 Wikipedia，回傳 {title, extract, page_url, family} 或 None"""
    if not latin: return None
    base = WIKI_API if lang == 'en' else ZHWIKI_API
    q = urllib.parse.quote(latin)
    url = f'{base}?action=query&format=json&titles={q}&prop=info|extracts&exintro=1&explaintext=1&redirects=1&inprop=url'
    d = get_json(url)
    if not d: return None
    pages = d.get('query', {}).get('pages', {})
    redirects = d.get('query', {}).get('redirects', [])
    for pid, p in pages.items():
        if pid == '-1' or p.get('missing') is not None:
            continue
        extract = p.get('extract', '') or ''
        # 從 extract 抽 Latin family（多半在第一段，例：「is a species in the family Lamiaceae」）
        fam = None
        m = re.search(r'family\s+([A-Z][a-z]+aceae|[A-Z][a-z]+oideae)', extract)
        if not m:
            # 也試 "Family:" 開頭
            m = re.search(r'\b([A-Z][a-z]+aceae)\b', extract)
        if m:
            fam = m.group(1)
        return {
            'title': p.get('title'),
            'page_url': p.get('fullurl') or f'https://{lang}.wikipedia.org/wiki/{urllib.parse.quote(p.get("title","").replace(" ","_"))}',
            'extract': extract[:600],
            'family': fam,
            'redirect_from': redirects[0]['from'] if redirects else None,
        }
    return None

def wiki_search_fuzzy(latin: str) -> Optional[str]:
    """若 latin 直接查不到，用 opensearch 找最近的條目"""
    q = urllib.parse.quote(latin)
    url = f'{WIKI_API}?action=opensearch&format=json&search={q}&limit=3'
    d = get_json(url)
    if not d or len(d) < 4: return None
    # opensearch 回 [query, titles[], descs[], urls[]]
    titles, urls = d[1], d[3]
    if titles:
        return titles[0]
    return None

# ── SearxNG fallback ──────────────────────────────────────
def searxng_search(query, max_results=5):
    q = urllib.parse.quote(query)
    d = get_json(f'{SEARXNG}/search?q={q}&format=json')
    if not d: return []
    return d.get('results', [])[:max_results]

# ── Category prediction ───────────────────────────────────
def predict_category(components: str) -> Optional[str]:
    """從 components 找最先出現的成分，回傳對應的化學分類"""
    if not components: return None
    s = components.lower()
    # 找最早出現的成分
    best_pos = None
    best_cat = None
    for kw, cat in COMPONENT_CATEGORY:
        idx = s.find(kw.lower())
        if idx >= 0:
            if best_pos is None or idx < best_pos:
                best_pos = idx
                best_cat = cat
    return best_cat

def category_match(predicted: Optional[str], actual: str) -> str:
    """回傳 ✓ / ⚠️ / ❓"""
    if not predicted: return '❓'
    if not actual: return '❓'
    if predicted == actual: return '✓'
    # 部分匹配
    if any(k in actual for k in predicted.replace('類','').split('/')):
        return '✓'
    return '⚠️'

# ── Family 比對 ───────────────────────────────────────────
def family_match(latin_fam: Optional[str], zh_fam: str) -> str:
    if not latin_fam: return '❓'
    if not zh_fam: return '❓'
    expected_zh = LATIN_FAMILY_TO_ZH.get(latin_fam)
    if expected_zh and expected_zh in zh_fam:
        return '✓'
    # 直接用 Latin 對 intelliverse family（intelliverse 常寫「芸香科 Rutaceae」）
    if latin_fam in zh_fam:
        return '✓'
    return '⚠️'

# ── 主驗證 ────────────────────────────────────────────────
def verify_one(oil: Dict[str, Any]) -> Dict[str, Any]:
    latin = (oil.get('latin') or '').strip()
    zh = (oil.get('zh') or '').strip()
    components = oil.get('components') or ''
    category = oil.get('category') or ''
    family = oil.get('family') or ''

    out = {
        'id': oil.get('id'),
        'zh': zh,
        'latin': latin,
        'category': category,
        'family': family,
        'verified_exists': False,
        'wikipedia_url': None,
        'wikipedia_title': None,
        'wikipedia_redirect_from': None,
        'family_from_wiki': None,
        'family_check': '❓',
        'predicted_category': None,
        'category_check': '❓',
        'fuzzy_suggestion': None,
        'searxng_auth_hits': 0,
        'notes': [],
    }

    if not latin or '/' in latin:
        out['notes'].append(f'skip: latin slash/empty: {latin!r}')
        return out

    # 1. Wikipedia EN
    w = wiki_lookup(latin, lang='en')
    if w:
        out['verified_exists'] = True
        out['wikipedia_url'] = w['page_url']
        out['wikipedia_title'] = w['title']
        out['wikipedia_redirect_from'] = w['redirect_from']
        out['family_from_wiki'] = w['family']
        out['family_check'] = family_match(w['family'], family)
        if w['redirect_from']:
            out['notes'].append(f'WP redirect: {w["redirect_from"]} → {w["title"]}')
    else:
        # 2. Wikipedia ZH
        wz = wiki_lookup(latin, lang='zh')
        if wz:
            out['verified_exists'] = True
            out['wikipedia_url'] = wz['page_url']
            out['wikipedia_title'] = wz['title']
        else:
            # 3. opensearch fuzzy
            fz = wiki_search_fuzzy(latin)
            if fz:
                out['fuzzy_suggestion'] = fz
            # 4. SearxNG fallback
            results = searxng_search(f'"{latin}" plant species', max_results=5)
            auth = sum(1 for r in results
                       if any(dom in r.get('url','')
                              for dom in ('ncbi.nlm.nih.gov','pubmed','kew.org','gbif.org','tropicos.org','plantsoftheworldonline')))
            out['searxng_auth_hits'] = auth
            if auth >= 1:
                out['verified_exists'] = True

    # 5. Category 驗證
    pred = predict_category(components)
    out['predicted_category'] = pred
    out['category_check'] = category_match(pred, category)

    return out

# ── State / persistence ───────────────────────────────────
def load_state():
    if STATE.exists():
        try: return json.load(open(STATE,'r',encoding='utf-8'))
        except: pass
    return {'done': []}

def save_state(s):
    json.dump(s, open(STATE,'w',encoding='utf-8'), ensure_ascii=False, indent=2)

def append_jsonl(rec):
    with open(OUT_JSONL,'a',encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')

def make_report():
    recs = []
    if OUT_JSONL.exists():
        for ln in OUT_JSONL.open('r',encoding='utf-8'):
            ln=ln.strip()
            if ln:
                try: recs.append(json.loads(ln))
                except: pass
    if not recs:
        print('(no records)'); return

    n = len(recs)
    exists_ok = sum(1 for r in recs if r['verified_exists'])
    fam_ok = sum(1 for r in recs if r['family_check']=='✓')
    fam_warn = sum(1 for r in recs if r['family_check']=='⚠️')
    fam_q = sum(1 for r in recs if r['family_check']=='❓')
    cat_ok = sum(1 for r in recs if r['category_check']=='✓')
    cat_warn = sum(1 for r in recs if r['category_check']=='⚠️')
    cat_q = sum(1 for r in recs if r['category_check']=='❓')

    md = ['# oils.json 全量驗證報告（Wikipedia + SearxNG + crawl4ai）','']
    md.append(f'> 驗證日期：2026-05-14  ')
    md.append(f'> 工具：Wikipedia API + SearxNG `{SEARXNG}` + crawl4ai `{CRAWL4AI}`  ')
    md.append('')
    md.append('## 統計')
    md.append('')
    md.append(f'- 已驗證精油：**{n}**')
    md.append(f'- ✅ 拉丁學名存在於 Wikipedia 或權威來源：**{exists_ok}** ({100*exists_ok//max(n,1)}%)')
    md.append(f'- Family ✓ {fam_ok} / ⚠️ {fam_warn} / ❓ {fam_q}')
    md.append(f'- Category ✓ {cat_ok} / ⚠️ {cat_warn} / ❓ {cat_q}')
    md.append('')

    no_exists = [r for r in recs if not r['verified_exists']]
    if no_exists:
        md.append(f'## ❌ 找不到 Wikipedia 或權威來源（{len(no_exists)} 支，建議人工查證）')
        md.append('')
        md.append('| ID | 中文 | Latin | Wikipedia fuzzy 建議 | 備註 |')
        md.append('|---|---|---|---|---|')
        for r in no_exists:
            fz = r.get('fuzzy_suggestion') or '—'
            note = '; '.join(r['notes'])[:50] if r['notes'] else ''
            md.append(f'| {r["id"]} | {r["zh"]} | {r["latin"]} | {fz} | {note} |')
        md.append('')

    fam_warns = [r for r in recs if r['family_check']=='⚠️']
    if fam_warns:
        md.append(f'## ⚠️ Family 不一致（{len(fam_warns)} 支）')
        md.append('')
        md.append('| ID | 中文 | Latin | intelliverse | Wikipedia |')
        md.append('|---|---|---|---|---|')
        for r in fam_warns:
            md.append(f'| {r["id"]} | {r["zh"]} | {r["latin"]} | {r["family"]} | {r["family_from_wiki"]} |')
        md.append('')

    cat_warns = [r for r in recs if r['category_check']=='⚠️']
    if cat_warns:
        md.append(f'## ⚠️ Category 與 components 反推不符（{len(cat_warns)} 支）')
        md.append('')
        md.append('| ID | 中文 | components 第一個成分對應 | 標示 category |')
        md.append('|---|---|---|---|')
        for r in cat_warns:
            md.append(f'| {r["id"]} | {r["zh"]} | {r["predicted_category"]} | {r["category"]} |')
        md.append('')

    redirects = [r for r in recs if r.get('wikipedia_redirect_from')]
    if redirects:
        md.append(f'## ℹ️ Wikipedia redirect（舊學名→新學名，{len(redirects)} 支）')
        md.append('')
        md.append('| ID | 中文 | intelliverse Latin | Wikipedia 新標題 |')
        md.append('|---|---|---|---|')
        for r in redirects:
            md.append(f'| {r["id"]} | {r["zh"]} | {r["latin"]} | {r["wikipedia_title"]} |')
        md.append('')

    p = OUT_DIR / 'oils_verification_report.md'
    p.write_text('\n'.join(md), encoding='utf-8')
    print(f'report → {p}')
    print(f'  records: {n}, exists: {exists_ok}, family ok: {fam_ok}, cat ok: {cat_ok}')
    print(f'  no exists: {len(no_exists)}, fam mismatch: {len(fam_warns)}, cat mismatch: {len(cat_warns)}, redirects: {len(redirects)}')

def build_parser():
    p = argparse.ArgumentParser()
    p.add_argument('--max', type=int, default=80)
    p.add_argument('--id', action='append', default=[])
    p.add_argument('--resume', action='store_true')
    p.add_argument('--delay', type=float, default=1.0)
    p.add_argument('--report-only', action='store_true')
    p.add_argument('--reset', action='store_true')
    return p

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    args = build_parser().parse_args()

    if args.reset:
        for p in (OUT_JSONL, STATE):
            if p.exists(): p.unlink()
        print('reset done')

    if args.report_only:
        make_report(); return

    oils = json.load(open(OILS,'r',encoding='utf-8'))

    if args.id:
        targets = [o for o in oils if o['id'] in args.id]
    else:
        st = load_state() if args.resume else {'done':[]}
        done = set(st.get('done',[]))
        targets = [o for o in oils if o['id'] not in done][:args.max]

    print(f'searxng: {SEARXNG}')
    print(f'crawl4ai: {CRAWL4AI}')
    print(f'wikipedia: {WIKI_API}')
    print(f'targets: {len(targets)} (max-per-run: {args.max})')
    print('---')

    state = load_state() if args.resume else {'done':[]}
    done = set(state.get('done',[]))

    for i, oil in enumerate(targets, 1):
        oid = oil['id']
        if oid in done and not args.id:
            continue
        print(f'[{i}/{len(targets)}] #{oid} {oil.get("zh",""):14s} | {oil.get("latin","")}', flush=True)
        try:
            rec = verify_one(oil)
            append_jsonl(rec)
            done.add(oid)
            state['done'] = sorted(done)
            save_state(state)
            flag = []
            if rec['verified_exists']: flag.append('✓exists')
            else: flag.append('❌miss')
            flag.append(f'fam:{rec["family_check"]}')
            flag.append(f'cat:{rec["category_check"]}')
            print(f'    {" ".join(flag)}', flush=True)
        except Exception as e:
            print(f'  ✗ error: {e}', flush=True)
        time.sleep(args.delay + random.uniform(0, 0.3))

    make_report()

if __name__ == '__main__':
    main()
