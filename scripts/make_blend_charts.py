# -*- coding: utf-8 -*-
"""
make_blend_charts.py — 把整理好的精油配方畫成「乾淨速查表」PNG 圖檔

來源：build_blend_page.py 的 EXTRA_TOPICS（已 OCR+簡轉繁+去品牌+癌症類中性化）
輸出：N:/精油功效表/繁體乾淨版/ 的 PNG（繁體、無他牌、加 intelliverse.tw 浮水印）
工具：Chrome headless 截圖（系統 Chrome，免裝 chromium）
"""
import sys
import subprocess
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_blend_page import EXTRA_TOPICS, OILS_META, SLUG, NOTE_COLOR  # noqa

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = Path(r'N:\精油功效表\繁體乾淨版')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

# 分組（用途名 → 組），依 EXTRA_TOPICS 排列歸類
GROUPS = [
    ('🧴 肌膚與頭皮保養', ['面部精華保養', '美膚防曬', '曬後美白修復', '美膚淡斑', '黑眼圈眼袋',
                          '抗衰緊緻', '肌膚回春', '疤痕修復', '痘痘調理', '生髮頭皮養護']),
    ('🫁 呼吸與換季', ['鼻炎', '清咽止咳', '咳嗽有痰', '久咳氣喘', '感冒配方', '抗病毒防護',
                      '退燒舒緩', '呼吸道日常舒緩']),
    ('🍽️ 消化與代謝循環', ['消化不良', '脾胃養護', '解酒', '養腎排毒', '護肝排毒', '淋巴排毒',
                          '祛濕／體態按摩', '腹部舒緩按摩']),
    ('💪 肌肉關節與循環', ['五星酸痛', '關節疼痛', '腰背舒緩', '肩頸舒緩', '高血壓舒緩',
                          '血管保養', '安神助眠']),
    ('🌸 女性與全身', ['暖宮調經', '子宮保養', '胸部舒緩按摩', '過敏舒緩', '濕疹舒緩',
                      '甲狀腺保養', '暈車舒緩', '滋補陽氣', '戶外防蚊',
                      '兒童日常保養（需稀釋）', '專注學習（需稀釋）']),
]


def drops_for(oils):
    """依前中後調分配合理滴數（總約 8-10 滴）"""
    d = {'top': 3, 'mid': 3, 'base': 2}
    out = []
    for o in oils:
        note = OILS_META.get(o, ('mid', []))[0]
        out.append((o, d.get(note, 2), note))
    return out


def build_html():
    topic_map = {name: oils for _, name, oils in EXTRA_TOPICS}
    sections = []
    for gtitle, names in GROUPS:
        cards = []
        for name in names:
            oils = topic_map.get(name)
            if not oils:
                continue
            rows = ''.join(
                f'<div style="display:flex;justify-content:space-between;font-size:14px;'
                f'padding:2px 0;color:#3D3328;"><span style="border-left:3px solid {NOTE_COLOR[note]};'
                f'padding-left:6px;">{o}</span><span style="color:{NOTE_COLOR[note]};font-weight:700;">{dp} 滴</span></div>'
                for o, dp, note in drops_for(oils))
            cards.append(
                f'<div style="background:#fff;border:1px solid #E5D9C0;border-radius:10px;'
                f'padding:12px 14px;break-inside:avoid;">'
                f'<div style="font-size:16px;font-weight:800;color:#3a5a40;margin-bottom:8px;'
                f'border-bottom:1px solid #EEE7D8;padding-bottom:5px;">{name}</div>{rows}</div>')
        sections.append(
            f'<h2 style="font-size:20px;color:#8B6F3E;margin:26px 0 12px;">{gtitle}</h2>'
            f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;">{"".join(cards)}</div>')

    return f'''<!DOCTYPE html><html lang="zh-TW"><head><meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;800&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;font-family:"Noto Sans TC",sans-serif;}}
body{{background:linear-gradient(135deg,#FBF7F1 0%,#F4EDE4 100%);padding:40px 44px;width:1280px;}}
</style></head><body>
  <div style="display:flex;align-items:center;gap:14px;border-bottom:3px solid #C8A673;padding-bottom:16px;margin-bottom:8px;">
    <span style="font-size:40px;">🌿</span>
    <div>
      <div style="font-size:30px;font-weight:800;color:#3a5a40;">精油配方速查表</div>
      <div style="font-size:15px;color:#8B6F3E;">精油能量圖譜 · intelliverse.tw　｜　前調 · 中調 · 後調 三色標示</div>
    </div>
  </div>
  <div style="display:flex;gap:16px;font-size:13px;color:#7A6852;margin-bottom:6px;">
    <span><b style="color:{NOTE_COLOR['top']};">▌</b>前調(揮發快)</span>
    <span><b style="color:{NOTE_COLOR['mid']};">▌</b>中調(核心)</span>
    <span><b style="color:{NOTE_COLOR['base']};">▌</b>後調(定香)</span>
  </div>
  {''.join(sections)}
  <div style="margin-top:28px;background:#FFF4E6;border-left:4px solid #E8A04B;border-radius:8px;padding:14px 18px;">
    <b style="color:#B5701A;font-size:13px;">⚠️ 重要聲明</b>
    <p style="font-size:12.5px;line-height:1.8;color:#5D4A28;margin-top:4px;">用途名稱僅為分類標籤，<b>不代表精油具醫療或治療效果</b>。精油是輔助身心平衡的芳香生活方式，非藥物，無法治療、診斷或預防疾病。身體不適請就醫，切勿以精油取代正規醫療。孕婦、嬰幼兒、慢性病、服藥中者請先諮詢醫師或專業芳療師。滴數為擴香建議；外用請稀釋（臉部 ≤1%、身體 2-3%）。柑橘類有光敏性，塗後 12 小時避日曬。</p>
  </div>
  <div style="text-align:center;margin-top:16px;font-size:12px;color:#999;">© 2026 精油能量圖譜 · intelliverse.tw　｜　依調香金字塔原理整理</div>
</body></html>'''


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html = build_html()
    htmlf = Path(tempfile.gettempdir()) / 'blend_chart.html'
    htmlf.write_text(html, encoding='utf-8')
    png = OUT_DIR / '精油配方速查表.png'
    print(f'生成 HTML: {htmlf}')
    print(f'截圖中（playwright full_page）...')
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel='chrome')
        pg = b.new_page(viewport={'width': 1280, 'height': 1000}, device_scale_factor=2)
        pg.goto(f'file:///{htmlf.as_posix()}')
        pg.wait_for_timeout(1800)  # 等 Google 字體載入
        pg.screenshot(path=str(png), full_page=True)
        b.close()
    if png.exists():
        kb = png.stat().st_size // 1024
        print(f'✓ 輸出: {png}（{kb} KB，full_page 完整）')
    else:
        print('✗ 截圖失敗')


if __name__ == '__main__':
    main()
