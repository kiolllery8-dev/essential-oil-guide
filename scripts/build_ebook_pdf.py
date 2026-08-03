# -*- coding: utf-8 -*-
"""產生「精油完全指南」電子書 PDF（public/essential-oil-guide-ebook.pdf）。

⚠ 舊版壞掉的原因：只嵌 /Type1 Helvetica（PDF 內建英文字型、零中文字符），
   中文卻以 UTF-16 位元組寫入 → 經 WinAnsi 對照全變亂碼（「精油」→「|¾l¹」）。
   本腳本改用 fpdf2 + 嵌入微軟正黑體（/Type0 CID 字型），中文才會正確渲染與可被複製/搜尋。

資料來源：本站自有的 data/oils.json；文案為本站原創，套用與網站相同的去療效化詞表。
"""
import json, os, re, sys, io
from fpdf import FPDF

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'C:\Users\User\Desktop\essential-oil-guide'
OUT = os.path.join(ROOT, 'public', 'essential-oil-guide-ebook.pdf')
FONT_R = r'C:\Windows\Fonts\msjh.ttc'
FONT_B = r'C:\Windows\Fonts\msjhbd.ttc'

GREEN = (61, 90, 62)
GOLD = (139, 111, 62)
GREY = (90, 90, 90)
BEIGE = (251, 247, 241)
BORDER = (229, 217, 192)

# 與 app/lib/schema.ts 的 sanitizeEffects 同步：機器可讀／對外文件不得帶醫療宣稱
SANITIZE = [
    ('強效化瘀消腫', '舒緩放鬆'), ('化瘀消腫', '舒緩放鬆'), ('活血化瘀', '循環按摩'),
    ('化瘀', '舒緩'), ('活血', '循環暢快'), ('止血收斂', '緊緻收斂'), ('止血', '緊緻'),
    ('溫腎壯陽', '溫暖活力'), ('消炎止痛', '舒緩放鬆'), ('抗菌消炎', '清新淨化'),
    ('呼吸道感染', '呼吸道保養'), ('皮膚感染', '肌膚呵護'), ('促進呼吸道暢通', '帶來呼吸清新感'),
    ('調理經期', '經期前後香氛陪伴'), ('增強免疫', '日常保養'), ('提升免疫', '日常保養'),
    ('免疫刺激', '日常保養'), ('抗病毒', '清新淨化'), ('抗真菌', '清新淨化'),
    ('抗菌', '清新淨化'), ('殺菌', '清新淨化'), ('抗發炎', '舒緩'), ('抗炎', '舒緩'), ('消炎', '舒緩'),
    ('化解黏液', '呼吸清新'), ('化痰', '呼吸清新'), ('祛痰', '呼吸清新'), ('止咳', '呼吸放鬆'),
    ('改善痤瘡', '肌膚保養'), ('抗痘', '肌膚保養'), ('止癢', '肌膚舒緩'),
    ('調經', '經期前後香氛陪伴'), ('通經', '經期前後香氛陪伴'),
    ('止痛', '放鬆'), ('鎮痛', '放鬆'), ('退燒', '清涼舒適'), ('退熱', '清涼舒適'),
    ('抗憂鬱', '情緒放鬆'), ('降血壓', '放鬆'), ('抗風濕', '溫暖舒緩'),
    ('抗腫瘤', '日常保養'), ('抗癌', '日常保養'), ('抗增生', '日常保養'),
    ('壯陽', '活力提升'), ('催情', '浪漫氛圍'), ('利尿', '循環暢快'), ('排毒', '淨化清爽'),
    ('消水腫', '循環按摩'), ('抗痙攣', '安撫放鬆'),
    ('治療', '護理'), ('治癒', '呵護'), ('根治', '呵護'), ('感染', '不適'),
]


def sanitize(s):
    out = str(s or '')
    for bad, good in SANITIZE:
        out = out.replace(bad, good)
    prev = ''
    while prev != out:  # 收合轉換後相鄰的重複詞
        prev = out
        out = re.sub(r'([\u4e00-\u9fff]{2,4})、?\1', r'\1', out)
    return out


def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', str(s or ''))).strip()


# ── 精選 10 支：對應站上新手推薦與流量最高的指南頁 ──
PICKS = ['真正薰衣草', '茶樹', '尤加利', '胡椒薄荷', '甜橙',
         '乳香', '佛手柑', '大馬士革玫瑰', '雪松', '檸檬']
SLUG = {
    '真正薰衣草': 'oil-lavender', '茶樹': 'oil-tea-tree', '尤加利': 'oil-eucalyptus',
    '胡椒薄荷': 'oil-peppermint', '甜橙': 'oil-sweet-orange', '乳香': 'oil-frankincense',
    '佛手柑': 'oil-bergamot', '大馬士革玫瑰': 'oil-rose', '雪松': 'oil-cedarwood', '檸檬': 'oil-lemon',
}


class Book(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('jh', '', 8)
        self.set_text_color(*GREY)
        self.cell(0, 8, '精油完全指南 ｜ 精油能量圖譜 intelliverse.tw', align='R')
        self.ln(10)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font('jh', '', 8)
        self.set_text_color(*GREY)
        self.cell(0, 10, str(self.page_no()), align='C')

    # —— 版面元件 ——
    # 每個元件先把游標拉回左邊界：multi_cell(w=0) 是「延伸到右邊界」，
    # 若上一個 cell 把 x 留在偏右處，寬度會算成極小值而拋
    # 「Not enough horizontal space」。
    def _reset_x(self):
        self.set_x(self.l_margin)

    def h1(self, t):
        self._reset_x()
        self.ln(2)
        self.set_font('jhb', '', 19)
        self.set_text_color(*GREEN)
        self.multi_cell(0, 10, t)
        self.set_draw_color(*BORDER)
        self.set_line_width(0.8)
        y = self.get_y() + 1
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(6)

    def h2(self, t):
        self._reset_x()
        self.ln(3)
        self.set_font('jhb', '', 13)
        self.set_text_color(*GOLD)
        self.multi_cell(0, 8, t)
        self.ln(1)

    def body(self, t, size=10.5):
        self._reset_x()
        self.set_font('jh', '', size)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6.4, t)
        self.ln(1.5)

    def bullet(self, t):
        self._reset_x()
        self.set_font('jh', '', 10.5)
        self.set_text_color(40, 40, 40)
        self.cell(5, 6.2, '・')
        self.set_x(self.l_margin + 5)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 5, 6.2, t)
        self._reset_x()

    def box(self, title, lines, fill=BEIGE):
        self._reset_x()
        self.ln(2)
        self.set_fill_color(*fill)
        self.set_draw_color(*BORDER)
        self.set_font('jhb', '', 10.5)
        self.set_text_color(*GOLD)
        self.multi_cell(0, 7, title, border='LTR', fill=True)
        self.set_font('jh', '', 10)
        self.set_text_color(60, 60, 60)
        for i, ln_ in enumerate(lines):
            last = (i == len(lines) - 1)
            self._reset_x()
            self.multi_cell(0, 6, '  ' + ln_, border=('LBR' if last else 'LR'), fill=True)
        self._reset_x()
        self.ln(3)

    def table(self, headers, rows, widths):
        self._reset_x()
        self.set_font('jhb', '', 9.5)
        self.set_fill_color(243, 238, 230)
        self.set_draw_color(*BORDER)
        self.set_text_color(*GREEN)
        for h, w in zip(headers, widths):
            self.cell(w, 8, h, border=1, align='C', fill=True)
        self.ln()
        self.set_font('jh', '', 9.5)
        self.set_text_color(50, 50, 50)
        for r in rows:
            hgt = 7
            if self.get_y() + hgt > self.h - 20:
                self.add_page()
            for c, w in zip(r, widths):
                self.cell(w, hgt, str(c), border=1, align='C')
            self.ln()
        self.ln(3)


def main():
    oils = json.load(open(os.path.join(ROOT, 'data', 'oils.json'), encoding='utf-8'))
    by_zh = {o.get('zh'): o for o in oils}

    pdf = Book(format='A4')
    pdf.set_auto_page_break(True, margin=18)
    pdf.add_font('jh', '', FONT_R)
    pdf.add_font('jhb', '', FONT_B)
    pdf.set_title('精油完全指南｜精油能量圖譜')
    pdf.set_author('精油能量圖譜 intelliverse.tw')
    pdf.set_subject('精油入門、化學分類、稀釋比例、DIY 配方與安全使用')

    # ── 封面 ──
    pdf.add_page()
    pdf.set_fill_color(*GREEN)
    pdf.rect(0, 0, pdf.w, 78, 'F')
    pdf.set_y(26)
    pdf.set_font('jhb', '', 30)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 14, '精油完全指南', align='C')
    pdf.ln(15)
    pdf.set_font('jh', '', 12)
    pdf.cell(0, 8, 'Essential Oil Complete Guide', align='C')

    pdf.set_y(100)
    pdf.set_font('jhb', '', 14)
    pdf.set_text_color(*GOLD)
    pdf.cell(0, 10, '10 支必備精油 ×  安全用油 ×  DIY 配方', align='C')
    pdf.ln(14)
    pdf.set_font('jh', '', 11)
    pdf.set_text_color(*GREY)
    for line in ['化學分類速查 ・ 稀釋比例對照 ・ 擴香方式比較',
                 '單方精油檔案 ・ 情境配方 ・ 特殊族群安全須知']:
        pdf.cell(0, 7, line, align='C')
        pdf.ln(7)

    pdf.set_y(210)
    pdf.set_font('jh', '', 10)
    pdf.set_text_color(*GREY)
    pdf.cell(0, 6, '精油能量圖譜 ｜ intelliverse.tw', align='C')
    pdf.ln(6)
    pdf.cell(0, 6, '由 IFA 芳療師整理的中文精油知識庫', align='C')
    pdf.ln(14)
    pdf.set_font('jh', '', 8.5)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(0, 5, '本電子書內容僅供生活知識參考，不構成醫療建議，亦不能取代專業診斷或治療。\n'
                         '精油為情緒陪伴、香氛儀式與肌膚保養用途；孕婦、嬰幼兒、慢性病或用藥中'
                         '請先諮詢醫師或合格芳療師。', align='C')

    # ── 目錄 ──
    pdf.add_page()
    pdf.h1('目錄')
    toc = [
        ('01', '精油是什麼？從植物到香氣'),
        ('02', '化學分類速查：8 大分子家族'),
        ('03', '10 支必備精油檔案'),
        ('04', '稀釋比例對照表'),
        ('05', '五種擴香方式比較'),
        ('06', '情境 DIY 配方'),
        ('07', '安全使用：特殊族群與光敏性'),
        ('08', '選購與保存辨識'),
        ('09', '延伸閱讀'),
    ]
    for num, name in toc:
        pdf.set_font('jhb', '', 11)
        pdf.set_text_color(*GOLD)
        pdf.cell(14, 9, num)
        pdf.set_font('jh', '', 11.5)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 9, name)
        pdf.ln(9)

    # ── 01 精油是什麼 ──
    pdf.add_page()
    pdf.h1('01 ｜ 精油是什麼？從植物到香氣')
    pdf.body('精油是植物為了生存而製造的揮發性物質——用來吸引授粉者、驅避啃食的昆蟲、'
             '或在受傷時保護自己。這些成分儲存在植物的腺體、油囊或樹脂道裡，'
             '透過蒸餾、冷壓或溶劑萃取後，才成為我們手上那一小瓶精油。')
    pdf.body('也因為這樣，同一種植物在不同產地、不同採收季節、甚至不同萃取部位，'
             '成分輪廓都會不一樣。這就是為什麼買精油要看拉丁學名，而不是只看中文名字。')
    pdf.h2('三種主要萃取方式')
    pdf.bullet('蒸氣蒸餾：最常見。水蒸氣帶出揮發成分後冷凝分離，副產物就是純露。')
    pdf.bullet('冷壓萃取：柑橘類果皮專用，保留新鮮果香，但也保留了光敏性成分。')
    pdf.bullet('溶劑萃取：花朵類（茉莉、玫瑰原精）用，得到的是「原精」而非精油。')
    pdf.box('為什麼要看拉丁學名？', [
        '「薰衣草」至少有四種：真正薰衣草、穗花薰衣草、醒目薰衣草、頭狀薰衣草，',
        '化學成分與安全注意完全不同。學名才是唯一準確的辨識依據。',
    ])

    # ── 02 化學分類 ──
    pdf.add_page()
    pdf.h1('02 ｜ 化學分類速查：8 大分子家族')
    pdf.body('精油的香氣、揮發速度與安全注意，本質上都由化學分子決定。'
             '認得分子家族，就能推測一支陌生精油大概的個性。')
    pdf.table(
        ['分子家族', '代表精油', '香氣與特性'],
        [
            ['單萜烯', '甜橙、檸檬、乳香', '前調、揮發快、易氧化'],
            ['單萜醇', '薰衣草、茶樹、玫瑰草', '溫和、安全性高、適合老幼'],
            ['倍半萜烯', '雪松、依蘭、德國洋甘菊', '後調、揮發慢、氣味厚實'],
            ['酯類', '薰衣草、快樂鼠尾草', '甜美花果香、放鬆感'],
            ['氧化物', '尤加利、迷迭香、月桂', '清涼通透、6 歲以下留意'],
            ['酮類', '鼠尾草、樟腦、薄荷', '！高劑量有神經毒性'],
            ['醛類', '檸檬草、香茅、山雞椒', '強烈檸檬香、需高度稀釋'],
            ['苯丙烷', '丁香、肉桂、茴香', '！皮膚刺激性高'],
        ],
        [40, 62, 68])
    pdf.body('※ 完整 14 大化學分類與 300+ 支精油分子索引，請見網站的「精油完全索引」。')

    # ── 03 10 支必備精油 ──
    pdf.add_page()
    pdf.h1('03 ｜ 10 支必備精油檔案')
    pdf.body('以下 10 支涵蓋日常八成情境，也是新手最不容易買錯的選擇。'
             '資料取自本站精油資料庫，安全提醒務必看完。')
    for zh in PICKS:
        o = by_zh.get(zh)
        if not o:
            continue
        if pdf.get_y() > pdf.h - 78:
            pdf.add_page()
        def row(text, size=9.5, color=(50, 50, 50), bold=False, h=5.6):
            pdf._reset_x()
            pdf.set_font('jhb' if bold else 'jh', '', size)
            pdf.set_text_color(*color)
            pdf.multi_cell(0, h, text)

        row(f"{zh}　{o.get('latin', '')}", size=12.5, color=GREEN, bold=True, h=8)
        row(f"科屬：{o.get('family', '—')}　｜　萃取：{o.get('extractPart', '—')}"
            f"　｜　化學分類：{o.get('category', '—')}", color=GREY)
        comp = strip_tags(o.get('components'))
        if comp:
            row(f"主要成分：{comp[:70]}")
        eff = sanitize(strip_tags(o.get('effects')))
        if eff:
            row(f"常見應用：{eff[:80]}")
        safe = strip_tags(o.get('safetyText'))
        if safe:
            row(f"安全提醒：{safe[:90]}", color=(150, 90, 20))
        slug = SLUG.get(zh)
        if slug:
            row(f"完整指南：intelliverse.tw/{slug}/", size=9, color=GOLD, h=5.4)
        pdf._reset_x()
        pdf.ln(3.5)

    # ── 04 稀釋 ──
    pdf.add_page()
    pdf.h1('04 ｜ 稀釋比例對照表')
    pdf.body('精油濃度太高是新手最常見的問題。以下比例以 10ml 基底油為基準，'
             '1 滴精油約 0.05ml。')
    pdf.table(['使用情境', '建議濃度', '10ml 基底油滴數'],
              [['臉部保養', '0.5 – 1%', '1 – 2 滴'],
               ['一般身體按摩', '1 – 2%', '2 – 4 滴'],
               ['局部集中（肩頸）', '3%', '6 滴'],
               ['嬰幼兒（2 歲以上）', '0.25 – 0.5%', '0.5 – 1 滴'],
               ['孕期中後期', '1% 以下', '2 滴以內'],
               ['長輩／敏感肌', '0.5 – 1%', '1 – 2 滴']],
              [55, 45, 70])
    pdf.h2('基底油怎麼挑')
    pdf.bullet('荷荷芭油：最接近人體皮脂，穩定不易酸敗，適合臉部與長期保存。')
    pdf.bullet('甜杏仁油：溫和保濕，親膚好推，是全身按摩的入門首選。')
    pdf.bullet('分餾椰子油：質地清爽不油膩，夏天或油性肌膚適合。')
    pdf.box('！精油不溶於水', [
        '直接滴進洗澡水，精油會浮在水面接觸皮膚，濃度極高容易刺激。',
        '正確做法：先用基底油、無香乳液或浴鹽稀釋後再入水。',
    ])

    # ── 05 擴香 ──
    pdf.add_page()
    pdf.h1('05 ｜ 五種擴香方式比較')
    pdf.table(['方式', '原理', '香氣強度', '適合空間'],
              [['擴香瓶（藤枝）', '毛細作用緩釋', '弱', '廁所、玄關'],
               ['擴香石', '孔隙吸附自然揮發', '弱', '車內、衣櫃、床頭'],
               ['超音波水氧機', '震盪霧化水氣', '中', '臥室、書房'],
               ['無水擴香儀', '文氏管噴霧純油', '強', '客廳、商業空間'],
               ['擴香木／擴香瓶蓋', '木材吸附釋放', '弱', '桌面、小空間']],
              [40, 50, 30, 50])
    pdf.h2('用量建議')
    pdf.bullet('水氧機：10 坪空間 3–5 滴，每次 30–60 分鐘、間隔 1 小時。')
    pdf.bullet('避免長時間密閉擴香，容易造成嗅覺疲勞與頭悶。')
    pdf.bullet('家有貓咪、鳥類或嬰幼兒時，務必保持門窗通風並讓寵物能自由離開。')

    # ── 06 DIY ──
    pdf.add_page()
    pdf.h1('06 ｜ 情境 DIY 配方')
    recipes = [
        ('睡前放鬆擴香', ['真正薰衣草 3 滴', '雪松 2 滴', '甜橙 2 滴'],
         '睡前 30 分鐘啟動，營造穩定放鬆的入睡氛圍。'),
        ('晨起提神滾珠', ['胡椒薄荷 2 滴', '檸檬 3 滴', '荷荷芭油 10ml'],
         '塗抹手腕、太陽穴（避開眼周）。柑橘類有光敏性，白天外出請留意。'),
        ('肩頸舒緩按摩油', ['真正薰衣草 4 滴', '甜馬鬱蘭 3 滴', '甜杏仁油 20ml'],
         '約 1.5% 濃度。畫圈輕撫，力道以舒服為準。'),
        ('浴室空間清新噴霧', ['茶樹 8 滴', '檸檬 6 滴', '無水酒精 10ml + 純水 40ml'],
         '搖勻後噴灑於空間；避免直接噴向人與寵物。'),
        ('書桌專注擴香', ['迷迭香 3 滴', '檸檬 3 滴', '尤加利 2 滴'],
         '工作或讀書前 10 分鐘開始擴香。'),
    ]
    for name, items, note in recipes:
        if pdf.get_y() > pdf.h - 62:
            pdf.add_page()
        pdf.h2(name)
        for it in items:
            pdf.bullet(it)
        pdf.set_font('jh', '', 9.5)
        pdf.set_text_color(*GREY)
        pdf.multi_cell(0, 5.6, f'　{note}')
        pdf.ln(2)

    # ── 07 安全 ──
    pdf.add_page()
    pdf.h1('07 ｜ 安全使用：特殊族群與光敏性')
    pdf.h2('特殊族群')
    pdf.table(['族群', '注意事項'],
              [['0–6 個月嬰兒', '完全避免使用'],
               ['6 個月–2 歲', '僅空間擴香，濃度 0.25% 以下'],
               ['2–6 歲', '避免薄荷腦、樟腦、酮類；濃度 0.5–1%'],
               ['孕期前 3 個月', '建議完全避免'],
               ['孕期中後期', '溫和精油 1% 以下，使用前諮詢醫師'],
               ['癲癇病史', '避免酮類、酚類（鼠尾草、迷迭香、樟腦等）'],
               ['蠶豆症', '含樟腦、薄荷腦類需特別謹慎'],
               ['貓咪', '肝臟代謝機制不同，茶樹、薄荷、柑橘類高風險']],
              [45, 125])
    pdf.h2('光敏性精油')
    pdf.body('含呋喃香豆素的精油塗抹後接觸紫外線，可能造成皮膚灼傷或色素沉澱。'
             '常見有：佛手柑、檸檬、葡萄柚、萊姆（冷壓）、圓葉當歸。'
             '塗抹後 12–24 小時請避免日曬。')
    pdf.box('！意外處理', [
        '誤入眼睛：不可用水沖（精油不溶於水），先用植物油沖洗再以清水沖，並就醫。',
        '誤吞：不要催吐，以植物油或全脂牛奶漱口、大量飲水，立即就醫。',
        '皮膚刺激：立即用基底油稀釋擦除，再用肥皂清水洗淨。',
    ])

    # ── 08 選購保存 ──
    pdf.add_page()
    pdf.h1('08 ｜ 選購與保存辨識')
    pdf.h2('看這五項判斷品質')
    for t in ['瓶身標示：拉丁學名、萃取部位、產地、批號缺一不可。',
              'GC/MS 成分報告：主要成分百分比是否符合該精油的標準輪廓。',
              '包裝：深色玻璃瓶（茶色／藍色），塑膠瓶會被精油侵蝕。',
              '價格合理性：玫瑰、茉莉、永久花本來就昂貴，過便宜多為稀釋或合成。',
              '氣味層次：真精油香氣會隨時間變化；香精則從頭到尾一個味道。']:
        pdf.bullet(t)
    pdf.h2('保存期限參考')
    pdf.table(['類型', '建議期限', '保存重點'],
              [['柑橘類', '1 – 2 年', '最易氧化，建議冷藏'],
               ['單萜烯類（松柏）', '2 – 3 年', '易氧化，避免高溫'],
               ['花朵／草本類', '3 – 4 年', '陰涼避光'],
               ['木質／樹脂類', '5 – 6 年', '越陳越香'],
               ['基底油', '6 – 12 個月', '開封後盡快用完']],
              [45, 45, 80])
    pdf.body('氧化的精油（顏色變深、質地變稠、氣味變酸）可能造成嚴重皮膚過敏，請直接丟棄。')

    # ── 09 延伸閱讀 ──
    pdf.add_page()
    pdf.h1('09 ｜ 延伸閱讀')
    pdf.body('這本電子書是入門的濃縮版。網站上有更完整的內容，全部免費：')
    links = [
        ('精油完全索引', 'intelliverse.tw/oils/', '46 支完整指南 + 300+ 支化學分子資料'),
        ('調配精油計算機', 'intelliverse.tw/blend/', '互動式配方工具，自動算稀釋比例'),
        ('精油安全指南', 'intelliverse.tw/safety/', '特殊族群、光敏性、意外處理完整版'),
        ('芳療應用教學', 'intelliverse.tw/aromatherapy/', '擴香、按摩、嗅吸、沐浴四種用法'),
        ('精油大百科', 'intelliverse.tw/encyclopedia/', '化學分子原理與世界產區'),
        ('生命靈數計算機', 'intelliverse.tw/numerology/', '主命數、九宮格與對應精油'),
    ]
    def link_row(text, size, color, bold=False, h=5.4):
        pdf._reset_x()
        pdf.set_font('jhb' if bold else 'jh', '', size)
        pdf.set_text_color(*color)
        pdf.multi_cell(0, h, text)

    for name, url, desc in links:
        link_row(name, 11, GREEN, bold=True, h=7)
        link_row(url, 9.5, GOLD)
        link_row(desc, 9.5, GREY)
        pdf._reset_x()
        pdf.ln(3)

    pdf._reset_x()
    pdf.ln(6)
    pdf.set_font('jh', '', 9)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(0, 5.4,
                   '【免責聲明】本電子書內容為生活知識教育性整理，不構成醫療建議，'
                   '無法治療、診斷或預防任何疾病。精油定位為情緒陪伴、香氛儀式與肌膚保養用途。'
                   '如有健康疑慮、正在服藥、懷孕或哺乳，請先諮詢醫師或合格芳療師。\n\n'
                   '© 精油能量圖譜 intelliverse.tw ｜ 靈境智造 Intelliverse Studio')

    pdf.output(OUT)
    print(f'完成：{OUT}（{pdf.page_no()} 頁、{os.path.getsize(OUT) // 1024} KB）')


if __name__ == '__main__':
    main()
