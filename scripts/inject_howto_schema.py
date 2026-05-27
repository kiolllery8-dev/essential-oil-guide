"""
inject_howto_schema.py — 從現有 oil-*.html 的 DIY 區塊提取配方，
注入 HowTo JSON-LD schema（Google Rich Results 大殺器）。

HowTo 是 Google 在搜尋結果中顯示步驟卡片的 schema，
對 DIY 配方類內容效益極高（精油 DIY 是高搜尋量需求）。
"""
import sys
import re
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')


def extract_diy_recipes(content: str) -> list:
    """從 HTML 提取 DIY 配方區塊"""
    recipes = []

    # 模式 1: diy-card 結構 (lavender-style)
    # <div class="diy-card">
    #   <div class="diy-card-header">配方名</div>
    #   <div class="diy-card-body">
    #     <ul class="diy-ingredients">...</ul>
    #     <div class="diy-steps">步驟</div>
    #   </div>
    # </div>
    pattern1 = re.compile(
        r'<div class="diy-card">\s*'
        r'<div class="diy-card-header">([^<]+)</div>\s*'
        r'<div class="diy-card-body">\s*'
        r'<ul[^>]*class="[^"]*diy-ingredients[^"]*"[^>]*>(.*?)</ul>\s*'
        r'<div[^>]*class="[^"]*diy-steps[^"]*"[^>]*>(.*?)</div>',
        re.DOTALL
    )
    for m in pattern1.finditer(content):
        name = m.group(1).strip()
        ingredients_html = m.group(2)
        steps_html = m.group(3)

        # Extract ingredients
        ingredients = []
        for li in re.findall(r'<li[^>]*>(.*?)</li>', ingredients_html, re.DOTALL):
            text = re.sub(r'<[^>]+>', '', li).strip()
            text = re.sub(r'\s+', ' ', text)
            if text:
                ingredients.append(text)

        # Extract steps (single paragraph; split by 。 or 步驟序號)
        steps_text = re.sub(r'<[^>]+>', '', steps_html).strip()
        steps_text = re.sub(r'\s+', ' ', steps_text)

        # Try splitting by sentence
        step_parts = re.split(r'[。；](?!\Z)', steps_text)
        step_parts = [s.strip() for s in step_parts if s.strip()]
        if not step_parts or len(step_parts) == 1:
            step_parts = [steps_text]

        if name and ingredients:
            recipes.append({
                'name': name,
                'ingredients': ingredients,
                'steps': step_parts,
            })

    # 模式 2: 新版頁面 (melissa, mandarin 等 agent-written)
    # <div style="background:#F5F0E6..."> with
    #   <div style="font-weight:700;font-size:16px;color:#8B6F3E...">🍯 配方名</div>
    #   <p style="...">
    #     使用容器 / 油<br>
    #     · <strong>精油1 X 滴</strong>...<br>
    #     · <strong>精油2 X 滴</strong>...<br><br>
    #     使用方式：...
    #   </p>
    # </div>
    pattern2 = re.compile(
        r'<div style="[^"]*background:#F5F0E6[^"]*"[^>]*>\s*'
        r'<div style="font-weight:700[^"]*color:#8B6F3E[^"]*"[^>]*>([^<]+)</div>\s*'
        r'<p style="[^"]*"[^>]*>(.*?)</p>',
        re.DOTALL
    )
    for m in pattern2.finditer(content):
        name = re.sub(r'[🍯🌸🕯️🩹🛁💆😴✨🌿🌹🌺🪷💜🌳🌲🌾🍊🍋🌱]\s*', '', m.group(1)).strip()
        body = m.group(2)

        # Body has format: "base info<br>· <strong>...</strong>...<br>· <strong>...</strong>...<br><br>使用方式：..."
        # Split by <br> tags
        body_clean = re.sub(r'<br\s*/?>', '\n', body)
        body_lines = [l.strip() for l in body_clean.split('\n') if l.strip()]

        ingredients = []
        steps = []
        in_steps = False
        for line in body_lines:
            line_clean = re.sub(r'<[^>]+>', '', line).strip()
            if not line_clean:
                continue
            if line_clean.startswith('使用方式') or line_clean.startswith('使用') or '：' in line_clean[:5]:
                in_steps = True
                if '：' in line_clean:
                    line_clean = line_clean.split('：', 1)[1].strip()
            if in_steps:
                if line_clean:
                    steps.append(line_clean)
            elif line_clean.startswith('·') or line_clean.startswith('•'):
                ingredients.append(line_clean.lstrip('·• ').strip())
            else:
                # Container/base oil line
                ingredients.append(line_clean)

        if not steps:
            steps = ['依配方比例混合，使用前搖勻']

        if name and ingredients:
            # Dedupe and avoid duplicating recipes already captured
            already = any(r['name'] == name for r in recipes)
            if not already:
                recipes.append({
                    'name': name,
                    'ingredients': ingredients,
                    'steps': steps,
                })

    return recipes


def build_howto_schema(slug: str, oil_zh: str, recipes: list) -> str:
    """產生 HowTo JSON-LD（陣列形式，多配方）"""
    page_url = f'https://intelliverse.tw/{slug}/'
    items = []
    for i, r in enumerate(recipes, 1):
        howto = {
            '@type': 'HowTo',
            '@id': f'{page_url}#howto-{i}',
            'name': f'{oil_zh}精油 DIY：{r["name"]}',
            'description': f'使用{oil_zh}精油的居家 DIY 配方，IFA 芳療師推薦。',
            'totalTime': 'PT10M',  # 一般 5-10 分鐘
            'estimatedCost': {
                '@type': 'MonetaryAmount',
                'currency': 'TWD',
                'value': '100-500',
            },
            'tool': [
                {'@type': 'HowToTool', 'name': '滴管或玻璃瓶'},
                {'@type': 'HowToTool', 'name': '量杯'},
            ],
            'supply': [
                {'@type': 'HowToSupply', 'name': name}
                for name in r['ingredients']
            ],
            'step': [
                {
                    '@type': 'HowToStep',
                    'position': j,
                    'name': f'步驟 {j}',
                    'text': step,
                }
                for j, step in enumerate(r['steps'], 1)
            ],
        }
        items.append(howto)

    # Wrap in @graph if multiple recipes
    if len(items) == 1:
        wrapper = {'@context': 'https://schema.org', **items[0]}
    else:
        wrapper = {
            '@context': 'https://schema.org',
            '@graph': items,
        }
    return json.dumps(wrapper, ensure_ascii=False, indent=2)


# Oil zh name lookup
OIL_ZH = {
    'oil-sweet-orange': '甜橙', 'oil-mandarin': '柑橘', 'oil-lemon': '檸檬',
    'oil-grapefruit': '葡萄柚', 'oil-bergamot': '佛手柑', 'oil-neroli': '橙花',
    'oil-petitgrain': '苦橙葉', 'oil-rose': '玫瑰', 'oil-jasmine': '茉莉',
    'oil-ylang-ylang': '依蘭', 'oil-helichrysum': '義大利永久花',
    'oil-roman-chamomile': '羅馬洋甘菊', 'oil-german-chamomile': '德國洋甘菊',
    'oil-yarrow': '西洋蓍草', 'oil-lavender': '真正薰衣草',
    'oil-spike-lavender': '穗花薰衣草', 'oil-lavandin': '醒目薰衣草',
    'oil-rosemary': '迷迭香', 'oil-marjoram': '甜馬鬱蘭',
    'oil-clary-sage': '快樂鼠尾草', 'oil-sweet-basil': '甜羅勒',
    'oil-thyme': '百里香', 'oil-melissa': '香蜂草', 'oil-geranium': '天竺葵',
    'oil-palmarosa': '玫瑰草', 'oil-peppermint': '胡椒薄荷',
    'oil-spearmint': '綠薄荷', 'oil-eucalyptus': '尤加利',
    'oil-tea-tree': '茶樹', 'oil-ravintsara': '桉油醇樟',
    'oil-lemon-eucalyptus': '檸檬尤加利', 'oil-bay': '月桂',
    'oil-cedarwood': '大西洋雪松', 'oil-sandalwood': '檀香',
    'oil-juniper': '杜松漿果', 'oil-cypress': '絲柏',
    'oil-black-spruce': '黑雲杉', 'oil-patchouli': '廣藿香',
    'oil-vetiver': '岩蘭草', 'oil-ginger': '薑', 'oil-black-pepper': '黑胡椒',
    'oil-clove': '丁香', 'oil-citronella': '香茅', 'oil-frankincense': '乳香',
    'oil-myrrh': '沒藥', 'oil-sweet-fennel': '甜茴香',
}


def process_file(path: Path):
    slug = path.stem
    if slug not in OIL_ZH:
        return False, 0

    content = path.read_text(encoding='utf-8')
    oil_zh = OIL_ZH[slug]

    recipes = extract_diy_recipes(content)
    if not recipes:
        return False, 0

    howto_jsonld = build_howto_schema(slug, oil_zh, recipes)
    script_block = (
        '\n  <!-- ===== HowTo JSON-LD (DIY 配方 Rich Results) ===== -->\n'
        f'  <script type="application/ld+json">\n{howto_jsonld}\n  </script>\n'
    )

    # Replace existing HowTo or insert before </head>
    existing_pattern = re.compile(
        r'\s*<!-- ===== HowTo JSON-LD.*?===== -->\s*<script type="application/ld\+json">.*?</script>\s*',
        re.DOTALL
    )
    if existing_pattern.search(content):
        content = existing_pattern.sub(script_block, content)
    elif '</head>' in content:
        content = content.replace('</head>', script_block + '</head>', 1)
    else:
        return False, 0

    path.write_text(content, encoding='utf-8')
    return True, len(recipes)


def main():
    html_dir = Path(r'C:\Users\User\Desktop\essential-oil-guide\html-source')
    success = 0
    total_recipes = 0
    no_recipes = []
    for path in sorted(html_dir.glob('oil-*.html')):
        ok, count = process_file(path)
        if ok:
            success += 1
            total_recipes += count
            print(f'  ✓ {path.stem}: {count} 個配方')
        else:
            no_recipes.append(path.stem)
            print(f'  ⊘ {path.stem}: 未找到 DIY 區塊')

    print()
    print(f'=== Done ===')
    print(f'  ✓ 注入 HowTo: {success} 頁')
    print(f'  📋 總配方數:  {total_recipes}')
    print(f'  ⊘ 無配方頁:   {len(no_recipes)}')
    if no_recipes:
        print(f'     {", ".join(no_recipes)}')


if __name__ == '__main__':
    main()
