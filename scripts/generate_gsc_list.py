"""
generate_gsc_list.py — 產出 Google Search Console「URL Inspection 手動送出」批次清單

Google 不提供開放 Indexing API（限 JobPosting/BroadcastEvent）。
GSC 的「請求建立索引」每日約 10-12 條 URL 額度，且必須一條條手動點。

這個工具產出依優先序排序的 URL 清單，分批給你貼進 GSC。
推送策略：
  - Day 1：首頁 + 5 個 hub（oils/encyclopedia/aromatherapy/safety/about）+ 5 個最新主題
  - Day 2：5 個高頻 oil-* 完整指南
  - Day 3 之後：剩餘逐批
"""
from __future__ import annotations
import json, sys, xml.etree.ElementTree as ET
from pathlib import Path

SITEMAP = Path('out/sitemap.xml')

# 優先序：hub 頁 > 新文章 > oil 完整指南 > oil/{id} datasheet
PRIORITY_GROUPS = [
    # (group name, url substring matchers, priority)
    ('🏠 首頁 + Hub', [
        'https://intelliverse.tw/',
        'https://intelliverse.tw/oils/',
        'https://intelliverse.tw/encyclopedia/',
        'https://intelliverse.tw/aromatherapy/',
        'https://intelliverse.tw/safety/',
    ]),
    ('📰 大主題文章', [
        '/article-tcm-aromatherapy/',
        '/article-spiritual-aromatherapy/',
        '/article-conifers/',
        '/article-citrus-comparison/',
        '/article-chamomile-comparison/',
        '/article-hydrosols/',
        '/article-newbie-mistakes/',
        '/article-children/',
        '/article-pregnancy/',
        '/article-pets/',
        '/article-office/',
    ]),
    ('🌹 高單價精油', [
        '/oil-rose/',
        '/oil-sandalwood/',
        '/oil-jasmine/',
        '/oil-neroli/',
        '/oil-helichrysum/',
        '/oil-myrrh/',
        '/oil-frankincense/',
    ]),
    ('🌿 常見精油', [
        '/oil-bergamot/',
        '/oil-lavender/',
        '/oil-tea-tree/',
        '/oil-eucalyptus/',
        '/oil-peppermint/',
        '/oil-lemon/',
        '/oil-sweet-orange/',
        '/oil-rosemary/',
        '/oil-grapefruit/',
        '/oil-geranium/',
    ]),
    ('🔥 辛香 / 木質', [
        '/oil-ginger/',
        '/oil-black-pepper/',
        '/oil-clove/',
        '/oil-bay/',
        '/oil-cedarwood/',
        '/oil-patchouli/',
        '/oil-vetiver/',
        '/oil-cypress/',
        '/oil-juniper/',
    ]),
    ('🌺 其他單品', [
        '/oil-clary-sage/',
        '/oil-marjoram/',
        '/oil-citronella/',
        '/oil-petitgrain/',
        '/oil-ravintsara/',
        '/oil-palmarosa/',
        '/oil-ylang-ylang/',
    ]),
    ('📚 站務頁', [
        '/about/',
        '/contact/',
        '/disclaimer/',
        '/privacy/',
    ]),
]


def read_sitemap_urls() -> list[str]:
    if not SITEMAP.exists():
        return []
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    tree = ET.parse(SITEMAP)
    root = tree.getroot()
    urls = []
    for u in root.findall('sm:url', ns):
        loc = u.find('sm:loc', ns)
        if loc is not None:
            urls.append(loc.text)
    return urls


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    all_urls = read_sitemap_urls()
    if not all_urls:
        print(f'✗ sitemap empty: {SITEMAP}')
        sys.exit(1)

    all_set = set(all_urls)
    used = set()
    grouped = []
    for name, patterns in PRIORITY_GROUPS:
        bucket = []
        for u in all_urls:
            if u in used:
                continue
            for p in patterns:
                if p == u or (p.startswith('/') and u.endswith(p)) or (not p.startswith('/') and p == u):
                    bucket.append(u)
                    used.add(u)
                    break
        grouped.append((name, bucket))

    # 剩下的（多半是 /oil/N/ datasheet）
    remaining = [u for u in all_urls if u not in used]
    grouped.append((f'📋 /oil/N/ 化學分子 datasheet（{len(remaining)} 個）', remaining))

    # 輸出
    out_lines = [
        '# Google Search Console「請求索引」批次清單',
        '',
        f'> 總計 {len(all_urls)} 個 URL，按優先序分批送出。',
        '> GSC 每日約 10-12 條額度，依下表逐日操作。',
        '',
        '## 操作步驟',
        '',
        '1. 開啟 [Google Search Console](https://search.google.com/search-console)',
        '2. 上方搜尋框貼一個 URL（或直接點 URL Inspection）',
        '3. 等待狀態檢查（紅色 ✗ = 未索引；綠色 ✓ = 已索引）',
        '4. 若未索引 → 點「請求建立索引」',
        '5. 每天約 10-12 條為單日上限，超過會被 throttle',
        '',
        '⚠️ Google 沒有開放給內容網站的程式化 Indexing API，**僅能手動操作**。',
        '但我們已透過 sitemap.xml + 內部連結 + 推薦的 robots.txt 給 Googlebot 友善信號，',
        '所以**就算不手動 request 一般 1-4 週也會自然索引**。手動只是加速。',
        '',
        '---',
        '',
    ]

    for i, (name, urls) in enumerate(grouped, 1):
        if not urls:
            continue
        out_lines.append(f'## Day {i}：{name}（{len(urls)} 條）')
        out_lines.append('')
        out_lines.append('```')
        for u in urls:
            out_lines.append(u)
        out_lines.append('```')
        out_lines.append('')

    out_path = Path('data/crawled/gsc_submit_list.md')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text('\n'.join(out_lines), encoding='utf-8')
    print(f'✓ 寫到 {out_path}')
    print(f'  {len(all_urls)} URLs，分 {len(grouped)} 組')
    for name, urls in grouped:
        print(f'    {name}: {len(urls)} 條')


if __name__ == '__main__':
    main()
