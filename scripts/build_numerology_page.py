# -*- coding: utf-8 -*-
"""
build_numerology_page.py — 產生「生命靈數」互動頁 html-source/numerology.html

輸入西元生日 → 算主命數、生日數、天賦數、星座數、九宮格連線、空缺數，
再對應精油芳療方向 + NLP 表象系統測驗 + 人際合盤。

內容根據畢達哥拉斯生命靈數（資料整理自 ifreesite.com/numerology 公開教學，
經改寫為本站語氣），精油對應結合本站 46 支精油指南。
全程不作醫療宣稱：占數為自我探索娛樂，精油為情緒陪伴 / 香氛儀式。
"""
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent))
from build_blend_page import SLUG  # noqa  46 精油 → slug

OUT = Path(r'C:\Users\User\Desktop\essential-oil-guide\html-source\numerology.html')


def otag(name):
    slug = SLUG.get(name, '')
    href = '/%s/' % slug if slug else '#'
    return '<a href="%s" class="num-oil">%s</a>' % (href, name)


def ochips(names):
    return ''.join(otag(n) for n in names)


# ── 主命數 1-9（性格／天賦／職涯／愛情／精油方向）──────────────────
# 文字整理自畢達哥拉斯占數傳統，改寫為本站語氣
LIFEPATH = {
    1: dict(
        title='開創數', tree='開創數', emoji='👑',
        keyword='獨立 · 領導 · 行動',
        good='獨立、積極、有創意、天生的領袖，衝勁十足、精力充沛，點子多、勇於嘗試。',
        bad='強勢、主觀、急躁，事情一出錯容易發火；在感情裡有時顯得太直接、不夠浪漫。',
        desc='你天生熱愛獨立，不喜歡依賴別人、也不喜歡別人依賴你。看事情習慣非黑即白，'
             '所以決定下得快，是當領導的料；但也容易走極端。你勇於改變、勇於開創，'
             '常有異於常人的想法，這正是你最容易發光、最容易成功的地方。',
        career='創業者、主管、業務、開創型的角色——只要能「自己做主、開疆闢土」你就活得起勁。',
        love='你愛得直接、忠誠，但步調快、要求高。記得在親密關係裡放慢一點、多一點溫柔。',
        oils=['乳香', '真正薰衣草', '大西洋雪松'],
        oilwhy='你的能量很衝、step 很快，木質與薰衣草系的沉穩香氣，最適合在你全力衝刺後，'
                '幫自己踩個剎車、把呼吸放長、好好沉澱。'),
    2: dict(
        title='協調數', tree='協調數', emoji='🤝',
        keyword='敏感 · 合作 · 體貼',
        good='敏感、體貼、善於分工合作，是天生的外交家與公關人才，溫和親切、重視群體。',
        bad='優柔寡斷、情緒易受他人影響，不擅長獨處，遇事不容易自己做決定。',
        desc='你很注意細節，分析與辨識能力一流，喜歡發問與思考。你不愛帶頭主導，'
             '寧可與人合作、等別人邀你加入。你對感情的話題特別敏感，是團體裡那個'
             '默默把氣氛潤滑好的人——你的價值，常常在「成全別人」裡發光。',
        career='諮詢師、人資、行政、協調與輔佐型角色——你最擅長讓一個團隊順順地運轉。',
        love='你溫柔、願意配合，但別一味退讓。練習把自己的需要也說出來，關係才會平衡。',
        oils=['佛手柑', '天竺葵', '岩蘭草'],
        oilwhy='你心思細、容易被別人的情緒牽動，佛手柑與天竺葵幫你穩住起伏，'
                '岩蘭草則像一條根，把你拉回自己的重心、不再隨風搖。'),
    3: dict(
        title='創意數', tree='繽紛之樹', emoji='🎨',
        keyword='表達 · 樂觀 · 社交',
        good='聰明機警、有創意、多有藝術天份，活潑有趣、表達力強，是天生的開心果。',
        bad='有點任性、愛面子、容易好高騖遠，是所有數字裡最固執的一群。',
        desc='你很在意形象與外觀，喜歡照自己的喜好行事。你長袖善舞、喜歡逗人開心，'
             '常把歡樂帶給大家。一旦遇到心動的對象就容易整個陷進去。從事創意工作的時候，'
             '是你最快樂、最像自己的時候。',
        career='藝術創作、設計、行銷、表演——任何能「秀出創意、感染別人」的舞台都適合你。',
        love='你愛得熱烈又浪漫，但容易三分鐘熱度。找一個欣賞你才華、陪你長跑的人最幸福。',
        oils=['甜橙', '橙花', '佛手柑'],
        oilwhy='柑橘與橙花的明亮花果香，剛好呼應你愛玩、愛美、愛表達的天性，'
                '在你靈感卡住或情緒上上下下時，幫你重新點亮那份快樂。'),
    4: dict(
        title='務實數', tree='穩重之樹', emoji='🧱',
        keyword='秩序 · 紀律 · 安全感',
        good='忠誠、有條理、組織力強、目光敏銳，能迅速抓到重點，是天生的建設好手。',
        bad='固執、不易妥協、容易緊張，安全感不足、不敢冒險，常因此讓機會溜走。',
        desc='你的安全感意識非常強。你不一定要從零創造，但很會從既有的東西裡選出最好的、'
             '把它做到極致。你比較適合在穩定的結構裡發揮，受到挑戰時會高度自我防衛、變得很固執。'
             '你的踏實，是很多人安心的依靠。',
        career='財會、工程師、專案管理、品管——需要「穩、準、有系統」的位置非你莫屬。',
        love='你重視承諾與穩定，是可靠的伴侶。練習對變化多一點彈性，關係會更輕鬆。',
        oils=['真正薰衣草', '葡萄柚', '乳香'],
        oilwhy='你容易把自己繃得很緊，薰衣草與乳香幫你鬆開肩膀、放下控制，'
                '葡萄柚的輕快則替你打開一點縫隙，讓新的可能透進來。'),
    5: dict(
        title='自由數', tree='自由數', emoji='🦋',
        keyword='自由 · 多變 · 善溝通',
        good='聰穎、適應力強、學得快，能言善道、口才一流，熱情豪爽、崇尚自由。',
        bad='博而不精、持續力差，不喜歡被束縛，容易放縱，有時口無遮攔得罪人。',
        desc='你對任何侵犯自由的事都很敏感。你口齒伶俐、很容易取得別人的信任，'
             '傳達訊息又清楚又簡潔，特別適合銷售、傳播、公關這類舞台。感情上，'
             '你需要愛卻又怕被綁住——學會在自由與承諾之間找到平衡，是你這輩子的功課。',
        career='業務、自由工作者、行銷、傳播——能到處跑、不斷接觸新事物的工作最適合你。',
        love='你需要空間、討厭被管。找一個同樣愛自由、又願意陪你定下來的人最合拍。',
        oils=['岩蘭草', '廣藿香', '大西洋雪松'],
        oilwhy='你像風一樣停不下來，岩蘭草、廣藿香這些厚實的大地系香氣，'
                '像錨一樣幫你紮根、收斂，讓自由不變成漂泊。'),
    6: dict(
        title='關懷數', tree='關懷數', emoji='💗',
        keyword='責任 · 奉獻 · 同理',
        good='穩定、可信賴、情感細膩、有正義感，擅長交際、樂於助人，重承諾與責任。',
        bad='容易缺乏自信、好強爭辯，付出不求回報時容易讓自己受傷。',
        desc='你天生就想「修補東西、解決問題」，對別人的痛苦感同身受，常常一頭栽進別人的問題裡。'
             '你勇於扛責任，即使超出能力範圍也在所不辭——因為「被需要」是你的生命補給。'
             '把這份熱誠用在志工、教育、照顧上，你會找到最深的滿足。',
        career='護理師、心理師、教育者、社福——任何能「照顧人、療癒人」的角色都是你的天命。',
        love='你照顧得無微不至，但小心別把責任全扛在自己身上。讓對方也有機會疼你。',
        oils=['玫瑰', '天竺葵', '佛手柑'],
        oilwhy='你總是先想到別人，玫瑰與天竺葵這些開「心輪」的花香，'
                '提醒你也要好好疼自己；佛手柑則幫你在付出與耗竭之間，守住一條界線。'),
    7: dict(
        title='探究數', tree='智慧之樹', emoji='🔭',
        keyword='內省 · 邏輯 · 真理',
        good='善於鑽研、追求真理，直覺敏銳、遇事理智，能一眼看穿問題所在。',
        bad='有時顯得冷漠、不夠圓滑，不容易被討好，太容易到手的東西反而不珍惜。',
        desc='你天生好奇，不看事情的表面，喜歡不斷發問、追究背後的真相。你可能是所有數字裡'
             '最講邏輯的——思考都建立在你確知的事實上，能快速分析情勢、做出務實的判斷。'
             '你從不怕說出誠實的意見，這份清醒，是你最珍貴的天賦。',
        career='科研、工程、寫作、諮商——需要「深入鑽研、獨立思考」的領域最能讓你發揮。',
        love='你理性、慢熱，習慣用腦袋多過用心。練習偶爾走出頭腦，讓對方真正靠近你。',
        oils=['乳香', '檀香', '橙花'],
        oilwhy='你常常住在腦子裡，乳香與檀香的沉靜樹脂香，是千年來靜心冥想的語言，'
                '幫你從思緒裡安定下來；橙花則溫柔地，把你從頭腦帶回心。'),
    8: dict(
        title='權威數', tree='豐盛之樹', emoji='⛰️',
        keyword='企圖 · 商業 · 行動力',
        good='忠貞、堅定、誠懇，有商業頭腦、行動力強，獨具慧眼、即知即行。',
        bad='容易太物質、心高氣傲，對喜歡的東西有異常執著，面對衝突時會勉強自己。',
        desc='你一眼就能看出哪些人事物有潛力，常常不為什麼就主動幫別人發展。你具備 1 的領導特質，'
             '會驅使自己追求金錢與獨立，而且目標往往遠超實際需求。有趣的是，你個性剛強，'
             '外表卻常像貓一樣溫順——你的強出頭，多半是為了別人。你天生就是生意人。',
        career='企業經營、管理職、投資——需要「掌舵、做大、創造價值」的位置最適合你。',
        love='你企圖心強、習慣掌控。記得別讓事業與成就，壓過了關係裡的溫度與柔軟。',
        oils=['依蘭', '天竺葵', '甜橙'],
        oilwhy='你習慣繃緊、追求成就，依蘭與天竺葵的甜美花香幫你卸下盔甲、柔軟下來，'
                '甜橙則提醒你：豐盛，也包括允許自己放鬆與享受。'),
    9: dict(
        title='智慧數', tree='理想之樹', emoji='🌈',
        keyword='博愛 · 想像 · 靈性',
        good='多才多藝、想像力豐富，充滿生命力與同理心，隨機應變、見招拆招。',
        bad='有時不夠務實、意志不夠堅定，想像太奔放會變成天馬行空，也容易被人利用。',
        desc='你是天生的夢想家，相信天下沒有不可能的事——因為你很早就發現自己學什麼都快。'
             '你的夢想與計畫常像電影情節，不受任何限制。你對別人的需求極度敏感，覺得助人是'
             '義不容辭；但要小心，別總是扛下超過自己的重擔，也別忘了把愛留一些給自己。',
        career='非營利組織、講師、心理輔導、創作——能「啟發人、服務更大的理想」最讓你滿足。',
        love='你浪漫、富同情心，容易為愛奉獻。記得感情是雙向的，也要讓自己被好好接住。',
        oils=['迷迭香', '大西洋雪松', '黑胡椒'],
        oilwhy='你常飄在理想的雲端，迷迭香幫你聚焦、清明，雪松與黑胡椒則像大地與火，'
                '把你的夢想穩穩地接回地面、化成行動。'),
}

# ── 連線（八主線 + 四副線）────────────────────────────────────
# nums, 名稱, 正面天賦, 負面提醒, 類型
LINES = [
    ([1, 2, 3], '藝術線', '獨立性強、富藝術與創作天份，雙手靈巧，帶著天生的領導力與審美感。',
     '少了 7 時容易過於自我、太理想化，施與受之間要學著拿捏。', 'main'),
    ([4, 5, 6], '組織線', '組織力強、做事標準高，善於解決問題、確保品質——天生的執行高手。',
     '太追求完美時容易變成潔癖與龜毛，記得對自己和別人鬆一點。', 'main'),
    ([7, 8, 9], '貴人線', '心智判斷敏銳、追求權力又人緣好，一路上容易遇到貴人提攜。',
     '少了 5 時容易變「懶人線」，習慣要別人相助，要練習自己動起來。', 'main'),
    ([1, 4, 7], '運動線', '務實穩定、愛打拼，充滿精力與勇氣去衝鋒陷陣，重視經濟上的安全感。',
     '少了 9 時容易太現實、太拜金，別讓賺錢蓋過了生活的其他風景。', 'main'),
    ([2, 5, 8], '感情線', '感情豐富、善於表達、文筆好、重朋友，有用文字與話語感動人的能力。',
     '有 7 時容易口直心快、話太多，也要記得家人和朋友一樣重要。', 'main'),
    ([3, 6, 9], '智慧線', '智商高、擅長思考、學習力強，常常替人出主意、指點迷津。',
     '少了 5 時容易愛作白日夢，該行動的時候還在空想，要把點子落地。', 'main'),
    ([1, 5, 9], '事業線', '企圖心強、有經營自己事業的決心，不工作會渾身不對勁，是天生的拚命三郎。',
     '太投入時容易變工作狂、忽略家庭，記得替生活留白。', 'main'),
    ([3, 5, 7], '人緣線', '自帶魅力、溝通力強、受人歡迎，能看穿別人真正的需要，把事情講得淺顯動人。',
     '好奇心太強時容易愛八卦、論人是非，把這份敏銳用在理解、別用在閒話。', 'main'),
    ([2, 4], '靈巧線', '應變能力強、舉一反三、見機行事，做事說話都靈活伶俐。',
     '用偏了會變成過度算計、心思太重，記得真誠待人最省力。', 'sub'),
    ([2, 6], '和平線', '具平等心、熱心助人、講求公平正義，是團體裡的潤滑劑與和事佬。',
     '少了 9 時要小心別淪為「利用他人」，付出與索取要拿捏。', 'sub'),
    ([6, 8], '誠懇線', '待人親切誠實、樂於幫人解決問題，很適合服務業與需要信任的工作。',
     '少了 5 時容易把真心話藏起來，練習坦白說出自己的感受。', 'sub'),
    ([4, 8], '穩定線', '四平八穩、做事負責又有效率，是團隊裡的工作模範生。',
     '少了 5 時內心容易缺乏安全感，記得安全感要自己給，不必凡事求穩。', 'sub'),
]

# ── 空缺數 0-9（人生功課 + 練習 + 精油方向）────────────────────
MISSING = {
    0: dict(theme='奉獻與格局',
            text='你擁有很多好機會，個人成就也不難得到；但真正的幸福，要在「為更大的群體付出」之後才嚐得到。'
                 '功課是放下太以自我為中心的眼光，對任何人事都不存偏見，你會發現世界回饋給你的更寬廣。',
            practice='每週做一件「不為自己、純粹利他」的小事——一句鼓勵、一次幫忙、一筆小捐款。',
            oils=['佛手柑', '乳香', '甜橙']),
    1: dict(theme='獨立與自我肯定',
            text='你的功課是學會獨立、相信自己的判斷。你常遇到「自己的想法和別人的期待不一樣」的拉扯，'
                 '要經過一番掙扎才認得出自己的意志力。別盲目從眾，肯定自己，你會長成最有原創性的那個你。',
            practice='每天替自己做一個小決定並堅持到底，從小事開始累積「我可以」的信心。',
            oils=['甜羅勒', '黑胡椒', '佛手柑']),
    2: dict(theme='安定與信任情緒',
            text='你很敏感，太懂別人對你的期待，於是常壓抑自己、怕被議論。你的高敏也是天賦——'
                 '別人還沒開口，你就讀懂了他的心。功課是別被情緒帶著走，學會安頓自己那份纖細。',
            practice='情緒上來時，先深呼吸三次、寫下來，再決定要不要反應。給自己一點緩衝。',
            oils=['真正薰衣草', '佛手柑', '香蜂草']),
    3: dict(theme='表達與自我接納',
            text='你是自己最嚴厲的批評者，做事前先懷疑自己、做完又狠狠檢討，常把真心藏在玩笑底下。'
                 '功課是把真實的自己帶出來——你的創意，絕對勝過你對自己的挑剔。',
            practice='找一種表達出口：寫作、畫畫、唱歌、跳舞都好，讓情緒有地方流動。',
            oils=['甜橙', '茉莉', '佛手柑']),
    4: dict(theme='踏實與組織',
            text='你容易少了一點組織與紀律，有時會幻想一些不切實際的計畫。功課是學會分辨「可能與不可能」，'
                 '把環境與步驟理清楚。為人生打一個長久的地基，需要的是毅力和持續的努力，不是一夜致富。',
            practice='用清單與行事曆把目標拆成小步驟，每天完成一格，讓踏實變成習慣。',
            oils=['岩蘭草', '廣藿香', '大西洋雪松']),
    5: dict(theme='彈性與承諾',
            text='你可能有兩種極端：一種像滾石，什麼都想試、靜不下來；一種剛好相反，害怕改變、緊抓過去。'
                 '功課是在「自由」與「穩定」之間找到中道——維持長久的關係與計畫，遇到困難時別輕易放手。',
            practice='挑一件事或一段關係，刻意練習「撐過想逃的那一刻」，為它留下根。',
            oils=['葡萄柚', '胡椒薄荷', '迷迭香']),
    6: dict(theme='柔軟與感恩',
            text='你的理想可能太高、太硬，讓自己和別人都辛苦，有時看不見生活裡的美。功課是放下'
                 '「非黑即白」的標準，多一點感謝與彈性——眼前的障礙鬆開了，更寬廣的視野才進得來。',
            practice='每天睡前寫下三件「值得感謝的小事」，練習把眼光從不足移到豐盛。',
            oils=['玫瑰', '天竺葵', '橙花']),
    7: dict(theme='信任與直覺',
            text='你對還沒被證明的事容易懷疑，尤其是心靈、直覺這類「不合邏輯」的部分，也因此壓抑了'
                 '內在自然的柔軟。功課是找到一套能讓你安心的信念，明白：感官能掌握的，只是生活的一小部分。',
            practice='給自己一段不分析、只感受的時間——散步、聽音樂、靜坐，練習相信當下。',
            oils=['乳香', '檀香', '岩蘭草']),
    8: dict(theme='平衡與豐盛',
            text='你可能會為了賺錢或掌權而拚到失衡，對財富的渴望淹過了其他需求，最後換來孤獨。'
                 '功課是把物質放回它該有的位置——錢是工具不是目的，內在與關係的富足同樣重要。',
            practice='每週留一段「不談工作、不看數字」的時間，純粹陪伴自己與在乎的人。',
            oils=['甜橙', '廣藿香', '乳香']),
    9: dict(theme='給予與連結',
            text='你會面臨一場心靈的考驗，慢慢明白「人活著不是只靠麵包」。功課是在物質與精神之間取得平衡——'
                 '與其當一座只進不出的湖，不如做一條涓涓不息的河，把養分不斷帶給身邊的人。',
            practice='把你擅長的事分享出去——教一個人、寫一篇心得、做一次志工，讓愛流動起來。',
            oils=['乳香', '玫瑰', '檀香']),
}

# ── 星座 → 星座數（牡羊=1...雙魚reduce）。(月,日起,日訖,名,數)────
ZODIAC = [
    (3, 21, 4, 19, '牡羊座', 1), (4, 20, 5, 20, '金牛座', 2), (5, 21, 6, 21, '雙子座', 3),
    (6, 22, 7, 22, '巨蟹座', 4), (7, 23, 8, 22, '獅子座', 5), (8, 23, 9, 22, '處女座', 6),
    (9, 23, 10, 22, '天秤座', 7), (10, 23, 11, 21, '天蠍座', 8), (11, 22, 12, 21, '射手座', 9),
    (12, 22, 1, 19, '摩羯座', 1), (1, 20, 2, 18, '水瓶座', 2), (2, 19, 3, 20, '雙魚座', 3),
]

# ── NLP 表象系統測驗（5 題，選項對 V/A/K/AD）─────────────────
NLP_Q = [
    ('學一樣新東西時，你最想要——',
     ['看圖解、影片，眼睛跟著畫面走', '聽人講解、用聽的把它記起來',
      '直接動手做做看，邊做邊學', '先搞懂它背後的邏輯與架構']),
    ('回想一段美好回憶，最先浮現的是——',
     ['當時的畫面與景象', '當時的聲音、音樂或對話',
      '身體的感受、溫度與觸感', '事情的來龍去脈與意義']),
    ('什麼最容易說服你？對方——',
     ['給你看實際的樣子、數據或圖', '語氣誠懇、條理分明地說給你聽',
      '讓你親自體驗、真的感受到', '提出嚴謹的分析與證據']),
    ('形容一個你喜歡的人，你會說——',
     ['「看起來很順眼、很亮眼」', '「跟他聊天很合拍、很對頻」',
      '「在他身邊很安心、很踏實」', '「他的想法很有深度」']),
    ('壓力很大時，最快讓你放鬆的是——',
     ['看美景、整理一下視覺環境', '聽音樂、或找人說說話',
      '泡澡、按摩、被好好抱一下', '一個人安靜地把事情想清楚']),
]
NLP_RESULT = {
    'V': dict(name='視覺型 V', icon='👁️',
              desc='你靠「看見」理解世界，說話偏快、腦中常有畫面。用圖表、心智圖、影片學習最有效率；'
                   '溝通時，給對方看實例會比光用講的更有說服力。',
              oils=['檸檬', '葡萄柚'],
              oilwhy='明亮清透的柑橘調，呼應你重視清晰與畫面的天性，幫你保持思緒乾淨俐落。'),
    'A': dict(name='聽覺型 A', icon='👂',
              desc='你對「聲音與語氣」特別敏感，有節奏感、重視對話。用聽的（錄音、講給自己聽、討論）'
                   '學最快；環境太吵會讓你分心。',
              oils=['天竺葵', '真正薰衣草'],
              oilwhy='平衡而柔和的花草調，陪你穩住內在的節奏，在喧鬧裡找回安靜。'),
    'K': dict(name='觸覺型 K', icon='🤲',
              desc='你用「身體與感受」記住事情，重視實際體驗與接觸，步調沉穩。動手做、實作、'
                   '走動式的學習最適合你。',
              oils=['檀香', '廣藿香', '薑'],
              oilwhy='厚實溫暖的木質與辛香，給你最需要的踏實感與安全感。'),
    'AD': dict(name='自語型 AD', icon='💭',
               desc='你理性、愛分析，凡事先在心裡想清楚邏輯才動。喜歡獨立思考、結構化的資訊，'
                    '討厭被催促。',
               oils=['迷迭香', '胡椒薄荷', '乳香'],
               oilwhy='清晰專注的草本與樹脂，陪你深度思考、把複雜的事一層層理順。'),
}

# ── 人際合盤（主命數相處建議）─────────────────────────────
COMPAT = {
    1: '和 2、6、8 最合拍——他們懂得配合、包容你的衝勁；遇到另一個 1 容易爭主導，記得輪流當領導。',
    2: '和 1、8、6 互補——讓有主見的人帶，你負責協調潤滑；但別忘了把自己的需要也說出來。',
    3: '和 5、7、9 來電——都是聰明有想法的組合，聊不完；但都怕無聊，要一起經營長期的承諾。',
    4: '和 2、8、6 穩定——務實的你需要懂你重視安全感的人，對方的彈性能鬆開你的固執。',
    5: '和 3、7、9 自由——彼此都愛新鮮、不黏膩；但要練習為這段關係，踩下承諾的根。',
    6: '和 2、9、1 溫暖——你的照顧遇上懂得回應的人最幸福；小心別把責任全扛在自己身上。',
    7: '和 3、5、9 深刻——心靈與智性的交流讓你著迷；記得偶爾走出腦袋，讓對方靠近你的心。',
    8: '和 2、4、1 互助——你的企圖心需要穩定的後盾；別讓事業與掌控，壓過了感情的溫度。',
    9: '和 3、6、7 投緣——理想主義者遇到懂你的人會發光；但要學會把愛，也留一些給自己。',
}

# ── 代表顏色（脈輪色系；整理自《幸福密碼》靈學表 + 流年顏色表）──
COLOR = {
    1: ('#D64545', '紅'), 2: ('#E2872E', '橙'), 3: ('#E5BE2E', '黃'),
    4: ('#5FA85F', '綠'), 5: ('#3F87C9', '藍'), 6: ('#5B6FB5', '靛'),
    7: ('#8A5FB5', '紫'), 8: ('#D87FA8', '粉紅'), 9: ('#C9A93F', '金'),
}

# ── 能量原型（《幸福密碼》密碼身份；趣味象徵）──
ARCHETYPE = {
    1: '皇宮貴族', 2: '外圍貴族', 3: '有錢人', 4: '讀書人', 5: '武將',
    6: '演員', 7: '巫女', 8: '商人', 9: '出家人',
}

# ── 流年運（個人年 1-9；主題＋香氣方向）──
# 計算：出生月＋出生日＋當年年份，各位數相加縮減成個位（前端用瀏覽器當下年份，每年自動更新）
YEAR_FLOW = {
    1: dict(name='開始年 · 播種', text='新的九年循環從這裡起跑——適合啟動新計畫、換跑道、立新目標。種子先種下，後面幾年才有得收。別怕從零開始。',
            oils=['迷迭香', '甜羅勒']),
    2: dict(name='關係年 · 等待', text='步調放慢的一年，重點在「人」——合作、感情、耐心經營。事情不一定快，但關係會加深。學會等待與配合。',
            oils=['天竺葵', '玫瑰']),
    3: dict(name='精彩年 · 表達', text='最閃亮、最好玩的一年——創意、社交、戀愛、自我表達都旺。把才華秀出來，盡情享受這份熱鬧。',
            oils=['甜橙', '佛手柑']),
    4: dict(name='築基年 · 落實', text='踏實打地基的一年——把計畫落地、把該做的紀律做好。會比較辛苦、瑣碎，但穩穩努力就會長出底氣。',
            oils=['岩蘭草', '大西洋雪松']),
    5: dict(name='變動年 · 自由', text='充滿變化與機會的一年——可能換環境、多了選擇、想往外跑。擁抱改變、別怕轉彎，但別衝過頭。',
            oils=['葡萄柚', '胡椒薄荷']),
    6: dict(name='責任年 · 愛與家', text='關於家庭、責任與愛的一年——照顧人也被照顧，適合安定、承諾、把家經營好。記得也留點愛給自己。',
            oils=['真正薰衣草', '天竺葵']),
    7: dict(name='沉澱年 · 內省', text='向內走的一年——適合休息、學習、沉澱、想清楚。外在可能慢下來，那是讓你充電、看見自己的時候。',
            oils=['乳香', '檀香']),
    8: dict(name='收成年 · 豐盛', text='努力開花結果的一年——事業、名利、成就容易豐收，也適合談錢、升遷、做大。穩穩收割前幾年的耕耘。',
            oils=['廣藿香', '甜橙']),
    9: dict(name='整理年 · 放下', text='一個循環的結尾——適合結束、清理、放下不再適合的人事物，為下一輪空出位置。先清空，才有新的進來。',
            oils=['乳香', '永久花']),
}

# ── 緣分合盤（兩人主命數「相差」→ 緣分類型；整理自《幸福密碼》挑戰指數）──
# diff: 0-8（兩人主命數差的絕對值）。score 沿用書中分數，純趣味參考。
COMPAT_DIFF = {
    0: ('靈魂伴侶', 85, '你們像同一種人，懂彼此的節奏，自在又契合；但太像也要小心一起鑽牛角尖。'),
    1: ('夢中情人', 80, '互相吸引、充滿想像，是會讓你心動的類型，相處有種剛剛好的甜。'),
    2: ('兄弟姊妹', 75, '像家人一樣自在、無話不談，沒有壓力——是能長久的那種陪伴。'),
    3: ('比例懸殊', 50, '兩人步調差得比較多，需要多一點耐心與磨合，但差異也能互補。'),
    4: ('知己之交', 70, '聊得深、懂彼此，是難得的靈魂知己，淡淡的卻很長久。'),
    5: ('前世的功課', 45, '像來還願的緣分，相處容易碰到要一起學的課題；走得過會很深。'),
    6: ('互相依戀', 95, '最有默契、最黏的一對，彼此離不開——緣分裡分數最高的組合。'),
    7: ('烈火情人', 60, '一見就來電、激情濃烈，火花十足，但也需要練習把熱情變成穩定。'),
    8: ('莫名的吸引', 55, '說不上理由就是被吸引，需要時間慢慢讀懂對方，磨合期長一點。'),
}

# ── 四階段大運（高峰期 Pinnacle；每個人生階段被哪個數字能量主導）──
# 計算用標準西方數字學：P1=月+日、P2=日+年、P3=P1+P2、P4=月+年（皆先縮減）
# 階段年齡：第一階段 0~(36-主命數)，之後每 9 年一段
PINNACLE_THEME = {
    1: '開創與獨立——適合啟動、闖蕩、為自己做主的階段。',
    2: '關係與合作——學習協調、耐心、與人共事的階段。',
    3: '表達與創造——發揮才華、社交、享受生活的階段。',
    4: '築基與務實——踏實工作、建立秩序與安全感的階段。',
    5: '變化與自由——擁抱改變、嘗試、拓展視野的階段。',
    6: '責任與愛——關於家庭、照顧、承擔與付出的階段。',
    7: '內省與智慧——適合學習、沉澱、向內探索的階段。',
    8: '成就與豐盛——衝刺事業、累積實力與資源的階段。',
    9: '圓滿與付出——服務、放下、整合與利他的階段。',
}

# ── 組合數（同一主命數的不同「總和」帶來的性格差異）──
# key = 生日全部數字相加的「總和兩位數」（先天總和），value = 性格微調
COMBO = {
    10: '最純粹的 1——0 放大了 1 的力量，獨立、開創、領導性都最鮮明，是天生的開路先鋒。',
    19: '1 與 9 的組合——理想色彩濃，是有願景、想為更大目標而開創的領袖型。',
    28: '經由 2 與 8——比一般 1 更懂合作與經營，領導裡帶著手腕與商業頭腦。',
    37: '經由 3 與 7——創意加上思辨，用點子和深度去開創，獨來獨往也自得其樂。',
    46: '經由 4 與 6——務實又有責任感的開創者，腳踏實地地當領導，讓人安心。',
    11: '大師數！11 是高敏感與直覺的「靈性數」，協調力再加上強烈第六感，天賦與壓力都加倍。',
    20: '最純粹的 2——0 放大了協調與敏感，是極致的協調者與傾聽者。',
    29: '經由 2 與 9——同理心特別強，溫柔裡帶著理想，容易為別人付出。',
    38: '經由 3 與 8——協調力配上表達與企圖，擅長公關、把人與資源連起來。',
    47: '經由 4 與 7——細膩又務實理性，是安靜可靠、把細節顧好的協調者。',
    12: '經由 1 與 2——創意裡有開創也有合作，點子比較容易落地。',
    21: '經由 2 與 1——表達中帶著主見與圓融，能說也能協調。',
    30: '最純粹的 3——0 放大了表達與創意，是天生的表演者與開心果。',
    39: '經由 3 與 9——創意加理想，想像力豐富，是有靈魂的創作者。',
    48: '經由 4 與 8——少見地把創意與務實、商業結合，能把才華變成事業。',
    13: '經由 1 與 3——務實裡有開創與創意，是能把點子真正做出來的實踐者。',
    22: '大師數！22 是「建築師數」，務實能量放到最大，有把宏大夢想蓋成真的能力。',
    31: '經由 3 與 1——表達加開創的務實者，做事有想法、不死板。',
    40: '最純粹的 4——0 放大了秩序與務實，是極致的組織者與建設好手。',
    14: '經由 1 與 4——自由裡有開創與紀律，是能管好自己的冒險家。',
    23: '經由 2 與 3——溝通力滿點，協調加表達，是天生的公關與業務。',
    32: '經由 3 與 2——表達加協調的自由人，很會帶氣氛、炒熱場子。',
    41: '經由 4 與 1——務實又獨立的冒險者，愛自由但不亂來。',
    15: '經由 1 與 5——照顧裡有開創與自由，是不被責任綁死的溫暖領導。',
    24: '經由 2 與 4——協調加務實，把家和團隊顧得穩穩的可靠照顧者。',
    33: '大師數！33 是「大愛數」，愛與奉獻放到最大，是療癒者與老師的能量。',
    42: '經由 4 與 2——務實又體貼，默默把身邊的人照顧好。',
    16: '經由 1 與 6——思辨裡有開創與責任，是有主見也有溫度的探究者。',
    25: '經由 2 與 5——敏感加靈活，直覺敏銳、看人很準。',
    34: '經由 3 與 4——創意加務實，把想法研究透徹再落地。',
    43: '經由 4 與 3——務實的思考者，鑽研中帶點創意。',
    17: '經由 1 與 7——企圖心配上獨立與思辨，是有遠見的經營者。',
    26: '經由 2 與 6——商業頭腦加上協調與責任，是顧及人情的領導者。',
    35: '經由 3 與 5——表達加靈活，擅長行銷、把生意做活。',
    44: '大師數！44 是「實業數」，務實與企圖放到最大，有把事業版圖蓋起來的耐力。',
    18: '經由 1 與 8——理想裡有開創與企圖，是想把大事做成的理想家。',
    27: '經由 2 與 7——同理加智慧，是溫柔又有深度的療癒型。',
    36: '經由 3 與 6——創意加愛，用才華服務人、充滿溫度。',
    45: '經由 4 與 5——務實加靈活，能把博愛落實成具體行動的理想家。',
}


def build_data():
    """組成給前端 JS 用的 JSON（精油已轉成連結 HTML）"""
    lifepath = {}
    for n, d in LIFEPATH.items():
        lifepath[n] = dict(
            title=d['title'], tree=d['title'], emoji=d['emoji'], keyword=d['keyword'],
            good=d['good'], bad=d['bad'], desc=d['desc'], career=d['career'], love=d['love'],
            oilsHtml=ochips(d['oils']), oilwhy=d['oilwhy'], compat=COMPAT[n],
            color=COLOR[n][0], colorName=COLOR[n][1], archetype=ARCHETYPE[n])
    year_flow = {n: dict(name=d['name'], text=d['text'], oilsHtml=ochips(d['oils']))
                 for n, d in YEAR_FLOW.items()}
    compat_diff = {k: dict(name=v[0], score=v[1], text=v[2]) for k, v in COMPAT_DIFF.items()}
    lines = [dict(nums=l[0], name=l[1], pos=l[2], neg=l[3], type=l[4]) for l in LINES]
    missing = {}
    for n, d in MISSING.items():
        missing[n] = dict(theme=d['theme'], text=d['text'], practice=d['practice'],
                          oilsHtml=ochips(d['oils']))
    zodiac = [dict(m1=z[0], d1=z[1], m2=z[2], d2=z[3], name=z[4], num=z[5]) for z in ZODIAC]
    nlp_q = [dict(q=q, opts=opts) for q, opts in NLP_Q]
    nlp_res = {}
    for k, d in NLP_RESULT.items():
        nlp_res[k] = dict(name=d['name'], icon=d['icon'], desc=d['desc'],
                          oilsHtml=ochips(d['oils']), oilwhy=d['oilwhy'])
    return dict(lifepath=lifepath, lines=lines, missing=missing,
                zodiac=zodiac, nlpQ=nlp_q, nlpRes=nlp_res,
                yearFlow=year_flow, compatDiff=compat_diff,
                pinnacle=PINNACLE_THEME, combo=COMBO)


# ── 數字意義速查（靜態，給 SEO/AI 爬蟲）─────────────────────
NUM_MEANING = [
    (1, '個性化、獨立、成就'), (2, '關係、合作、協調'), (3, '表達、歡樂、創意'),
    (4, '限制、秩序、務實'), (5, '自由、變化、溝通'), (6, '平衡、責任與愛'),
    (7, '分析、探究、智慧'), (8, '權力、物質、企圖'), (9, '博愛、理想、人道'),
]


# ── 頁面骨架（plain string；用 __PLACEHOLDER__ 注入，避開 f-string 大括號）──
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
      <li><a href="blend.html">調配精油</a></li>
      <li><a href="numerology.html" class="active">生命靈數</a></li>
      <li><a href="aromatherapy.html">芳療應用</a></li>
      <li><a href="safety.html">安全指南</a></li>
    </ul></nav>
    <button class="menu-toggle">☰</button>
  </div>
</header>'''

DESC = ('輸入西元生日，免費計算你的生命靈數主命數、生日數、天賦數、星座數、九宮格連線與空缺數，'
        '並對應精油芳療方向與 NLP 學習風格。源自畢達哥拉斯占數，結合芳香療法的自我探索工具。')


def build():
    data_json = json.dumps(build_data(), ensure_ascii=False)
    meaning_rows = ''.join(
        '<tr><td style="padding:8px 12px;border:1px solid #E5D9C0;text-align:center;font-weight:800;color:#8B6F3E;">%d</td>'
        '<td style="padding:8px 12px;border:1px solid #E5D9C0;">%s</td></tr>' % (n, t)
        for n, t in NUM_MEANING)

    lunar_js = (Path(__file__).parent / 'lunar_convert.js').read_text(encoding='utf-8')
    calc_js = lunar_js + '\n' + CALC_JS.replace('__DATA__', data_json)

    html = (HTML_HEAD
            + '<body>\n' + HEADER + '\n'
            + SCHEMA_BLOCK + '\n'
            + BREADCRUMB
            + MAIN_TOP
            + CALC_SECTION
            + NLP_SECTION
            + EDU_SECTION.replace('__MEANING_ROWS__', meaning_rows)
            + MAIN_BOTTOM
            + FOOTER
            + '<script>\n' + calc_js + '\n</script>\n'
            + '</body>\n</html>')
    OUT.write_text(html, encoding='utf-8')
    print('OK 產出 %s（%d chars）' % (OUT, len(html)))


HTML_HEAD = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>生命靈數計算機｜免費算主命數、九宮格連線、空缺數與精油處方 | 精油能量圖譜</title>
  <meta name="description" content="''' + DESC + '''" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css" />
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
  <link rel="icon" href="favicon.ico">
  <!-- SEO_START -->
  <link rel="canonical" href="https://intelliverse.tw/numerology/" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="精油能量圖譜" />
  <meta property="og:locale" content="zh_TW" />
  <meta property="og:title" content="生命靈數計算機｜主命數、九宮格連線、空缺數與精油處方" />
  <meta property="og:description" content="''' + DESC + '''" />
  <meta property="og:url" content="https://intelliverse.tw/numerology/" />
  <meta property="og:image" content="https://cdn.jsdelivr.net/gh/kiolllery8-dev/essential-oil-cdn@main/images/hero-home.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="生命靈數計算機｜主命數、九宮格連線、空缺數與精油處方" />
  <meta name="twitter:description" content="''' + DESC + '''" />
  <meta name="twitter:image" content="https://cdn.jsdelivr.net/gh/kiolllery8-dev/essential-oil-cdn@main/images/hero-home.png" />
  <!-- SEO_END -->
  <style>
    .num-oil{display:inline-block;margin:3px 5px 3px 0;padding:4px 12px;background:#fff;border:1.5px solid #C8A67388;border-radius:14px;font-size:13px;font-weight:600;color:#8B6F3E;text-decoration:none;transition:all .12s;}
    .num-oil:hover{background:#8B6F3E;color:#fff;border-color:#8B6F3E;}
    .num-sel{padding:11px 14px;font-size:16px;font-family:inherit;border:1.5px solid #C8A673;border-radius:10px;background:#fff;color:#3D3328;cursor:pointer;}
    .num-card{background:#fff;border:1px solid #E5D9C0;border-radius:14px;padding:20px 22px;margin:16px 0;}
    .num-h2{font-size:21px;color:#3a5a40;border-bottom:2px solid #EEE7D8;padding-bottom:8px;margin:0 0 14px;}
    .num-stat{background:#FBF7F1;border-radius:10px;padding:10px 8px;text-align:center;}
    .num-stat b{display:block;font-size:23px;color:#8B6F3E;line-height:1.2;word-break:break-all;}
    .num-stat span{font-size:11.5px;color:#7A6852;}
    .num-line{display:flex;gap:10px;padding:10px 0;border-bottom:1px dashed #EEE7D8;}
    .nlp-opt{display:block;width:100%;text-align:left;padding:11px 14px;margin:6px 0;background:#fff;border:1.5px solid #E5D9C0;border-radius:10px;font-size:14px;font-family:inherit;color:#3D3328;cursor:pointer;transition:all .12s;}
    .nlp-opt:hover{border-color:#88BC88;background:#F4F9F4;}
    .nlp-opt.on{border-color:#88BC88;background:#EAF4EA;font-weight:600;}
  </style>
</head>
'''

SCHEMA_BLOCK = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "生命靈數計算機",
  "url": "https://intelliverse.tw/numerology/",
  "applicationCategory": "LifestyleApplication",
  "operatingSystem": "Web",
  "inLanguage": "zh-TW",
  "description": "輸入西元生日，免費計算生命靈數主命數、生日數、天賦數、九宮格連線與空缺數，並對應精油芳療方向。",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "TWD"},
  "publisher": {"@id": "https://intelliverse.tw/#organization"},
  "author": {"@id": "https://intelliverse.tw/#author"}
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "如何計算生命靈數（主命數）",
  "inLanguage": "zh-TW",
  "description": "用西元出生年月日計算生命靈數主命數的方法。",
  "step": [
    {"@type": "HowToStep", "position": 1, "name": "相加所有數字", "text": "把西元出生年、月、日的每一個數字全部相加。例如 1977 年 6 月 20 日：1+9+7+7+0+6+2+0=32。"},
    {"@type": "HowToStep", "position": 2, "name": "縮減成個位數", "text": "若相加結果是兩位數，把這兩位數字再相加，重複到剩下個位數。例如 32 → 3+2=5，主命數就是 5。"},
    {"@type": "HowToStep", "position": 3, "name": "填入九宮格", "text": "把出生日期、過程數字與主命數填進 3×3 九宮格，圈愈多代表該數能量愈強，沒出現的就是空缺數。"},
    {"@type": "HowToStep", "position": 4, "name": "連線與解讀", "text": "把有圈的數字連起來形成連線（如事業線、感情線），對照主命數、連線與空缺數解讀性格、天賦與課題。"}
  ]
}
</script>'''

HERO = '''<div class="oil-cover-hero" style="--c1:#7A5A8E;--c2:#B79BCB;background:linear-gradient(135deg,#7A5A8E 0%,#B79BCB 100%);">
  <span class="oil-cover-bg-emoji">🔢</span>
  <div class="oil-cover-overlay"></div>
  <div class="oil-cover-content">
    <span class="oil-cover-cat">🌳 互動工具 · 畢達哥拉斯占數</span>
    <h1>生命靈數</h1>
    <p class="oil-cover-latin">用你的生日，看見天生的性格、天賦與該補的功課——再用香氣陪你成長</p>
  </div>
</div>
'''

BREADCRUMB = '''<div class="breadcrumb"><div class="breadcrumb-inner">
  <a href="index.html">首頁</a><span class="sep">›</span><span>生命靈數</span>
</div></div>
'''

MAIN_TOP = '''<main style="max-width:980px;margin:0 auto;padding:0 20px;">

  <div style="margin:26px 0 4px;">
    <h1 style="font-size:30px;font-weight:800;color:#7A5A8E;margin:0 0 6px;">生命靈數計算機</h1>
    <p style="font-size:15px;color:#7A6852;margin:0;">用你的生日，看見天生的性格、天賦與該補的功課——再用香氣陪你成長</p>
  </div>

  <div style="display:flex;gap:20px;flex-wrap:wrap;align-items:stretch;margin:18px 0 8px;">
    <!-- 左：什麼是生命靈數（框）-->
    <section style="flex:1 1 300px;min-width:280px;background:linear-gradient(135deg,#F3EEF6 0%,#EAE2F0 100%);border:1px solid #DBC9E6;border-left:4px solid #B79BCB;padding:18px 22px;border-radius:12px;">
      <h2 style="font-size:18px;font-weight:700;color:#7A5A8E;margin:0 0 10px;">✦ 什麼是生命靈數？</h2>
      <p style="font-size:14.5px;line-height:1.85;color:#3D3328;margin:0 0 8px;">
        生命靈數源自兩千五百年前的古希臘數學家<strong>畢達哥拉斯</strong>，他相信「數字是宇宙的真理」——
        每個人的西元生日裡，都藏著一組專屬的數字密碼。把生日的數字一路相加、縮減，就能得到你的
        <strong>主命數</strong>，再搭配<strong>九宮格連線</strong>與<strong>空缺數</strong>，看見你天生的性格、天賦，
        以及這輩子要學的功課，最後對應到適合的<strong>精油香氣方向</strong>。
      </p>
      <p style="font-size:12.5px;color:#8A7A98;margin:0;">
        ※ 生命靈數屬於自我探索與娛樂，不是命定、也非醫療診斷；精油在這裡是「情緒陪伴與香氛儀式」，並非藥物。身心不適請就醫，孕婦、嬰幼兒、慢性病或用藥中請先諮詢專業芳療師或醫師。
      </p>
    </section>

    <!-- 右：計算器 -->
    <section id="calc" style="flex:1 1 320px;min-width:280px;background:#fff;border:1px solid #E5D9C0;border-radius:12px;padding:18px 22px;display:flex;flex-direction:column;justify-content:center;">
      <h2 style="font-size:18px;font-weight:700;color:#5A7A4A;margin:0 0 12px;">🔢 輸入你的生日</h2>
      <div style="display:flex;gap:16px;align-items:center;margin-bottom:12px;font-size:14px;color:#3D3328;">
        <label style="cursor:pointer;"><input type="radio" name="cal-type" value="solar" checked style="vertical-align:-1px;margin-right:4px;">國曆</label>
        <label style="cursor:pointer;"><input type="radio" name="cal-type" value="lunar" style="vertical-align:-1px;margin-right:4px;">農曆</label>
        <label id="leap-wrap" style="cursor:pointer;display:none;color:#7A5A8E;font-weight:600;"><input type="checkbox" id="num-leap" style="vertical-align:-1px;margin-right:4px;">閏月</label>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;">
        <input id="num-y" class="num-sel" type="number" inputmode="numeric" placeholder="年（如 1990）" min="1" max="2200" style="width:140px;" />
        <select id="num-m" class="num-sel"></select>
        <select id="num-d" class="num-sel"></select>
      </div>
      <button id="num-go" style="margin-top:14px;padding:12px 28px;background:#7A5A8E;color:#fff;border:none;border-radius:10px;font-size:16px;font-weight:700;cursor:pointer;font-family:inherit;">算出我的生命靈數 ✨</button>
      <p style="font-size:12px;color:#9A8AA8;margin:12px 0 0;">預設國曆（陽曆）；選農曆會自動換算成國曆再計算。年份可直接打字輸入。</p>
    </section>
  </div>

  <div id="num-result" style="margin-top:8px;"></div>
'''

CALC_SECTION = ''  # 計算器已併入 MAIN_TOP 的右欄

NLP_SECTION = '''
  <!-- NLP 表象系統測驗 -->
  <section id="nlp" style="margin:40px 0;">
    <h2 style="font-size:22px;color:var(--green-dark);border-bottom:2px solid var(--beige);padding-bottom:8px;">🧠 大腦說明書 — NLP 表象系統小測驗</h2>
    <p style="font-size:15px;line-height:1.9;margin:12px 0 6px;">
      除了生日，你「接收世界的方式」也決定了你怎麼學習、怎麼溝通最順。這 5 題會看出你偏向
      <strong>視覺 V／聽覺 A／觸覺 K／自語 AD</strong> 哪一型，並給你對應的學習建議與香氣方向。憑直覺選就好。
    </p>
    <div id="nlp-quiz"></div>
    <button id="nlp-go" style="padding:11px 24px;background:#88BC88;color:#fff;border:none;border-radius:10px;font-size:15px;font-weight:700;cursor:pointer;font-family:inherit;margin-top:8px;">看我的大腦類型</button>
    <div id="nlp-result" style="margin-top:14px;"></div>
  </section>
'''

EDU_SECTION = '''
  <!-- 靜態知識（SEO / AI 友善）-->
  <section style="margin:44px 0;">
    <h2 style="font-size:22px;color:var(--green-dark);border-bottom:2px solid var(--beige);padding-bottom:8px;">📐 生命靈數怎麼算？</h2>
    <p style="font-size:15px;line-height:1.9;margin:12px 0;">計算方法其實很簡單，自己用紙筆就能算：</p>
    <ol style="font-size:15px;line-height:2;padding-left:22px;">
      <li><strong>把生日數字全部相加</strong>：西元出生年月日的每個數字相加。以 1977 年 6 月 20 日為例：1+9+7+7+0+6+2+0 = 32。</li>
      <li><strong>縮減成個位數</strong>：如果是兩位數，把兩個數字再相加，直到剩個位數。32 → 3+2 = 5，所以<strong>主命數是 5</strong>。</li>
      <li><strong>生日數</strong>：只把「日」相加縮減。20 日 → 2+0 = 2。<strong>天賦數</strong>：全部相加後、變成個位數前的那個兩位數（這裡是 32，即 3、2）。</li>
      <li><strong>填九宮格、找連線與空缺</strong>：把出生日期、過程數字、主命數圈進 3×3 九宮格，圈愈多的數字能量愈強；連成線就是你的天賦連線，沒被圈到的 1–9 就是<strong>空缺數</strong>（人生功課）。</li>
    </ol>

    <h2 style="font-size:22px;color:var(--green-dark);border-bottom:2px solid var(--beige);padding-bottom:8px;margin-top:32px;">🔣 1–9 數字的意義</h2>
    <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;font-size:14px;background:#fff;border-radius:10px;overflow:hidden;margin-top:12px;">
      <thead><tr style="background:#7A5A8E;color:#fff;"><th style="padding:10px 12px;">數字</th><th style="padding:10px 12px;text-align:left;">形而上的意義</th></tr></thead>
      <tbody>__MEANING_ROWS__</tbody>
    </table>
    </div>

    <h2 style="font-size:22px;color:var(--green-dark);border-bottom:2px solid var(--beige);padding-bottom:8px;margin-top:32px;">💫 為什麼生命靈數可以搭配精油？</h2>
    <p style="font-size:15px;line-height:1.9;margin:12px 0;">
      生命靈數幫你看見自己的「樣子」——主命數是你的核心性格與天賦、連線是你外在的優勢、
      空缺數是還沒補上的人生課題。而精油，是陪你照顧自己的方式：當你看見自己容易繃緊、
      容易飄、容易自我批評，就能挑對應方向的香氣，在情緒上給自己一點支持。木質調幫你紮根、花香調溫柔療癒、
      柑橘調帶來明亮、草本調讓思緒清晰——這不是治療，而是用香味，溫柔地陪自己練習成長。每支推薦精油都可以
      點進去看完整的<a href="oils.html">成分與用法指南</a>，調配方式可參考<a href="blend.html">調配精油工具</a>。
    </p>

    <h2 style="font-size:22px;color:var(--green-dark);border-bottom:2px solid var(--beige);padding-bottom:8px;margin-top:32px;">🧭 這個工具還會幫你算什麼？</h2>
    <ul style="font-size:15px;line-height:2;padding-left:22px;">
      <li><strong>代表顏色</strong>：每個主命數對應一個脈輪色系（1 紅、2 橙、3 黃、4 綠、5 藍、6 靛、7 紫、8 粉紅、9 金），是你的能量主色。</li>
      <li><strong>能量原型</strong>：用《幸福密碼》的密碼身份，給你一個象徵原型（如 1 號皇宮貴族、5 號武將、9 號出家人），純趣味象徵。</li>
      <li><strong>流年運</strong>：用你的生日加上今年年份，算出你正走在九年循環的哪一年（開始年、精彩年、收成年⋯），以及今年適合的香氣方向；跨年會自動更新。</li>
      <li><strong>緣分合盤</strong>：輸入對方的主命數，用兩人主命數的「相差」看緣分類型（相差 6 互相依戀分數最高、相差 0 靈魂伴侶⋯）。</li>
      <li><strong>NLP 學習風格</strong>：5 題小測驗看你偏視覺／聽覺／觸覺／自語，給你對應的學習與溝通建議。</li>
    </ul>

    <h2 style="font-size:22px;color:var(--green-dark);border-bottom:2px solid var(--beige);padding-bottom:8px;margin-top:32px;">❓ 常見問題</h2>
    <div class="num-card"><strong style="color:#7A5A8E;">Q：要用國曆還是農曆生日？</strong><p style="margin:8px 0 0;font-size:14.5px;line-height:1.85;">兩種都可以。預設是<strong>國曆（西元／陽曆）</strong>；如果你只記得農曆，把計算器切到<strong>農曆</strong>（閏月年份再勾「閏月」），系統會自動換算成國曆再計算，不用自己查萬年曆。生命靈數本身是用國曆日期推算的。</p></div>
    <div class="num-card"><strong style="color:#7A5A8E;">Q：主命數和星座哪個準？</strong><p style="margin:8px 0 0;font-size:14.5px;line-height:1.85;">兩者看的角度不同：星座偏「當下的情緒與風格」，生命靈數偏「天生的性格與人生方向」。它們都是認識自己的工具，參考、對照著看就好，不必當成命定。</p></div>
    <div class="num-card"><strong style="color:#7A5A8E;">Q：空缺數是不是不好？</strong><p style="margin:8px 0 0;font-size:14.5px;line-height:1.85;">不是缺點，而是「這輩子要練習的功課」。看見它，你就有機會補上；補上之後，往往會變成你最有故事、最有厚度的地方。</p></div>
    <div class="num-card"><strong style="color:#7A5A8E;">Q：精油真的能改運嗎？</strong><p style="margin:8px 0 0;font-size:14.5px;line-height:1.85;">精油不是法術，也不是藥物。它能做的是在你需要的時候，用香氣支持你的情緒、陪你建立小儀式。把它當成「照顧自己的方式」，而不是「改變命運的工具」。</p></div>
  </section>
'''

MAIN_BOTTOM = '''
  <div class="info-box" style="background:#FFF4E6;border-left:4px solid #E8A04B;border-radius:8px;padding:16px 20px;margin:24px 0;">
    <strong style="color:#B5701A;">⚠️ 溫馨提醒</strong>
    <p style="font-size:14px;line-height:1.8;color:#5D4A28;margin:6px 0 0;">生命靈數為自我探索與休閒娛樂，測算結果僅供參考，不代表命定。本頁精油建議屬於一般芳香生活方向，非醫療處方，無法治療、診斷或預防疾病。孕婦、嬰幼兒、慢性病或用藥中請先諮詢專業芳療師或醫師；精油請稀釋後使用並先做肌膚測試。</p>
  </div>

</main>
'''

FOOTER = '''<footer>
  <div class="footer-inner" style="max-width:1100px;margin:0 auto;padding:32px 20px;">
    <p>© 2026 精油能量圖譜 · 靈境智造 Intelliverse Studio</p>
    <p style="font-size:12px;color:#999;margin-top:8px;">本站資訊僅供教育參考，不取代醫療建議。作者：<a href="author-yuling.html" style="color:#8B6F3E;">玉玲（IFA 國際認證芳療師）</a>｜<a href="references.html" style="color:#8B6F3E;">引用來源</a></p>
  </div>
</footer>
'''

CALC_JS = r'''
(function(){
  var D = __DATA__;
  function byId(id){return document.getElementById(id);}
  function el(tag,html){var e=document.createElement(tag);if(html!=null)e.innerHTML=html;return e;}
  function pad(n){return n<10?'0'+n:''+n;}
  function sumDigits(n){var s=0;n=Math.abs(n);while(n>0){s+=n%10;n=Math.floor(n/10);}return s;}
  function reduceNum(n){while(n>9)n=sumDigits(n);return n;}

  // 年份改為手動輸入（input）；月、日仍用下拉；可切換國曆／農曆
  var ySel=byId('num-y'),mSel=byId('num-m'),dSel=byId('num-d');
  function opt(v,t){var o=document.createElement('option');o.value=v;o.textContent=t;return o;}
  mSel.appendChild(opt('','月'));
  for(var m=1;m<=12;m++)mSel.appendChild(opt(m,m+' 月'));
  function calType(){var r=document.querySelector('input[name=cal-type]:checked');return r?r.value:'solar';}
  function fillDays(){
    var cur=dSel.value,yy=+ySel.value,mm=+mSel.value,max=31;
    if(calType()==='lunar'){max=30;}
    else{var dim=[31,28,31,30,31,30,31,31,30,31,30,31];if(mm>=1&&mm<=12){max=dim[mm-1];if(mm===2&&yy&&((yy%4===0&&yy%100!==0)||yy%400===0))max=29;}}
    dSel.innerHTML='';dSel.appendChild(opt('','日'));
    for(var dd=1;dd<=max;dd++)dSel.appendChild(opt(dd,dd+' 日'));
    if(cur&&+cur<=max)dSel.value=cur;
  }
  function updateLeap(){
    var wrap=byId('leap-wrap'),cb=byId('num-leap');if(!wrap)return;
    if(calType()!=='lunar'){wrap.style.display='none';cb.checked=false;return;}
    wrap.style.display='inline-block';
    var yy=+ySel.value,mm=+mSel.value,has=!!(yy>=1900&&yy<=2100&&mm&&LUNAR.leapMonth(yy)===mm);
    cb.disabled=!has;if(!has)cb.checked=false;wrap.style.opacity=has?'1':'0.4';
  }
  function refresh(){fillDays();updateLeap();}
  ySel.oninput=refresh;mSel.onchange=refresh;
  Array.prototype.forEach.call(document.querySelectorAll('input[name=cal-type]'),function(r){r.onchange=refresh;});
  refresh();

  function zodiacOf(m,d){
    for(var i=0;i<D.zodiac.length;i++){var z=D.zodiac[i];
      if((m===z.m1&&d>=z.d1)||(m===z.m2&&d<=z.d2))return z;}
    return null;
  }

  // 九宮格 SVG
  var GPOS={1:[0,0],4:[1,0],7:[2,0],2:[0,1],5:[1,1],8:[2,1],3:[0,2],6:[1,2],9:[2,2]};
  function cx(c){return 42+c*70;}
  function cyf(r){return 42+r*70;}
  function gridSvg(counts,activeLines){
    var W=84+2*70,s='<svg viewBox="0 0 '+W+' '+W+'" width="240" height="240" style="max-width:100%;">';
    activeLines.forEach(function(ln){
      var col=ln.type==='main'?'#88BC88':'#C8A673';
      var a=GPOS[ln.nums[0]],b=GPOS[ln.nums[ln.nums.length-1]];
      s+='<line x1="'+cx(a[0])+'" y1="'+cyf(a[1])+'" x2="'+cx(b[0])+'" y2="'+cyf(b[1])+'" stroke="'+col+'" stroke-width="7" stroke-linecap="round" opacity="0.45"/>';
    });
    for(var n=1;n<=9;n++){var p=GPOS[n],on=counts[n]>0;
      s+='<circle cx="'+cx(p[0])+'" cy="'+cyf(p[1])+'" r="24" fill="'+(on?'#fff':'#F3EFE9')+'" stroke="'+(on?'#7A5A8E':'#D8CFC2')+'" stroke-width="'+(on?2:1.5)+'"'+(on?'':' stroke-dasharray="3 3"')+'/>';
      s+='<text x="'+cx(p[0])+'" y="'+(cyf(p[1])+6)+'" text-anchor="middle" font-size="19" font-weight="800" fill="'+(on?'#7A5A8E':'#C8BFB2')+'">'+n+'</text>';
      if(counts[n]>1)s+='<text x="'+(cx(p[0])+20)+'" y="'+(cyf(p[1])-16)+'" text-anchor="middle" font-size="12" font-weight="800" fill="#E8A04B">×'+counts[n]+'</text>';
    }
    return s+'</svg>';
  }

  function stat(v,label){return '<div class="num-stat"><b>'+v+'</b><span>'+label+'</span></div>';}

  byId('num-go').onclick=function(){
    var y=+ySel.value,m=+mSel.value,d=+dSel.value;
    if(!y||!m||!d){alert('請先填好完整的生日喔（年份直接輸入數字）');return;}
    if(y<1||y>2200){alert('年份請輸入合理的西元年，例如 1990');return;}
    var lunarNote='';
    if(calType()==='lunar'){
      if(y<1900||y>2100){alert('農曆換算僅支援西元 1900–2100 年');return;}
      var isLeap=byId('num-leap')&&byId('num-leap').checked;
      var sol=LUNAR.lunar2solar(y,m,d,isLeap);
      if(!sol||sol===-1){alert('這個農曆日期不存在喔（可能該農曆月只有 29 天，或該年沒有這個閏月）。請確認後再試。');return;}
      lunarNote='農曆 '+y+' 年 '+(isLeap?'閏':'')+m+' 月 '+d+' 日　＝　國曆 '+sol.y+'-'+pad(sol.m)+'-'+pad(sol.d);
      y=sol.y;m=sol.m;d=sol.d;
    }
    var ymd=''+y+pad(m)+pad(d),digs=ymd.split('').map(Number);
    var first=digs.reduce(function(a,b){return a+b;},0);
    var chain=[first],s=first;while(s>9){s=sumDigits(s);chain.push(s);}
    var life=chain[chain.length-1];
    var talent=chain.length>=2?chain[chain.length-2]:chain[0];
    var bday=reduceNum(d),zo=zodiacOf(m,d);
    var plot=digs.slice();chain.forEach(function(v){(''+v).split('').forEach(function(c){plot.push(+c);});});
    var counts={};for(var i=1;i<=9;i++)counts[i]=0;
    plot.forEach(function(v){if(v>=1&&v<=9)counts[v]++;});
    var missing=[];for(var i=1;i<=9;i++)if(counts[i]===0)missing.push(i);
    var innate=digs.filter(function(v){return v>0;}).join(' ');
    var active=D.lines.filter(function(ln){return ln.nums.every(function(n){return counts[n]>0;});});
    var ty=new Date().getFullYear();
    var flow=reduceNum(reduceNum(m)+reduceNum(d)+reduceNum(ty));
    var rm=reduceNum(m),rd=reduceNum(d),ry=reduceNum(y);
    var p1=reduceNum(rm+rd),p2=reduceNum(rd+ry),p3=reduceNum(p1+p2),p4=reduceNum(rm+ry);
    var e1=36-life,age=ty-y;
    var stages=[{num:p1,from:0,to:e1},{num:p2,from:e1+1,to:e1+9},{num:p3,from:e1+10,to:e1+18},{num:p4,from:e1+19,to:null}];
    var curStage=age<=e1?0:(age<=e1+9?1:(age<=e1+18?2:3));
    render(life,bday,talent,zo,innate,counts,missing,active,flow,ty,first,stages,curStage,age,lunarNote);
  };

  function render(life,bday,talent,zo,innate,counts,missing,active,flow,ty,combo,stages,curStage,age,lunarNote){
    var lp=D.lifepath[life],talentStr=(''+talent).split('').join(' '),h='';
    h+='<div class="num-card" style="border-top:4px solid '+lp.color+';">';
    h+='<div style="text-align:center;margin-bottom:6px;"><span style="font-size:13px;color:#9A8AA8;">你的生命靈數</span><div style="font-size:28px;font-weight:800;color:#7A5A8E;">'+lp.emoji+' 主命數 '+life+'｜'+lp.tree+'</div><div style="font-size:14px;color:#7A6852;">'+lp.keyword+'</div></div>';
    h+='<div style="text-align:center;margin-bottom:2px;font-size:13px;color:#7A6852;"><span style="display:inline-block;width:11px;height:11px;border-radius:50%;background:'+lp.color+';margin-right:5px;vertical-align:-1px;"></span>代表色 '+lp.colorName+'　·　能量原型 '+lp.archetype+'</div>';
    if(lunarNote)h+='<div style="text-align:center;font-size:12.5px;color:#9A8AA8;margin-bottom:4px;">📅 '+lunarNote+'</div>';
    h+='<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:14px;">';
    h+=stat(innate,'先天數')+stat(life,'主命數')+stat(bday,'生日數');
    h+=stat(talentStr,'天賦數')+stat(zo?zo.num:'-',(zo?zo.name:'')+'·星座數')+stat(missing.length?missing.join(' '):'無','空缺數');
    h+='</div></div>';
    h+='<div class="num-card" style="text-align:center;"><h3 class="num-h2" style="border:none;">你的九宮格與連線</h3>';
    h+=gridSvg(counts,active);
    h+='<div style="font-size:12.5px;color:#7A6852;margin-top:8px;"><span style="color:#88BC88;font-weight:700;">━ 綠線</span> 主連線（天賦）　<span style="color:#C8A673;font-weight:700;">━ 棕線</span> 副連線　虛線圈＝空缺數</div></div>';
    h+='<div class="num-card"><h3 class="num-h2">💠 核心性格 — 主命數 '+life+'（'+lp.tree+'）</h3>';
    h+='<p style="font-size:15px;line-height:1.9;margin:0 0 12px;">'+lp.desc+'</p>';
    h+='<div style="display:grid;gap:8px;font-size:14px;">';
    h+='<div style="background:#F4F9F4;border-left:4px solid #88BC88;padding:10px 14px;border-radius:8px;"><b style="color:#5A7A4A;">✦ 天生優點：</b>'+lp.good+'</div>';
    h+='<div style="background:#FDF3F3;border-left:4px solid #D89090;padding:10px 14px;border-radius:8px;"><b style="color:#B56A6A;">✦ 要留意的：</b>'+lp.bad+'</div>';
    h+='<div style="background:#F7F4FA;border-left:4px solid #B79BCB;padding:10px 14px;border-radius:8px;"><b style="color:#7A5A8E;">💼 適合的職涯：</b>'+lp.career+'</div>';
    h+='<div style="background:#FFF6F0;border-left:4px solid #E8A04B;padding:10px 14px;border-radius:8px;"><b style="color:#C57A2A;">💞 愛情裡的你：</b>'+lp.love+'</div>';
    h+='</div></div>';
    h+='<div class="num-card"><h3 class="num-h2">🔗 連線天賦（'+active.length+' 條）</h3>';
    if(active.length){active.forEach(function(ln){
      h+='<div class="num-line"><div style="min-width:54px;font-weight:800;color:'+(ln.type==='main'?'#5A7A4A':'#A6863F')+';">'+ln.nums.join('-')+'</div><div><b>'+ln.name+'</b>　'+ln.pos+'<div style="font-size:13px;color:#9A8A78;margin-top:3px;">⚠ '+ln.neg+'</div></div></div>';
    });}else{h+='<p style="font-size:14.5px;color:#7A6852;margin:0;">你目前沒有完整的三格連線——這代表你的能量比較分散、不被單一模式定義，反而更有彈性。可以多看主命數與空缺數來認識自己。</p>';}
    h+='</div>';
    h+='<div class="num-card"><h3 class="num-h2">💧 生日數 '+bday+' & 天賦數 '+talentStr+'</h3>';
    h+='<p style="font-size:14.5px;line-height:1.9;margin:0 0 10px;"><b>生日數 '+bday+'</b>：'+D.lifepath[bday].title+'的特質——'+D.lifepath[bday].keyword+'，是你在日常裡最自然流露的一面。<br><b>天賦數 '+talentStr+'</b>：藏在你身上、可以好好發揮的潛在才能。</p>';
    if(D.combo[combo]){h+='<div style="background:#F7F4FA;border-left:4px solid #B79BCB;border-radius:8px;padding:10px 14px;font-size:14px;line-height:1.85;"><b style="color:#7A5A8E;">🔢 你的數字組合 '+combo+'：</b>'+D.combo[combo]+'</div>';}
    h+='</div>';
    h+='<div class="num-card"><h3 class="num-h2">🧩 空缺數功課 & 精油處方</h3>';
    if(missing.length){missing.forEach(function(n){var ms=D.missing[n];
      h+='<div style="margin-bottom:16px;padding-bottom:14px;border-bottom:1px dashed #EEE7D8;">';
      h+='<div style="font-weight:800;color:#B5701A;font-size:15px;">缺 '+n+'：'+ms.theme+'</div>';
      h+='<p style="font-size:14px;line-height:1.85;margin:6px 0;">'+ms.text+'</p>';
      h+='<div style="font-size:13.5px;color:#5A7A4A;background:#F4F9F4;padding:8px 12px;border-radius:8px;margin:6px 0;">🌱 小練習：'+ms.practice+'</div>';
      h+='<div style="font-size:13.5px;">🌿 香氣陪伴：'+ms.oilsHtml+'</div></div>';
    });}else{h+='<p style="font-size:14.5px;color:#7A6852;margin:0;">你的九宮格 1–9 都有圈到，沒有明顯空缺數——能量相對完整、均衡。可以把下面主命數的精油方向，當成日常的香氣陪伴。</p>';}
    h+='</div>';
    h+='<div class="num-card" style="background:linear-gradient(135deg,#F7F4FA 0%,#F0EAF6 100%);"><h3 class="num-h2" style="border-color:#DCD0E6;">🌸 適合你（主命數 '+life+'）的精油方向</h3>';
    h+='<p style="font-size:14.5px;line-height:1.85;margin:0 0 10px;">'+lp.oilwhy+'</p><div>'+lp.oilsHtml+'</div></div>';
    var yf=D.yearFlow[flow];
    h+='<div class="num-card" style="background:linear-gradient(135deg,#FBF6EE 0%,#F5ECDD 100%);"><h3 class="num-h2" style="border-color:#E8D9BE;">📅 '+ty+' 流年運 — 今年你走「'+yf.name+'」</h3>';
    h+='<p style="font-size:14.5px;line-height:1.9;margin:0 0 10px;">'+yf.text+'</p>';
    h+='<div style="font-size:13.5px;">🌿 今年的香氣陪伴：'+yf.oilsHtml+'</div>';
    h+='<div style="font-size:12px;color:#9A8AA8;margin-top:8px;">流年＝出生月＋出生日＋今年（'+ty+'），跨年會自動更新。</div></div>';
    h+='<div class="num-card"><h3 class="num-h2">⛰️ 人生四階段大運</h3>';
    h+='<p style="font-size:13.5px;color:#7A6852;margin:0 0 10px;">人生分成四個階段，每段被一個數字能量主導。你現在大約 '+age+' 歲，正走在標亮的那一段。</p>';
    var labels=['第一階段','第二階段','第三階段','第四階段'];
    stages.forEach(function(st,i){
      var on=i===curStage;
      var range=st.to===null?(st.from+' 歲以後'):(st.from+'–'+st.to+' 歲');
      h+='<div style="display:flex;gap:12px;align-items:flex-start;padding:10px 12px;margin:6px 0;border-radius:10px;border:1px solid '+(on?'#C8A673':'#EEE7D8')+';background:'+(on?'#FBF6EE':'#fff')+';">';
      h+='<div style="min-width:66px;text-align:center;"><div style="font-size:11px;color:#9A8AA8;">'+labels[i]+'</div><div style="font-size:23px;font-weight:800;color:#8B6F3E;">'+st.num+'</div><div style="font-size:11px;color:#7A6852;">'+range+'</div></div>';
      h+='<div style="flex:1;font-size:13.5px;line-height:1.8;color:#3D3328;">'+(on?'<b style="color:#B5701A;">▸ 你現在這裡：</b>':'')+D.pinnacle[st.num]+'</div></div>';
    });
    h+='<div style="font-size:12px;color:#9A8AA8;margin-top:6px;">※ 高峰數＝月+日、日+年、兩者相加、月+年（皆先縮減）；年齡為粗估，實際以生日為準。</div></div>';
    h+='<div class="num-card"><h3 class="num-h2">💞 人際合盤</h3><p style="font-size:14.5px;line-height:1.9;margin:0 0 14px;">'+lp.compat+'</p>';
    h+='<div style="background:#FBF7F1;border-radius:10px;padding:14px 16px;">';
    h+='<div style="font-size:14px;font-weight:700;color:#7A5A8E;margin-bottom:6px;">🔮 看你和某個人的緣分</div>';
    h+='<div style="font-size:13px;color:#7A6852;margin-bottom:8px;">選對方的主命數（不知道的話，可以幫他也算一次）：</div>';
    h+='<select id="partner-sel" class="num-sel" style="font-size:14px;padding:8px 12px;"><option value="">對方主命數…</option>';
    for(var pn=1;pn<=9;pn++)h+='<option value="'+pn+'">'+pn+' 號 · '+D.lifepath[pn].tree+'</option>';
    h+='</select><div id="partner-res" style="margin-top:12px;"></div></div></div>';
    var box=byId('num-result');box.innerHTML=h;
    var ps=byId('partner-sel');
    if(ps)ps.onchange=function(){
      var pv=+ps.value,pr=byId('partner-res');
      if(!pv){pr.innerHTML='';return;}
      var cd=D.compatDiff[Math.abs(life-pv)];
      var col=cd.score>=80?'#5FA85F':(cd.score>=60?'#E2872E':'#B56A6A');
      pr.innerHTML='<div style="background:#fff;border:1px solid #E5D9C0;border-left:4px solid '+col+';border-radius:8px;padding:12px 14px;"><div style="font-weight:800;color:'+col+';font-size:15px;">'+life+' × '+pv+' → '+cd.name+'　<span style="font-size:13px;font-weight:600;">緣分指數 '+cd.score+'</span></div><div style="font-size:14px;line-height:1.8;margin-top:6px;color:#3D3328;">'+cd.text+'</div></div>';
    };
    box.scrollIntoView({behavior:'smooth',block:'start'});
  }

  // NLP 測驗
  var nlpAns={},quiz=byId('nlp-quiz'),keys=['V','A','K','AD'];
  D.nlpQ.forEach(function(item,qi){
    var card=el('div','<div style="font-weight:700;font-size:15px;margin:14px 0 4px;color:#3a5a40;">'+(qi+1)+'. '+item.q+'</div>');
    item.opts.forEach(function(o,oi){
      var b=el('button',o);b.className='nlp-opt';
      b.onclick=function(){nlpAns[qi]=keys[oi];
        Array.prototype.forEach.call(card.querySelectorAll('.nlp-opt'),function(x){x.classList.remove('on');});
        b.classList.add('on');};
      card.appendChild(b);
    });
    quiz.appendChild(card);
  });
  byId('nlp-go').onclick=function(){
    var n=Object.keys(nlpAns).length;
    if(n<D.nlpQ.length){alert('還有 '+(D.nlpQ.length-n)+' 題沒選喔');return;}
    var tally={V:0,A:0,K:0,AD:0};Object.keys(nlpAns).forEach(function(k){tally[nlpAns[k]]++;});
    var best='V',bv=-1;keys.forEach(function(k){if(tally[k]>bv){bv=tally[k];best=k;}});
    var r=D.nlpRes[best];
    var h='<div class="num-card" style="border-top:4px solid #88BC88;">';
    h+='<div style="font-size:22px;font-weight:800;color:#3a5a40;">'+r.icon+' 你是「'+r.name+'」</div>';
    h+='<p style="font-size:14.5px;line-height:1.9;margin:10px 0;">'+r.desc+'</p>';
    h+='<div style="font-size:13.5px;color:#7A6852;margin-bottom:6px;">分數：視覺 '+tally.V+'｜聽覺 '+tally.A+'｜觸覺 '+tally.K+'｜自語 '+tally.AD+'</div>';
    h+='<div style="background:#F7F4FA;border-radius:8px;padding:12px 14px;"><div style="font-size:13.5px;line-height:1.8;margin-bottom:8px;">🌿 '+r.oilwhy+'</div>'+r.oilsHtml+'</div></div>';
    byId('nlp-result').innerHTML=h;
    byId('nlp-result').scrollIntoView({behavior:'smooth',block:'nearest'});
  };
})();
'''

if __name__ == '__main__':
    build()
