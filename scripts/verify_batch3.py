# -*- coding: utf-8 -*-
"""批次3 驗證：logo/sameAs/noindex/摘要/alt/日期/robots/llms/og:image"""
import glob, json, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ok = True
def chk(name, cond, detail=''):
    global ok
    print(('OK ' if cond else 'NG '), name, detail)
    if not cond: ok = False

# 1. logo 192 + sameAs（任一頁的 layout schema）
h = open('out/safety/index.html', encoding='utf-8').read()
chk('Organization logo 192', 'android-chrome-192.png' in h)
chk('Organization sameAs', 'show.intelliverse.tw' in h)

# 2. noindex：search / author-yuling；atlas
chk('search noindex', 'noindex' in open('out/search/index.html', encoding='utf-8').read())
chk('author-yuling noindex', 'noindex' in open('out/author-yuling/index.html', encoding='utf-8').read())
chk('atlas noindex', 'noindex' in open('out/atlas.html', encoding='utf-8').read())

# 3. 首頁 AISummary（definition-first Question in WebPage.mainEntity）
h = open('out/index.html', encoding='utf-8').read()
chk('首頁快速答案', '高濃度芳香物質' in h and '"mainEntity"' in h)

# 4. AISummary 不再裸 Question（抽 oil/100）
h = open('out/oil/100/index.html', encoding='utf-8').read()
bare = re.findall(r'<script type="application/ld\+json">\s*\{"@context":\s*"https://schema.org",\s*"@type":\s*"Question"', h)
chk('AISummary 已包 WebPage', len(bare) == 0)

# 5. oilSchema image + 收編頁 schema url 對齊 canonical
h = open('out/oil/165/index.html', encoding='utf-8').read()  # 165 → oil-lavender
chk('oilSchema 有 image', '"image"' in h and 'hero-home.png' in h)
chk('收編頁 schema url=canonical', '"@id": "https://intelliverse.tw/oil-lavender/"' in h or '"@id":"https://intelliverse.tw/oil-lavender/"' in h)

# 6. 假日期消除：sitemap lastmod 非全同一天
sm = open('out/sitemap.xml', encoding='utf-8').read()
days = set(re.findall(r'<lastmod>(\d{4}-\d{2}-\d{2})', sm))
chk('sitemap lastmod 多日期', len(days) > 1, f'({len(days)} 個不同日期)')

# 7. 摘要新增 6+1
from_src = open('app/lib/pageSummaries.ts', encoding='utf-8').read()
for s in ['index', 'numerology-vs-fortune-telling', 'oil-lemon', 'oil-rosemary', 'oil-ylang-ylang', 'oil-cedarwood']:
    chk(f'摘要 {s}', f"'{s}':" in from_src)
chk('numerology 頁快速答案輸出', '生命靈數計算機：輸入西元生日' in open('out/numerology/index.html', encoding='utf-8').read())

# 8. robots/llms
r = open('out/robots.txt', encoding='utf-8').read()
chk('robots +5 AI UA', all(u in r for u in ['Meta-ExternalAgent','Amazonbot','DuckAssistBot','YouBot','MistralAI-User']))
l = open('out/llms.txt', encoding='utf-8').read()
chk('llms 含對照表頁', 'numerology-vs-fortune-telling' in l)
chk('llms 範例已修', '{specific-page}' not in l and 'oil-{name}' not in l)

# 9. vs 頁 og:image
chk('vs 頁 og:image', 'og:image' in open('out/numerology-vs-fortune-telling/index.html', encoding='utf-8').read())

# 10. alt 全補
n = 0
for f in glob.glob('out/oil-*/index.html'):
    n += len(re.findall(r'oilpg-[^"]*"[^>]*alt=""', open(f, encoding='utf-8').read()))
chk('oilpg 空 alt 歸零', n == 0, f'(殘留 {n})')

# 11. lazy 斜線
n = sum('" / loading=' in open(f, encoding='utf-8').read() for f in glob.glob('out/*/index.html'))
chk('lazy 斜線修正', n == 0, f'(殘留 {n})')

# 12. title 功效化生效 + oil-mandarin 單一 FAQPage
chk('oil-lavender title 功效', '功效與完整指南' in open('out/oil-lavender/index.html', encoding='utf-8').read())
m = open('out/oil-mandarin/index.html', encoding='utf-8').read()
chk('mandarin microdata 移除', 'itemtype="https://schema.org/FAQPage"' not in m and '"FAQPage"' in m)

print()
print('=== 批次3 全部通過 ===' if ok else '=== 有項目未過 ===')
