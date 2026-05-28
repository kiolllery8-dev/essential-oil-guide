"""
graph_to_related_links.py — 把知識圖譜的關係邊轉成網站的「智慧關聯精油」區塊

用途（SEO #1 內鏈 + #2 智慧相關精油）：
  1. 從 knowledge-graph.json 抽出每支精油的真實關係
     - contradicts → 安全/特性對比（最有價值，導向比較）
     - builds_on   → 替代/進階關係
     - related     → 常見搭配/相關
     - 同化學分類 / 同植物科 → 同類精油
  2. 產生「🔗 智慧關聯」HTML 區塊注入各 oil-*.html（idempotent）
  3. 輸出關係資料 JSON 供 internalLinks.ts 參考

執行：
  python scripts/graph_to_related_links.py            # 注入網站
  python scripts/graph_to_related_links.py --dry-run  # 只看每支精油的關聯
"""
import sys
import json
import re
import argparse
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r'C:\Users\User\Desktop\essential-oil-guide')
GRAPH = ROOT / 'knowledge-wiki' / '.understand-anything' / 'knowledge-graph.json'
HTML_DIR = ROOT / 'html-source'

# 中文精油名 → 網站 slug（46 支有完整頁面的）
NAME_TO_SLUG = {
    '真正薰衣草': 'oil-lavender', '穗花薰衣草': 'oil-spike-lavender', '醒目薰衣草': 'oil-lavandin',
    '茶樹': 'oil-tea-tree', '尤加利': 'oil-eucalyptus', '胡椒薄荷': 'oil-peppermint',
    '綠薄荷': 'oil-spearmint', '甜橙': 'oil-sweet-orange', '柑橘': 'oil-mandarin',
    '檸檬': 'oil-lemon', '葡萄柚': 'oil-grapefruit', '佛手柑': 'oil-bergamot',
    '橙花': 'oil-neroli', '苦橙葉': 'oil-petitgrain', '玫瑰': 'oil-rose',
    '茉莉': 'oil-jasmine', '依蘭': 'oil-ylang-ylang', '義大利永久花': 'oil-helichrysum',
    '羅馬洋甘菊': 'oil-roman-chamomile', '德國洋甘菊': 'oil-german-chamomile', '西洋蓍草': 'oil-yarrow',
    '迷迭香': 'oil-rosemary', '甜馬鬱蘭': 'oil-marjoram', '快樂鼠尾草': 'oil-clary-sage',
    '甜羅勒': 'oil-sweet-basil', '百里香': 'oil-thyme', '香蜂草': 'oil-melissa',
    '天竺葵': 'oil-geranium', '玫瑰草': 'oil-palmarosa', '桉油醇樟': 'oil-ravintsara',
    '檸檬尤加利': 'oil-lemon-eucalyptus', '月桂': 'oil-bay', '大西洋雪松': 'oil-cedarwood',
    '檀香': 'oil-sandalwood', '杜松漿果': 'oil-juniper', '絲柏': 'oil-cypress',
    '黑雲杉': 'oil-black-spruce', '廣藿香': 'oil-patchouli', '岩蘭草': 'oil-vetiver',
    '薑': 'oil-ginger', '黑胡椒': 'oil-black-pepper', '丁香': 'oil-clove',
    '香茅': 'oil-citronella', '乳香': 'oil-frankincense', '沒藥': 'oil-myrrh',
    '甜茴香': 'oil-sweet-fennel',
}
SLUG_TO_NAME = {v: k for k, v in NAME_TO_SLUG.items()}

EMOJI = {
    'oil-lavender': '💜', 'oil-spike-lavender': '💜', 'oil-lavandin': '🪻',
    'oil-tea-tree': '🌲', 'oil-eucalyptus': '🌿', 'oil-peppermint': '🌿',
    'oil-spearmint': '🌿', 'oil-sweet-orange': '🍊', 'oil-mandarin': '🍊',
    'oil-lemon': '🍋', 'oil-grapefruit': '🍊', 'oil-bergamot': '🍋',
    'oil-neroli': '🌼', 'oil-petitgrain': '🌿', 'oil-rose': '🌹',
    'oil-jasmine': '🌸', 'oil-ylang-ylang': '🌸', 'oil-helichrysum': '🌼',
    'oil-roman-chamomile': '🌼', 'oil-german-chamomile': '💙', 'oil-yarrow': '💙',
    'oil-rosemary': '🌱', 'oil-marjoram': '🌿', 'oil-clary-sage': '🌸',
    'oil-sweet-basil': '🌿', 'oil-thyme': '🌿', 'oil-melissa': '🌿',
    'oil-geranium': '🌸', 'oil-palmarosa': '🌾', 'oil-ravintsara': '🌿',
    'oil-lemon-eucalyptus': '🍋', 'oil-bay': '🌿', 'oil-cedarwood': '🌲',
    'oil-sandalwood': '🌳', 'oil-juniper': '🌲', 'oil-cypress': '🌲',
    'oil-black-spruce': '🌲', 'oil-patchouli': '🌿', 'oil-vetiver': '🌾',
    'oil-ginger': '🫚', 'oil-black-pepper': '🌶️', 'oil-clove': '🌶️',
    'oil-citronella': '🌾', 'oil-frankincense': '🌳', 'oil-myrrh': '🌳',
    'oil-sweet-fennel': '🌿',
}


def load_graph():
    g = json.load(open(GRAPH, encoding='utf-8'))
    nodes = {n['id']: n for n in g['nodes']}
    return g, nodes


def article_name(nid, nodes):
    n = nodes.get(nid, {})
    return n.get('name', '')


def build_relations():
    g, nodes = load_graph()

    # 每支精油的關係：{slug: {contradicts:[], builds_on_out:[], builds_on_in:[], related:[], chem:set, family:str}}
    rel = {slug: {'contradicts': [], 'builds_out': [], 'builds_in': [],
                  'related': [], 'chem': set(), 'family': None}
           for slug in SLUG_TO_NAME}

    # 收集精油的化學分類與植物科（從 article node 的 frontmatter/tags）
    for nid, n in nodes.items():
        name = n.get('name', '')
        if name in NAME_TO_SLUG and n.get('type') == 'article':
            slug = NAME_TO_SLUG[name]
            km = n.get('knowledgeMeta', {})
            # family from frontmatter in content
            content = km.get('content', '')
            mfam = re.search(r'family:\s*(\S+)', content)
            if mfam:
                rel[slug]['family'] = mfam.group(1)
            mtags = re.search(r'tags:\s*\[([^\]]*)\]', content)
            if mtags:
                tags = re.findall(r'"([^"]+)"', mtags.group(1))
                rel[slug]['chem'] = set(tags)

    # 處理邊
    for e in g['edges']:
        s_name = article_name(e['source'], nodes)
        t_name = article_name(e['target'], nodes)
        s_slug = NAME_TO_SLUG.get(s_name)
        t_slug = NAME_TO_SLUG.get(t_name)
        etype = e['type']
        desc = e.get('description', '')

        # 只關心兩端都是精油頁（或一端精油一端概念）
        if etype == 'contradicts':
            if s_slug and t_slug:
                rel[s_slug]['contradicts'].append((t_slug, desc))
                rel[t_slug]['contradicts'].append((s_slug, desc))
        elif etype == 'builds_on':
            if s_slug and t_slug:
                rel[s_slug]['builds_out'].append((t_slug, desc))
                rel[t_slug]['builds_in'].append((s_slug, desc))
        elif etype == 'related':
            if s_slug and t_slug:
                rel[s_slug]['related'].append(t_slug)
                rel[t_slug]['related'].append(s_slug)

    # 同化學分類 / 同科 補充（按共用分類數排序，越相似越前面）
    for slug, data in rel.items():
        scored = []
        siblings_fam = []
        for other_slug, other in rel.items():
            if other_slug == slug:
                continue
            overlap = len(data['chem'] & other['chem'])
            if overlap:
                # 同科 +1 加權
                same_fam = 1 if (data['family'] and data['family'] == other['family']) else 0
                scored.append((overlap + same_fam, other_slug))
            if data['family'] and data['family'] == other['family']:
                siblings_fam.append(other_slug)
        scored.sort(reverse=True)
        data['same_chem'] = [s for _, s in scored]
        data['same_family'] = siblings_fam

    # 真正的「應用情境」節點名稱（category == 應用情境）
    usecase_names = {n['name'] for n in nodes.values()
                     if n.get('knowledgeMeta', {}).get('category') == '應用情境'}

    # 同應用情境（只算真正的 use-case 節點，排除化學/科/安全/學派等通用概念）
    usecase_oils = {}  # usecase_name -> [oil_slug]
    for n in nodes.values():
        if n.get('name') in NAME_TO_SLUG and n.get('type') == 'article':
            slug = NAME_TO_SLUG[n['name']]
            for wl in n.get('knowledgeMeta', {}).get('wikilinks', []):
                if wl in usecase_names:
                    usecase_oils.setdefault(wl, [])
                    if slug not in usecase_oils[wl]:
                        usecase_oils[wl].append(slug)
    for slug, data in rel.items():
        name = SLUG_TO_NAME[slug]
        sibs = []
        node = next((n for n in nodes.values() if n.get('name') == name and n.get('type') == 'article'), None)
        if node:
            for wl in node.get('knowledgeMeta', {}).get('wikilinks', []):
                if wl in usecase_names:
                    for o in usecase_oils.get(wl, []):
                        if o != slug and o not in sibs:
                            sibs.append(o)
        data['same_usecase'] = sibs

    return rel


def render_section(slug, data):
    """產生「🔗 智慧關聯」HTML 區塊"""
    def card(target_slug, label):
        name = SLUG_TO_NAME.get(target_slug, target_slug)
        emoji = EMOJI.get(target_slug, '🌿')
        return (f'<a href="{target_slug}.html" class="rel-oil-card" '
                f'style="display:flex;align-items:center;gap:10px;padding:12px 14px;'
                f'background:#fff;border:1px solid var(--border,#E5D9C0);border-radius:10px;'
                f'text-decoration:none;color:inherit;transition:transform .15s,box-shadow .2s;">'
                f'<span style="font-size:22px;flex-shrink:0;">{emoji}</span>'
                f'<span style="flex:1;"><span style="display:block;font-weight:600;font-size:14px;color:#3D3328;">{name}</span>'
                f'<span style="display:block;font-size:12px;color:#8B6F3E;margin-top:2px;">{label}</span></span></a>')

    blocks = []
    seen = set()

    # 安全/特性對比（contradicts）— 最有價值
    for tslug, desc in data['contradicts'][:3]:
        if tslug in seen:
            continue
        seen.add(tslug)
        blocks.append(card(tslug, '⚡ 安全特性對比'))

    # 替代/進階（builds_on）
    for tslug, desc in data['builds_in'][:2]:  # 別人 builds_on 我 = 我是更溫和/原型
        if tslug in seen:
            continue
        seen.add(tslug)
        blocks.append(card(tslug, '🔄 替代選擇'))
    for tslug, desc in data['builds_out'][:2]:
        if tslug in seen:
            continue
        seen.add(tslug)
        blocks.append(card(tslug, '⬆️ 進階/衍生'))

    # 常見搭配（related）
    for tslug in data['related']:
        if len(blocks) >= 8:
            break
        if tslug in seen:
            continue
        seen.add(tslug)
        blocks.append(card(tslug, '🤝 常見搭配'))

    # 同類精油（同化學分類）補滿到 8
    for tslug in data['same_chem']:
        if len(blocks) >= 8:
            break
        if tslug in seen:
            continue
        seen.add(tslug)
        blocks.append(card(tslug, '🧬 同化學分類'))

    # 後備：同植物科（給單一成員化學類的精油，如永久花/甜茴香）
    for tslug in data.get('same_family', []):
        if len(blocks) >= 8:
            break
        if tslug in seen:
            continue
        seen.add(tslug)
        blocks.append(card(tslug, '🌱 同植物科'))

    # 最終後備：同應用情境（給化學/植物科都獨特的精油，如甜茴香）
    for tslug in data.get('same_usecase', []):
        if len(blocks) >= 6:
            break
        if tslug in seen:
            continue
        seen.add(tslug)
        blocks.append(card(tslug, '🎯 相似應用'))

    if not blocks:
        return None

    cards_html = '\n    '.join(blocks)
    return f'''<!-- ===== 🔗 智慧關聯精油（由知識圖譜生成）===== -->
<section style="max-width:920px;margin:32px auto;padding:0 20px;">
  <h2 style="font-size:20px;font-weight:700;color:var(--green-dark,#3a5a40);margin:0 0 6px;padding-bottom:8px;border-bottom:2px solid var(--beige,#E5D9C0);">🔗 智慧關聯精油</h2>
  <p style="font-size:13px;color:var(--text-mid,#7A6852);margin:0 0 16px;">由 IFA 知識圖譜分析精油間的化學、安全與應用關係自動生成。</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;">
    {cards_html}
  </div>
</section>'''


def inject(rel, dry_run):
    pat = re.compile(
        r'\s*<!-- ===== 🔗 智慧關聯精油.*?===== -->.*?</section>',
        re.DOTALL
    )
    updated = 0
    for slug, data in rel.items():
        section = render_section(slug, data)
        if dry_run:
            n_rel = len(data['contradicts']) + len(data['builds_in']) + len(data['builds_out'])
            print(f'{slug}: contradicts={len(data["contradicts"])} '
                  f'builds_in={len(data["builds_in"])} builds_out={len(data["builds_out"])} '
                  f'related={len(set(data["related"]))} same_chem={len(data["same_chem"])}')
            if data['contradicts']:
                for t, d in data['contradicts'][:2]:
                    print(f'    ⚡ vs {SLUG_TO_NAME.get(t,t)}')
            continue
        if not section:
            continue
        path = HTML_DIR / f'{slug}.html'
        if not path.exists():
            continue
        content = path.read_text(encoding='utf-8')
        # Remove existing
        content = pat.sub('', content)
        # Insert before footer, else before </body>
        if '<footer' in content:
            content = content.replace('<footer', section + '\n\n<footer', 1)
        elif '</body>' in content:
            content = content.replace('</body>', section + '\n</body>', 1)
        else:
            content += '\n' + section
        path.write_text(content, encoding='utf-8')
        updated += 1
    if not dry_run:
        print(f'✓ 注入 {updated} 個精油頁的智慧關聯區塊')

    # 輸出關係 JSON 供 internalLinks 參考
    if not dry_run:
        out = ROOT / 'data' / 'crawled' / 'graph_relations.json'
        export = {}
        for slug, data in rel.items():
            export[slug] = {
                'contradicts': [t for t, _ in data['contradicts']],
                'builds_on': [t for t, _ in data['builds_out']],
                'is_base_for': [t for t, _ in data['builds_in']],
                'same_chem': data['same_chem'],
                'same_family': data['same_family'],
            }
        out.write_text(json.dumps(export, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'✓ 關係資料輸出到 {out}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    rel = build_relations()
    inject(rel, args.dry_run)


if __name__ == '__main__':
    main()
