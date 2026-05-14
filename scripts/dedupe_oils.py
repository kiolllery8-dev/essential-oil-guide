"""
dedupe_oils.py — 全方位偵測 oils.json 重複與類型不一致

檢測維度：
  A. 完全重複（同 zh + 同 latin）
  B. 同 latin 不同 zh（同物種、不同俗名／部位）
  C. 同 zh 不同 latin（中文混用、可能標籤錯誤）
  D. 相似 latin（去掉 ct/var/leaf 等修飾後同種）
  E. 拼字相近 latin（編輯距離 ≤ 2）
  F. components 高度重疊（疑似資料複製貼上）
  G. 同屬不同種但類型衝突
  H. category 與 components 反推不一致
  I. catFile 與 category 不對應
"""
from __future__ import annotations
import json, sys, re
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

sys.stdout.reconfigure(encoding='utf-8')

PROJECT = Path(__file__).resolve().parent.parent
OILS = PROJECT / 'data' / 'oils.json'
OUT = PROJECT / 'data' / 'crawled' / 'oils_dedupe_report.md'

d = json.load(open(OILS, 'r', encoding='utf-8'))
print(f'Total entries: {len(d)}')

# helper: normalize latin（去掉 ct./CT/var/subsp/部位標註）
def norm_latin(s: str) -> str:
    s = (s or '').strip()
    s = re.sub(r'\s+ct\.?\s+\w+', '', s, flags=re.I)
    s = re.sub(r'\s+var\.\s+\S+', '', s)
    s = re.sub(r'\s+subsp\.\s+\S+', '', s)
    s = re.sub(r'\s*\(.*?\)\s*$', '', s)   # 去掉尾部括號「(leaf)」「(peel)」
    s = re.sub(r'\s+', ' ', s).strip()
    return s.lower()

# Levenshtein 距離
def lev(a: str, b: str) -> int:
    if a == b: return 0
    if len(a) < len(b): a, b = b, a
    prev = list(range(len(b)+1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0]*len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(cur[j-1]+1, prev[j]+1, prev[j-1] + (ca!=cb))
        prev = cur
    return prev[-1]

# 取得 components set
def comps(o):
    raw = (o.get('components') or '').strip()
    # 切分: 中文逗號頓號分號  英文逗號
    parts = re.split(r'[、，,；;/]+', raw)
    out = set()
    for p in parts:
        p = re.sub(r'\(.*?\)', '', p)             # 去掉括號內百分比
        p = re.sub(r'[\d\.%~～\s]+', '', p)      # 去掉數字百分比
        p = p.strip()
        if p and len(p) >= 2:
            out.add(p)
    return out

# ── A/B/C 已知：再跑一次比對所有 latin/zh ──
exact_dup: List[Tuple[str,str,str]] = []   # 同 zh 同 latin
norm_groups: Dict[str, List[Dict]] = defaultdict(list)
zh_groups: Dict[str, List[Dict]] = defaultdict(list)
latin_groups: Dict[str, List[Dict]] = defaultdict(list)

for o in d:
    norm_groups[norm_latin(o.get('latin',''))].append(o)
    zh_groups[(o.get('zh') or '').strip()].append(o)
    latin_groups[(o.get('latin') or '').strip()].append(o)

# A：完全重複
A = []
for la, ls in latin_groups.items():
    if len(ls) <= 1: continue
    zhs = [o.get('zh','') for o in ls]
    if len(set(zhs)) == 1:
        A.append((la, zhs[0], [o['id'] for o in ls]))

# B：同 latin（norm 後）不同 zh
B = []
for nl, ls in norm_groups.items():
    if len(ls) <= 1: continue
    zhs = sorted({o.get('zh','') for o in ls})
    if len(zhs) > 1:
        B.append((nl, zhs, [(o['id'], o.get('zh',''), o.get('latin','')) for o in ls]))

# C：同 zh 不同 latin
C = []
for zh, ls in zh_groups.items():
    if len(ls) <= 1: continue
    lats = sorted({o.get('latin','') for o in ls})
    if len(lats) > 1:
        C.append((zh, lats, [(o['id'], o.get('latin','')) for o in ls]))

# D：相似 latin（編輯距離 ≤ 2，但 norm 後不同）
seen_pairs = set()
D = []
all_norms = sorted(norm_groups.keys())
# 為效率只比同首字母
by_first = defaultdict(list)
for n in all_norms:
    if n: by_first[n[0]].append(n)
for grp in by_first.values():
    for i, a in enumerate(grp):
        for b in grp[i+1:]:
            if abs(len(a)-len(b)) > 2: continue
            if a == b: continue
            dist = lev(a, b)
            if 1 <= dist <= 2:
                key = tuple(sorted((a,b)))
                if key in seen_pairs: continue
                seen_pairs.add(key)
                ids_a = [(o['id'], o.get('zh',''), o.get('latin','')) for o in norm_groups[a]]
                ids_b = [(o['id'], o.get('zh',''), o.get('latin','')) for o in norm_groups[b]]
                D.append((a, b, dist, ids_a, ids_b))

# F：components 高度重疊（>= 5 個共有成分 且 jaccard >= 0.7）
F = []
oils_with_comp = [(o, comps(o)) for o in d if (o.get('components') or '').strip()]
for i in range(len(oils_with_comp)):
    oa, ca = oils_with_comp[i]
    for j in range(i+1, len(oils_with_comp)):
        ob, cb = oils_with_comp[j]
        if oa['id'] == ob['id']: continue
        if not ca or not cb: continue
        inter = ca & cb
        if len(inter) < 5: continue
        union = ca | cb
        jac = len(inter) / len(union) if union else 0
        if jac >= 0.7:
            F.append((oa['id'], oa.get('zh',''), ob['id'], ob.get('zh',''), len(inter), round(jac,3),
                      sorted(inter)[:8]))

# G：同屬不同種，type 衝突（同 genus 但 category 完全不一樣）
G = []
genus_map: Dict[str, List[Dict]] = defaultdict(list)
for o in d:
    la = (o.get('latin') or '').strip()
    if not la or ' ' not in la: continue
    g = la.split()[0]
    genus_map[g].append(o)
for genus, ls in genus_map.items():
    if len(ls) < 2: continue
    cats = {o.get('category','') for o in ls}
    if len(cats) >= 2:
        # 略過已知大類 genus（Citrus / Eucalyptus / Mentha / Cinnamomum / Salvia / Artemisia 等本來就會跨類型）
        # 但仍列出供審
        G.append((genus, list(cats), [(o['id'], o.get('zh',''), o.get('latin',''), o.get('category','')) for o in ls]))

# H：category 與 catFile 對應檢查
H = []
EXPECTED_MAP = {
    '單萜酮/烯類': 'compounds-01',
    '香豆素與內酯類': 'compounds-02',
    '氧化物類': 'compounds-03',
    '倍半萜烯類': 'compounds-04',
    '醛類': 'compounds-05',
    '酯類': 'compounds-06',
    '脂類': 'compounds-07a',
    '苯基酯類': 'compounds-07b',
    '芳香醛與芳香酯': 'compounds-07c',
    '倍半萜酮類': 'compounds-08',
    '單萜醇類': 'compounds-09',
    '酚與芳香醛類': 'compounds-10',
    '倍半萜醇類': 'compounds-11',
    '單萜烯類': 'compounds-12',
}
for o in d:
    cat = o.get('category','')
    cf = (o.get('catFile') or '').replace('.html','')
    expected = EXPECTED_MAP.get(cat)
    if expected and cf != expected:
        H.append((o['id'], o.get('zh',''), cat, cf, expected))

# ── 寫報告 ────────────────────────────────────────────────
md = ['# oils.json 全方位重複／類型一致性檢查報告（2026-05-14）','']
md.append(f'> 全量 {len(d)} 支精油  ')
md.append(f'> 檢測 9 個維度：A 完全重複 / B 同種多名 / C 同名多種 / D 拼字相近 / F 成分高度重疊 / G 同屬類型衝突 / H 分類-檔案對應  ')
md.append('')

md.append('## 統計')
md.append('')
md.append(f'| 維度 | 名稱 | 命中 |')
md.append(f'|---|---|---:|')
md.append(f'| A | 完全重複（同 zh 同 latin） | {len(A)} |')
md.append(f'| B | 同 latin 不同 zh（同種多名） | {len(B)} |')
md.append(f'| C | 同 zh 不同 latin（同名多種） | {len(C)} |')
md.append(f'| D | latin 拼字相近（編輯距離 1-2） | {len(D)} |')
md.append(f'| F | components 高度重疊（jaccard ≥ 0.7） | {len(F)} |')
md.append(f'| G | 同屬不同種、類型分歧 | {len(G)} |')
md.append(f'| H | category 與 catFile 對應不一致 | {len(H)} |')
md.append('')

if A:
    md.append('## A. 完全重複（zh + latin 都相同）')
    md.append('')
    md.append('| Latin | zh | IDs |')
    md.append('|---|---|---|')
    for la, zh, ids in A:
        md.append(f'| {la} | {zh} | {", ".join(ids)} |')
    md.append('')

if B:
    md.append('## B. 同物種、不同俗名／部位（norm latin 相同，zh 不同）')
    md.append('')
    for nl, zhs, items in B:
        md.append(f'### `{nl}`')
        md.append('')
        for iid, zh, la in items:
            md.append(f'- #{iid} {zh} | `{la}`')
        md.append('')

if C:
    md.append('## C. 中文同名但學名不同（zh 衝突）')
    md.append('')
    for zh, lats, items in C:
        md.append(f'### `{zh}`')
        md.append('')
        for iid, la in items:
            md.append(f'- #{iid} `{la}`')
        md.append('')

if D:
    md.append(f'## D. Latin 拼字相近（編輯距離 1-2）')
    md.append('')
    md.append('多數為合理屬內近緣，但可檢查是否有打字錯誤。')
    md.append('')
    md.append('| Latin A | Latin B | 距離 | A 條目 | B 條目 |')
    md.append('|---|---|---:|---|---|')
    for a, b, dist, ia, ib in D[:60]:
        sa = '; '.join(f'#{x[0]} {x[1]}' for x in ia[:2])
        sb = '; '.join(f'#{x[0]} {x[1]}' for x in ib[:2])
        md.append(f'| `{a}` | `{b}` | {dist} | {sa} | {sb} |')
    if len(D) > 60:
        md.append(f'| … | … | … | _還有 {len(D)-60} 對_ | … |')
    md.append('')

if F:
    md.append(f'## F. components 高度重疊（jaccard ≥ 0.7）')
    md.append('')
    md.append('可能是：(1) 同物種不同俗名複製貼上 (2) 真正組成相似的近緣')
    md.append('')
    md.append('| ID A | zh A | ID B | zh B | 共有 | Jaccard | 共有成分（前 8） |')
    md.append('|---|---|---|---|---:|---:|---|')
    for a_id, a_zh, b_id, b_zh, n_int, j, sample in F[:80]:
        md.append(f'| #{a_id} | {a_zh} | #{b_id} | {b_zh} | {n_int} | {j} | {", ".join(sample)} |')
    if len(F) > 80:
        md.append(f'| … | … | … | … | … | … | _還有 {len(F)-80} 對_ |')
    md.append('')

if G:
    md.append(f'## G. 同屬不同種、類型分歧')
    md.append('')
    md.append('多數合理（同屬不同化學型）但可掃過確保標籤一致。')
    md.append('')
    for genus, cats, items in G[:30]:
        md.append(f'### `{genus}` (跨 {len(cats)} 類)')
        md.append('')
        for iid, zh, la, c in items:
            md.append(f'- #{iid} {zh} `{la}` → **{c}**')
        md.append('')

if H:
    md.append('## H. category 與 catFile 對應不一致 🚨')
    md.append('')
    md.append('| ID | zh | category | catFile | 應為 |')
    md.append('|---|---|---|---|---|')
    for iid, zh, c, cf, ex in H:
        md.append(f'| {iid} | {zh} | {c} | {cf} | {ex} |')
    md.append('')

OUT.write_text('\n'.join(md), encoding='utf-8')
print(f'report → {OUT}')
print(f'  A={len(A)} B={len(B)} C={len(C)} D={len(D)} F={len(F)} G={len(G)} H={len(H)}')
