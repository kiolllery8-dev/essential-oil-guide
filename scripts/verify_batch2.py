# -*- coding: utf-8 -*-
"""批次2 驗證：內鏈分布 / 自連消除 / 工具頁輸血 / 對照表頁擴寫"""
import glob, json, re, io, sys, os
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ok = True
def chk(name, cond, detail=''):
    global ok
    print(('OK ' if cond else 'NG '), name, detail)
    if not cond: ok = False

pages = glob.glob('out/*/index.html') + glob.glob('out/oil/*/index.html')

# 1. 自連檢查
selfs = 0
for f in pages:
    h = open(f, encoding='utf-8').read()
    m = re.search(r'<nav class="related-links".*?</nav>', h, re.S)
    if not m: continue
    parts = f.replace(os.sep, '/').split('/')[1:-1]
    path = '/' + '/'.join(parts) + '/'
    if 'href="%s"' % path in m.group(0): selfs += 1
chk('related-links 無自連', selfs == 0, '(自連頁數 %d)' % selfs)

# 2. 分布 + 工具頁覆蓋
cnt = Counter(); promoted_pages = 0; total_rl = 0
PROM = {'/numerology/', '/blend/', '/numerology-vs-fortune-telling/', '/numerology/#numerology-oils'}
for f in pages:
    h = open(f, encoding='utf-8').read()
    m = re.search(r'<nav class="related-links".*?</nav>', h, re.S)
    if not m: continue
    total_rl += 1
    hrefs = set(re.findall(r'href="([^"]+)"', m.group(0)))
    for x in hrefs: cnt[x] += 1
    if hrefs & PROM: promoted_pages += 1
print('   延伸閱讀區塊總數:', total_rl, '| 含工具頁:', promoted_pages)
chk('工具頁輸血覆蓋 >=90%', promoted_pages >= total_rl * 0.9, '(%d/%d)' % (promoted_pages, total_rl))
print('   被連最多 top6:', cnt.most_common(6))
chk('火力不再全灌薰衣草', cnt.get('/oil-lavender/', 0) < 30, '(lavender %d 頁, 原67)' % cnt.get('/oil-lavender/', 0))

# 3. vs 頁
h = open('out/numerology-vs-fortune-telling/index.html', encoding='utf-8').read()
text = re.sub(r'<script.*?</script>', '', h, flags=re.S)
text = re.sub(r'<style.*?</style>', '', text, flags=re.S)
text = re.sub(r'<[^>]+>', '', text)
zh = len(re.findall(r'[一-鿿]', text))
chk('vs 頁中文字數 >800', zh > 800, '(%d 字)' % zh)
chk('vs 頁 H1 含算命', '算命／東方命理' in h)
types = []
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
    try: types.append(json.loads(b).get('@type'))
    except Exception: types.append('PARSE_ERR')
chk('vs 頁 FAQPage 有效', 'FAQPage' in types and 'PARSE_ERR' not in types, str(types))
chk('vs 頁 3 題 Q', h.count('box-title') >= 3)

# 4. 入鏈計數
def inlinks(target):
    n = 0
    tgt_file = target.strip('/') + '/index.html'
    for f in pages:
        if tgt_file in f.replace(os.sep, '/'): continue
        if 'href="%s"' % target in open(f, encoding='utf-8').read(): n += 1
    return n
vs_in = inlinks('/numerology-vs-fortune-telling/')
print('   vs 頁入鏈頁數:', vs_in, '| /numerology/ 入鏈頁數(含nav):', inlinks('/numerology/'))
chk('vs 頁入鏈 >=3', vs_in >= 3)

# 5. 油頁靈數行 + 薰衣草比較文
h = open('out/oil-lavender/index.html', encoding='utf-8').read()
chk('oil-lavender 靈數行已連 /numerology/', 'title="生命靈數計算機：算主命數與對應精油"' in h)
chk('oil-lavender 連薰衣草比較文', '/article-lavender-comparison/' in h)

print()
print('=== 批次2 全部通過 ===' if ok else '=== 有項目未過 ===')
