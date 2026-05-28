"""
wiki_name_match.py — 用 Wikipedia 拉丁學名查中文名，俗名優先策略

策略（用戶指定：俗名優先）：
  - 主名 zh 保留芳療俗名（茶樹、薰衣草）— SEO 不動
  - Wikipedia 植物學名加進 aliases（豐富資料 + 照顧植物名搜尋 + AI）
  - 簡體 → 繁體（用 Wikipedia zh-tw 變體轉換）
  - 產出待審報告：current zh 可能有誤的標記出來人工判斷

流程：
  1. 批次查 en.wikipedia（50 拉丁名/call）取 zh langlink
  2. zh 標題用 zh.wikipedia variant=zh-tw 轉繁
  3. 加進 aliases；產出報告

CLI:
  python scripts/wiki_name_match.py            # dry-run（只報告）
  python scripts/wiki_name_match.py --apply    # 寫回 oils.json
"""
import sys
import json
import re
import time
import argparse
import urllib.request
import urllib.parse
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

OILS = Path(r'C:\Users\User\Desktop\essential-oil-guide\data\oils.json')
REPORT = Path(r'C:\Users\User\Desktop\essential-oil-guide\data\crawled\wiki_name_match_report.md')
UA = 'IntelliverseOilVerify/1.0 (linsonder6@gmail.com)'

_variant_cache = {}


def clean_latin(latin):
    """清理拉丁學名（去 ct./同義名標註/括號）取主二名"""
    s = re.sub(r'\(.*?\)', '', latin or '')
    s = re.sub(r'\bct\.?\s+\w+', '', s, flags=re.I)
    s = re.sub(r'\bsyn\.?.*$', '', s, flags=re.I)
    s = re.sub(r'\bvar\.?\s+\w+', '', s, flags=re.I)
    s = s.strip()
    # 取前兩個詞（屬+種）
    parts = s.split()
    if len(parts) >= 2:
        return f'{parts[0]} {parts[1]}'
    return s


def batch_langlinks(latins):
    """批次查 en.wikipedia 取 zh langlink（最多 50/call）"""
    result = {}  # latin -> zh_title
    for i in range(0, len(latins), 50):
        chunk = latins[i:i+50]
        url = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode({
            'action': 'query', 'titles': '|'.join(chunk),
            'prop': 'langlinks', 'lllang': 'zh', 'lllimit': 'max',
            'format': 'json', 'redirects': '1',
        })
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            d = json.load(urllib.request.urlopen(req, timeout=30))
        except Exception as e:
            print(f'  ✗ batch {i} 失敗: {e}', file=sys.stderr)
            continue
        q = d.get('query', {})
        # normalized + redirects 對應回原 title
        norm = {n['to']: n['from'] for n in q.get('normalized', [])}
        redir = {r['to']: r['from'] for r in q.get('redirects', [])}
        for p in q.get('pages', {}).values():
            title = p.get('title', '')
            lls = p.get('langlinks', [])
            zh = lls[0].get('*') if lls else None
            # 回溯到原查詢 latin
            orig = title
            if orig in redir: orig = redir[orig]
            if orig in norm: orig = norm[orig]
            result[orig] = zh
            result[title] = zh  # 也存 resolved title
        time.sleep(0.3)
        print(f'  查詢進度 {min(i+50,len(latins))}/{len(latins)}', file=sys.stderr)
    return result


def to_traditional(zh_title):
    """用 zh.wikipedia variant=zh-tw 轉繁體"""
    if not zh_title:
        return None
    if zh_title in _variant_cache:
        return _variant_cache[zh_title]
    url = 'https://zh.wikipedia.org/w/api.php?' + urllib.parse.urlencode({
        'action': 'parse', 'page': zh_title, 'prop': 'displaytitle',
        'variant': 'zh-tw', 'format': 'json', 'redirects': '1',
    })
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        d = json.load(urllib.request.urlopen(req, timeout=15))
        dt = d.get('parse', {}).get('displaytitle', zh_title)
        dt = re.sub(r'<[^>]+>', '', dt).strip()
        _variant_cache[zh_title] = dt or zh_title
    except Exception:
        _variant_cache[zh_title] = zh_title
    time.sleep(0.2)
    return _variant_cache[zh_title]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='寫回 oils.json')
    ap.add_argument('--limit', type=int, default=None)
    args = ap.parse_args()

    oils = json.load(open(OILS, encoding='utf-8'))
    if args.limit:
        oils = oils[:args.limit]

    # 1. 收集所有 clean latin
    latins = []
    for o in oils:
        cl = clean_latin(o.get('latin', ''))
        o['_clean_latin'] = cl
        if cl:
            latins.append(cl)
    latins = list(dict.fromkeys(latins))
    print(f'查 {len(latins)} 個唯一拉丁學名...', file=sys.stderr)

    # 2. 批次查 zh langlink
    latin_to_zh = batch_langlinks(latins)

    # 3. 分類 + 加 alias
    rows = []
    n_alias_added = 0
    n_no_article = 0
    n_review = 0
    for o in oils:
        cur = o.get('zh', '').strip()
        cl = o.get('_clean_latin', '')
        zh_simp = latin_to_zh.get(cl)
        wiki_zh = to_traditional(zh_simp) if zh_simp else None

        status = ''
        if not wiki_zh:
            status = 'no-article'
            n_no_article += 1
        elif wiki_zh == cur:
            status = 'match'
        elif wiki_zh in (o.get('aliases') or []):
            status = 'alias-exists'
        else:
            # 加進 aliases（俗名優先：不替換主名）
            status = 'alias-added'
            # 判斷 current 是否可能有誤：若 current 與 wiki 完全無共字且 current 很短
            common = set(cur) & set(wiki_zh)
            if len(common) == 0 and len(cur) <= 4:
                status = 'review'
                n_review += 1

        rows.append({
            'id': o['id'], 'current': cur, 'latin': o.get('latin', ''),
            'clean_latin': cl, 'wiki_zh': wiki_zh or '—', 'status': status,
        })

        # 套用 alias
        if args.apply and wiki_zh and wiki_zh != cur:
            aliases = o.get('aliases') or []
            if wiki_zh not in aliases:
                aliases.append(wiki_zh)
                o['aliases'] = aliases
                n_alias_added += 1

    # 清掉暫存欄位
    for o in oils:
        o.pop('_clean_latin', None)

    if args.apply:
        # 重新讀完整 oils（因 --limit 可能只取部分；apply 時不應截斷）
        if args.limit:
            print('⚠ --apply 不可與 --limit 併用（避免截斷）', file=sys.stderr)
            sys.exit(1)
        OILS.write_text(json.dumps(oils, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'✓ 寫回 oils.json：新增 {n_alias_added} 個 Wikipedia 別名')

    # 報告
    from collections import Counter
    stat = Counter(r['status'] for r in rows)
    print('\n=== 統計 ===')
    for s, c in stat.most_common():
        print(f'  {s}: {c}')

    # 待審清單
    review = [r for r in rows if r['status'] == 'review']
    print(f'\n=== 待人工審查（current 與 Wikipedia 完全無共字，可能有誤）：{len(review)} 個 ===')
    for r in review[:40]:
        print(f'  #{r["id"]} 現名「{r["current"]}」 vs Wiki「{r["wiki_zh"]}」({r["clean_latin"]})')

    # 寫 markdown 報告
    lines = ['# Wikipedia 中文名比對報告', '',
             f'共 {len(rows)} 個精油。策略：俗名優先（主名不動，Wikipedia 名加進 aliases）。', '',
             '## 統計', '']
    for s, c in stat.most_common():
        lines.append(f'- {s}: {c}')
    lines += ['', '## 待人工審查（current 與 Wikipedia 完全無共字）', '',
              '| ID | 現名 | Wikipedia | 拉丁學名 |', '|----|------|-----------|----------|']
    for r in review:
        lines.append(f'| {r["id"]} | {r["current"]} | {r["wiki_zh"]} | {r["clean_latin"]} |')
    lines += ['', '## 全部對照', '', '| ID | 現名 | Wikipedia(繁) | 狀態 |', '|----|------|------|------|']
    for r in rows:
        lines.append(f'| {r["id"]} | {r["current"]} | {r["wiki_zh"]} | {r["status"]} |')
    REPORT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'\n✓ 報告寫到 {REPORT}')


if __name__ == '__main__':
    main()
