# -*- coding: utf-8 -*-
"""OCR《幸福密碼》書頁照片（GPT-5.5 vision，高精度設定）
沿用先前驗證過的管線：reasoning_effort=high、detail=high；
若輸出空白（reasoning 吃光 token）→ 以 medium + max_completion_tokens 重試。
輸出：reference/ocr_new/<圖檔名>.md（已存在則跳過，可中斷續跑）"""
import base64, json, os, sys, time, urllib.request, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

KEY = ''
with open(r'C:\Users\User\.claude\skills\gpt-image-generator\.env', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('export '): line = line[7:]
        if line.startswith('OPENAI_API_KEY'):
            KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
assert KEY, 'no api key'

IMGS = [rf'C:\Users\User\Downloads\S__191611{n}_0.jpg' for n in
        [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48]]
OUTDIR = r'C:\Users\User\Desktop\essential-oil-guide\reference\ocr_new'
os.makedirs(OUTDIR, exist_ok=True)

PROMPT = (
    '這是繁體中文命理書《幸福密碼》的書頁照片（可能旋轉 90 度，一張照片可能含左右兩頁）。'
    '請逐字完整轉錄頁面上的所有文字：\n'
    '1. 保持原文用字，不要改寫、不要補充、不要翻譯\n'
    '2. 表格用 markdown 表格呈現，欄位對應要準確（特別注意「優點」「缺點」不要搞混）\n'
    '3. 每一頁開頭標明頁碼（若可見），左右兩頁分開轉錄\n'
    '4. 看不清的字用〔?〕標記，絕對不要用猜的\n'
    '5. 只輸出轉錄內容，不要任何評論'
)

def call(img_b64, effort, max_tok=None):
    body = {
        'model': 'gpt-5.5',
        'reasoning_effort': effort,
        'messages': [{'role': 'user', 'content': [
            {'type': 'text', 'text': PROMPT},
            {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{img_b64}', 'detail': 'high'}},
        ]}],
    }
    if max_tok: body['max_completion_tokens'] = max_tok
    req = urllib.request.Request(
        'https://api.openai.com/v1/chat/completions',
        data=json.dumps(body).encode(),
        headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=900) as r:
        d = json.load(r)
    return (d['choices'][0]['message'].get('content') or '').strip()

def process(path):
    name = os.path.splitext(os.path.basename(path))[0]
    out = os.path.join(OUTDIR, name + '.md')
    if os.path.exists(out) and os.path.getsize(out) > 200:
        return f'[skip] {name}'
    b64 = base64.b64encode(open(path, 'rb').read()).decode()
    t0 = time.time()
    try:
        text = call(b64, 'medium', 30000)  # medium 已足夠（清晰重拍），快 3-5 倍
        if len(text) < 50:
            text = call(b64, 'high')
    except Exception as e:
        try:
            text = call(b64, 'medium', 26000)
        except Exception as e2:
            return f'[fail] {name}: {e2}'
    open(out, 'w', encoding='utf-8').write(f'<!-- 來源: {os.path.basename(path)} -->\n\n{text}\n')
    return f'[ok] {name}  {len(text)} chars  {time.time()-t0:.0f}s'

from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=4) as ex:
    for r in ex.map(process, IMGS):
        print(r, flush=True)
print('ALL DONE')
