"""
crawl_twaa.py — 透過 crawl4ai server (192.168.1.236:11235) 安全爬取
TWAA 台灣芳療協會（https://www.tw-aa.org/）公開芳療知識內容。

目標：作為 intelliverse.tw「精油能量圖譜」內容擴充的「**參考索引**」。
**不**做逐字轉載，只做摘要 / 重寫 / 主題分類 / FAQ / 風險詞掃描。

源站含「版權所有 © 2016 未經同意請勿任意轉載」明示版權聲明，
所有輸出檔自動標 `copyright_warning: true`。

CLI:
  python scripts/crawl_twaa.py --dry-run                       # 不發任何請求，列計畫
  python scripts/crawl_twaa.py --single-url URL                # 只爬一頁
  python scripts/crawl_twaa.py --max-pages 10 --delay 3        # 小量測試
  python scripts/crawl_twaa.py --max-pages 200 --depth 2       # 第一階段
  python scripts/crawl_twaa.py --resume                        # 從上次中斷處接著爬

支援：
  - 已爬 URL 去重（state file）
  - dry-run / 單頁 / 小量
  - 結構化 JSONL 輸出
  - 風險詞掃描
  - 內容類別分類
  - 自動移除導覽/footer/側欄
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import random
import re
import sys
import time
import urllib.parse as _up
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import urllib.request, urllib.error

# ── 基本設定 ──────────────────────────────────────────────────────────
CRAWL4AI_BASE = os.environ.get('CRAWL4AI_BASE', 'http://192.168.1.236:11235')
SITE_BASE = 'https://www.tw-aa.org/'
ALLOWED_HOSTS = {'www.tw-aa.org', 'tw-aa.org'}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / 'data' / 'crawled'
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_JSONL = OUT_DIR / 'twaa_articles.jsonl'
STATE_FILE = OUT_DIR / 'twaa_crawl_state.json'
REPORT_MD = OUT_DIR / 'twaa_crawl_report.md'
RISK_MD = OUT_DIR / 'twaa_risk_terms_report.md'

# 來源版權警告（每筆都會帶上）
COPYRIGHT_NOTE = '源站「版權所有 © 2016 未經同意請勿任意轉載」— 僅可做摘要/重寫/索引，不可逐字轉載。'
REUSE_POLICY = '只可摘要與重寫，不可逐字轉載'

# 起始 URL（覆蓋使用者列出的所有分類）
SEED_URLS: List[str] = [
    SITE_BASE,
    # tag pages（從首頁解析得到）
    'https://www.tw-aa.org/tags-41.html',   # 芳療新手
    'https://www.tw-aa.org/tags-48.html',   # 國際芳療認證分析
    'https://www.tw-aa.org/tags-33.html',   # 精油功效速查
    'https://www.tw-aa.org/tags-35.html',   # 精油安全守則
    'https://www.tw-aa.org/tags-37.html',   # 最受歡迎的熱門精油
    'https://www.tw-aa.org/tags-42.html',   # 純露使用全攻略
    'https://www.tw-aa.org/tags-53.html',   # 女性經期調理
    'https://www.tw-aa.org/tags-3.html',    # 家長必備精油
    'https://www.tw-aa.org/tags-50.html',   # 寵物芳療
    'https://www.tw-aa.org/tags-51.html',   # 中醫 × 芳療
    'https://www.tw-aa.org/tags-45.html',   # 銀髮族保健
    'https://www.tw-aa.org/tags-43.html',   # 上班族必備精油
    'https://www.tw-aa.org/tags-44.html',   # 學生專注力
    'https://www.tw-aa.org/tags-54.html',   # 芳療戒菸法
    'https://www.tw-aa.org/tags-55.html',   # 告別憂鬱情緒
    'https://www.tw-aa.org/tags-59.html',   # 失眠有救了
    'https://www.tw-aa.org/tags-57.html',   # 星座 × 精油
    'https://www.tw-aa.org/tags-58.html',   # 芳療保健
    'https://www.tw-aa.org/tags-61.html',   # 頭痛/偏頭痛
    'https://www.tw-aa.org/tags-62.html',   # 健康與芳療
]

# 排除字串（URL contains 即跳過）
BLOCKED_URL_SUBSTRINGS = [
    '/wp-admin', '/login', '/cart', '/checkout', '/my-account',
    '/member', '/account', '/wp-login.php',
    'demoev.php', '/admin', '/admincontrol', '/images/logs',
    '?search=',                    # 內部搜尋（重複 + 噪音）
    'pay', 'order',
    'lesson.php', 'about-annual',  # 課程/活動頁，不是知識內容
    '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.zip',
]

# 文章 URL 形態：/articledetail-{id}.html
RE_ARTICLE = re.compile(r'/articledetail-\d+\.html$')
# Tag 列表頁形態：/tags-{id}.html
RE_TAG = re.compile(r'/tags-\d+\.html$')

# 風險詞分類（與 risk_scan.py 對齊）
RISK_WORDS = {
    '醫療療效': ['治療', '療效', '改善疾病', '治癒', '修復傷口', '退燒', '免疫提升'],
    '抗菌抗病毒': ['抗菌', '殺菌', '抗病毒', '消炎', '抗炎', '抗腫瘤', '抗癌'],
    '症狀緩解': ['止痛', '改善失眠', '助眠', '舒緩焦慮', '緩解頭痛', '緩解肌肉酸痛', '祛痰', '化痰'],
    '皮膚醫療': ['治痘', '去痘', '皮膚炎', '濕疹', '過敏治療'],
    '其他高風險': ['神經毒性', '免疫'],
}

# 用於從正文識別精油 / 純露 / 基底油的詞庫
OIL_DICT = [
    '薰衣草', '茶樹', '尤加利', '薄荷', '甜橙', '檸檬', '佛手柑', '乳香', '沒藥', '雪松',
    '迷迭香', '依蘭', '玫瑰', '茉莉', '橙花', '苦橙葉', '丁香', '肉桂', '黑胡椒', '薑',
    '岩蘭草', '檀香', '廣藿香', '快樂鼠尾草', '羅勒', '馬鬱蘭', '甜馬鬱蘭', '葡萄柚', '萊姆',
    '冷杉', '杜松', '絲柏', '松', '黑雲杉', '檸檬尤加利', '茶樹', '辣木',
    '德國洋甘菊', '羅馬洋甘菊', '永久花', '天竺葵', '玫瑰天竺葵',
    '羅文莎葉', '澳洲尤加利', '葡萄柚', '香茅', '檸檬香茅', '玫瑰純露', '橙花純露',
    '荷荷芭', '甜杏仁', '椰子', '酪梨', '芝麻', '橄欖', '玫瑰果', '月見草',
]
HYDROSOL_DICT = ['純露', '橙花純露', '玫瑰純露', '薰衣草純露', '茶樹純露', '迷迭香純露']
CARRIER_DICT = ['基底油', '荷荷芭', '荷荷芭油', '甜杏仁油', '椰子油', '酪梨油', '玫瑰果油', '月見草油']

# 使用情境 / 場景
USE_CASE_DICT = [
    '睡前', '助眠', '失眠', '焦慮', '紓壓', '頭痛', '感冒', '咳嗽', '鼻塞', '塵蟎',
    '寵物', '嬰幼兒', '兒童', '孕婦', '孕期', '經期', '更年期', '中醫', '銀髮',
    '上班', '專注力', '記憶力', '提神', '居家清潔', '消毒', '塵螨', '蚊蟲', '驅蚊',
    '按摩', '擴香', '泡澡', '熱敷', '蒸氣嗅吸',
]

# 安全族群
SAFETY_GROUP_DICT = ['孕婦', '哺乳', '嬰幼兒', '兒童', '老年人', '癲癇', '高血壓', '低血壓', '蠶豆症', '寵物', '貓', '狗']

# ── HTTP / API ────────────────────────────────────────────────────────
def post_json(url: str, payload: Dict[str, Any], timeout: float = 90) -> Dict[str, Any]:
    body = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url, data=body,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))


def fetch_md(url: str, retries: int = 2, timeout: float = 90) -> Optional[str]:
    """呼叫 crawl4ai /md 取得頁面 markdown。失敗回 None。
    HTTP 404/500 視為「頁面不存在」立即放棄（不重試），其它錯誤重試。
    """
    for attempt in range(retries + 1):
        try:
            data = post_json(
                f'{CRAWL4AI_BASE}/md',
                {'url': url, 'f': 'fit'},
                timeout=timeout,
            )
            if not data.get('success', True):
                raise RuntimeError(f'crawl4ai returned success=false: {data}')
            return data.get('markdown', '') or ''
        except urllib.error.HTTPError as e:
            # 4xx/5xx 視為頁面不存在或永久錯誤，不重試
            if e.code in (404, 500, 502, 503):
                print(f'  ✗ HTTP {e.code}: {url}', flush=True)
                return None
            if attempt < retries:
                wait = 2 + attempt * 2
                print(f'  ! retry {attempt+1}/{retries} after {wait}s (HTTP {e.code})', flush=True)
                time.sleep(wait)
            else:
                return None
        except Exception as e:  # noqa: BLE001
            if attempt < retries:
                wait = 2 + attempt * 2
                print(f'  ! retry {attempt+1}/{retries} after {wait}s ({e})', flush=True)
                time.sleep(wait)
            else:
                print(f'  ✗ failed {url}: {e}', flush=True)
                return None
    return None


# ── 內容清洗 ──────────────────────────────────────────────────────────
NOISE_PATTERNS = [
    r'^\s*Top\s*↑\s*$',
    r'^#{0,4}\s*(最新文章|推薦文章|熱門文章|相關推薦|延伸閱讀|關鍵字)\s*$',
    r'^\s*Previous\s*$', r'^\s*Next\s*$',
    r'^\s*圖片來源[:：]',
    r'^\s*版權所有.*$',
    r'^\s*\* \[.*\]\(.*\)\s*$',  # bare nav-style link list rows
]

def clean_markdown(md: str) -> Tuple[str, List[str]]:
    """切掉 nav / footer / 推薦/熱門/側欄列表。回傳 (cleaned, captured_link_titles)。"""
    if not md:
        return '', []

    lines = md.split('\n')
    # 找到「熱門文章 / 最新文章 / 推薦文章」這類段落起點，切掉之後（多半是側欄）
    cut_idx = len(lines)
    sidebar_markers = ['#### 最新文章', '#### 推薦文章', '#### 熱門文章', '推薦文章', '延伸閱讀']
    seen_main = False
    for i, ln in enumerate(lines):
        stripped = ln.strip()
        if stripped.startswith('# ') and not seen_main:
            seen_main = True
            continue
        if seen_main and any(m == stripped for m in sidebar_markers):
            cut_idx = i
            break
    kept = lines[:cut_idx]

    # 移除常見導覽 / 噪音
    out: List[str] = []
    captured: List[str] = []
    for ln in kept:
        if any(re.match(p, ln) for p in NOISE_PATTERNS):
            continue
        # 抓「[title](url)」純連結行的 title
        m = re.match(r'^\s*\[([^\]]{2,})\]\([^)]+\)\s*$', ln)
        if m:
            captured.append(m.group(1).strip())
            continue
        out.append(ln)
    cleaned = '\n'.join(out).strip()
    # 清掉重複空行
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned, captured


# ── 連結擷取 ──────────────────────────────────────────────────────────
# Markdown link 形式：
#   [text](URL)
#   [text](URL "title")
# 都要抓得到（TWAA 大量用後者）
RE_LINK = re.compile(r'\]\((https?://[^)\s"]+)(?:\s+"[^"]*")?\)')

def extract_links(md: str) -> List[str]:
    seen: Set[str] = set()
    out: List[str] = []
    for m in RE_LINK.finditer(md or ''):
        u = m.group(1).split('#')[0].split('?')[0]  # strip fragment + query
        if u in seen:
            continue
        seen.add(u)
        out.append(u)
    return out


def is_allowed(url: str) -> bool:
    try:
        p = _up.urlparse(url)
    except Exception:  # noqa: BLE001
        return False
    if p.netloc not in ALLOWED_HOSTS:
        return False
    low = url.lower()
    for b in BLOCKED_URL_SUBSTRINGS:
        if b in low:
            return False
    return True


def url_kind(url: str) -> str:
    if RE_ARTICLE.search(url):
        return 'article'
    if RE_TAG.search(url):
        return 'tag'
    if url.rstrip('/') == SITE_BASE.rstrip('/'):
        return 'home'
    return 'other'


# ── 內容萃取 / NER ────────────────────────────────────────────────────
RE_TITLE = re.compile(r'^#\s+(.+?)\s*$', re.M)
RE_DATE = re.compile(r'(20\d{2})[/-](\d{1,2})[/-](\d{1,2})')

def first_h1(md: str) -> str:
    m = RE_TITLE.search(md)
    return (m.group(1).strip() if m else '').strip()


def find_date(md: str) -> Optional[str]:
    m = RE_DATE.search(md)
    if not m:
        return None
    y, mo, d = m.groups()
    try:
        return f'{int(y):04d}-{int(mo):02d}-{int(d):02d}'
    except Exception:  # noqa: BLE001
        return None


def find_entities(plain: str) -> Dict[str, List[str]]:
    """從清洗後 plain text 找精油 / 純露 / 基底油 / 情境 / 安全族群"""
    found_oils = sorted({o for o in OIL_DICT if o in plain})
    found_hydro = sorted({h for h in HYDROSOL_DICT if h in plain})
    found_carrier = sorted({c for c in CARRIER_DICT if c in plain})
    found_uc = sorted({u for u in USE_CASE_DICT if u in plain})
    found_sg = sorted({s for s in SAFETY_GROUP_DICT if s in plain})
    return {
        'essential_oils': found_oils,
        'hydrosols': found_hydro,
        'carrier_oils': found_carrier,
        'conditions_or_use_cases': found_uc,
        'safety_groups': found_sg,
    }


def find_risk_terms(plain: str) -> List[Dict[str, Any]]:
    """掃 plain 中所有高風險字，回傳[{word,category,excerpt}]"""
    hits: List[Dict[str, Any]] = []
    seen_pairs: Set[Tuple[str, int]] = set()
    for cat, words in RISK_WORDS.items():
        for w in words:
            for m in re.finditer(re.escape(w), plain):
                key = (w, m.start())
                if key in seen_pairs:
                    continue
                seen_pairs.add(key)
                s = max(0, m.start() - 25)
                e = min(len(plain), m.end() + 30)
                hits.append({
                    'word': w,
                    'category': cat,
                    'excerpt': plain[s:e].replace('\n', ' ').strip(),
                })
    return hits


def make_summary(plain: str, max_chars: int = 180) -> str:
    """簡易摘要：取前面有實質內容的前 N 字，去除星號/連結等"""
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', plain)
    text = re.sub(r'[#*_>`-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    # 去頭部 h1（已經單獨抓了）
    if not text:
        return ''
    return text[:max_chars].rstrip() + ('…' if len(text) > max_chars else '')


def make_key_points(plain: str, max_n: int = 5) -> List[str]:
    """抓條列 / 段落首句作為 key_points"""
    points: List[str] = []
    # 1) bullet lines
    for ln in plain.split('\n'):
        m = re.match(r'^\s*[\*\-]\s+(.{8,80}?)[\s。：]', ln)
        if m:
            t = m.group(1).strip()
            if t and t not in points:
                points.append(t)
        if len(points) >= max_n:
            break
    # 2) bold 段落（**...**）
    if len(points) < max_n:
        for m in re.finditer(r'\*\*([^*\n]{3,40})\*\*', plain):
            t = m.group(1).strip()
            if t and t not in points:
                points.append(t)
            if len(points) >= max_n:
                break
    return points[:max_n]


def page_type_of(url: str, md: str, plain: str) -> str:
    kind = url_kind(url)
    if kind == 'tag' or kind == 'home':
        return 'listing'
    # 文章但內容太少 → listing 般
    if len(plain) < 250:
        return 'listing'
    return 'article'


# ── 主流程 ────────────────────────────────────────────────────────────
def load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding='utf-8'))
        except Exception:  # noqa: BLE001
            pass
    return {'visited': [], 'queued': []}


def save_state(state: Dict[str, Any]) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')


def append_jsonl(record: Dict[str, Any]) -> None:
    with OUT_JSONL.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def derive_category(url: str, plain: str, captured: List[str]) -> str:
    """從 URL/正文/標題候選推測分類"""
    map_kw = [
        ('安全', '芳療安全'),
        ('禁忌', '芳療安全'),
        ('稀釋', '芳療安全'),
        ('純露', '關於純露'),
        ('基底油', '關於基底油'),
        ('DIY', '精油DIY'),
        ('懶人包', '芳療懶人包'),
        ('小貼士', '芳療小貼士'),
        ('保健', '芳療保健'),
        ('美容', '精油美容'),
        ('按摩', '精油按摩'),
        ('心靈', '心靈芳療'),
        ('中醫', '中醫芳療'),
        ('居家', '居家芳療'),
        ('兒童', '兒童芳療'),
        ('長輩', '長輩芳療'),
        ('銀髮', '長輩芳療'),
        ('新趨勢', '芳療新趨勢'),
        ('筆記', '芳療學習筆記'),
        ('參考文獻', '參考文獻'),
        ('精油', '關於精油'),
    ]
    for kw, cat in map_kw:
        if kw in plain[:300] or any(kw in c for c in captured[:5]):
            return cat
    return '芳療知識'


def process_page(url: str) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    """爬一頁、回傳 (record_or_None, discovered_links)"""
    md = fetch_md(url)
    if md is None:
        return None, []
    cleaned, captured = clean_markdown(md)
    title = first_h1(md) or first_h1(cleaned) or '(無標題)'
    date_pub = find_date(md)
    plain = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', cleaned)
    plain = re.sub(r'[#*_>`]', '', plain)
    plain = re.sub(r'\s+', ' ', plain).strip()
    page_type = page_type_of(url, md, plain)
    entities = find_entities(plain)
    risk_hits = find_risk_terms(plain)
    risk_words = sorted({h['word'] for h in risk_hits})
    quality = 'low' if len(plain) < 300 else ('medium' if len(plain) < 1200 else 'high')
    record = {
        'source_site': 'TWAA 台灣芳療協會',
        'source_url': url,
        'title': title,
        'date_published': date_pub,
        'date_crawled': _dt.date.today().isoformat(),
        'category': derive_category(url, plain, captured),
        'tags': [],
        'page_type': page_type,
        'content_quality': quality,
        'raw_markdown': cleaned,           # 已清洗，僅供索引比對；不可直接發佈
        'summary_zh': make_summary(plain),
        'key_points': make_key_points(cleaned),
        'entities': entities,
        'risk_terms': risk_words,
        'risk_hits': risk_hits[:30],
        'copyright_warning': True,
        'reuse_policy': REUSE_POLICY,
    }
    links = [u for u in extract_links(md) if is_allowed(u)]
    return record, links


def plan_seeds(extra_seed: Optional[str] = None) -> List[str]:
    seeds = list(SEED_URLS)
    if extra_seed:
        seeds.append(extra_seed)
    return [s for s in seeds if is_allowed(s)]


def crawl(args: argparse.Namespace) -> None:
    state = load_state() if args.resume else {'visited': [], 'queued': []}
    visited: Set[str] = set(state.get('visited', []))
    # state 中的 queued 可能是 ['url',...] 舊格式或 [['url',depth],...] 新格式
    queue: List[Tuple[str, int]] = []
    for item in state.get('queued', []):
        if isinstance(item, list) and len(item) == 2:
            queue.append((item[0], int(item[1])))
        elif isinstance(item, str):
            # 舊 state：URL 沒帶 depth，視為 1（曾從 depth-0 listing 發現的）
            queue.append((item, 1))

    if not queue:
        seeds = plan_seeds(args.single_url)
        for s in seeds:
            if s not in visited:
                queue.append((s, 0))

    print(f'crawl4ai: {CRAWL4AI_BASE}', flush=True)
    print(f'seeds: {len(queue)} / visited so far: {len(visited)} / max_pages: {args.max_pages} / depth: {args.depth}', flush=True)
    print(f'dry_run={args.dry_run} single_url={args.single_url}', flush=True)
    print(f'output: {OUT_JSONL}', flush=True)
    print('---', flush=True)

    if args.dry_run:
        print('[dry-run] would crawl:', flush=True)
        for u, d in queue[:30]:
            print(f'  d={d} {u}')
        if len(queue) > 30:
            print(f'  ... and {len(queue)-30} more')
        return

    # 若 single_url，只跑那頁
    if args.single_url:
        queue = [(args.single_url, 0)]

    pages_done = 0
    # 優先順序：article > tag > 其它；同優先順序內依插入順序
    def queue_key(item: Tuple[str, int]) -> Tuple[int, int]:
        u, d = item
        k = url_kind(u)
        prio = {'article': 0, 'tag': 1}.get(k, 2)
        return (prio, d)

    while queue and pages_done < args.max_pages:
        # 每輪取「優先級最高」的一筆
        queue.sort(key=queue_key)
        url, depth = queue.pop(0)
        if url in visited:
            continue
        if depth > args.depth:
            continue
        visited.add(url)
        print(f'[{pages_done+1}/{args.max_pages}] d={depth} {url}', flush=True)

        rec, links = process_page(url)
        if rec is None:
            pages_done += 1
            time.sleep(args.delay + random.uniform(0, 1))
            continue

        # 只把 page_type=article 寫進 JSONL；listing 頁只用來探索
        if rec['page_type'] == 'article':
            append_jsonl(rec)

        # 探索新連結（只 article + tag）
        if depth < args.depth:
            for nu in links:
                if nu in visited:
                    continue
                kind = url_kind(nu)
                if kind not in {'article', 'tag'}:
                    continue
                queue.append((nu, depth + 1))

        pages_done += 1

        # 存 state（每頁存一次，方便 resume；保留 [url, depth] 配對）
        save_state({
            'visited': sorted(visited),
            'queued': [[u, d] for (u, d) in queue],
        })

        time.sleep(args.delay + random.uniform(0, 1))

    print('---', flush=True)
    print(f'done. visited={len(visited)} written_records={count_jsonl(OUT_JSONL)}', flush=True)


def count_jsonl(p: Path) -> int:
    if not p.exists():
        return 0
    return sum(1 for _ in p.open('r', encoding='utf-8'))


# ── 報告產生 ──────────────────────────────────────────────────────────
def load_jsonl(p: Path) -> List[Dict[str, Any]]:
    if not p.exists():
        return []
    out: List[Dict[str, Any]] = []
    for ln in p.open('r', encoding='utf-8'):
        ln = ln.strip()
        if ln:
            try:
                out.append(json.loads(ln))
            except json.JSONDecodeError:
                continue
    return out


def make_report() -> None:
    records = load_jsonl(OUT_JSONL)
    n = len(records)
    article_n = sum(1 for r in records if r.get('page_type') == 'article')
    low_n = sum(1 for r in records if r.get('content_quality') == 'low')

    cat_cnt = Counter(r.get('category') for r in records)
    oil_cnt: Counter[str] = Counter()
    uc_cnt: Counter[str] = Counter()
    sg_cnt: Counter[str] = Counter()
    risk_cnt: Counter[str] = Counter()
    for r in records:
        e = r.get('entities') or {}
        oil_cnt.update(e.get('essential_oils') or [])
        uc_cnt.update(e.get('conditions_or_use_cases') or [])
        sg_cnt.update(e.get('safety_groups') or [])
        risk_cnt.update(r.get('risk_terms') or [])

    md: List[str] = []
    md.append('# TWAA 爬取內容分析報告')
    md.append('')
    md.append(f'> 來源：TWAA 台灣芳療協會 https://www.tw-aa.org/  ')
    md.append(f'> 版權聲明：源站「版權所有 © 2016 未經同意請勿任意轉載」  ')
    md.append(f'> 重用政策：**{REUSE_POLICY}**  ')
    md.append(f'> 產生日期：{_dt.date.today().isoformat()}  ')
    md.append('')
    md.append('## 統計')
    md.append('')
    md.append(f'- 已爬頁數（含 listing）：{n + sum(1 for r in records if r.get("page_type")=="listing")}')
    md.append(f'- 寫入 JSONL 的文章頁：**{article_n}**')
    md.append(f'- 內容品質 low 的頁面：{low_n}')
    md.append(f'- 分類分布：')
    for cat, c in cat_cnt.most_common():
        md.append(f'  - {cat}：{c}')
    md.append('')
    md.append('## 最常見精油（Top 20）')
    md.append('')
    md.append('| # | 精油 | 出現文章數 |')
    md.append('|---|---|---|')
    for i, (oil, c) in enumerate(oil_cnt.most_common(20), 1):
        md.append(f'| {i} | {oil} | {c} |')
    md.append('')
    md.append('## 最常見使用情境（Top 15）')
    md.append('')
    md.append('| # | 情境 | 出現文章數 |')
    md.append('|---|---|---|')
    for i, (uc, c) in enumerate(uc_cnt.most_common(15), 1):
        md.append(f'| {i} | {uc} | {c} |')
    md.append('')
    md.append('## 最常見安全族群')
    md.append('')
    md.append('| # | 族群 | 出現文章數 |')
    md.append('|---|---|---|')
    for i, (sg, c) in enumerate(sg_cnt.most_common(10), 1):
        md.append(f'| {i} | {sg} | {c} |')
    md.append('')
    md.append('## 高風險療效詞統計（Top 20）')
    md.append('')
    md.append('| # | 字詞 | 出現文章數 |')
    md.append('|---|---|---|')
    for i, (w, c) in enumerate(risk_cnt.most_common(20), 1):
        md.append(f'| {i} | {w} | {c} |')
    md.append('')
    md.append('## 推薦 intelliverse.tw 可補充的內容主題')
    md.append('')
    # 推薦：oil_cnt 前 10 但 intelliverse 沒有
    md.append('（依爬取內容中出現頻率最高的精油 / 情境 / 族群推測）')
    md.append('')
    md.append('| 建議方向 | 來源證據 |')
    md.append('|---|---|')
    for oil, c in oil_cnt.most_common(10):
        md.append(f'| 完整指南：{oil}精油 | TWAA 提到 {c} 次 |')
    for uc, c in uc_cnt.most_common(5):
        md.append(f'| 主題文章：精油與「{uc}」 | TWAA 提到 {c} 次 |')
    md.append('')
    md.append('## 不建議直接使用的頁面原因')
    md.append('')
    md.append('1. 源站有版權聲明，**不可逐字搬運**')
    md.append('2. 部分文章帶高療效宣稱（治療、抗病毒、抗癌），不可照抄 → 須改寫為非醫療語氣')
    md.append('3. 文章類別重複度高，建議「同主題多篇 → intelliverse 整併成一篇大文」')
    md.append('')
    REPORT_MD.write_text('\n'.join(md), encoding='utf-8')
    print(f'report → {REPORT_MD}', flush=True)


def make_risk_report() -> None:
    records = load_jsonl(OUT_JSONL)
    md: List[str] = []
    md.append('# TWAA 高風險療效字詞統計')
    md.append('')
    md.append(f'> 此報告僅供 intelliverse.tw 改寫時對照使用。源站版權聲明：「未經同意請勿任意轉載」。')
    md.append(f'> 原文節錄不超過 30 字，僅供識別風險詞上下文。')
    md.append('')
    md.append('## 通用改寫建議')
    md.append('')
    md.append('| 醫療字眼 | intelliverse 建議改為 |')
    md.append('|---|---|')
    suggestions = {
        '治療': '日常香氛 / 香氛搭配',
        '治癒': '陪伴感受',
        '療效': '常見用途',
        '抗菌': '清新香氛',
        '殺菌': '空間香氛',
        '抗病毒': '空間清新感',
        '消炎': '肌膚保養',
        '抗炎': '舒適感受',
        '止痛': '放鬆按摩',
        '改善失眠': '睡前儀式',
        '助眠': '睡前放鬆氛圍',
        '舒緩焦慮': '情緒支持',
        '緩解頭痛': '太陽穴放鬆按摩',
        '緩解肌肉酸痛': '運動後放鬆按摩',
        '祛痰': '呼吸放鬆氛圍',
        '化痰': '呼吸香氛',
        '抗腫瘤': '研究文獻探討（非醫療建議）',
        '抗癌': '建議刪除或標研究背景',
        '免疫': '日常保養支持',
        '退燒': '建議刪除（醫療字眼）',
        '皮膚炎': '肌膚不適',
        '濕疹': '肌膚乾燥不適',
        '神經毒性': '保留並加註研究背景、非醫療建議',
    }
    for k, v in suggestions.items():
        md.append(f'| {k} | {v} |')
    md.append('')
    md.append('## 各文章命中明細')
    md.append('')
    for r in records:
        hits = r.get('risk_hits') or []
        if not hits:
            continue
        md.append(f'### {r.get("title","(無標題)")} ')
        md.append(f'`{r.get("source_url")}`  ')
        for h in hits[:8]:
            md.append(f'- **「{h["word"]}」**（{h["category"]}）')
            md.append(f'  - 節錄：`...{h["excerpt"]}...`')
            md.append(f'  - 建議：{suggestions.get(h["word"], "（人工審核）")}')
        if len(hits) > 8:
            md.append(f'- _還有 {len(hits)-8} 處風險詞_')
        md.append('')
    RISK_MD.write_text('\n'.join(md), encoding='utf-8')
    print(f'risk report → {RISK_MD}', flush=True)


# ── CLI ───────────────────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='Crawl TWAA via crawl4ai server')
    p.add_argument('--max-pages', type=int, default=10)
    p.add_argument('--depth', type=int, default=2)
    p.add_argument('--delay', type=float, default=3.0, help='requests interval in seconds (+ jitter)')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--single-url', type=str, default=None)
    p.add_argument('--resume', action='store_true')
    p.add_argument('--report-only', action='store_true', help='跳過爬蟲，只重生報告')
    return p


def main() -> None:
    sys.stdout.reconfigure(encoding='utf-8')
    args = build_parser().parse_args()
    if not args.report_only:
        crawl(args)
    make_report()
    make_risk_report()


if __name__ == '__main__':
    main()
