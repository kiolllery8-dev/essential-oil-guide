"""
indexnow_push.py — 把網站所有 URL 推送給 IndexNow（Bing / Yandex / Seznam / Naver）

IndexNow 是 Microsoft 主導的開放協定，一次推送多個搜尋引擎，無需 OAuth、無數量限制。
Google 不參與 IndexNow（Google 需透過 sitemap 自然抓取 + 手動 URL Inspection）。

文檔：https://www.indexnow.org/documentation

CLI:
  python scripts/indexnow_push.py                  # push all sitemap URLs
  python scripts/indexnow_push.py --recent N       # only URLs modified in last N days
  python scripts/indexnow_push.py --urls URL1 URL2  # push specific URLs
  python scripts/indexnow_push.py --dry-run        # 只列計畫
"""
from __future__ import annotations
import argparse, json, sys, time
import urllib.request, urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

KEY = 'cb187285fac7ad8ef500998dea9b6f6f2487cb90db7a73528bc650f68189212c'
HOST = 'intelliverse.tw'
KEY_LOCATION = f'https://{HOST}/{KEY}.txt'

# IndexNow 端點（任一個都會自動分享給所有參與的引擎）
ENDPOINTS = [
    'https://api.indexnow.org/IndexNow',     # 預設聚合端點
    'https://www.bing.com/indexnow',         # Bing 直連
    'https://yandex.com/indexnow',           # Yandex 直連
]

UA = 'IntelliverseTW-IndexNow/1.0'


def post_json(url, data, timeout=30):
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(
        url, data=body,
        headers={
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': UA,
            'Host': urllib.parse.urlparse(url).hostname,
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        body_err = e.read().decode('utf-8', errors='replace') if hasattr(e, 'read') else ''
        return e.code, body_err
    except Exception as e:  # noqa: BLE001
        return 0, str(e)


def read_sitemap(sitemap_path: Path) -> list[tuple[str, str | None]]:
    """從 sitemap.xml 讀 (url, lastmod) 列表"""
    if not sitemap_path.exists():
        return []
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    out = []
    for url in root.findall('sm:url', ns):
        loc_el = url.find('sm:loc', ns)
        lm_el = url.find('sm:lastmod', ns)
        if loc_el is not None:
            out.append((loc_el.text, lm_el.text if lm_el is not None else None))
    return out


def push_batch(urls: list[str], endpoint: str) -> tuple[int, str]:
    """單次最多 10 000 URLs / 推一次"""
    payload = {
        'host': HOST,
        'key': KEY,
        'keyLocation': KEY_LOCATION,
        'urlList': urls[:10000],
    }
    return post_json(endpoint, payload)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--sitemap', default='out/sitemap.xml',
                   help='Path to sitemap.xml（預設 out/sitemap.xml，會用 build 結果）')
    p.add_argument('--recent', type=int, default=None,
                   help='只推 lastmod 在最近 N 天內的 URL')
    p.add_argument('--urls', nargs='+', default=None,
                   help='直接指定 URL 列表（覆蓋 sitemap 讀取）')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--limit', type=int, default=None,
                   help='只推前 N 個 URL（除錯用）')
    args = p.parse_args()

    sys.stdout.reconfigure(encoding='utf-8')

    if args.urls:
        urls = args.urls
        print(f'手動指定 {len(urls)} 個 URL')
    else:
        sm_path = Path(args.sitemap)
        entries = read_sitemap(sm_path)
        if not entries:
            print(f'✗ sitemap 為空或不存在：{sm_path}')
            print('  → 先跑 `npx next build` 產出 out/sitemap.xml')
            sys.exit(1)
        urls = []
        cutoff = None
        if args.recent:
            from datetime import datetime, timedelta, timezone
            cutoff = (datetime.now(timezone.utc) - timedelta(days=args.recent))
        for u, lm in entries:
            if cutoff and lm:
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(lm.replace('Z', '+00:00'))
                    if dt < cutoff:
                        continue
                except Exception:
                    pass
            urls.append(u)
        print(f'sitemap → {len(urls)} URLs 將推送')

    if args.limit:
        urls = urls[:args.limit]
        print(f'限制為前 {args.limit} 個')

    if args.dry_run:
        print('--- dry-run ---')
        for u in urls[:20]:
            print(f'  {u}')
        if len(urls) > 20:
            print(f'  ... and {len(urls)-20} more')
        return

    print(f'key: {KEY[:16]}...')
    print(f'keyLocation: {KEY_LOCATION}')
    print(f'host: {HOST}')
    print()

    for endpoint in ENDPOINTS:
        print(f'→ POST {endpoint}')
        status, body = push_batch(urls, endpoint)
        if status in (200, 202):
            print(f'  ✓ {status}  {body[:120]}')
        else:
            print(f'  ✗ {status}  {body[:200]}')
        time.sleep(2)


if __name__ == '__main__':
    main()
