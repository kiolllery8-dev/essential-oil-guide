"""
check_external_links.py — 檢查 46 個 oil-*.html 加上的所有外部連結是否 404

風險點：Wikipedia 連結用拉丁學名動態生成，部分可能：
- 學名拼錯/有空格但 Wikipedia 用底線
- 學名過時，Wikipedia 用較新分類
- 多字學名 (e.g., "Cinnamomum camphora ct cineole") Wikipedia 沒有
- 物種有同義名稱

報告：列出所有失效連結 + 建議替代 URL
"""
import sys
import re
import urllib.request
import urllib.error
import urllib.parse
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')


def check_url(url, timeout=15):
    """檢查 URL 是否可訪問（HEAD 或 GET）"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Intelliverse-LinkChecker/1.0)',
                'Accept': 'text/html,application/xhtml+xml',
            },
            method='HEAD',
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return (url, r.status, '')
    except urllib.error.HTTPError as e:
        # Some sites block HEAD, try GET
        if e.code == 405:
            try:
                req2 = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req2, timeout=timeout) as r:
                    return (url, r.status, '')
            except Exception as e2:
                return (url, 0, f'GET fallback: {e2}')
        return (url, e.code, e.reason)
    except urllib.error.URLError as e:
        return (url, 0, str(e.reason))
    except Exception as e:
        return (url, 0, str(e))


def main():
    html_dir = Path(r'C:\Users\User\Desktop\essential-oil-guide\html-source')

    # Collect all external URLs from oil-*.html files
    url_map = {}  # url -> [files that contain it]
    pattern = re.compile(r'href="(https?://[^"]+)"')

    for f in sorted(html_dir.glob('oil-*.html')):
        content = f.read_text(encoding='utf-8')
        urls = pattern.findall(content)
        for u in urls:
            # Skip our own CDN, cdn.jsdelivr.net, google fonts
            if 'intelliverse.tw' in u:
                continue
            if 'cdn.jsdelivr.net' in u:
                continue
            if 'fonts.googleapis.com' in u or 'fonts.gstatic.com' in u:
                continue
            if 'schema.org' in u:
                continue
            url_map.setdefault(u, []).append(f.name)

    print(f'=== 共發現 {len(url_map)} 個唯一外部連結 ===')
    print()

    # Check all in parallel
    results = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(check_url, url): url for url in url_map.keys()}
        for i, fut in enumerate(as_completed(futures), 1):
            url, status, err = fut.result()
            results.append((url, status, err))
            mark = '✓' if status in (200, 301, 302, 303, 307, 308) else '✗'
            print(f'  [{i:3d}/{len(url_map)}] {mark} {status:3d}  {url[:80]}')
            if err:
                print(f'         └─ {err[:100]}')

    # Summary
    ok = [r for r in results if r[1] in (200, 301, 302, 303, 307, 308)]
    redir = [r for r in results if r[1] in (301, 302, 303, 307, 308)]
    bad = [r for r in results if r[1] not in (200, 301, 302, 303, 307, 308)]

    print()
    print('=== 摘要 ===')
    print(f'  ✓ OK (含 redirect): {len(ok)}')
    print(f'  ↪ Redirect:          {len(redir)}')
    print(f'  ✗ 失效:              {len(bad)}')

    if bad:
        print()
        print('=== 失效連結（需要修復）===')
        for url, status, err in sorted(bad, key=lambda x: x[1]):
            files = url_map[url]
            print(f'  [{status}] {url}')
            print(f'         錯誤: {err[:80]}')
            print(f'         出現於: {len(files)} 個檔案')
            # Show first 3 files
            for fn in files[:3]:
                print(f'           - {fn}')

    # Write report
    report_path = Path(r'C:\Users\User\Desktop\essential-oil-guide\data\crawled\external_links_check.md')
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ['# 外部連結健康度檢查報告', '', f'總計 {len(url_map)} 個唯一連結；OK {len(ok)} / 失效 {len(bad)}', '']
    if bad:
        lines.append('## ❌ 失效連結（需修復）')
        lines.append('')
        for url, status, err in sorted(bad, key=lambda x: x[1]):
            files = url_map[url]
            lines.append(f'- **[{status}]** {url}')
            lines.append(f'  - 錯誤: {err}')
            lines.append(f'  - 出現於 {len(files)} 個檔案: {", ".join(files[:5])}{" ..." if len(files) > 5 else ""}')
    lines.append('')
    lines.append('## ✓ 健康連結')
    lines.append('')
    for url, status, err in sorted(ok):
        lines.append(f'- [{status}] {url}')
    report_path.write_text('\n'.join(lines), encoding='utf-8')
    print()
    print(f'✓ 報告寫入: {report_path}')


if __name__ == '__main__':
    main()
