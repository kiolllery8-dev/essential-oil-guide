# -*- coding: utf-8 -*-
"""批次回填 html-source/*.html 內 <img> 的 width/height 屬性（修 CLS）。
讀 CDN 圖實際尺寸（PIL），只補「有 src 且尚無 width 屬性」的 <img>。
既有 inline style="width:100%;height:auto" 仍控制實際渲染，瀏覽器只拿屬性算 aspect-ratio 預留空間，視覺不變。
"""
import os, re, io, sys, glob, urllib.request
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'C:\Users\User\Desktop\essential-oil-guide\html-source'
UA = 'IntelliverseTW-img-dims/1.0'
_cache = {}

def dims(src):
    """回傳 (w, h) 或 None。支援 CDN 絕對網址；相對路徑略過（多為 404 或非內容圖）。"""
    if src in _cache:
        return _cache[src]
    res = None
    try:
        if src.startswith('http'):
            req = urllib.request.Request(src, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            im = Image.open(io.BytesIO(data))
            res = im.size
    except Exception as e:
        print('  ! 讀取失敗', src[:70], e)
    _cache[src] = res
    return res

IMG_RE = re.compile(r'<img\b[^>]*>', re.I)
SRC_RE = re.compile(r'\bsrc\s*=\s*"([^"]+)"', re.I)
HAS_WH = re.compile(r'\b(width|height)\s*=', re.I)

def process(path):
    html = open(path, encoding='utf-8').read()
    changed = [0]
    def repl(m):
        tag = m.group(0)
        if HAS_WH.search(tag):
            return tag  # 已有 width/height
        sm = SRC_RE.search(tag)
        if not sm:
            return tag
        d = dims(sm.group(1))
        if not d:
            return tag
        w, h = d
        # 在 <img 後插入 width/height（放最前面，不影響其他屬性）
        new = re.sub(r'^<img\b', f'<img width="{w}" height="{h}"', tag, count=1, flags=re.I)
        changed[0] += 1
        return new
    out = IMG_RE.sub(repl, html)
    if changed[0]:
        open(path, 'w', encoding='utf-8').write(out)
    return changed[0]

total = 0
files = 0
for fp in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    n = process(fp)
    if n:
        files += 1
        total += n
        print(f'{os.path.basename(fp)}: +{n}')
print(f'\n完成：{files} 檔、共回填 {total} 個 <img> width/height（快取 {len(_cache)} 張圖）')
