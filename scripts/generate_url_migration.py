"""
generate_url_migration.py — 從 oils.json 產生 URL 語意化遷移計畫

輸出：
1. data/crawled/url_mapping.json — ID → 語意 slug 完整對照
2. data/crawled/cloudflare_bulk_redirects.json — Cloudflare 規則
3. data/crawled/nginx_redirects.conf — Nginx 備用規則
4. data/crawled/htaccess_redirects.conf — Apache 備用規則

策略：
- 已有 46 個語意化頁面的精油 → /oil/N/ 301 redirect → /oil-X/
- 其餘 256 個 datasheet → 保留 /oil/N/（不強制改 URL）
  原因：(a) 不重複內容 (b) 改 URL 風險高 (c) 已有 canonical 修正
"""
import sys
import json
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# 已知對應映射（從 page.tsx CANONICAL_OVERRIDES 同步）
CANONICAL_OVERRIDES = {
    # 柑橘類
    '34': 'oil-lemon', '310': 'oil-lemon',
    '144': 'oil-lemon-eucalyptus',
    '159': 'oil-petitgrain',
    '160': 'oil-bergamot',
    '218': 'oil-neroli',
    '311': 'oil-grapefruit',
    # 花朵類
    '182': 'oil-jasmine',
    '192': 'oil-rose', '234': 'oil-rose',
    '207': 'oil-helichrysum',
    # 菊科
    '92': 'oil-yarrow',
    '108': 'oil-german-chamomile',
    '157': 'oil-roman-chamomile',
    # 薰衣草系
    '82': 'oil-spike-lavender',
    '165': 'oil-lavender', '209': 'oil-lavender',
    '166': 'oil-lavandin',
    # 香草類
    '47': 'oil-rosemary', '87': 'oil-rosemary',
    '150': 'oil-melissa',
    '171': 'oil-clary-sage',
    '222': 'oil-palmarosa',
    '230': 'oil-sweet-basil',
    '233': 'oil-geranium',
    '238': 'oil-thyme',
    # 薄荷類
    '41': 'oil-spearmint',
    '42': 'oil-peppermint', '226': 'oil-peppermint',
    # 呼吸類
    '72': 'oil-bay',
    '73': 'oil-ravintsara',
    '76': 'oil-eucalyptus',
    '224': 'oil-tea-tree',
    # 木質/松柏
    '102': 'oil-myrrh',
    '201': 'oil-cedarwood',
    '285': 'oil-patchouli',
    '287': 'oil-sandalwood',
    '292': 'oil-vetiver',
    '315': 'oil-cypress',
    '320': 'oil-juniper',
    '325': 'oil-black-spruce',
    # 辛香類
    '120': 'oil-ginger',
    '143': 'oil-citronella',
    '252': 'oil-clove',
    '330': 'oil-black-pepper',
    # 樹脂・其他
    '124': 'oil-sweet-fennel',
    '301': 'oil-frankincense',
    # 依蘭
    '97': 'oil-ylang-ylang',
}


def main():
    out_dir = Path(r'C:\Users\User\Desktop\essential-oil-guide\data\crawled')
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load oils.json for context (zh name lookup)
    oils_path = Path(r'C:\Users\User\Desktop\essential-oil-guide\data\oils.json')
    with oils_path.open(encoding='utf-8') as f:
        oils = json.load(f)
    id_to_zh = {o['id']: o.get('zh', '') for o in oils}

    # 1. url_mapping.json — 完整對照表
    mapping = []
    for oid, slug in CANONICAL_OVERRIDES.items():
        mapping.append({
            'id': oid,
            'zh': id_to_zh.get(oid, ''),
            'old_url': f'/oil/{oid}/',
            'new_url': f'/{slug}/',
            'status': 'mapped',
        })
    # Sort by ID
    mapping.sort(key=lambda x: int(x['id']))

    (out_dir / 'url_mapping.json').write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f'✓ url_mapping.json: {len(mapping)} 個對應')

    # 2. Cloudflare Bulk Redirects format
    # https://developers.cloudflare.com/rules/url-forwarding/bulk-redirects/
    cf_rules = []
    for m in mapping:
        cf_rules.append({
            'source_url': f'https://intelliverse.tw{m["old_url"]}',
            'target_url': f'https://intelliverse.tw{m["new_url"]}',
            'status_code': 301,
            'preserve_query_string': False,
            'preserve_path_suffix': False,
        })

    cf_data = {
        '_comment': '上傳到 Cloudflare Dashboard → Bulk Redirects → Create New List',
        '_total_rules': len(cf_rules),
        '_target_zone': 'intelliverse.tw',
        'rules': cf_rules,
    }
    (out_dir / 'cloudflare_bulk_redirects.json').write_text(
        json.dumps(cf_data, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f'✓ cloudflare_bulk_redirects.json: {len(cf_rules)} 條 301 規則')

    # 3. Nginx config
    nginx_lines = [
        '# Nginx 301 redirects: 數字 ID URL → 語意化 URL',
        '# 放在 server 區塊內',
        '',
    ]
    for m in mapping:
        nginx_lines.append(f'rewrite ^{m["old_url"]}$ {m["new_url"]} permanent;')
    (out_dir / 'nginx_redirects.conf').write_text(
        '\n'.join(nginx_lines), encoding='utf-8'
    )
    print(f'✓ nginx_redirects.conf: {len(mapping)} 條 rewrite 規則')

    # 4. Apache .htaccess
    apache_lines = [
        '# Apache .htaccess 301 redirects: 數字 ID URL → 語意化 URL',
        'RewriteEngine On',
        '',
    ]
    for m in mapping:
        apache_lines.append(f'RewriteRule ^oil/{m["id"]}/?$ {m["new_url"]} [R=301,L]')
    (out_dir / 'htaccess_redirects.conf').write_text(
        '\n'.join(apache_lines), encoding='utf-8'
    )
    print(f'✓ htaccess_redirects.conf: {len(mapping)} 條 RewriteRule')

    # 5. Markdown human-readable report
    md_lines = [
        '# URL 語意化遷移計畫',
        '',
        f'共 **{len(mapping)} 個 URL** 需要 301 redirect 從 `/oil/N/` 收編到 `/oil-X/`',
        '',
        '## 對照表',
        '',
        '| ID | 中文名 | 舊 URL | → | 新 URL |',
        '|----|--------|--------|---|--------|',
    ]
    for m in mapping:
        md_lines.append(f'| {m["id"]} | {m["zh"]} | `{m["old_url"]}` | → | `{m["new_url"]}` |')

    md_lines.extend([
        '',
        '## 部署方式（擇一）',
        '',
        '### 方法 A：Cloudflare Bulk Redirects（推薦）',
        '1. 登入 Cloudflare Dashboard',
        '2. 進入 `intelliverse.tw` zone',
        '3. **Rules** → **URL Forwarding** → **Bulk Redirects**',
        '4. Create new list，上傳 `data/crawled/cloudflare_bulk_redirects.json`',
        '5. 啟用 list',
        '',
        '### 方法 B：Nginx (備用)',
        '把 `nginx_redirects.conf` 內容貼到 server 區塊內，重啟 nginx',
        '',
        '### 方法 C：Apache (備用)',
        '把 `htaccess_redirects.conf` 內容貼到網站根目錄 `.htaccess`',
        '',
        '## 為什麼只遷移這 ' + str(len(mapping)) + ' 個',
        '',
        f'oils.json 共 302 個精油 datasheet，但只有 {len(mapping)} 個有對應的完整指南頁面（`/oil-X/`）。',
        '其餘 ~256 個 datasheet 為獨特物種（非重複內容），保留 `/oil/N/` 不需 redirect。',
        '已透過 `app/oil/[id]/page.tsx` 的 `CANONICAL_OVERRIDES` map 處理 canonical 標籤。',
    ])

    (out_dir / 'url_migration_plan.md').write_text(
        '\n'.join(md_lines), encoding='utf-8'
    )
    print(f'✓ url_migration_plan.md')
    print()
    print(f'📁 全部輸出到: {out_dir}')


if __name__ == '__main__':
    main()
