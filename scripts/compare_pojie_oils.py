# -*- coding: utf-8 -*-
"""把《破解精油》萃取出的事實，對上本站 data/oils.json，列出待人工判斷的差異。

只產出報告，**不會改動 oils.json**。
輸出：reference/破解精油_vs_oils_差異.md
"""
import json, os, sys, io, re, unicodedata
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'C:\Users\User\Desktop\essential-oil-guide'
REF = os.path.join(ROOT, 'reference')


def norm_latin(s):
    """拉丁學名正規化：小寫、去 var./ssp./作者名、只留屬＋種。

    ⚠ 化學型（ct.）與萃取部位不併進來，另由 qualifier() 取出——
    同種不同化學型（如 Cinnamomum camphora ct. linalool vs 白色樟腦油）
    安全性天差地遠，不能當成同一支油。
    """
    if not s:
        return ''
    s = unicodedata.normalize('NFKC', str(s)).lower()
    s = re.split(r'\bct\.?\b|\(', s)[0]          # 砍掉化學型與括號補述
    s = re.sub(r'\b(var|subsp|ssp|f|cv)\.?\s*', ' ', s)
    s = re.sub(r'[^a-z\s]', ' ', s)
    parts = [p for p in s.split() if len(p) > 1]
    return ' '.join(parts[:2])


def qualifier(s):
    """取出化學型 / 萃取部位等限定詞；沒有就回空字串。"""
    if not s:
        return ''
    t = unicodedata.normalize('NFKC', str(s)).lower()
    bits = []
    m = re.search(r'\bct\.?\s*([a-z\-]+)', t)
    if m:
        bits.append('ct:' + m.group(1))
    m = re.search(r'\((leaf|leaves|peel|rind|fruit|flower|wood|root|seed|bark)[^)]*\)', t)
    if m:
        bits.append('part:' + m.group(1))
    return '|'.join(bits)


def zh_qualifier(s):
    """從中文名判斷部位／型別，補拉丁名沒寫的情況。"""
    t = str(s or '')
    bits = []
    for kw, tag in (('葉', 'part:leaf'), ('果皮', 'part:peel'), ('花', 'part:flower'),
                    ('根', 'part:root'), ('籽', 'part:seed'), ('種子', 'part:seed'),
                    ('木', 'part:wood')):
        if kw in t:
            bits.append(tag)
            break
    return '|'.join(bits)


def norm_zh(s):
    """中文品名正規化。

    書裡的寫法很雜：「多香果 Pimento berry」「橘（桔）與柑」「玫瑰原精 Rose」，
    要先剝掉英文俗名、括號補述與「精油／原精」字尾，才不會把站上有的油
    誤判成缺漏。
    """
    s = unicodedata.normalize('NFKC', str(s or '')).strip()
    s = re.sub(r'[（(][^）)]*[）)]', '', s)            # 括號補述
    s = re.sub(r'[A-Za-z][A-Za-z\s\'\-\.]*$', '', s)  # 尾端英文俗名
    s = re.sub(r'[／/、].*$', '', s)                   # 「A／B」只取第一個
    s = re.sub(r'(精油|原精|純露|花油)$', '', s.strip())
    return s.strip()


with open(os.path.join(ROOT, 'data', 'oils.json'), encoding='utf-8') as f:
    site = json.load(f)
with open(os.path.join(REF, '破解精油_oil_facts.json'), encoding='utf-8') as f:
    book = json.load(f)['oils']

print(f'網站 {len(site)} 筆、書中 {len(book)} 支')

by_zh = defaultdict(list)
by_latin = defaultdict(list)
for o in site:
    by_zh[norm_zh(o.get('zh'))].append(o)
    nl = norm_latin(o.get('latin'))
    if nl:
        by_latin[nl].append(o)

# 網站自身的重複品名
dupes = {k: v for k, v in by_zh.items() if len(v) > 1 and k}

latin_diff, safety_flag, comp_flag, missing, ct_split = [], [], [], [], []
matched = 0

for b in book:
    zh, bl = norm_zh(b['zh']), norm_latin(b.get('latin'))
    bq = qualifier(b.get('latin')) or zh_qualifier(b['zh'])
    cands = by_zh.get(zh)
    how = 'zh'
    if not cands and bl:
        # 只靠拉丁名配對時，化學型／部位不同就不算同一支油
        pool = by_latin.get(bl) or []
        cands = [o for o in pool
                 if (qualifier(o.get('latin')) or zh_qualifier(o.get('zh'))) == bq]
        how = 'latin'
        rejected = [o for o in pool if o not in cands]
        if rejected and not cands:
            ct_split.append({'zh': b['zh'], 'book_latin': b.get('latin'),
                             'book_q': bq or '（未標）', 'page': b.get('page'),
                             'site': '、'.join(f'{o.get("zh")}({o.get("id")}) '
                                               f'{qualifier(o.get("latin")) or zh_qualifier(o.get("zh")) or "（未標）"}'
                                               for o in rejected)})
    if not cands:
        missing.append(b)
        continue
    matched += 1
    s = cands[0]
    b['_how'] = how
    sl = norm_latin(s.get('latin'))
    if bl and sl and bl != sl:
        # 屬相同只是種不同 → 標為「同屬異種」，風險較高
        same_genus = bl.split()[:1] == sl.split()[:1]
        latin_diff.append({'zh': b['zh'], 'site_id': s.get('id'),
                           'site': s.get('latin'), 'book': b.get('latin'),
                           'page': b.get('page'), 'same_genus': same_genus})
    # 安全性：書中出現毒性字眼，但網站標 safe
    bs = ' '.join(str(b.get(k) or '') for k in ('safety', 'notes'))
    if s.get('safetyLevel') == 'safe':
        hits = []
        for m in re.finditer(r'毒性|有毒|禁用|禁忌|致癌|致敏|過敏|刺激|光敏|'
                             r'癲癇|流產|墮胎|抽搐|不適合|須小心|需注意|不可超過', bs):
            # 前 6 字若是否定詞（無毒、不刺激、毒性甚微…）就不算風險
            before = bs[max(0, m.start() - 6):m.start()]
            after = bs[m.end():m.end() + 4]
            if re.search(r'[無不非未]$|甚微$|極低$', before) or re.match(r'甚微|極低|很低', after):
                continue
            hits.append(bs[max(0, m.start() - 30):m.end() + 40])
        if hits:
            site_txt = str(s.get('safetyText') or '') + str(s.get('tags') or '')
            # 站上已經寫過同類警語就不必再提
            kws = set(re.findall(r'癲癇|孕婦|嬰幼兒|光敏|口服|過敏|氣喘|兒童', ' '.join(hits)))
            new_kws = [k for k in kws if k not in site_txt]
            if new_kws:
                safety_flag.append({
                    'zh': b['zh'], 'site_id': s.get('id'),
                    'site_level': s.get('safetyLevel'),
                    'site_text': (s.get('safetyText') or '')[:70],
                    'book': ' ／ '.join(hits[:2])[:220],
                    'new': '、'.join(sorted(new_kws)), 'page': b.get('page')})
    # 成分：抓出雙方各自的化學成分詞，看有沒有完全不交集
    def chems(t):
        return set(re.findall(
            r'[\u4e00-\u9fff]{2,6}(?:醇|酯|酮|醛|烯|酚|醚|氧化物|內酯|香豆素)', str(t or '')))
    cb, cs = chems(b.get('components')), chems(s.get('components'))
    if cb and cs and not (cb & cs):
        comp_flag.append({'zh': b['zh'], 'site_id': s.get('id'),
                          'site': s.get('components'), 'book': b.get('components'),
                          'page': b.get('page')})

L = ['# 《破解精油》× 本站 oils.json 差異報告', '',
     f'> 網站 {len(site)} 筆 vs 書中 {len(book)} 支；比對上 {matched} 支。',
     '> 產生方式：`scripts/compare_pojie_oils.py`（**只報告，不改資料**）。',
     '> ⚠️ 書也可能誤植或用舊分類。每一條都要人工判斷後才動 `oils.json`。', '']

L += ['## 一、拉丁學名不一致', '',
      '同物異名很常見（低風險）；**同屬異種**要特別看，不同種的安全性可能差很多。', '',
      '| 中文名 | 站上 id | 站上學名 | 書中學名 | 頁碼 | 風險 |', '|---|---|---|---|---|---|']
for d in sorted(latin_diff, key=lambda x: not x['same_genus']):
    risk = '⚠ 同屬異種' if d['same_genus'] else '同物異名？'
    L.append(f'| {d["zh"]} | {d["site_id"]} | *{d["site"]}* | *{d["book"]}* | {d["page"]} | {risk} |')
L.append('')

L += ['## 二、安全等級疑慮（書中提到風險、站上標 safe）', '',
      '| 中文名 | 站上 id | 站上等級 | 站上說明 | 書中敘述 | 頁碼 |', '|---|---|---|---|---|---|']
for d in safety_flag:
    L.append(f'| {d["zh"]} | {d["site_id"]} | `{d["site_level"]}` | {d["site_text"]} '
             f'| {d["book"]} | {d["page"]} |')
L.append('')

L += ['## 三、主要成分完全不交集', '',
      '通常代表其中一方張冠李戴，或講的是不同化學型（CT）。', '',
      '| 中文名 | 站上 id | 站上成分 | 書中成分 | 頁碼 |', '|---|---|---|---|---|']
for d in comp_flag:
    L.append(f'| {d["zh"]} | {d["site_id"]} | {d["site"]} | {d["book"]} | {d["page"]} |')
L.append('')

L += ['## 三之二、同種但化學型／部位不同（不可混為一談）', '',
      '拉丁學名同屬同種，但**化學型（ct.）或萃取部位不同**，安全性與用途可能天差地遠。',
      '這些沒有被算成「差異」，而是提醒你站上可能缺了另一個型別。', '',
      '| 書中名稱 | 書中學名 | 書中型別／部位 | 站上同種的是 | 頁碼 |', '|---|---|---|---|---|']
for d in ct_split:
    L.append(f'| {d["zh"]} | *{d["book_latin"]}* | {d["book_q"]} | {d["site"]} | {d["page"]} |')
L.append('')

# 同一支油可能在正文與附錄各出現一次（附錄多半沒印學名），依正規化名合併
miss_merged = {}
for b in missing:
    k = norm_zh(b['zh'])
    cur = miss_merged.get(k)
    if cur is None:
        miss_merged[k] = dict(b)
    else:  # 保留資訊較多的那筆，頁碼合併
        if len(str(b.get('latin') or '')) > len(str(cur.get('latin') or '')):
            pg = cur.get('page')
            cur.update(b)
            cur['page'] = f'{pg}、{b.get("page")}'
        else:
            cur['page'] = f'{cur.get("page")}、{b.get("page")}'

def near_matches(book_zh, book_latin):
    """找站上名稱或學名相近的既有條目，避免照清單重複建檔。"""
    k = norm_zh(book_zh)
    hits = []
    if len(k) >= 2:
        for o in site:
            sz = norm_zh(o.get('zh'))
            if sz and (k in sz or sz in k):
                hits.append(f'{o.get("zh")}({o.get("id")})')
    bl = norm_latin(book_latin)
    if bl and not hits:
        genus = bl.split()[0]
        for o in site:
            if norm_latin(o.get('latin')).startswith(genus + ' '):
                hits.append(f'{o.get("zh")}({o.get("id")})')
    return '、'.join(dict.fromkeys(hits)[:4] if isinstance(hits, dict)
                     else list(dict.fromkeys(hits))[:4])


L += ['## 四、書中有、站上沒有的精油', '',
      f'共 **{len(miss_merged)}** 支（{len(missing)} 筆原始紀錄合併後）。可評估是否補建 datasheet。',
      '最後一欄列出站上名稱或同屬的既有條目——有值的多半只是**命名不同**，不是真的缺，'
      '補建前先看這欄。', '',
      '| 中文名 | 拉丁學名 | 科屬 | 頁碼 | 站上相近條目 |',
      '|---|---|---|---|---|']
for k in sorted(miss_merged):
    b = miss_merged[k]
    near = near_matches(b['zh'], b.get('latin'))
    L.append(f'| {b["zh"]} | *{b.get("latin") or "—"}* | {b.get("family") or "—"} '
             f'| {b.get("page")} | {near or "—"} |')
L.append('')

L += ['## 五、oils.json 自身的重複品名', '',
      '同一個中文名有多筆，會讓內部連結與檢索指到不同頁。', '',
      '| 中文名 | 重複的 id | 各自學名 |', '|---|---|---|']
for k, v in sorted(dupes.items()):
    L.append(f'| {k} | {"、".join(str(x.get("id")) for x in v)} '
             f'| {"；".join(str(x.get("latin")) for x in v)} |')
L.append('')

out = os.path.join(REF, '破解精油_vs_oils_差異.md')
with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(L))

print(f'學名不一致 {len(latin_diff)}（其中同屬異種 {sum(1 for d in latin_diff if d["same_genus"])}）')
print(f'安全等級疑慮 {len(safety_flag)}')
print(f'成分不交集 {len(comp_flag)}')
print(f'站上缺少 {len(missing)}')
print(f'站上重複品名 {len(dupes)}')
print('✓', out)
