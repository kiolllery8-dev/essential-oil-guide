# -*- coding: utf-8 -*-
"""
convert_aisummary_to_jsonld.py — 把 html-source 內嵌的可見「快速答案」框
轉成純 JSON-LD（不顯示給人，只供 AI/爬蟲讀取）。

緣由：使用者要頁面乾淨（移除可見米色框），但保留 AI 引用能力。
做法：<section/div class="ai-summary"> 可見框 → <script type="application/ld+json"> Question schema。
非 cloaking：摘要的同等資訊正文本來就有；JSON-LD 是 Google 官方推薦的機器資料層。

處理：
- 36 個 <section class="ai-summary">（無巢狀 section，regex non-greedy 安全）
- 1 個 <div class="ai-summary">（oils.html，巢狀 div，用平衡配對）
"""
import sys
import re
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
HTML = Path(r'C:\Users\User\Desktop\essential-oil-guide\html-source')


def strip_tags(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def page_topic(html):
    """從 <title> 抽主題（｜/| 前段，去常見尾綴）"""
    m = re.search(r'<title>([^<]*)</title>', html)
    if not m:
        return ''
    t = m.group(1)
    t = re.split(r'[｜|]', t)[0].strip()
    t = re.sub(r'(完整指南|完整介紹|完整介紹與安全|精油完全索引).*$', '', t).strip()
    return t


def make_question(h2_text, answer_text, topic):
    """決定 Question.name"""
    name = strip_tags(h2_text)
    name = re.sub(r'^[✦\s]*', '', name)
    name = re.sub(r'快速答案[:：]?\s*', '', name).strip()
    if name and ('？' in name or '?' in name):
        return name
    base = topic or name or '本頁主題'
    return f'{base}有哪些特性、常見用途與使用注意？'


def build_script(question_name, answer_text):
    data = {
        '@context': 'https://schema.org',
        '@type': 'Question',
        'name': question_name,
        'acceptedAnswer': {'@type': 'Answer', 'text': answer_text},
    }
    return ('<!-- 快速答案：純 JSON-LD（不顯示給人，供 AI 引用）-->\n'
            '<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False) + '\n</script>')


def extract_inner(block):
    """從 ai-summary 區塊抽 h2 與 answer p"""
    h2 = re.search(r'<h2[^>]*itemprop="name"[^>]*>(.*?)</h2>', block, re.DOTALL)
    h2_text = h2.group(1) if h2 else ''
    # answer：itemprop="text" 的 p
    p = re.search(r'<p[^>]*itemprop="text"[^>]*>(.*?)</p>', block, re.DOTALL)
    ans = strip_tags(p.group(1)) if p else ''
    return h2_text, ans


def find_div_block(html):
    """平衡配對找 <div class="ai-summary"> ... </div>（處理巢狀 div）"""
    start = re.search(r'<div\b[^>]*class="ai-summary"[^>]*>', html)
    if not start:
        return None
    i = start.end()
    depth = 1
    pos = i
    tag = re.compile(r'<(/?)div\b[^>]*>', re.DOTALL)
    while depth > 0:
        m = tag.search(html, pos)
        if not m:
            return None
        depth += -1 if m.group(1) else 1
        pos = m.end()
    return start.start(), pos  # (block_start, block_end)


def process(path):
    html = path.read_text(encoding='utf-8')
    topic = page_topic(html)
    changed = False

    # 1) section 版（non-greedy，無巢狀 section）
    sec_pat = re.compile(r'<section\b[^>]*class="ai-summary"[^>]*>.*?</section>', re.DOTALL)

    def repl_sec(m):
        nonlocal changed
        block = m.group(0)
        h2t, ans = extract_inner(block)
        if not ans:
            return block  # 抽不到答案就不動
        changed = True
        return build_script(make_question(h2t, ans, topic), ans)

    html = sec_pat.sub(repl_sec, html)

    # 2) div 版（平衡配對）
    span = find_div_block(html)
    if span:
        block = html[span[0]:span[1]]
        h2t, ans = extract_inner(block)
        if ans:
            script = build_script(make_question(h2t, ans, topic), ans)
            html = html[:span[0]] + script + html[span[1]:]
            changed = True

    if changed:
        path.write_text(html, encoding='utf-8')
    return changed


def main():
    n = 0
    for path in sorted(HTML.glob('*.html')):
        if process(path):
            n += 1
            print(f'  ✓ {path.name}')
    print(f'\n✓ 轉換 {n} 個檔案的可見「快速答案」→ JSON-LD')


if __name__ == '__main__':
    main()
