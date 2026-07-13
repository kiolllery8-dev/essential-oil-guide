# -*- coding: utf-8 -*-
"""46 支單油指南 title 批次補英文名（P0：白撿 patchouli/sandalwood/tea tree oil 等英文查詢，
競品 aromaharvest DR5 靠雙語標題吃英文詞）。
規則：在「... | 精油能量圖譜」前插入「｜{English} Oil」；title/og:title/twitter:title 同字串一起換（訊號一致性）。
太長（>68 全形寬估算）或已含英文者跳過。"""
import re, glob, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'C:\Users\User\Desktop\essential-oil-guide\html-source'

def eng_from_slug(slug):
    words = slug.replace('oil-', '').split('-')
    return ' '.join(w.capitalize() for w in words)

SPECIAL = {  # slug → 顯示英文（slug 直翻不自然者）
    'oil-ylang-ylang': 'Ylang Ylang', 'oil-tea-tree': 'Tea Tree',
    'oil-german-chamomile': 'German Chamomile', 'oil-roman-chamomile': 'Roman Chamomile',
    'oil-clary-sage': 'Clary Sage', 'oil-black-pepper': 'Black Pepper',
    'oil-black-spruce': 'Black Spruce', 'oil-sweet-orange': 'Sweet Orange',
    'oil-sweet-basil': 'Sweet Basil', 'oil-sweet-fennel': 'Sweet Fennel',
    'oil-spike-lavender': 'Spike Lavender', 'oil-lemon-eucalyptus': 'Lemon Eucalyptus',
    'oil-bay': 'Bay Laurel', 'oil-juniper': 'Juniper Berry', 'oil-melissa': 'Melissa',
}

changed = skipped = 0
for fp in sorted(glob.glob(os.path.join(ROOT, 'oil-*.html'))):
    slug = os.path.basename(fp)[:-5]
    if slug == 'oil-detail':
        continue
    html = open(fp, encoding='utf-8').read()
    m = re.search(r'<title>([^<]+)</title>', html)
    if not m:
        continue
    title = m.group(1)
    if re.search(r'[A-Za-z]{3,}', title):  # 已含英文（如自帶學名者）跳過
        skipped += 1
        print(f'  skip(已含英文) {slug}: {title[:40]}')
        continue
    if ' | 精油能量圖譜' not in title:
        skipped += 1
        print(f'  skip(無標準尾綴) {slug}')
        continue
    eng = SPECIAL.get(slug, eng_from_slug(slug))
    core = title.replace(' | 精油能量圖譜', '')
    new_title = f'{core}｜{eng} Oil | 精油能量圖譜'
    # 全形字算 2、半形算 1 的粗略寬度檢查（Google 標題約 60-70 顯示寬）
    width = sum(2 if ord(c) > 0x2E80 else 1 for c in new_title)
    if width > 78:
        skipped += 1
        print(f'  skip(過長 {width}) {slug}: {new_title[:50]}')
        continue
    html2 = html.replace(title, new_title)  # title/og:title/twitter:title 同字串一起換
    n = html.count(title)
    open(fp, 'w', encoding='utf-8').write(html2)
    changed += 1
    print(f'  ✓ {slug} (×{n}): …｜{eng} Oil')

print(f'\n完成：改 {changed} 檔、跳過 {skipped} 檔')
