# -*- coding: utf-8 -*-
"""
build_blend_page.py — 產生「調配精油」互動頁 html-source/blend.html

依使用者的感覺/環境，用調香金字塔（前中後調）原理產出精油配方。
資料來自本站 302 精油 + 知識圖譜情境對應 + IFA 調香原理。
參考 aromaschool.com.tw 的「配方計算器」概念（自建，非複製其 login-gated 內容）。
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

OUT = Path(r'C:\Users\User\Desktop\essential-oil-guide\html-source\blend.html')

# 精油 → slug（連到完整指南）
SLUG = {
    '甜橙': 'oil-sweet-orange', '柑橘': 'oil-mandarin', '檸檬': 'oil-lemon', '葡萄柚': 'oil-grapefruit',
    '佛手柑': 'oil-bergamot', '橙花': 'oil-neroli', '苦橙葉': 'oil-petitgrain', '玫瑰': 'oil-rose',
    '茉莉': 'oil-jasmine', '依蘭': 'oil-ylang-ylang', '永久花': 'oil-helichrysum',
    '羅馬洋甘菊': 'oil-roman-chamomile', '德國洋甘菊': 'oil-german-chamomile', '西洋蓍草': 'oil-yarrow',
    '真正薰衣草': 'oil-lavender', '穗花薰衣草': 'oil-spike-lavender', '醒目薰衣草': 'oil-lavandin',
    '迷迭香': 'oil-rosemary', '甜馬鬱蘭': 'oil-marjoram', '快樂鼠尾草': 'oil-clary-sage',
    '甜羅勒': 'oil-sweet-basil', '百里香': 'oil-thyme', '香蜂草': 'oil-melissa', '天竺葵': 'oil-geranium',
    '玫瑰草': 'oil-palmarosa', '胡椒薄荷': 'oil-peppermint', '綠薄荷': 'oil-spearmint',
    '尤加利': 'oil-eucalyptus', '茶樹': 'oil-tea-tree', '桉油醇樟': 'oil-ravintsara',
    '檸檬尤加利': 'oil-lemon-eucalyptus', '月桂': 'oil-bay', '大西洋雪松': 'oil-cedarwood',
    '檀香': 'oil-sandalwood', '杜松漿果': 'oil-juniper', '絲柏': 'oil-cypress', '黑雲杉': 'oil-black-spruce',
    '廣藿香': 'oil-patchouli', '岩蘭草': 'oil-vetiver', '薑': 'oil-ginger', '黑胡椒': 'oil-black-pepper',
    '丁香': 'oil-clove', '香茅': 'oil-citronella', '乳香': 'oil-frankincense', '沒藥': 'oil-myrrh',
    '甜茴香': 'oil-sweet-fennel',
}

# 16 情境配方。note: top前/mid中/base後。drops 為擴香基準（總 8-10 滴）
# (emoji, 情境名, 類別 feeling/env, [(精油,滴,note)], 方法建議, 為什麼)
BLENDS = [
    # ── 感覺 / 情緒 ──
    ('😴', '放鬆助眠', 'feeling', [('真正薰衣草',4,'mid'),('羅馬洋甘菊',2,'mid'),('大西洋雪松',2,'base')],
     '睡前 30 分鐘擴香；或滾珠瓶（2%）塗手腕、枕邊',
     '薰衣草的乙酸沉香酯安撫神經、羅馬洋甘菊溫柔抗痙攣、雪松後調延長放鬆並接地，是最經典的安眠金字塔。'),
    ('😰', '紓壓抗焦慮', 'feeling', [('佛手柑',3,'top'),('真正薰衣草',3,'mid'),('乳香',2,'base')],
     '辦公桌擴香或掌心嗅吸；佛手柑用 FCF 版可日間用',
     '佛手柑明亮前調瞬間提振、薰衣草穩定情緒、乳香深沉後調拉長呼吸節奏——焦慮急救的黃金組合。'),
    ('⚡', '提神專注', 'feeling', [('迷迭香',3,'mid'),('檸檬',3,'top'),('胡椒薄荷',2,'top')],
     '工作/讀書時擴香；嗅吸棒隨身',
     '迷迭香增強記憶與專注、檸檬清新提神、薄荷的薄荷腦瞬間醒腦——咖啡之外的天然提神配方。'),
    ('🌈', '振奮情緒', 'feeling', [('甜橙',4,'top'),('天竺葵',2,'mid'),('依蘭',1,'mid')],
     '早晨擴香喚醒好心情；客廳空間香氛',
     '甜橙的陽光氣息驅散低落、天竺葵平衡情緒高低、依蘭帶來愉悅暖意——情緒低落時的陽光配方。'),
    ('🧘', '冥想沉澱', 'feeling', [('乳香',3,'base'),('檀香',2,'base'),('大西洋雪松',2,'base'),('甜橙',1,'top')],
     '冥想/瑜伽前擴香；靜心空間',
     '乳香、檀香、雪松三大後調營造神聖沉靜，一滴甜橙提亮層次——千年來聖殿與冥想的香氣語言。'),
    ('💕', '浪漫愉悅', 'feeling', [('佛手柑',3,'top'),('依蘭',2,'mid'),('玫瑰草',2,'mid'),('檀香',1,'base')],
     '臥室氛圍擴香；稀釋成身體按摩油（2%）',
     '佛手柑開場、依蘭與玫瑰草的花香之心、檀香木質定香——溫暖而不甜膩的浪漫氛圍。'),
    ('⚖️', '平衡穩定', 'feeling', [('天竺葵',3,'mid'),('真正薰衣草',2,'mid'),('岩蘭草',2,'base')],
     '情緒起伏大時擴香；滾珠瓶塗太陽神經叢',
     '天竺葵平衡荷爾蒙與情緒、薰衣草穩定、岩蘭草深沉接地——適合忽高忽低、需要重心的時刻。'),
    # ── 環境 / 情境 ──
    ('🛏️', '臥室助眠', 'env', [('真正薰衣草',4,'mid'),('甜馬鬱蘭',2,'mid'),('大西洋雪松',2,'base')],
     '睡前擴香或枕頭噴霧（1% 稀釋）',
     '薰衣草+甜馬鬱蘭雙重溫和鎮靜、雪松接地，營造深沉睡眠的臥室氛圍。'),
    ('💼', '辦公室提神', 'env', [('迷迭香',3,'mid'),('檸檬',3,'top'),('葡萄柚',2,'top')],
     '辦公桌小型擴香；共用空間請控制劑量、保持通風',
     '迷迭香提升專注、檸檬與葡萄柚明亮提神，趕走午後昏沉又不擾鄰座。'),
    ('🛁', '浴室 SPA', 'env', [('尤加利',3,'top'),('胡椒薄荷',2,'top'),('迷迭香',3,'mid')],
     '泡澡先用基底油/浴鹽乳化再入水；或淋浴蒸氣嗅吸',
     '尤加利與薄荷的清涼桉葉感打開呼吸、迷迭香活絡循環——居家 SPA 的清新蒸氣。'),
    ('🕉️', '瑜伽冥想', 'env', [('乳香',3,'base'),('檀香',3,'base'),('岩蘭草',2,'base')],
     '練習前擴香整個空間',
     '三大後調木質與樹脂香緩慢釋放，幫助呼吸沉穩、思緒落定，是瑜伽與冥想的接地香氣。'),
    ('📚', '讀書專注', 'env', [('迷迭香',3,'mid'),('檸檬',3,'top'),('甜羅勒',2,'mid')],
     '書桌擴香；嗅吸棒於休息時補吸',
     '迷迭香與甜羅勒養護神經、強化記憶，檸檬保持頭腦清醒——考試與深度工作的專注配方。'),
    ('🏡', '客廳迎賓', 'env', [('甜橙',4,'top'),('佛手柑',2,'top'),('大西洋雪松',2,'base')],
     '訪客來訪前擴香；日常居家香氛',
     '柑橘的溫暖好客感加上雪松的沉穩底蘊，營造放鬆又有質感的待客空間。'),
    ('✨', '淨化空間', 'env', [('茶樹',3,'top'),('檸檬',3,'top'),('杜松漿果',2,'mid')],
     '空間擴香；換季或久未通風時使用',
     '茶樹與檸檬清新淨化、杜松漿果傳統用於能量淨化——換季、搬新家、想重整空間時的清新配方。'),
    ('🎉', '派對歡聚', 'env', [('葡萄柚',4,'top'),('甜橙',3,'top'),('依蘭',1,'mid')],
     '聚會空間擴香',
     '葡萄柚與甜橙的歡快柑橘氣泡感加一滴依蘭的異國花香，讓聚會氣氛輕鬆愉悅。'),
    ('🌸', '泡澡放鬆', 'env', [('真正薰衣草',3,'mid'),('依蘭',2,'mid'),('橙花',2,'mid')],
     '精油先以 1 大匙基底油或全脂奶乳化再入浴，浸泡 15 分鐘',
     '薰衣草、依蘭、橙花三種花香交織，把浴缸變成療癒的香氛聖殿。'),
    # ── 感覺 / 情緒（擴充）──
    ('🎯', '專注創意', 'feeling', [('迷迭香',3,'mid'),('佛手柑',3,'top'),('乳香',2,'base')],
     '創作/企劃工作時擴香；嗅吸棒卡關時補吸',
     '迷迭香打開記憶與思路、佛手柑提振而不亢奮、乳香拉長專注的呼吸節奏——適合需要靈感又要穩定的腦力工作。'),
    ('🦁', '勇氣自信', 'feeling', [('甜羅勒',3,'mid'),('黑胡椒',2,'mid'),('佛手柑',3,'top')],
     '上台/面試/重要決定前掌心嗅吸',
     '甜羅勒振奮精神主權、黑胡椒點燃行動暖意、佛手柑化解緊繃——「香草之王」配辛香,給你站出去的底氣。'),
    ('🕊️', '放下釋懷', 'feeling', [('乳香',3,'base'),('永久花',2,'mid'),('橙花',2,'mid')],
     '情緒卡住、放不下時擴香或塗心口',
     '乳香深沉地鬆開緊抓的呼吸、永久花化解心裡的瘀堵、橙花溫柔承接——適合需要對自己慈悲、把事情放下的時刻。'),
    ('🩹', '情緒療傷', 'feeling', [('玫瑰',1,'mid'),('永久花',2,'mid'),('檀香',2,'base')],
     '低潮、失落、需要被接住時塗心口或擴香',
     '玫瑰打開心的盔甲、永久花修復情緒瘀傷、檀香沉穩定錨——失去與哀傷時最溫柔的陪伴配方。'),
    # ── 環境 / 情境（擴充）──
    ('🚗', '車內清新', 'env', [('胡椒薄荷',2,'top'),('檸檬',3,'top'),('迷迭香',2,'mid')],
     '車用擴香（通風口夾或微量擴香）；長途防睏',
     '薄荷醒腦防暈、檸檬清新除悶、迷迭香維持專注——長途駕駛保持清醒、化解車內悶味。'),
    ('🍳', '廚房除味', 'env', [('檸檬',4,'top'),('甜橙',3,'top'),('迷迭香',2,'mid')],
     '料理後擴香除味；垃圾桶旁滴於棉球',
     '檸檬與甜橙的柑橘酸香中和油煙與廚餘味、迷迭香添清新草本——比化學芳香劑天然的廚房除味。'),
    ('🚪', '玄關迎賓', 'env', [('佛手柑',3,'top'),('大西洋雪松',2,'base'),('檸檬',2,'top')],
     '入口處擴香，建立第一印象',
     '佛手柑的明亮好客、雪松的沉穩質感、檸檬的乾淨清新——進門那一刻的香氣名片。'),
    ('🌧️', '除濕除霉', 'env', [('茶樹',3,'top'),('尤加利',3,'top'),('檸檬',2,'top')],
     '潮濕季節、浴廁、衣櫥角落擴香或噴霧',
     '茶樹與尤加利清新淨化潮濕悶味、檸檬提亮——梅雨季、久未通風空間的清爽配方。'),
]

NOTE_LABEL = {'top': '前調', 'mid': '中調', 'base': '後調'}
NOTE_COLOR = {'top': '#E8A04B', 'mid': '#88BC88', 'base': '#7898B8'}

HEADER = '''<div class="topbar">🌿 精油能量圖譜 — 用知識療癒您的生活 社會修行</div>
<header>
  <div class="header-inner">
    <a href="index.html" class="logo-wrap" style="text-decoration:none;display:flex;align-items:center;gap:12px;">
      <div class="logo-icon">🌿</div>
      <div class="logo-text"><div class="site-title">精油能量圖譜</div><div class="site-sub">精油學 · 從植物到身心靈</div></div>
    </a>
    <nav><ul>
      <li><a href="index.html">首頁</a></li>
      <li><a href="encyclopedia.html">大百科</a></li>
      <li><a href="oils.html">精油</a></li>
      <li><a href="blend.html" class="active">調配精油</a></li>
      <li><a href="aromatherapy.html">芳療應用</a></li>
      <li><a href="safety.html">安全指南</a></li>
    </ul></nav>
    <input class="nav-search" type="text" placeholder="搜尋精油..." onkeydown="if(event.key===&quot;Enter&quot;&&this.value.trim())location.href=&quot;search.html?q=&quot;+encodeURIComponent(this.value.trim())" />
    <button class="menu-toggle">☰</button>
  </div>
</header>'''


def oil_chip(name, drops, note):
    slug = SLUG.get(name, '')
    color = NOTE_COLOR[note]
    label = NOTE_LABEL[note]
    href = f'{slug}.html' if slug else '#'
    return (f'<a href="{href}" class="blend-oil" '
            f'style="display:flex;align-items:center;gap:8px;padding:8px 12px;background:#fff;'
            f'border:1px solid {color}55;border-left:4px solid {color};border-radius:8px;'
            f'text-decoration:none;color:#3D3328;">'
            f'<span style="font-weight:700;color:{color};font-size:13px;min-width:30px;">{label}</span>'
            f'<span style="flex:1;font-weight:600;font-size:14px;">{name}</span>'
            f'<span style="background:{color}22;color:{color};font-weight:700;font-size:13px;'
            f'padding:2px 10px;border-radius:12px;">{drops} 滴</span></a>')


# 46 精油 metadata（供自訂計算器）：note 揮發調性；flags 安全旗標
# note: top前 / mid中 / base後；flags: photo光敏 preg孕婦避 kids幼兒避 cat貓避
OILS_META = {
    '甜橙': ('top', ['photo', 'cat']), '柑橘': ('top', ['photo', 'cat']), '檸檬': ('top', ['photo', 'cat']),
    '葡萄柚': ('top', ['photo', 'cat']), '佛手柑': ('top', ['photo', 'cat']),
    '胡椒薄荷': ('top', ['preg', 'kids', 'cat']), '綠薄荷': ('top', []),
    '檸檬尤加利': ('top', ['kids', 'cat']), '香茅': ('top', ['kids', 'cat']),
    '尤加利': ('top', ['preg', 'kids', 'cat']), '茶樹': ('top', ['cat']), '桉油醇樟': ('top', ['preg', 'kids']),
    '橙花': ('mid', []), '玫瑰': ('mid', ['preg']), '茉莉': ('mid', ['preg']), '依蘭': ('mid', []),
    '永久花': ('mid', []), '羅馬洋甘菊': ('mid', []), '德國洋甘菊': ('mid', []), '西洋蓍草': ('mid', ['preg', 'kids']),
    '真正薰衣草': ('mid', []), '穗花薰衣草': ('mid', ['preg', 'kids']), '醒目薰衣草': ('mid', ['preg', 'kids']),
    '迷迭香': ('mid', ['preg', 'kids']), '甜馬鬱蘭': ('mid', ['preg']), '快樂鼠尾草': ('mid', ['preg']),
    '甜羅勒': ('mid', ['preg']), '百里香': ('mid', ['preg', 'kids', 'cat']), '香蜂草': ('mid', ['preg']),
    '天竺葵': ('mid', ['cat']), '玫瑰草': ('mid', []), '苦橙葉': ('mid', []), '月桂': ('mid', []),
    '薑': ('mid', []), '黑胡椒': ('mid', []), '丁香': ('mid', ['preg', 'kids', 'cat']), '甜茴香': ('mid', ['preg', 'kids']),
    '杜松漿果': ('mid', ['preg']), '絲柏': ('mid', ['preg']), '黑雲杉': ('mid', []),
    '大西洋雪松': ('base', ['preg']), '檀香': ('base', []), '廣藿香': ('base', []),
    '岩蘭草': ('base', []), '乳香': ('base', []), '沒藥': ('base', ['preg']),
}


def build_calculator():
    """自訂調配計算器：選精油→即時算前中後調平衡、基底油用量、安全旗標"""
    import json
    groups = {'top': [], 'mid': [], 'base': []}
    for name, (note, flags) in OILS_META.items():
        groups[note].append(name)
    js_data = {name: {'note': note, 'flags': flags, 'slug': SLUG.get(name, '')}
               for name, (note, flags) in OILS_META.items()}

    def chips(note):
        c = NOTE_COLOR[note]
        return ''.join(
            f'<button type="button" class="calc-oil" data-oil="{n}" '
            f'style="padding:6px 12px;margin:3px;background:#fff;border:1.5px solid {c}66;'
            f'border-radius:16px;font-size:13px;font-weight:600;color:#3D3328;cursor:pointer;'
            f'font-family:inherit;transition:all .12s;">{n}</button>'
            for n in groups[note])

    return f'''
  <!-- 自訂調配計算器 -->
  <section id="calc" style="margin:44px 0 32px;">
    <h2 style="font-size:22px;color:var(--green-dark);border-bottom:2px solid var(--beige);padding-bottom:8px;">🧪 自己調配（自訂計算器）</h2>
    <p style="font-size:15px;line-height:1.9;margin:12px 0 18px;">點選你想用的精油（可多選、可調滴數），下方即時算出<strong>前中後調平衡</strong>、<strong>各用途要配多少基底油</strong>，並標出<strong>安全旗標</strong>（光敏／孕婦／幼兒／貓）。</p>

    <div style="background:#fff;border:1px solid var(--border,#E5D9C0);border-radius:12px;padding:16px 18px;">
      <div style="margin-bottom:10px;"><span style="display:inline-block;width:10px;height:10px;background:{NOTE_COLOR['top']};border-radius:50%;margin-right:6px;"></span><strong style="color:{NOTE_COLOR['top']};font-size:13px;">前調（揮發快）</strong><div style="margin-top:6px;">{chips('top')}</div></div>
      <div style="margin-bottom:10px;"><span style="display:inline-block;width:10px;height:10px;background:{NOTE_COLOR['mid']};border-radius:50%;margin-right:6px;"></span><strong style="color:#5A7A4A;font-size:13px;">中調（核心）</strong><div style="margin-top:6px;">{chips('mid')}</div></div>
      <div><span style="display:inline-block;width:10px;height:10px;background:{NOTE_COLOR['base']};border-radius:50%;margin-right:6px;"></span><strong style="color:{NOTE_COLOR['base']};font-size:13px;">後調（定香）</strong><div style="margin-top:6px;">{chips('base')}</div></div>
    </div>

    <div id="calc-selected" style="margin-top:16px;"></div>
    <div id="calc-result" style="margin-top:16px;"></div>
  </section>

  <script>
  (function(){{
    var META={json.dumps(js_data, ensure_ascii=False)};
    var NOTE_LABEL={{top:'前調',mid:'中調',base:'後調'}};
    var NOTE_COLOR={{top:'{NOTE_COLOR['top']}',mid:'{NOTE_COLOR['mid']}',base:'{NOTE_COLOR['base']}'}};
    var FLAG={{photo:'☀️ 光敏（塗後避日曬）',preg:'🤰 孕婦避用',kids:'👶 幼兒避用',cat:'🐱 貓家庭避擴香'}};
    var state={{}};  // oilName -> drops
    var selBox=document.getElementById('calc-selected');
    var resBox=document.getElementById('calc-result');

    function render(){{
      var names=Object.keys(state);
      // 已選清單
      if(!names.length){{
        selBox.innerHTML='<div style="text-align:center;padding:20px;color:var(--text-mid);background:#FBF7F1;border-radius:10px;">👆 點選上方精油開始調配</div>';
        resBox.innerHTML='';
        document.querySelectorAll('.calc-oil').forEach(function(b){{b.style.background='#fff';b.style.boxShadow='none';}});
        return;
      }}
      var rows=names.map(function(n){{
        var c=NOTE_COLOR[META[n].note], slug=META[n].slug;
        var link=slug?'<a href="'+slug+'.html" style="color:'+c+';text-decoration:none;font-weight:600;">'+n+'</a>':'<strong>'+n+'</strong>';
        return '<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:#fff;border:1px solid '+c+'44;border-left:4px solid '+c+';border-radius:8px;margin-bottom:6px;">'
          +'<span style="font-size:11px;color:'+c+';font-weight:700;min-width:28px;">'+NOTE_LABEL[META[n].note]+'</span>'
          +'<span style="flex:1;font-size:14px;">'+link+'</span>'
          +'<button type="button" class="calc-minus" data-oil="'+n+'" style="width:26px;height:26px;border:1px solid '+c+';background:#fff;color:'+c+';border-radius:6px;cursor:pointer;font-size:16px;font-family:inherit;">−</button>'
          +'<span style="min-width:42px;text-align:center;font-weight:700;font-size:14px;">'+state[n]+' 滴</span>'
          +'<button type="button" class="calc-plus" data-oil="'+n+'" style="width:26px;height:26px;border:1px solid '+c+';background:'+c+';color:#fff;border-radius:6px;cursor:pointer;font-size:16px;font-family:inherit;">+</button>'
          +'</div>';
      }}).join('');
      selBox.innerHTML=rows;

      // 計算
      var total=0,byNote={{top:0,mid:0,base:0}},flags={{}};
      names.forEach(function(n){{
        total+=state[n]; byNote[META[n].note]+=state[n];
        META[n].flags.forEach(function(f){{flags[f]=(flags[f]||[]);flags[f].push(n);}});
      }});
      var pct=function(v){{return total?Math.round(v/total*100):0;}};
      // 基底油用量（滴×0.05ml÷濃度）
      var ml=function(p){{return (total*0.05/p).toFixed(1);}};
      // 平衡提示
      var tip='';
      if(!byNote.base) tip='💡 缺後調定香，香氣易快速消散——可加檀香/乳香/岩蘭草/廣藿香延長尾韻。';
      else if(!byNote.top) tip='💡 缺前調，第一印象較弱——可加柑橘/薄荷類提亮開場。';
      else if(byNote.base>byNote.top+byNote.mid) tip='💡 後調偏重，香氣厚重沉穩——若想更輕盈可增前調。';
      else tip='✅ 前中後三調齊全，層次平衡。';

      var flagHtml='';
      var fk=Object.keys(flags);
      if(fk.length){{
        flagHtml='<div style="background:#FFF4E6;border-left:4px solid #E8A04B;border-radius:8px;padding:12px 16px;margin-top:12px;">'
          +'<strong style="color:#B5701A;font-size:14px;">⚠️ 安全旗標</strong><div style="font-size:13px;line-height:1.9;color:#5D4A28;margin-top:4px;">'
          +fk.map(function(f){{return FLAG[f]+'：'+flags[f].join('、');}}).join('<br>')
          +'</div></div>';
      }}

      resBox.innerHTML=
        '<div style="background:#FBF7F1;border-radius:12px;padding:16px 18px;">'
        +'<div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px;"><strong style="font-size:16px;color:var(--green-dark);">調配分析</strong><span style="font-size:13px;color:var(--text-mid);">共 '+total+' 滴 · '+names.length+' 支精油</span></div>'
        // 前中後調比例
        +'<div style="display:flex;height:28px;border-radius:6px;overflow:hidden;margin-bottom:6px;">'
        +(byNote.top?'<div style="width:'+pct(byNote.top)+'%;background:'+NOTE_COLOR.top+';color:#fff;font-size:11px;display:flex;align-items:center;justify-content:center;">前'+pct(byNote.top)+'%</div>':'')
        +(byNote.mid?'<div style="width:'+pct(byNote.mid)+'%;background:'+NOTE_COLOR.mid+';color:#fff;font-size:11px;display:flex;align-items:center;justify-content:center;">中'+pct(byNote.mid)+'%</div>':'')
        +(byNote.base?'<div style="width:'+pct(byNote.base)+'%;background:'+NOTE_COLOR.base+';color:#fff;font-size:11px;display:flex;align-items:center;justify-content:center;">後'+pct(byNote.base)+'%</div>':'')
        +'</div>'
        +'<p style="font-size:13px;color:#5A7A4A;margin:0 0 14px;">'+tip+'</p>'
        // 基底油用量
        +'<div style="font-size:13px;font-weight:700;color:#8B6F3E;margin-bottom:8px;">💧 這個配方要配多少基底油</div>'
        +'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;font-size:13px;text-align:center;">'
        +'<div><div style="font-size:18px;">🌫️</div><div style="font-weight:600;">擴香</div><div style="color:var(--text-mid);">直接滴 '+total+' 滴入水氧機</div></div>'
        +'<div><div style="font-size:18px;">🧴</div><div style="font-weight:600;">滾珠瓶 2%</div><div style="color:var(--text-mid);">+ 約 '+ml(0.02)+' ml 基底油</div></div>'
        +'<div><div style="font-size:18px;">💆</div><div style="font-weight:600;">按摩油 3%</div><div style="color:var(--text-mid);">+ 約 '+ml(0.03)+' ml 基底油</div></div>'
        +'</div>'
        +flagHtml
        +'</div>';
    }}

    document.querySelectorAll('.calc-oil').forEach(function(b){{
      b.onclick=function(){{
        var n=b.getAttribute('data-oil');
        if(state[n]){{delete state[n];b.style.background='#fff';b.style.boxShadow='none';}}
        else{{state[n]=2;var c=NOTE_COLOR[META[n].note];b.style.background=c+'22';b.style.boxShadow='0 0 0 2px '+c+'55';}}
        render();
      }};
    }});
    document.addEventListener('click',function(e){{
      var n=e.target.getAttribute&&e.target.getAttribute('data-oil');
      if(!n||!state[n])return;
      if(e.target.classList.contains('calc-plus')&&state[n]<12)state[n]++;
      else if(e.target.classList.contains('calc-minus')){{state[n]--;if(state[n]<1)delete state[n];
        var btn=document.querySelector('.calc-oil[data-oil="'+n+'"]');if(btn&&!state[n]){{btn.style.background='#fff';btn.style.boxShadow='none';}}}}
      else return;
      render();
    }});
    render();
  }})();
  </script>'''


# 從網路流傳的精油配方表（多來源）萃取整理的配方主題。
# 用途名稱依原表保留；惟癌症/腫瘤/結節/結石類已中性化（避免「精油治癌」假訊息致人延誤治療）。
# 品牌名、原表用法與行銷紅字一律移除。精油組合為合理搭配，滴數引導用上方計算器自調。
# (emoji, 用途名, [精油（須在 SLUG）])
EXTRA_TOPICS = [
    # 面部與肌膚
    ('💆', '面部精華保養', ['乳香', '真正薰衣草', '天竺葵']),
    ('☀️', '美膚防曬', ['乳香', '天竺葵', '真正薰衣草']),
    ('🌅', '曬後美白修復', ['真正薰衣草', '永久花', '乳香']),
    ('💧', '美膚淡斑', ['檸檬', '乳香', '玫瑰']),
    ('👁️', '黑眼圈眼袋', ['永久花', '真正薰衣草', '天竺葵']),
    ('⏳', '抗衰緊緻', ['乳香', '玫瑰', '檀香']),
    ('🌷', '肌膚回春', ['乳香', '玫瑰', '永久花']),
    ('✨', '疤痕修復', ['永久花', '乳香', '真正薰衣草']),
    ('🧴', '痘痘調理', ['茶樹', '真正薰衣草', '天竺葵']),
    ('💇', '生髮頭皮養護', ['迷迭香', '大西洋雪松', '胡椒薄荷']),
    # 呼吸／換季
    ('👃', '鼻炎', ['尤加利', '胡椒薄荷', '茶樹']),
    ('🗣️', '清咽止咳', ['檸檬', '乳香', '薑']),
    ('🌬️', '咳嗽有痰', ['尤加利', '乳香', '檸檬']),
    ('💨', '久咳氣喘', ['乳香', '真正薰衣草', '絲柏']),
    ('🤧', '感冒配方', ['茶樹', '尤加利', '胡椒薄荷', '檸檬']),
    ('🛡️', '抗病毒防護', ['茶樹', '桉油醇樟', '檸檬', '丁香']),
    ('🌡️', '退燒舒緩', ['胡椒薄荷', '真正薰衣草', '檸檬']),
    # 消化／代謝循環
    ('🍽️', '消化不良', ['薑', '胡椒薄荷', '甜茴香']),
    ('🫃', '脾胃養護', ['薑', '甜茴香', '甜羅勒']),
    ('🍷', '解酒', ['胡椒薄荷', '葡萄柚', '薑']),
    ('💧', '養腎排毒', ['杜松漿果', '葡萄柚', '絲柏']),
    ('🧬', '護肝排毒', ['葡萄柚', '迷迭香', '胡椒薄荷']),
    ('🌊', '淋巴排毒', ['葡萄柚', '絲柏', '杜松漿果', '薑']),
    ('🍃', '祛濕／體態按摩', ['葡萄柚', '杜松漿果', '絲柏']),
    # 循環／神經
    ('❤️', '高血壓舒緩', ['真正薰衣草', '依蘭', '甜馬鬱蘭', '佛手柑']),
    ('🩸', '血管保養', ['絲柏', '檸檬', '天竺葵']),
    ('😴', '安神助眠', ['真正薰衣草', '羅馬洋甘菊', '大西洋雪松']),
    # 肌肉關節
    ('💪', '五星酸痛', ['胡椒薄荷', '黑胡椒', '薑', '甜馬鬱蘭']),
    ('🦴', '關節疼痛', ['薑', '黑胡椒', '乳香', '甜馬鬱蘭']),
    ('🧎', '腰背舒緩', ['甜馬鬱蘭', '黑胡椒', '薑', '檀香']),
    ('💆‍♂️', '肩頸舒緩', ['胡椒薄荷', '甜馬鬱蘭', '乳香']),
    # 女性／婦科（纖維瘤類已中性化為胸部舒緩）
    ('🌸', '暖宮調經', ['快樂鼠尾草', '天竺葵', '甜茴香', '薑']),
    ('🌺', '子宮保養', ['快樂鼠尾草', '天竺葵', '玫瑰']),
    ('🤱', '胸部舒緩按摩', ['真正薰衣草', '天竺葵', '乳香']),
    # 過敏／皮膚舒緩
    ('🌿', '過敏舒緩', ['德國洋甘菊', '真正薰衣草', '永久花']),
    ('🩹', '濕疹舒緩', ['德國洋甘菊', '真正薰衣草', '永久花']),
    # 腹部舒緩（結石類中性化）／呼吸舒緩（結節類中性化）
    ('🫄', '腹部舒緩按摩', ['胡椒薄荷', '薑', '檸檬']),
    ('🫁', '呼吸道日常舒緩', ['乳香', '尤加利', '真正薰衣草']),
    # 其他
    ('🛡️', '甲狀腺保養', ['乳香', '天竺葵', '檀香']),
    ('🚗', '暈車舒緩', ['胡椒薄荷', '薑', '檸檬']),
    ('🔥', '滋補陽氣', ['薑', '黑胡椒', '大西洋雪松']),
    ('🦟', '戶外防蚊', ['檸檬尤加利', '香茅', '真正薰衣草', '天竺葵']),
    # 兒童（需稀釋）／學習
    ('🧒', '兒童日常保養（需稀釋）', ['甜橙', '真正薰衣草', '羅馬洋甘菊']),
    ('📖', '專注學習（需稀釋）', ['迷迭香', '檸檬', '乳香']),
]


def build_extra_topics():
    """從網路配方表合規化萃取的「保養與身體」主題卡片區塊"""
    cards = []
    for emoji, name, oils in EXTRA_TOPICS:
        chips = ''.join(
            f'<a href="{SLUG.get(o,"#")}.html" style="display:inline-block;padding:4px 11px;margin:3px;'
            f'background:#fff;border:1px solid #C8A67355;border-radius:14px;font-size:13px;'
            f'color:#5D4A28;text-decoration:none;font-weight:600;">{o}</a>'
            for o in oils)
        cards.append(
            f'<div style="background:#fff;border:1px solid var(--border,#E5D9C0);border-radius:12px;padding:14px 16px;">'
            f'<div style="font-size:16px;font-weight:700;color:var(--green-dark,#3a5a40);margin-bottom:8px;">{emoji} {name}</div>'
            f'<div>{chips}</div></div>')
    return f'''
  <!-- 更多配方主題（配方參考庫）-->
  <section style="margin:44px 0 32px;">
    <h2 style="font-size:22px;color:var(--green-dark);border-bottom:2px solid var(--beige);padding-bottom:8px;">🌿 精油配方參考庫</h2>
    <div style="background:#FFF4E6;border-left:4px solid #E8A04B;border-radius:8px;padding:14px 18px;margin:14px 0 18px;">
      <strong style="color:#B5701A;font-size:14px;">⚠️ 重要聲明（請務必閱讀）</strong>
      <p style="font-size:13px;line-height:1.85;color:#5D4A28;margin:6px 0 0;">以下配方蒐集整理自各家流傳的精油使用紀錄，<strong>用途名稱僅為分類標籤，不代表精油具有任何醫療或治療效果</strong>。精油是輔助身心平衡的芳香生活方式，<strong>不是藥物，無法治療、診斷或預防任何疾病</strong>。身體不適請就醫；切勿以精油取代正規醫療。孕婦、嬰幼兒、慢性病、服藥中者使用前請先諮詢醫師或專業芳療師。</p>
    </div>
    <p style="font-size:14px;line-height:1.85;margin:0 0 18px;color:var(--text-mid);">點精油看完整指南，<strong>滴數請用上方「自訂計算器」</strong>依用途調配（臉部 ≤1%、身體 2-3%、擴香適量）。</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;">
      {''.join(cards)}
    </div>
  </section>'''


def build():
    # 配方卡片 HTML（JS 用 data-* 切換）
    cards = []
    for i, (emoji, name, cat, oils, method, why) in enumerate(BLENDS):
        total = sum(d for _, d, _ in oils)
        chips = '\n        '.join(oil_chip(n, d, nt) for n, d, nt in oils)
        # 稀釋換算
        diffuser = total
        roller = max(2, round(total * 0.4))  # 2% 10ml 滾珠約
        massage = max(3, round(total * 0.6))
        card = f'''    <div class="blend-card" data-cat="{cat}" data-idx="{i}" style="display:none;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
        <span style="font-size:40px;">{emoji}</span>
        <div>
          <h3 style="margin:0;font-size:22px;color:var(--green-dark);">{name}</h3>
          <span style="font-size:13px;color:var(--text-mid);">{"依感覺情緒" if cat=="feeling" else "依環境情境"} · 共 {total} 滴</span>
        </div>
      </div>
      <div style="display:grid;gap:8px;margin-bottom:18px;">
        {chips}
      </div>
      <div style="background:#FBF7F1;border-radius:10px;padding:14px 16px;margin-bottom:14px;">
        <div style="font-size:13px;font-weight:700;color:#8B6F3E;margin-bottom:8px;">💧 三種用法稀釋換算</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;font-size:13px;">
          <div style="text-align:center;"><div style="font-size:20px;">🌫️</div><div style="font-weight:600;">擴香</div><div style="color:var(--text-mid);">水氧機加 {diffuser} 滴</div></div>
          <div style="text-align:center;"><div style="font-size:20px;">🧴</div><div style="font-weight:600;">滾珠瓶</div><div style="color:var(--text-mid);">10ml 基底油 + {roller} 滴(2%)</div></div>
          <div style="text-align:center;"><div style="font-size:20px;">💆</div><div style="font-weight:600;">按摩油</div><div style="color:var(--text-mid);">10ml 基底油 + {massage} 滴(3%)</div></div>
        </div>
      </div>
      <p style="font-size:14px;line-height:1.85;color:#3D3328;margin:0;background:#EEF5EE;border-left:4px solid #88BC88;padding:12px 16px;border-radius:8px;">
        <strong>🌿 為什麼這樣調：</strong>{why}
      </p>
    </div>'''
        cards.append(card)

    # 情境選擇按鈕
    feeling_btns = []
    env_btns = []
    for i, (emoji, name, cat, *_ ) in enumerate(BLENDS):
        btn = (f'<button class="scenario-btn" data-idx="{i}" '
               f'style="display:flex;flex-direction:column;align-items:center;gap:6px;padding:16px 10px;'
               f'background:#fff;border:2px solid var(--border);border-radius:14px;cursor:pointer;'
               f'transition:all .15s;font-family:inherit;">'
               f'<span style="font-size:30px;">{emoji}</span>'
               f'<span style="font-size:14px;font-weight:600;color:#3D3328;">{name}</span></button>')
        (feeling_btns if cat == 'feeling' else env_btns).append(btn)

    calc_html = build_calculator()
    extra_html = build_extra_topics()

    desc ='依你的感覺或環境一鍵生成精油配方，或用自訂計算器自己選精油調配。內建調香金字塔（前中後調）平衡分析、基底油用量換算、光敏／孕婦／幼兒／貓安全旗標，46 支精油即點即連完整指南。'
    html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>調配精油｜依感覺與環境一鍵生成精油配方 | 精油能量圖譜</title>
  <meta name="description" content="{desc}" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css" />
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
  <link rel="icon" href="favicon.ico">
  <script src="assets/js/nav.js" defer></script>
  <!-- SEO_START -->
  <link rel="canonical" href="https://intelliverse.tw/blend/" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="精油能量圖譜" />
  <meta property="og:locale" content="zh_TW" />
  <meta property="og:title" content="調配精油｜依感覺與環境一鍵生成精油配方" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="https://intelliverse.tw/blend/" />
  <meta property="og:image" content="https://cdn.jsdelivr.net/gh/kiolllery8-dev/essential-oil-cdn@main/images/hero-home.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="調配精油｜依感覺與環境一鍵生成精油配方" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="https://cdn.jsdelivr.net/gh/kiolllery8-dev/essential-oil-cdn@main/images/hero-home.png" />
  <!-- SEO_END -->
</head>
<body>
{HEADER}
<!-- WebApplication schema（放 body 內，避免被 loadHtml 剝除 head）-->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "精油調配工具",
  "url": "https://intelliverse.tw/blend/",
  "applicationCategory": "LifestyleApplication",
  "operatingSystem": "Web",
  "inLanguage": "zh-TW",
  "description": "{desc}",
  "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "TWD"}},
  "publisher": {{"@id": "https://intelliverse.tw/#organization"}},
  "author": {{"@id": "https://intelliverse.tw/#author"}}
}}
</script>

<div class="oil-cover-hero" style="--c1:#5A7A6A;--c2:#88BC88;background:linear-gradient(135deg,#5A7A6A 0%,#88BC88 100%);">
  <span class="oil-cover-bg-emoji">⚗️</span>
  <div class="oil-cover-overlay"></div>
  <div class="oil-cover-content">
    <span class="oil-cover-cat">🧪 互動工具 · 調香金字塔</span>
    <h1>調配精油</h1>
    <p class="oil-cover-latin">依你的感覺與環境，一鍵生成專屬精油配方</p>
  </div>
</div>

<div class="breadcrumb"><div class="breadcrumb-inner">
  <a href="index.html">首頁</a><span class="sep">›</span><span>調配精油</span>
</div></div>

<main style="max-width:920px;margin:0 auto;padding:0 20px;">

  <section class="blend-intro" style="background:linear-gradient(135deg,#F5F0E6 0%,#EEE7D8 100%);border-left:4px solid #C8A673;padding:20px 24px;border-radius:12px;margin:28px 0;">
    <h2 style="font-size:18px;font-weight:700;color:#8B6F3E;margin:0 0 10px;">✦ 如何調配精油？</h2>
    <p style="font-size:15px;line-height:1.85;color:#3D3328;margin:0;">
      精油調配遵循「調香金字塔」：<strong>前調</strong>（柑橘、薄荷，揮發快、第一印象）、<strong>中調</strong>（薰衣草、天竺葵，配方核心）、<strong>後調</strong>（檀香、乳香，揮發慢、定香延長）。一般比例約前調 3：中調 5：後調 2。本頁提供兩種用法：① 依<strong>感覺／環境</strong>一鍵套用 24 組現成配方；② 用下方<strong>自訂計算器</strong>自己選精油，即時算前中後調平衡、基底油用量與安全旗標。使用前請參考 <a href="safety.html">精油安全指南</a>。
    </p>
  </section>

  <!-- 模式切換 -->
  <div style="display:flex;gap:10px;margin:24px 0 18px;">
    <button id="tab-feeling" class="mode-tab" style="flex:1;padding:14px;border:2px solid #88BC88;background:#88BC88;color:#fff;border-radius:12px;font-size:16px;font-weight:700;cursor:pointer;font-family:inherit;">😊 依感覺／情緒</button>
    <button id="tab-env" class="mode-tab" style="flex:1;padding:14px;border:2px solid #88BC88;background:#fff;color:#5A7A6A;border-radius:12px;font-size:16px;font-weight:700;cursor:pointer;font-family:inherit;">🏠 依環境／情境</button>
  </div>

  <!-- 情境按鈕 -->
  <div id="grid-feeling" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:12px;margin-bottom:28px;">
    {''.join(feeling_btns)}
  </div>
  <div id="grid-env" style="display:none;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:12px;margin-bottom:28px;">
    {''.join(env_btns)}
  </div>

  <!-- 配方結果 -->
  <div id="result" style="margin-bottom:32px;">
{chr(10).join(cards)}
    <div id="result-empty" style="text-align:center;padding:40px 20px;color:var(--text-mid);background:#FBF7F1;border-radius:14px;">
      👆 點選上方任一情境，即可看到專屬配方
    </div>
  </div>

{calc_html}
{extra_html}

  <!-- 調香金字塔教學 -->
  <section style="margin:40px 0;">
    <h2 style="font-size:22px;color:var(--green-dark);border-bottom:2px solid var(--beige);padding-bottom:8px;">🔺 調香金字塔原理</h2>
    <p style="font-size:15px;line-height:1.9;">專業調香依精油的<strong>揮發速度</strong>分三層，組合起來香氣才有層次與持久度：</p>
    <div style="display:grid;gap:10px;margin:16px 0;">
      <div style="background:#E8A04B18;border-left:4px solid #E8A04B;padding:12px 16px;border-radius:8px;"><strong style="color:#E8A04B;">前調（Top）</strong>：柑橘類、薄荷、尤加利。揮發最快，是第一印象，10-30 分鐘消散。約佔 30%。</div>
      <div style="background:#88BC8818;border-left:4px solid #88BC88;padding:12px 16px;border-radius:8px;"><strong style="color:#5A7A4A;">中調（Middle）</strong>：薰衣草、天竺葵、迷迭香、洋甘菊。配方的心臟，2-4 小時。約佔 50%。</div>
      <div style="background:#7898B818;border-left:4px solid #7898B8;padding:12px 16px;border-radius:8px;"><strong style="color:#5A6F98;">後調（Base）</strong>：檀香、乳香、岩蘭草、廣藿香。揮發最慢，定香延長整體香氣，可達數小時至數天。約佔 20%。</div>
    </div>
  </section>

  <!-- 稀釋比例表 -->
  <section style="margin:40px 0;">
    <h2 style="font-size:22px;color:var(--green-dark);border-bottom:2px solid var(--beige);padding-bottom:8px;">💧 安全稀釋比例</h2>
    <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;font-size:14px;background:#fff;border-radius:10px;overflow:hidden;margin-top:12px;">
      <thead><tr style="background:#5A7A6A;color:#fff;">
        <th style="padding:12px;text-align:left;">用途</th><th style="padding:12px;">濃度</th><th style="padding:12px;">10ml 基底油滴數</th></tr></thead>
      <tbody>
        <tr><td style="padding:10px 12px;border:1px solid #E5D9C0;">臉部 / 敏感肌</td><td style="padding:10px 12px;border:1px solid #E5D9C0;text-align:center;">0.5–1%</td><td style="padding:10px 12px;border:1px solid #E5D9C0;text-align:center;">1–2 滴</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #E5D9C0;">身體按摩 / 滾珠</td><td style="padding:10px 12px;border:1px solid #E5D9C0;text-align:center;">2–3%</td><td style="padding:10px 12px;border:1px solid #E5D9C0;text-align:center;">4–6 滴</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #E5D9C0;">局部急性 / 短期</td><td style="padding:10px 12px;border:1px solid #E5D9C0;text-align:center;">5%</td><td style="padding:10px 12px;border:1px solid #E5D9C0;text-align:center;">10 滴</td></tr>
        <tr><td style="padding:10px 12px;border:1px solid #E5D9C0;">兒童 / 孕婦</td><td style="padding:10px 12px;border:1px solid #E5D9C0;text-align:center;">≤ 1%</td><td style="padding:10px 12px;border:1px solid #E5D9C0;text-align:center;">先諮詢專業</td></tr>
      </tbody>
    </table>
    </div>
    <p style="font-size:13px;color:var(--text-light);margin-top:10px;">※ 1 滴精油 ≈ 0.05ml。柑橘類有光敏性，塗抹後 12 小時避免日曬。詳見 <a href="safety.html">安全指南</a>。</p>
  </section>

  <div class="info-box" style="background:#FFF4E6;border-left:4px solid #E8A04B;border-radius:8px;padding:16px 20px;margin:24px 0;">
    <strong style="color:#B5701A;">⚠️ 提醒</strong>
    <p style="font-size:14px;line-height:1.8;color:#5D4A28;margin:6px 0 0;">本工具配方為一般芳香生活建議，非醫療處方。孕婦、嬰幼兒、慢性病或用藥中請先諮詢專業芳療師或醫師。精油請稀釋後使用並先做肌膚測試。</p>
  </div>

</main>

<footer>
  <div class="footer-inner" style="max-width:1100px;margin:0 auto;padding:32px 20px;">
    <p>© 2026 精油能量圖譜 · 靈境智造 Intelliverse Studio</p>
    <p style="font-size:12px;color:#999;margin-top:8px;">本站資訊僅供教育參考，不取代醫療建議。作者：<a href="author-yuling.html" style="color:#8B6F3E;">玉玲（IFA 國際認證芳療師）</a>｜<a href="references.html" style="color:#8B6F3E;">引用來源</a></p>
  </div>
</footer>

<script>
(function(){{
  var feelingTab=document.getElementById('tab-feeling'),envTab=document.getElementById('tab-env');
  var gridF=document.getElementById('grid-feeling'),gridE=document.getElementById('grid-env');
  var cards=document.querySelectorAll('.blend-card'),empty=document.getElementById('result-empty');
  function setMode(m){{
    var f=m==='feeling';
    gridF.style.display=f?'grid':'none';gridE.style.display=f?'none':'grid';
    feelingTab.style.background=f?'#88BC88':'#fff';feelingTab.style.color=f?'#fff':'#5A7A6A';
    envTab.style.background=f?'#fff':'#88BC88';envTab.style.color=f?'#5A7A6A':'#fff';
    showCard(-1);
  }}
  function showCard(idx){{
    var any=false;
    cards.forEach(function(c){{
      var on=parseInt(c.getAttribute('data-idx'))===idx;
      c.style.display=on?'block':'none';if(on)any=true;
    }});
    empty.style.display=any?'none':'block';
    document.querySelectorAll('.scenario-btn').forEach(function(b){{
      var on=parseInt(b.getAttribute('data-idx'))===idx;
      b.style.borderColor=on?'#88BC88':'var(--border)';
      b.style.background=on?'#EEF5EE':'#fff';
      b.style.boxShadow=on?'0 4px 12px rgba(136,188,136,0.25)':'none';
    }});
    if(idx>=0){{document.getElementById('result').scrollIntoView({{behavior:'smooth',block:'nearest'}});}}
  }}
  feelingTab.onclick=function(){{setMode('feeling');}};
  envTab.onclick=function(){{setMode('env');}};
  document.querySelectorAll('.scenario-btn').forEach(function(b){{
    b.onclick=function(){{showCard(parseInt(b.getAttribute('data-idx')));}};
  }});
}})();
</script>
</body>
</html>'''
    OUT.write_text(html, encoding='utf-8')
    print(f'✓ 產出 {OUT}（{len(html)} chars，{len(BLENDS)} 個情境配方）')


if __name__ == '__main__':
    build()
