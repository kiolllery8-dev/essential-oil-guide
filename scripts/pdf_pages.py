# -*- coding: utf-8 -*-
"""從掃描版 PDF 抽出頁面內嵌圖（給 Read 工具以影像方式閱讀）。
用法: python pdf_pages.py "<pdf路徑>" <起頁> <迄頁> "<輸出資料夾>" [旋轉度數CW: 0/90/180/270]
輸出: <資料夾>/p001.jpg（單頁）或 p001_L.jpg + p001_R.jpg（跨頁掃描自動切半）
頁碼 = PDF 頁序（1-based）。先旋轉再判斷：寬>高視為左右跨頁、切半。
各書校準（掃描方向不同）：破解精油→90；芳療實證全書/方療應用全書/IFA/驅蟲→0"""
import sys, os, io
from pypdf import PdfReader
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
pdf, start, end, outdir = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rot = int(sys.argv[5]) if len(sys.argv) > 5 else 0
os.makedirs(outdir, exist_ok=True)
r = PdfReader(pdf)
n = len(r.pages)
for i in range(max(1, start) - 1, min(end, n)):
    try:
        imgs = r.pages[i].images
        if not imgs:
            print(f'p{i+1}: 無內嵌圖'); continue
        big = max(imgs, key=lambda im: len(im.data))
        im = Image.open(io.BytesIO(big.data))
        if im.mode not in ('RGB', 'L'): im = im.convert('RGB')
        if rot: im = im.rotate(-rot, expand=True)  # PIL 正值=逆時針，取負=順時針
        w, h = im.size
        halves = []
        if w > h * 1.15:  # 跨頁掃描 → 切左右
            halves = [('_L', im.crop((0, 0, w // 2, h))), ('_R', im.crop((w // 2, 0, w, h)))]
        else:
            halves = [('', im)]
        for suf, part in halves:
            pw, ph = part.size
            if pw < 1400:  # 放大到至少 1400px 寬，提升 OCR 可讀性
                part = part.resize((1400, int(ph * 1400 / pw)), Image.LANCZOS)
            path = os.path.join(outdir, f'p{i+1:03d}{suf}.jpg')
            part.save(path, 'JPEG', quality=88)
            print(f'p{i+1}{suf}: {part.size} -> {path}')
    except Exception as e:
        print(f'p{i+1}: ERR {e}')
print(f'總頁數 {n}')
