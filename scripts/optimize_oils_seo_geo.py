"""
optimize_oils_seo_geo.py — 強化 /oils/ 頁面的 SEO/GEO 訊號

加上：
1. ItemList JSON-LD（46 支精油頁面）— AI search 最重要
2. Organization + Person JSON-LD（EEAT 作者權威）
3. WebPage JSON-LD with dateModified
4. 視覺化作者署名 + 更新日期（visible EEAT）
5. 用途快速查找表（GEO 友善 — LLM 愛表格）
6. DefinedTerm 化學分類定義
"""
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

OIL_PAGES = [
    ('oil-sweet-orange', '甜橙', 'Citrus sinensis', '柑橘類'),
    ('oil-mandarin', '柑橘', 'Citrus reticulata', '柑橘類'),
    ('oil-lemon', '檸檬', 'Citrus limon', '柑橘類'),
    ('oil-grapefruit', '葡萄柚', 'Citrus paradisi', '柑橘類'),
    ('oil-bergamot', '佛手柑', 'Citrus bergamia', '柑橘類'),
    ('oil-neroli', '橙花', 'Citrus aurantium flos', '柑橘類'),
    ('oil-petitgrain', '苦橙葉', 'Citrus aurantium fol', '柑橘類'),
    ('oil-rose', '玫瑰', 'Rosa damascena', '花朵類'),
    ('oil-jasmine', '茉莉', 'Jasminum grandiflorum', '花朵類'),
    ('oil-ylang-ylang', '依蘭', 'Cananga odorata', '花朵類'),
    ('oil-helichrysum', '義大利永久花', 'Helichrysum italicum', '花朵類'),
    ('oil-roman-chamomile', '羅馬洋甘菊', 'Chamaemelum nobile', '菊科'),
    ('oil-german-chamomile', '德國洋甘菊', 'Matricaria chamomilla', '菊科'),
    ('oil-yarrow', '西洋蓍草', 'Achillea millefolium', '菊科'),
    ('oil-lavender', '真正薰衣草', 'Lavandula angustifolia', '薰衣草'),
    ('oil-spike-lavender', '穗花薰衣草', 'Lavandula latifolia', '薰衣草'),
    ('oil-lavandin', '醒目薰衣草', 'Lavandula intermedia', '薰衣草'),
    ('oil-rosemary', '迷迭香', 'Salvia rosmarinus', '香草'),
    ('oil-marjoram', '甜馬鬱蘭', 'Origanum majorana', '香草'),
    ('oil-clary-sage', '快樂鼠尾草', 'Salvia sclarea', '香草'),
    ('oil-sweet-basil', '甜羅勒', 'Ocimum basilicum', '香草'),
    ('oil-thyme', '百里香', 'Thymus vulgaris', '香草'),
    ('oil-melissa', '香蜂草', 'Melissa officinalis', '香草'),
    ('oil-geranium', '天竺葵', 'Pelargonium graveolens', '香草'),
    ('oil-palmarosa', '玫瑰草', 'Cymbopogon martinii', '香草'),
    ('oil-peppermint', '胡椒薄荷', 'Mentha piperita', '薄荷'),
    ('oil-spearmint', '綠薄荷', 'Mentha spicata', '薄荷'),
    ('oil-eucalyptus', '尤加利', 'Eucalyptus globulus', '呼吸類'),
    ('oil-tea-tree', '茶樹', 'Melaleuca alternifolia', '呼吸類'),
    ('oil-ravintsara', '桉油醇樟', 'Cinnamomum camphora ct cineole', '呼吸類'),
    ('oil-lemon-eucalyptus', '檸檬尤加利', 'Corymbia citriodora', '呼吸類'),
    ('oil-bay', '月桂', 'Laurus nobilis', '呼吸類'),
    ('oil-cedarwood', '大西洋雪松', 'Cedrus atlantica', '木質'),
    ('oil-sandalwood', '檀香', 'Santalum album', '木質'),
    ('oil-juniper', '杜松漿果', 'Juniperus communis', '木質'),
    ('oil-cypress', '絲柏', 'Cupressus sempervirens', '木質'),
    ('oil-black-spruce', '黑雲杉', 'Picea mariana', '木質'),
    ('oil-patchouli', '廣藿香', 'Pogostemon cablin', '木質'),
    ('oil-vetiver', '岩蘭草', 'Chrysopogon zizanioides', '木質'),
    ('oil-ginger', '薑', 'Zingiber officinale', '辛香'),
    ('oil-black-pepper', '黑胡椒', 'Piper nigrum', '辛香'),
    ('oil-clove', '丁香', 'Syzygium aromaticum', '辛香'),
    ('oil-citronella', '香茅', 'Cymbopogon winterianus', '辛香'),
    ('oil-frankincense', '乳香', 'Boswellia carterii', '樹脂'),
    ('oil-myrrh', '沒藥', 'Commiphora myrrha', '樹脂'),
    ('oil-sweet-fennel', '甜茴香', 'Foeniculum vulgare', '其他'),
]


def build_itemlist_jsonld():
    """46 支精油 ItemList JSON-LD — GEO/AI 引擎最愛這個"""
    items = []
    for i, (slug, zh, latin, cat) in enumerate(OIL_PAGES, 1):
        items.append({
            '@type': 'ListItem',
            'position': i,
            'name': f'{zh}精油',
            'url': f'https://intelliverse.tw/{slug}/',
            'item': {
                '@type': 'Thing',
                'name': f'{zh}（{latin}）',
                'description': f'{cat}精油，IFA 標準完整指南',
                'url': f'https://intelliverse.tw/{slug}/',
            }
        })
    import json
    schema = {
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        '@id': 'https://intelliverse.tw/oils/#oil-pages',
        'name': '46 支精油完整指南清單',
        'description': '靈境智造精油能量圖譜整理的 46 支主流精油深度指南，每篇 5000+ 字 IFA 芳療標準',
        'numberOfItems': len(OIL_PAGES),
        'itemListOrder': 'https://schema.org/ItemListOrderDescending',
        'itemListElement': items,
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def build_organization_jsonld():
    """Organization + Person schema — EEAT 權威性"""
    import json
    schema = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'Organization',
                '@id': 'https://intelliverse.tw/#organization',
                'name': '靈境智造 Intelliverse Studio',
                'alternateName': '精油能量圖譜',
                'url': 'https://intelliverse.tw/',
                'logo': 'https://cdn.jsdelivr.net/gh/kiolllery8-dev/essential-oil-cdn@main/images/logo.png',
                'sameAs': [
                    'https://github.com/kiolllery8-dev/essential-oil-guide',
                ],
                'description': '結合 30 年 IFA 芳療專業、化妝品電商實務、設計思維的精油知識平台',
                'address': {
                    '@type': 'PostalAddress',
                    'addressLocality': '臺中',
                    'addressRegion': '臺中市',
                    'addressCountry': 'TW',
                },
            },
            {
                '@type': 'Person',
                '@id': 'https://intelliverse.tw/#author',
                'name': '玉玲（Intelliverse Studio 主理人）',
                'description': '30 年 IFA 國際芳療師認證、英國 IFPA 進階課程、化妝品電商實務經驗。專精於精油化學分類、IFA 芳療標準、中醫五行與精油的跨領域整合。',
                'jobTitle': 'IFA 國際認證芳療師 / Intelliverse Studio 主理人',
                'worksFor': {'@id': 'https://intelliverse.tw/#organization'},
                'knowsAbout': [
                    'IFA 國際芳療標準',
                    '精油化學分類',
                    '中醫芳療',
                    '芳療安全使用',
                    'GC/MS 精油鑑別',
                ],
                'hasCredential': [
                    {
                        '@type': 'EducationalOccupationalCredential',
                        'credentialCategory': '專業認證',
                        'name': 'IFA 國際芳療師認證',
                        'recognizedBy': {
                            '@type': 'Organization',
                            'name': 'International Federation of Aromatherapists',
                        },
                    },
                ],
            },
            {
                '@type': 'WebPage',
                '@id': 'https://intelliverse.tw/oils/#webpage',
                'url': 'https://intelliverse.tw/oils/',
                'name': '精油完全索引｜46 支完整指南 + 14 大化學分類',
                'isPartOf': {'@id': 'https://intelliverse.tw/#website'},
                'about': {'@id': 'https://intelliverse.tw/#organization'},
                'author': {'@id': 'https://intelliverse.tw/#author'},
                'reviewedBy': {'@id': 'https://intelliverse.tw/#author'},
                'datePublished': '2025-08-01',
                'dateModified': '2026-05-22',
                'inLanguage': 'zh-TW',
                'primaryImageOfPage': {
                    '@type': 'ImageObject',
                    'url': 'https://cdn.jsdelivr.net/gh/kiolllery8-dev/essential-oil-cdn@main/images/hero-oils.png',
                },
            },
            {
                '@type': 'WebSite',
                '@id': 'https://intelliverse.tw/#website',
                'url': 'https://intelliverse.tw/',
                'name': '精油能量圖譜',
                'description': '台灣最完整的 IFA 標準精油知識平台',
                'publisher': {'@id': 'https://intelliverse.tw/#organization'},
                'inLanguage': 'zh-TW',
            },
        ]
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def build_definedterm_jsonld():
    """DefinedTermSet for 14 chemistry classes — AI 引擎理解化學分類定義"""
    import json
    terms = [
        ('單萜烯類', 'Monoterpenes', '由 10 個碳原子組成的揮發性化合物，代表分子如 α-蒎烯、檸檬烯，常見於柑橘類和松柏類精油，香氣明亮輕快，揮發快，氧化後可能刺激皮膚。'),
        ('單萜醇類', 'Monoterpenols', '含羥基的單萜化合物，代表分子沉香醇、牻牛兒醇，化學上最溫和，是薰衣草、玫瑰、天竺葵的主成分，適合敏感族群和兒童。'),
        ('倍半萜醇類', 'Sesquiterpenols', '由 15 個碳原子組成的醇類化合物，代表分子檀香醇、岩蘭草醇、廣藿香醇，深沉木質香，揮發極慢，是優秀的香水定香劑。'),
        ('倍半萜烯類', 'Sesquiterpenes', '由 15 個碳原子組成的不飽和烴類，代表分子 β-石竹烯、母菊天藍烴，常見於依蘭、薑、洋甘菊，具溫和抗炎特性。'),
        ('單萜酮類', 'Monoterpenones', '含羰基的單萜化合物，代表分子薄荷酮、樟腦，有強烈神經系統作用，孕婦嬰幼兒癲癇患者須避用，但少量有助於黏液溶解和提神。'),
        ('倍半萜酮類', 'Sesquiterpenones', '由 15 碳組成的酮類，代表分子義大利雙酮，含於永久花精油，神經毒性極低卻有強大化瘀消腫效果。'),
        ('氧化物類', 'Oxides', '含氧雜環結構的化合物，代表分子 1,8-桉葉素（cineole），常見於尤加利、桉油醇樟、迷迭香，呼吸系統保健代表。'),
        ('醛類', 'Aldehydes', '含醛基的化合物，代表分子檸檬醛（橙花醛+香葉醛），常見於香蜂草、檸檬香茅、山雞椒，香氣強烈帶柑橘感，可能刺激皮膚需稀釋。'),
        ('酯類', 'Esters', '酸與醇結合的化合物，代表分子乙酸沉香酯，常見於佛手柑、快樂鼠尾草、羅馬洋甘菊，是芳療界最溫和鎮靜的化學族群。'),
        ('苯基酯類', 'Benzyl Esters', '苯環架構的酯類，代表分子乙酸苄酯，主要見於茉莉、依蘭原精，香氣甜美持久，是高級香水基底。'),
        ('芳香醛與芳香酯', 'Aromatic Aldehydes/Esters', '帶苯環的醛類和酯類，代表分子肉桂醛、水楊酸甲酯，常見於肉桂、秘魯香脂，刺激性較強需嚴格稀釋（≤0.5%）。'),
        ('酚類', 'Phenols', '帶羥基苯環的化合物，代表分子丁香酚、百里酚，常見於丁香、百里香 ct.thymol，抗菌效力最強但黏膜刺激性也最強（≤1%）。'),
        ('香豆素與內酯類', 'Coumarins/Lactones', '苯並吡喃結構化合物，代表分子佛手柑素（bergaptene），常見於柑橘果皮，會引起 12 小時光敏反應需避日曬。'),
        ('脂類', 'Fatty Acids/Lipids', '雖然精油主要為小分子，但部分如苦橙葉、頭狀薰衣草含微量脂類成分，影響香氣的圓潤度。'),
    ]
    schema = {
        '@context': 'https://schema.org',
        '@type': 'DefinedTermSet',
        '@id': 'https://intelliverse.tw/oils/#chemistry-glossary',
        'name': '14 大精油化學分類定義',
        'description': '芳療學界（IFA/IFPA/NAHA）通用的精油化學分子分類',
        'hasDefinedTerm': [
            {
                '@type': 'DefinedTerm',
                'name': zh,
                'alternateName': en,
                'description': desc,
                'inDefinedTermSet': 'https://intelliverse.tw/oils/#chemistry-glossary',
            }
            for zh, en, desc in terms
        ]
    }
    import json
    return json.dumps(schema, ensure_ascii=False, indent=2)


def build_author_section_html():
    """視覺化作者署名 + 編輯資訊（EEAT）"""
    return '''
<!-- ===== EEAT 作者署名 + 編輯資訊 ===== -->
<section style="max-width:1100px;margin:24px auto;padding:0 20px;">
  <div style="background:linear-gradient(135deg,#FBF7F1 0%,#F4EDE4 100%);border-left:4px solid #8B6F3E;padding:20px 24px;border-radius:12px;display:grid;grid-template-columns:auto 1fr;gap:20px;align-items:center;">
    <div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#C8A673,#8B6F3E);display:flex;align-items:center;justify-content:center;font-size:32px;flex-shrink:0;">
      🌿
    </div>
    <div>
      <h2 style="font-size:16px;font-weight:700;color:#8B6F3E;margin:0 0 6px;">關於這份精油完全索引</h2>
      <p style="font-size:14px;line-height:1.85;color:#5D5040;margin:0 0 8px;">
        由 <strong>玉玲（Intelliverse Studio 主理人）</strong>整理，依據 30 年 <strong>IFA 國際芳療師</strong>專業背景與英國 IFPA 進階課程框架。所有精油資料皆參照 IFA 官方教材、Tisserand &amp; Young《Essential Oil Safety》、Pierre Franchomme &amp; Daniel Pénoël《L&apos;aromathérapie exactement》三大芳療學派。
      </p>
      <div style="font-size:13px;color:var(--text-mid);display:flex;gap:16px;flex-wrap:wrap;">
        <span>📅 首次發布：2025-08-01</span>
        <span>🔄 最近更新：<time datetime="2026-05-22">2026-05-22</time></span>
        <span>✅ 46 支完整指南 + 302 化學 datasheet</span>
        <span>📚 5 本 IFA 教材內化</span>
      </div>
    </div>
  </div>
</section>'''


def build_usecase_table_html():
    """用途快速查找表 — GEO 友善（LLM 愛這種精準對應表）"""
    use_cases = [
        ('😴 失眠/助眠', ['oil-lavender', 'oil-roman-chamomile', 'oil-vetiver', 'oil-cedarwood', 'oil-marjoram']),
        ('😰 焦慮/壓力', ['oil-bergamot', 'oil-melissa', 'oil-neroli', 'oil-frankincense', 'oil-lavender']),
        ('🌸 PMS/女性週期', ['oil-clary-sage', 'oil-geranium', 'oil-rose', 'oil-sweet-fennel', 'oil-palmarosa']),
        ('💆 肌肉緊繃', ['oil-marjoram', 'oil-black-pepper', 'oil-ginger', 'oil-spike-lavender', 'oil-rosemary']),
        ('🫁 呼吸保健', ['oil-eucalyptus', 'oil-ravintsara', 'oil-tea-tree', 'oil-spike-lavender', 'oil-bay']),
        ('🌿 敏感肌膚', ['oil-german-chamomile', 'oil-roman-chamomile', 'oil-helichrysum', 'oil-rose', 'oil-yarrow']),
        ('🦟 天然驅蚊', ['oil-lemon-eucalyptus', 'oil-citronella', 'oil-geranium', 'oil-lavender', 'oil-spike-lavender']),
        ('🧠 提神專注', ['oil-rosemary', 'oil-peppermint', 'oil-sweet-basil', 'oil-lemon', 'oil-black-spruce']),
        ('🍽️ 消化舒緩', ['oil-ginger', 'oil-sweet-fennel', 'oil-peppermint', 'oil-spearmint', 'oil-sweet-basil']),
        ('🧘 冥想沉澱', ['oil-frankincense', 'oil-myrrh', 'oil-sandalwood', 'oil-patchouli', 'oil-vetiver']),
        ('👶 兒童友善（2 歲以上）', ['oil-lavender', 'oil-roman-chamomile', 'oil-mandarin', 'oil-spearmint', 'oil-sweet-orange']),
        ('🤰 孕婦中後期低劑量', ['oil-lavender', 'oil-roman-chamomile', 'oil-neroli', 'oil-mandarin', 'oil-petitgrain']),
    ]

    slug_to_name = {p[0]: p[1] for p in OIL_PAGES}

    rows = []
    for use, slugs in use_cases:
        oils_html = ' · '.join(
            f'<a href="{s}.html" style="color:#8B6F3E;text-decoration:none;font-weight:600;">{slug_to_name.get(s, s)}</a>'
            for s in slugs
        )
        rows.append(f'''        <tr>
          <td style="padding:12px 14px;border:1px solid #E5D9C0;font-weight:600;color:#5D5040;background:#FBF7F1;white-space:nowrap;">{use}</td>
          <td style="padding:12px 14px;border:1px solid #E5D9C0;line-height:2;">{oils_html}</td>
        </tr>''')

    return f'''
<!-- ===== 用途快速查找表（GEO 友善：LLM 易讀對應表）===== -->
<section style="max-width:1100px;margin:32px auto;padding:0 20px;">
  <div class="chem-header">
    <h2 class="chem-badge" style="background:#5A7A6A;margin:0;display:inline-flex;color:#fff;">🎯 12 大常見情境精油對照表</h2>
    <div class="title-line"></div>
    <span class="chem-count">5 支/情境</span>
  </div>
  <p style="font-size:14px;color:var(--text-mid);margin:-4px 0 18px;padding-left:2px;">
    一眼找到對應你需求的精油。每個情境列出芳療師最常推薦的 5 支精油，點擊直達 5000+ 字完整指南。
  </p>
  <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;font-size:14px;background:#fff;border-radius:10px;overflow:hidden;">
      <thead>
        <tr style="background:#5A7A6A;color:#fff;">
          <th style="padding:14px;text-align:left;font-weight:700;width:180px;">情境/需求</th>
          <th style="padding:14px;text-align:left;font-weight:700;">推薦精油（點擊查看完整指南）</th>
        </tr>
      </thead>
      <tbody>
{chr(10).join(rows)}
      </tbody>
    </table>
  </div>
  <p style="font-size:12px;color:var(--text-light);margin:12px 0 0;font-style:italic;">
    ⚠ 上表為一般建議，特殊狀況（疾病、用藥、孕期、慢性病）請諮詢專業芳療師或醫師。
  </p>
</section>'''


def main():
    oils_path = Path(r'C:\Users\User\Desktop\essential-oil-guide\html-source\oils.html')
    content = oils_path.read_text(encoding='utf-8')

    # 1. Build new JSON-LD scripts (3 new schemas to add)
    new_schemas = [
        ('ItemList-46-oils', build_itemlist_jsonld()),
        ('Organization-Person-EEAT', build_organization_jsonld()),
        ('DefinedTermSet-chemistry', build_definedterm_jsonld()),
    ]

    new_scripts = '\n\n'.join(
        f'<!-- {name} -->\n<script type="application/ld+json">\n{schema}\n</script>'
        for name, schema in new_schemas
    )

    # Insert before existing JSON-LD script
    existing_script_start = content.find('<script type="application/ld+json">')
    if existing_script_start == -1:
        print('ERROR: cannot find existing JSON-LD script')
        sys.exit(1)

    content = content[:existing_script_start] + new_scripts + '\n\n' + content[existing_script_start:]
    print(f'✓ Added 3 new JSON-LD schemas before existing one')

    # 2. Add EEAT author section after breadcrumb
    author_section = build_author_section_html()
    breadcrumb_end_marker = '</div></div>\n\n<!-- ===== AI 友善'
    if breadcrumb_end_marker in content:
        content = content.replace(breadcrumb_end_marker, '</div></div>' + author_section + '\n\n<!-- ===== AI 友善')
        print(f'✓ Added EEAT author section after breadcrumb')
    else:
        # Fallback: insert after breadcrumb closing
        bc_idx = content.find('<div class="breadcrumb">')
        if bc_idx > 0:
            bc_end = content.find('</div></div>', bc_idx) + len('</div></div>')
            content = content[:bc_end] + author_section + content[bc_end:]
            print(f'✓ Added EEAT author section after breadcrumb (fallback)')

    # 3. Add use-case lookup table before FAQ section
    usecase_section = build_usecase_table_html()
    faq_marker = '<!-- ===== 常見問題 FAQ'
    if faq_marker in content:
        content = content.replace(faq_marker, usecase_section + '\n\n' + faq_marker)
        print(f'✓ Added use-case lookup table before FAQ')
    else:
        # Try alternative FAQ marker
        faq_idx = content.find('常見問題 FAQ')
        if faq_idx > 0:
            # Find the section opening before this
            sec_open = content.rfind('<section', 0, faq_idx)
            content = content[:sec_open] + usecase_section + '\n\n' + content[sec_open:]
            print(f'✓ Added use-case lookup table before FAQ (fallback)')

    oils_path.write_text(content, encoding='utf-8')

    # Verify
    print()
    print('=== Verification ===')
    print(f'  ItemList-46-oils:        {"ItemList-46-oils" in content}')
    print(f'  Organization-EEAT:       {"Organization-Person-EEAT" in content}')
    print(f'  DefinedTermSet:          {"DefinedTermSet" in content}')
    print(f'  EEAT author section:     {"關於這份精油完全索引" in content}')
    print(f'  Use-case table:          {"12 大常見情境精油對照表" in content}')
    print(f'  Total JSON-LD scripts:   {content.count(chr(34) + "application/ld+json" + chr(34))}')
    print(f'  Total file size:         {len(content)} chars')


if __name__ == '__main__':
    main()
