"""
optimize_oils_page.py — 重建 oils.html 的「精選精油」區塊
從只有 10 個精油擴展到全部 46 個精油，分 10 類別組織。
"""
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# 46 oils organized by category
# Each: (slug, chinese, latin, emoji, desc, pill1, pill2)
CATEGORIES = [
    ('🍊 柑橘類', '#DCA898', [
        ('oil-sweet-orange', '甜橙', 'Citrus sinensis', '🍊', '溫暖甜蜜的陽光氣息，最親切的情緒精油', '抗焦慮', '兒童友善'),
        ('oil-mandarin', '柑橘（桔）', 'Citrus reticulata', '🍊', '柑橘類中最溫和，兒童夜哭安撫首選', '兒童最佳', '助眠'),
        ('oil-lemon', '檸檬', 'Citrus limon', '🍋', '清新銳利，淨化空間首選，提振注意力', '淨化', '光敏注意'),
        ('oil-grapefruit', '葡萄柚', 'Citrus paradisi', '🍊', '明亮甜美，循環按摩控油保養', '循環', '藥物交互'),
        ('oil-bergamot', '佛手柑', 'Citrus bergamia', '🍋', '香水之王，焦慮舒緩經典精油', '抗焦慮', '光敏注意'),
        ('oil-neroli', '橙花', 'Citrus aurantium', '🌼', '最溫和的花朵精油，孕婦可低劑量', '安神', '孕婦OK'),
        ('oil-petitgrain', '苦橙葉', 'Citrus aurantium', '🌿', '苦橙樹三兄弟中性價比首選', '抗壓', '無光敏'),
    ]),
    ('🌸 花朵類', '#D4878B', [
        ('oil-rose', '玫瑰', 'Rosa damascena', '🌹', '3000 朵花釀一滴的芳療皇后', '抗老', '深度療癒'),
        ('oil-jasmine', '茉莉', 'Jasminum grandiflorum', '🌸', '8000 朵夜花僅產 1ml 的原精', '情緒沉澱', '香水基底'),
        ('oil-ylang-ylang', '依蘭', 'Cananga odorata', '🌸', '濃郁異國花香，舒緩情緒張力', '情緒平衡', '護髮'),
        ('oil-helichrysum', '義大利永久花', 'Helichrysum italicum', '🌼', '化瘀消腫、疤痕修護的義大利皇后', '化瘀', '疤痕修護'),
    ]),
    ('🌼 菊科藍色精油', '#4878A8', [
        ('oil-roman-chamomile', '羅馬洋甘菊', 'Chamaemelum nobile', '🌼', '芳療界最溫柔，嬰幼兒孕婦首選', '兒童', '深度助眠'),
        ('oil-german-chamomile', '德國洋甘菊', 'Matricaria chamomilla', '💙', '深藍色精油，敏感肌抗炎之王', '敏感肌', '抗炎'),
        ('oil-yarrow', '西洋蓍草', 'Achillea millefolium', '💙', '阿基里斯傷藥，藍綠色稀有精油', '皮膚修護', '女性週期'),
    ]),
    ('💜 薰衣草家族', '#BEB0D0', [
        ('oil-lavender', '真正薰衣草', 'Lavandula angustifolia', '💜', '芳療之母，鎮靜助眠修復皮膚', '助眠', '萬用'),
        ('oil-spike-lavender', '穗花薰衣草', 'Lavandula latifolia', '💜', '呼吸保健、肌肉緊繃的薰衣草', '呼吸', '肌肉舒緩'),
        ('oil-lavandin', '醒目薰衣草', 'Lavandula intermedia', '🪻', '商業實用版，居家清潔香氛', '居家', '經濟實惠'),
    ]),
    ('🌿 香草類', '#98C4A0', [
        ('oil-rosemary', '迷迭香', 'Salvia rosmarinus', '🌱', '增強記憶與專注，促進頭皮循環', '記憶力', '循環'),
        ('oil-marjoram', '甜馬鬱蘭', 'Origanum majorana', '🌿', '溫和鎮靜代表，肌肉舒緩自律調節', '鎮靜', '肌肉'),
        ('oil-clary-sage', '快樂鼠尾草', 'Salvia sclarea', '🌸', '女性週期之首，PMS 舒緩經典', 'PMS', '深度助眠'),
        ('oil-sweet-basil', '甜羅勒', 'Ocimum basilicum', '🌿', '神經養護精油，提振注意力的香草', '提神', '消化'),
        ('oil-thyme', '百里香', 'Thymus vulgaris', '🌿', '多化學型強效抗菌（CT 必確認）', '抗菌', '需確認CT'),
        ('oil-melissa', '香蜂草', 'Melissa officinalis', '🌿', '精油界最昂貴，情緒急救之星', '抗焦慮', '稀有'),
        ('oil-geranium', '天竺葵', 'Pelargonium graveolens', '🌸', '平衡精油，女性週期/皮膚/驅蚊', '平衡', '女性'),
        ('oil-palmarosa', '玫瑰草', 'Cymbopogon martinii', '🌾', '禾本科平價玫瑰，保濕抗菌', '保濕', '平價玫瑰'),
    ]),
    ('🌱 薄荷類', '#88BC88', [
        ('oil-peppermint', '胡椒薄荷', 'Mentha piperita', '🌿', '強烈清涼，即時提神緩解頭痛', '提神', '止痛'),
        ('oil-spearmint', '綠薄荷', 'Mentha spicata', '🌿', '兒童友善的溫和薄荷（3歲+）', '兒童', '溫和'),
    ]),
    ('💨 呼吸類', '#78B498', [
        ('oil-eucalyptus', '尤加利', 'Eucalyptus globulus', '🌿', '呼吸道守護者，抗菌祛痰提神', '呼吸道', '抗菌'),
        ('oil-tea-tree', '茶樹', 'Melaleuca alternifolia', '🌲', '抗菌之王，澳洲原住民傳承', '抗菌', '皮膚'),
        ('oil-ravintsara', '桉油醇樟', 'Cinnamomum camphora', '🌿', '馬達加斯加好葉子，秋冬呼吸保健', '呼吸', '免疫'),
        ('oil-lemon-eucalyptus', '檸檬尤加利', 'Corymbia citriodora', '🍋', 'CDC 認證的天然驅蚊精油', '驅蚊', '清新'),
        ('oil-bay', '月桂', 'Laurus nobilis', '🌿', '希臘羅馬桂冠樹，淋巴循環', '淋巴', '消化'),
    ]),
    ('🌲 松柏木質', '#5A7A6A', [
        ('oil-cedarwood', '大西洋雪松', 'Cedrus atlantica', '🌲', '黎巴嫩聖殿木，深沉助眠', '助眠', '頭皮'),
        ('oil-sandalwood', '檀香', 'Santalum album', '🌳', '3000 年東方木質代表，冥想之首', '冥想', '高單價'),
        ('oil-juniper', '杜松漿果', 'Juniperus communis', '🌲', '利尿排毒、淨化能量代表', '淨化', '排毒'),
        ('oil-cypress', '絲柏', 'Cupressus sempervirens', '🌲', '收斂止汗、靜脈循環、人生過渡', '收斂', '靜脈'),
        ('oil-black-spruce', '黑雲杉', 'Picea mariana', '🌲', '加拿大腎上腺疲勞天然提神', '腎上腺', '能量'),
        ('oil-patchouli', '廣藿香', 'Pogostemon cablin', '🌿', '陳年越香，皮膚修護定香之王', '皮膚', '定香'),
        ('oil-vetiver', '岩蘭草', 'Chrysopogon zizanioides', '🌾', '寧靜的精油，冥想接地之王', '深層助眠', '接地'),
    ]),
    ('🔥 辛香類', '#C58040', [
        ('oil-ginger', '薑', 'Zingiber officinale', '🫚', '溫暖循環、消化舒緩、暈車', '暖性', '消化'),
        ('oil-black-pepper', '黑胡椒', 'Piper nigrum', '🌶️', '東方香料之王，肌肉循環經典', '循環', '溫暖'),
        ('oil-clove', '丁香', 'Syzygium aromaticum', '🌶️', '丁香酚之王，傳統牙痛應急', '牙痛', '辛香'),
        ('oil-citronella', '香茅', 'Cymbopogon winterianus', '🌾', '天然驅蚊驅蟲、空間清新代表', '驅蚊', '清新'),
    ]),
    ('🕉️ 樹脂・特殊', '#B09878', [
        ('oil-frankincense', '乳香', 'Boswellia carterii', '🌳', '聖經三禮物，冥想抗老化代表', '冥想', '抗老'),
        ('oil-myrrh', '沒藥', 'Commiphora myrrha', '🌳', '聖油，皮膚修復口腔保健', '皮膚', '口腔'),
        ('oil-sweet-fennel', '甜茴香', 'Foeniculum vulgare', '🌿', '消化系統與女性週期的傘形科', '消化', '女性週期'),
    ]),
]


def build_new_section():
    # Use same wrapper as original: <section class="chem-section" data-chem="featured" id="featured">
    parts = []
    parts.append('<section class="chem-section" data-chem="featured" id="featured">')
    parts.append('    <div class="chem-header">')
    parts.append('      <h2 class="chem-badge" style="background:linear-gradient(135deg,#D4878B,#98ACC8);margin:0;display:inline-flex;color:#fff;">⭐ 全 46 支精油完整指南</h2>')
    parts.append('      <div class="title-line"></div>')
    parts.append('      <span class="chem-count">46 種</span>')
    parts.append('    </div>')
    parts.append('    <p style="font-size:14px;color:var(--text-mid);margin:-4px 0 24px;padding-left:2px;">每支精油皆有 5000+ 字深度頁面（化學成分、用法、安全、DIY、IFA 觀點、中醫對應、研究文獻、心靈能量）。按植物科屬／化學類型分為 10 大族群。</p>')

    total = sum(len(oils) for _, _, oils in CATEGORIES)
    print(f'Total oils being added: {total}')

    for cat_name, color, oils in CATEGORIES:
        parts.append('')
        parts.append(f'    <h3 style="font-size:17px;color:var(--green-dark);margin:24px 0 12px;padding:6px 14px;background:{color}15;border-left:4px solid {color};border-radius:6px;">{cat_name}（{len(oils)} 支）</h3>')
        parts.append('    <div class="oils-full-grid">')
        for slug, zh, latin, emoji, desc, p1, p2 in oils:
            card = (
                f'      <a href="{slug}.html" class="oil-index-card" data-chem="featured" '
                f'data-name="{zh}" data-latin="{latin.lower()}" style="border-top:3px solid {color};">'
                f'<div class="oil-index-emoji">{emoji}</div>'
                f'<div class="oil-index-name">{zh}</div>'
                f'<div class="oil-index-latin">{latin}</div>'
                f'<div class="oil-index-desc">{desc}</div>'
                f'<div class="oil-index-pills">'
                f'<span class="oil-index-pill" style="background:{color}20;color:{color};border:1px solid {color}40;">{p1}</span>'
                f'<span class="oil-index-pill" style="background:{color}20;color:{color};border:1px solid {color}40;">{p2}</span>'
                f'</div></a>'
            )
            parts.append(card)
        parts.append('    </div>')

    parts.append('  </section>')
    return '\n'.join(parts)


def main():
    oils_path = Path(r'C:\Users\User\Desktop\essential-oil-guide\html-source\oils.html')
    content = oils_path.read_text(encoding='utf-8')

    # Find PRECISE bounds: just the featured oils <section> (not the AI summary wrapper)
    # It opens with: <section class="chem-section" data-chem="featured" id="featured">
    # It closes right before: <section class="chem-section" data-chem="cat01"
    open_marker = '<section class="chem-section" data-chem="featured" id="featured">'
    close_marker_after = '<section class="chem-section" data-chem="cat01"'

    section_start = content.find(open_marker)
    if section_start == -1:
        print('ERROR: cannot find featured section opening')
        sys.exit(1)

    cat01_start = content.find(close_marker_after)
    if cat01_start == -1:
        print('ERROR: cannot find cat01 section')
        sys.exit(1)
    # The </section> closing this featured section is right before cat01_start
    section_end = content.rfind('</section>', 0, cat01_start) + len('</section>')

    print(f'Replacing: {section_start} → {section_end} ({section_end - section_start} chars)')
    print(f'Preview start: {content[section_start:section_start+100]}')
    print(f'Preview end:   {content[section_end-100:section_end]}')

    new_section = build_new_section()
    new_content = content[:section_start] + new_section + content[section_end:]
    oils_path.write_text(new_content, encoding='utf-8')

    print()
    print(f'✓ Done')
    print(f'  Old file: {len(content)} chars')
    print(f'  New file: {len(new_content)} chars')
    print(f'  New section: {len(new_section)} chars')

    # Verify all 46 oil links now present
    links = re.findall(r'href="(oil-[a-z\-]+\.html)"', new_content)
    unique = sorted(set(links))
    print(f'  Unique oil-* links in oils.html: {len(unique)}')
    for u in unique:
        print(f'    {u}')


if __name__ == '__main__':
    main()
