# -*- coding: utf-8 -*-
"""從《破解精油》翻拍頁的萃取結果，組裝成參考檔與可餵 RAG 的資料集。

輸入：scratchpad 內由 collect_raw.py 從 workflow journal 撈出的
      raw_sections.json / raw_oils.json / raw_concepts.json / raw_notes.json
      以及（可選）retry_*.json 補跑批次。
輸出：reference/破解精油_重點整理.md
      reference/破解精油_oil_facts.json
      reference/破解精油_knowledge.jsonl   ← 一行一則，供 RAG 索引

⚠ 本檔處理的是「事實欄位」與「改寫後的重點」，不含原書逐字內容。
"""
import json, os, sys, io, glob, re
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCRATCH = (r'C:\Users\User\AppData\Local\Temp\claude'
           r'\C--Users-User-Desktop-Claude---'
           r'\a7118eaf-4d84-4caa-93c9-3c1cebdd3bf2\scratchpad')
REF = r'C:\Users\User\Desktop\essential-oil-guide\reference'
TOTAL_SCANS = 335

NULLS = {'null', 'None', '', '該頁未載明', '未載明', 'N/A', 'n/a', '無', '-'}


def clean(v):
    """把 agent 回傳的各種空值正規化成 None。"""
    if v is None:
        return None
    s = str(v).strip()
    return None if s in NULLS else s


def pnum(p):
    """從頁碼字串取第一個數字，供排序用。"""
    m = re.search(r'\d+', str(p or ''))
    return int(m.group()) if m else None


def load(name):
    p = os.path.join(SCRATCH, name)
    if not os.path.exists(p):
        return []
    with open(p, encoding='utf-8') as f:
        return json.load(f)


# ---------- 讀取（含補跑批次） ----------
sections = load('raw_sections.json')
oils = load('raw_oils.json')
concepts = load('raw_concepts.json')
notes = load('raw_notes.json')

for extra in sorted(glob.glob(os.path.join(SCRATCH, 'retry_*.json'))):
    with open(extra, encoding='utf-8') as f:
        r = json.load(f)
    sections += r.get('sections') or []
    oils += r.get('oil_facts') or []
    concepts += r.get('concepts') or []
    if r.get('range_note'):
        notes.append(r['range_note'])
    print(f'  併入補跑：{os.path.basename(extra)}')

print(f'輸入：章節 {len(sections)}、精油 {len(oils)}、知識點 {len(concepts)}')

# ---------- 章節索引 ----------
CHAPTER_RE = re.compile(r'(Chapter|Part|第)\s*(\d+|[一二三四五六七八九十]+)|附錄\s*[A-F]')


def canon_chapter(title):
    """把各批 agent 各自加的註記與編號寫法收斂成同一個章名。

    例：「Chapter 8 來自被子植物的精油（本批頁面的章名頁眉）」
        「Chapter 08｜來自被子植物的精油」  → 都收成「Chapter 8 來自被子植物的精油」
    """
    t = re.sub(r'[（(][^）)]*[）)]\s*$', '', str(title)).strip()   # 砍尾端註記
    t = t.replace('｜', ' ').replace('：', ' ')
    m = re.match(r'\s*(Chapter|Part)\s*0*(\d+)\s*(.*)', t, re.I)
    if m:
        kind = 'Chapter' if m.group(1).lower() == 'chapter' else 'Part'
        return f'{kind} {int(m.group(2))} {m.group(3)}'.strip()
    m = re.match(r'\s*(附錄\s*[A-F])\s*(.*)', t)
    if m:
        return f'{m.group(1).replace(" ", "")} {m.group(2)}'.strip()
    return t
seen_sec = set()
sec_rows = []
for s in sections:
    title = clean(s.get('title'))
    if not title:
        continue
    page = clean(s.get('page')) or ''
    key = (title, page)
    if key in seen_sec:
        continue
    seen_sec.add(key)
    sec_rows.append({'title': title, 'page': page, 'n': pnum(page) or 9999,
                     'level': str(s.get('level') or '')})
sec_rows.sort(key=lambda r: (r['n'], r['title']))

# 章節邊界：用「章／Part／附錄」層級的條目切段，供知識點分組。
# 同一章可能被多批 agent 以不同寫法回報，先收斂再取每個章名最小的起始頁。
def chapter_key(name):
    """Chapter 8 / Part 2 / 附錄C → 用來合併同一章的鍵。"""
    m = re.match(r'(Chapter|Part)\s+(\d+)', name)
    if m:
        return f'{m.group(1)} {int(m.group(2))}'
    m = re.match(r'(附錄[A-F])', name)
    return m.group(1) if m else None


_marks = {}
for r in sec_rows:
    name = canon_chapter(r['title'])
    # 收斂後仍看得出是章／附錄才算（避免「水平協同作用（Chapter 5…）」被誤判成章）
    key = chapter_key(name)
    if not key or r['n'] >= 9999:
        continue
    # 「交叉引用自 296」這種非純頁碼的字串不能拿來當章起始頁
    if not re.fullmatch(r'[\d\s\-–—,、]+', str(r['page']).strip()):
        continue
    cur = _marks.get(key)
    if cur is None or r['n'] < cur[0]:
        _marks[key] = (r['n'], name if cur is None else
                       max(name, cur[1], key=len))
    elif len(name) > len(cur[1]):
        _marks[key] = (cur[0], name)
chapter_marks = sorted(_marks.values())


def chapter_of(page_n):
    name = '（書前：序與目錄）'
    for start, title in chapter_marks:
        if page_n is not None and page_n >= start:
            name = title
        else:
            break
    return name


# ---------- 精油事實：以 中文名+拉丁名 合併 ----------
merged = {}
for o in oils:
    zh = clean(o.get('zh'))
    if not zh:
        continue
    latin = clean(o.get('latin')) or ''
    key = (zh, latin.lower())
    rec = merged.setdefault(key, {
        'zh': zh, 'latin': latin or None, 'family': None, 'components': None,
        'extraction': None, 'safety': None, 'notes': [], 'pages': []})
    for field in ('family', 'components', 'extraction'):
        v = clean(o.get(field))
        if v and not rec[field]:
            rec[field] = v
        elif v and rec[field] and v not in rec[field]:
            rec[field] = f'{rec[field]}；{v}'
    saf = clean(o.get('safety')) or clean(o.get('safety_note'))
    if saf:
        rec['safety'] = saf if not rec['safety'] else (
            rec['safety'] if saf in rec['safety'] else f'{rec["safety"]}；{saf}')
    nt = clean(o.get('notes'))
    if nt and nt not in rec['notes']:
        rec['notes'].append(nt)
    pg = clean(o.get('page'))
    if pg and pg not in rec['pages']:
        rec['pages'].append(pg)

oil_list = []
for i, rec in enumerate(sorted(merged.values(),
                               key=lambda r: (pnum(r['pages'][0]) if r['pages'] else 9999,
                                              r['zh'])), 1):
    oil_list.append({
        'id': i, 'zh': rec['zh'], 'latin': rec['latin'], 'family': rec['family'],
        'components': rec['components'], 'extraction': rec['extraction'],
        'safety': rec['safety'],
        'notes': '；'.join(rec['notes']) if rec['notes'] else None,
        'page': '、'.join(rec['pages']) if rec['pages'] else None,
    })
print(f'精油事實：{len(oils)} 筆原始 → 合併為 {len(oil_list)} 支')

# ---------- 知識點：依章節分組 ----------
by_chapter = defaultdict(list)
seen_topic = set()
for c in concepts:
    topic = clean(c.get('topic'))
    summary = clean(c.get('summary'))
    if not summary:
        continue
    page = clean(c.get('page')) or ''
    key = (topic or '', summary[:40])
    if key in seen_topic:
        continue
    seen_topic.add(key)
    n = pnum(page)
    by_chapter[chapter_of(n)].append(
        {'topic': topic or '（未標題）', 'summary': summary, 'page': page, 'n': n or 9999})
for v in by_chapter.values():
    v.sort(key=lambda r: r['n'])
kept = sum(len(v) for v in by_chapter.values())
print(f'知識點：{len(concepts)} 筆 → 去重後 {kept} 則，分入 {len(by_chapter)} 個章節')

# ---------- 組 Markdown ----------
def cell(v, limit=90):
    if not v:
        return '—'
    s = str(v).replace('|', '／').replace('\n', ' ').strip()
    return s if len(s) <= limit else s[:limit - 1] + '…'


pages_covered = sorted({pnum(o['page']) for o in oil_list if pnum(o['page'])})
sec_pages = sorted({r['n'] for r in sec_rows if r['n'] < 9999})

L = []
L.append('# 《破解精油》重點整理')
L.append('')
L.append(f'> **來源**：玉玲提供的《破解精油》紙本翻拍照片 **{TOTAL_SCANS} 張**（'
         f'`IFA芳療聖經\\破解精油_已轉正\\`，已用 Tesseract OSD 逐頁轉正）。')
L.append('> **方法**：多個視覺模型分批逐頁辨識 → 抽出「事實欄位」與「改寫後的重點」→ '
         '程式化合併、去重、依頁碼排序。')
L.append('> **信心標示**：`（？）`＝字跡看不清；`【待核】`＝辨識有出入或與常理有落差；'
         '`⚠`＝原書可能誤植或需回查紙本。')
L.append('>')
L.append('> ⚠️ **本檔是事實整理與重點改寫，不是全書原文。** 需要原文請翻紙本或掃描檔。')
L.append('> ⚠️ 本檔供**內部知識庫**使用（交叉驗證 `data/oils.json`、供內容產線參考）。'
         '第二節保留原書偏醫療取向的用語以利比對，**對外文案一律改寫**，規則見第三節開頭。')
L.append('>')
if sec_pages:
    L.append(f'> **涵蓋範圍**：章節索引 p.{sec_pages[0]}–p.{sec_pages[-1]}；'
             f'精油事實 p.{pages_covered[0]}–p.{pages_covered[-1]}（{len(pages_covered)} 個頁面有精油條目）。')
L.append('> **已知缺頁**：p.211、p.235（翻拍時漏拍，需補拍）。'
         '另有數個檔名編號缺號但書頁未斷（重拍剔除所致）。')
L.append('')
L.append('---')
L.append('')

# 一、章節索引
L.append('## 一、全書章節索引')
L.append('')
L.append('> 依書上印刷頁碼排序。要查什麼主題，先在這裡定位頁碼再翻紙本。')
L.append('')
L.append('| 頁碼 | 章節／小節 |')
L.append('|---:|---|')
for r in sec_rows:
    lv = r['level']
    bold = any(k in lv for k in ('chapter', 'part', '章', 'h1')) or CHAPTER_RE.search(r['title'])
    title = f'**{r["title"]}**' if bold else f'　{r["title"]}'
    L.append(f'| {r["page"] or "—"} | {title} |')
L.append('')

# 二、精油事實速查表
L.append('## 二、精油事實速查表')
L.append('')
L.append(f'> **{len(oil_list)} 支**。欄位過長者在表中截斷，完整值以 '
         '`破解精油_oil_facts.json` 為準。')
L.append('> ⚠️ 本表是**內部比對用**（校對 `data/oils.json`），保留原書用語，不可直接當對外文案。')
L.append('')
L.append('| # | 中文名 | 拉丁學名 | 科屬 | 主要成分 | 萃取 | 安全 | 頁碼 |')
L.append('|---:|---|---|---|---|---|---|---|')
for o in oil_list:
    L.append('| {id} | {zh} | *{latin}* | {family} | {comp} | {ext} | {saf} | {pg} |'.format(
        id=o['id'], zh=cell(o['zh'], 20),
        latin=cell(o['latin'], 40) if o['latin'] else '—',
        family=cell(o['family'], 20), comp=cell(o['components'], 110),
        ext=cell(o['extraction'], 40), saf=cell(o['safety'], 70), pg=cell(o['page'], 24)))
L.append('')

# 三、知識重點
L.append('## 三、知識重點')
L.append('')
L.append('> ### ⛔ 對外文案使用規則（三條紅線）')
L.append('> 1. **不得宣稱療效**。原書偏醫療取向（治療／抗菌／消炎／調經等），'
         '本站對外一律改寫為情緒陪伴、香氛儀式、日常保養的語氣。')
L.append('> 2. **不得逐字引用**。這裡的重點已是改寫版；再寫成文章時要再寫一次，不要照抄本檔。')
L.append('> 3. **能量／靈性觀點**須標註「非科學事實」，與化學、藥理內容分開陳述。')
L.append('')
order = sorted(by_chapter.keys(),
               key=lambda k: min((c['n'] for c in by_chapter[k]), default=9999))
for ch in order:
    items = by_chapter[ch]
    L.append(f'### {ch}')
    L.append('')
    for c in items:
        pg = f'（p.{c["page"]}）' if c['page'] else ''
        L.append(f'**{c["topic"]}**{pg}')
        L.append('')
        L.append(c['summary'])
        L.append('')

# 四、與 oils.json 的比對入口
L.append('---')
L.append('')
L.append('## 四、與本站 data/oils.json 的比對')
L.append('')
L.append('比對腳本：`scripts/compare_pojie_oils.py`（輸出差異清單，不自動改資料）。')
L.append('建議優先回查的欄位：')
L.append('')
L.append('- **拉丁學名**：同物異名 vs 真的抓錯種，要分開處理；不同種的安全性可能天差地遠。')
L.append('- **主要成分**：本站若把 A 精油的成分輪廓寫到 B 精油上，會連帶讓安全說明失準。')
L.append('- **安全等級**：原書標示有毒性／刺激性，而本站標 `safe` 的，一律下修並補說明。')
L.append('- **本站沒有的精油**：可評估是否補建 datasheet。')
L.append('')
L.append('---')
L.append('')
L.append('## 附錄：各批萃取的範圍備註')
L.append('')
for n in notes:
    L.append(f'- {str(n).strip()}')
L.append('')

md = '\n'.join(L)
os.makedirs(REF, exist_ok=True)
md_path = os.path.join(REF, '破解精油_重點整理.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md)

# ---------- JSON ----------
payload = {
    'source': '《破解精油》紙本翻拍 %d 張' % TOTAL_SCANS,
    'method': '視覺辨識分批萃取 → 程式化合併去重（以 中文名+拉丁名 為鍵）',
    'warning': '事實欄位整理，非原書全文；對外文案不得沿用原書療效用語',
    'null_policy': '該頁未載明者為 null',
    'count': len(oil_list),
    'oils': oil_list,
}
json_path = os.path.join(REF, '破解精油_oil_facts.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)

# ---------- RAG 用 JSONL ----------
jsonl_path = os.path.join(REF, '破解精油_knowledge.jsonl')
with open(jsonl_path, 'w', encoding='utf-8') as f:
    for o in oil_list:
        bits = [f'{o["zh"]}（{o["latin"]}）' if o['latin'] else o['zh']]
        for label, key in (('科屬', 'family'), ('主要成分', 'components'),
                           ('萃取', 'extraction'), ('安全', 'safety'), ('備註', 'notes')):
            if o[key]:
                bits.append(f'{label}：{o[key]}')
        f.write(json.dumps({'type': 'oil_fact', 'title': o['zh'],
                            'text': '。'.join(bits), 'page': o['page'],
                            'source': '破解精油'}, ensure_ascii=False) + '\n')
    for ch, items in by_chapter.items():
        for c in items:
            f.write(json.dumps({'type': 'concept', 'title': c['topic'],
                                'text': c['summary'], 'page': c['page'],
                                'chapter': ch, 'source': '破解精油'},
                               ensure_ascii=False) + '\n')

for p in (md_path, json_path, jsonl_path):
    print(f'✓ {os.path.basename(p)}  {os.path.getsize(p):,} bytes')
