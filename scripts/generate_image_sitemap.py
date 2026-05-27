"""
generate_image_sitemap.py — 產生 Google Image Sitemap

依 Google 標準: https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps
讓 Google Image Search 可索引所有精油/文章的主圖。

輸出: public/sitemap-images.xml
"""
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

SITE = 'https://intelliverse.tw'
CDN = 'https://cdn.jsdelivr.net/gh/kiolllery8-dev/essential-oil-cdn@main/images'

# 46 oil pages with hero image, alt text
OIL_PAGES = [
    ('oil-sweet-orange', '甜橙', 'Citrus sinensis', '芸香科甜橙樹果皮冷壓萃取'),
    ('oil-mandarin', '柑橘', 'Citrus reticulata', '芸香科柑橘果皮冷壓萃取'),
    ('oil-lemon', '檸檬', 'Citrus limon', '芸香科檸檬果皮冷壓萃取'),
    ('oil-grapefruit', '葡萄柚', 'Citrus paradisi', '芸香科葡萄柚果皮冷壓萃取'),
    ('oil-bergamot', '佛手柑', 'Citrus bergamia', '義大利卡拉布里亞佛手柑果皮冷壓萃取'),
    ('oil-neroli', '橙花', 'Citrus aurantium', '苦橙樹花朵蒸氣蒸餾'),
    ('oil-petitgrain', '苦橙葉', 'Citrus aurantium', '苦橙樹葉片蒸氣蒸餾'),
    ('oil-rose', '玫瑰', 'Rosa damascena', '保加利亞大馬士革玫瑰花瓣蒸餾'),
    ('oil-jasmine', '茉莉', 'Jasminum grandiflorum', '木犀科大花茉莉夜開花溶劑萃取'),
    ('oil-ylang-ylang', '依蘭', 'Cananga odorata', '番荔枝科依蘭樹花朵蒸氣蒸餾'),
    ('oil-helichrysum', '義大利永久花', 'Helichrysum italicum', '科西嘉島菊科永久花蒸餾'),
    ('oil-roman-chamomile', '羅馬洋甘菊', 'Chamaemelum nobile', '菊科羅馬洋甘菊花朵手採蒸餾'),
    ('oil-german-chamomile', '德國洋甘菊', 'Matricaria chamomilla', '菊科德國洋甘菊深藍色精油'),
    ('oil-yarrow', '西洋蓍草', 'Achillea millefolium', '菊科蓍草藍綠色稀有精油'),
    ('oil-lavender', '真正薰衣草', 'Lavandula angustifolia', '法國普羅旺斯真正薰衣草花穗蒸餾'),
    ('oil-spike-lavender', '穗花薰衣草', 'Lavandula latifolia', '西班牙穗花薰衣草呼吸保健精油'),
    ('oil-lavandin', '醒目薰衣草', 'Lavandula intermedia', '法國 Grosso 醒目薰衣草雜交品種'),
    ('oil-rosemary', '迷迭香', 'Salvia rosmarinus', '地中海迷迭香枝葉蒸氣蒸餾'),
    ('oil-marjoram', '甜馬鬱蘭', 'Origanum majorana', '唇形科甜馬鬱蘭葉片蒸餾'),
    ('oil-clary-sage', '快樂鼠尾草', 'Salvia sclarea', '唇形科快樂鼠尾草開花頂端蒸餾'),
    ('oil-sweet-basil', '甜羅勒', 'Ocimum basilicum', '甜羅勒 ct.linalool 沉香醇型蒸餾'),
    ('oil-thyme', '百里香', 'Thymus vulgaris', '地中海百里香多化學型代表'),
    ('oil-melissa', '香蜂草', 'Melissa officinalis', '唇形科香蜂草精油界最珍貴品種'),
    ('oil-geranium', '天竺葵', 'Pelargonium graveolens', '波旁島天竺葵葉片蒸氣蒸餾'),
    ('oil-palmarosa', '玫瑰草', 'Cymbopogon martinii', '禾本科玫瑰草平價玫瑰'),
    ('oil-peppermint', '胡椒薄荷', 'Mentha piperita', '唇形科胡椒薄荷葉片蒸餾'),
    ('oil-spearmint', '綠薄荷', 'Mentha spicata', '兒童友善綠薄荷香芹酮型'),
    ('oil-eucalyptus', '尤加利', 'Eucalyptus globulus', '澳洲藍膠尤加利葉片蒸餾'),
    ('oil-tea-tree', '茶樹', 'Melaleuca alternifolia', '澳洲茶樹 ISO 4730 標準'),
    ('oil-ravintsara', '桉油醇樟', 'Cinnamomum camphora ct cineole', '馬達加斯加桉油醇樟葉片蒸餾'),
    ('oil-lemon-eucalyptus', '檸檬尤加利', 'Corymbia citriodora', 'CDC 認證 OLE 檸檬尤加利驅蚊精油'),
    ('oil-bay', '月桂', 'Laurus nobilis', '希臘羅馬桂冠樹葉片蒸餾'),
    ('oil-cedarwood', '大西洋雪松', 'Cedrus atlantica', '黎巴嫩雪松木質聖殿木'),
    ('oil-sandalwood', '檀香', 'Santalum album', '印度檀香心材蒸氣蒸餾'),
    ('oil-juniper', '杜松漿果', 'Juniperus communis', '柏科杜松漿果琴酒香料來源'),
    ('oil-cypress', '絲柏', 'Cupressus sempervirens', '地中海絲柏針葉嫩枝蒸餾'),
    ('oil-black-spruce', '黑雲杉', 'Picea mariana', '加拿大魁北克黑雲杉腎上腺精油'),
    ('oil-patchouli', '廣藿香', 'Pogostemon cablin', '印尼廣藿香葉片陳年蒸餾'),
    ('oil-vetiver', '岩蘭草', 'Chrysopogon zizanioides', '海地岩蘭草根部深沉精油'),
    ('oil-ginger', '薑', 'Zingiber officinale', '薑科薑根莖蒸氣蒸餾'),
    ('oil-black-pepper', '黑胡椒', 'Piper nigrum', '東方香料之王胡椒果實蒸餾'),
    ('oil-clove', '丁香', 'Syzygium aromaticum', '丁香花苞蒸氣蒸餾丁香酚之王'),
    ('oil-citronella', '香茅', 'Cymbopogon winterianus', '爪哇香茅天然驅蚊精油'),
    ('oil-frankincense', '乳香', 'Boswellia carterii', '阿曼乳香樹脂蒸餾聖經三禮物'),
    ('oil-myrrh', '沒藥', 'Commiphora myrrha', '索馬利亞沒藥樹脂蒸餾'),
    ('oil-sweet-fennel', '甜茴香', 'Foeniculum vulgare', '地中海甜茴香種子蒸餾'),
]

# 19 article pages with hero
ARTICLE_PAGES = [
    ('article-beginners', '芳療新手入門', '精油新手 5 大居家必備'),
    ('article-sleep', '助眠精油', '睡前香氛儀式完整指南'),
    ('article-stress', '紓壓配方', '日間紓壓精油配方'),
    ('article-dustmites', '塵蟎研究', '精油防塵蟎文獻探討'),
    ('article-eucalyptus', '尤加利指南', '5 大尤加利品種比較'),
    ('article-extraction', '萃取方式', '精油萃取方式完整比較'),
    ('article-conifers', '松柏家族', '6 大松柏精油比較'),
    ('article-hydrosols', '純露指南', '純露完整使用指南'),
    ('article-newbie-mistakes', '10 大新手錯誤', '新手最常犯的精油使用錯誤'),
    ('article-citrus-comparison', '柑橘類比較', '7 大柑橘精油完整對比'),
    ('article-chamomile-comparison', '洋甘菊比較', '羅馬 vs 德國洋甘菊對比'),
    ('article-children', '兒童芳療', '0-12 歲兒童精油分齡安全'),
    ('article-pregnancy', '孕期芳療', '孕期精油使用完整指南'),
    ('article-pets', '寵物芳療', '貓狗鳥精油安全清單'),
    ('article-office', '辦公室提神', '上班族 5 支提神精油'),
    ('article-tcm-aromatherapy', '中醫芳療', '12 經絡五行精油對應'),
    ('article-spiritual-aromatherapy', '心靈芳療', '脈輪情緒冥想精油'),
    ('article-insect-repellent', '天然驅蟲', '12 大驅蟲精油 18 配方'),
    ('article-lavender-comparison', '薰衣草比較', '5 種薰衣草完整對比'),
]


def main():
    today = datetime.now().strftime('%Y-%m-%d')
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]

    # Oil pages
    for slug, zh, latin, caption in OIL_PAGES:
        page_url = f'{SITE}/{slug}/'
        img_url = f'{CDN}/{slug}.jpg'
        lines.extend([
            f'  <url>',
            f'    <loc>{page_url}</loc>',
            f'    <lastmod>{today}</lastmod>',
            f'    <image:image>',
            f'      <image:loc>{img_url}</image:loc>',
            f'      <image:title>{zh}精油（{latin}）</image:title>',
            f'      <image:caption>{caption}</image:caption>',
            f'    </image:image>',
            f'  </url>',
        ])

    # Article pages
    for slug, zh, caption in ARTICLE_PAGES:
        page_url = f'{SITE}/{slug}/'
        img_url = f'{CDN}/{slug}.jpg'
        lines.extend([
            f'  <url>',
            f'    <loc>{page_url}</loc>',
            f'    <lastmod>{today}</lastmod>',
            f'    <image:image>',
            f'      <image:loc>{img_url}</image:loc>',
            f'      <image:title>{zh}｜精油能量圖譜</image:title>',
            f'      <image:caption>{caption}</image:caption>',
            f'    </image:image>',
            f'  </url>',
        ])

    # Index pages with hero
    index_pages = [
        ('', 'hero-home', '精油能量圖譜首頁', '精油學從植物到身心靈'),
        ('oils/', 'hero-oils', '精油完全索引', '46 支完整指南 + 302 化學分類 datasheet'),
        ('encyclopedia/', 'hero-encyclopedia', '精油大百科', '化學分子分類完整介紹'),
        ('aromatherapy/', 'hero-aromatherapy', '芳療應用教學', '擴香按摩嗅吸沐浴入門'),
        ('safety/', 'hero-safety', '精油安全使用指南', '7 大常見安全議題'),
    ]
    for path, img_name, title, caption in index_pages:
        page_url = f'{SITE}/{path}'
        img_url = f'{CDN}/{img_name}.png'
        lines.extend([
            f'  <url>',
            f'    <loc>{page_url}</loc>',
            f'    <lastmod>{today}</lastmod>',
            f'    <image:image>',
            f'      <image:loc>{img_url}</image:loc>',
            f'      <image:title>{title}</image:title>',
            f'      <image:caption>{caption}</image:caption>',
            f'    </image:image>',
            f'  </url>',
        ])

    lines.append('</urlset>')

    out_path = Path(r'C:\Users\User\Desktop\essential-oil-guide\public\sitemap-images.xml')
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    total_pages = len(OIL_PAGES) + len(ARTICLE_PAGES) + len(index_pages)
    total_images = total_pages  # 1 image per page (hero)
    print(f'✓ Generated: {out_path}')
    print(f'  {total_pages} pages, {total_images} images')


if __name__ == '__main__':
    main()
