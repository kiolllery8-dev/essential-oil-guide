/* faq-accordion.js — 全站 FAQ 折疊式（accordion）
 * 處理三種 FAQ 標記，內容仍留在 DOM（對 SEO / FAQ 結構化資料無影響）：
 *   A. 精油頁／部分文章：schema.org/Question 微資料（itemprop name + acceptedAnswer）
 *   C. 文章：.info-box 內 .box-title 以「Q」開頭
 *   B. 生命靈數：.num-card 首個 <strong> 以「Q」開頭
 * 預設全部收合，點問題（或 Enter/Space）展開。
 */
(function () {
  var QRE = /^Q\s*\d*\s*[:：]/;

  function siblingsAfter(node) {
    var out = [], n = node.nextElementSibling;
    while (n) { out.push(n); n = n.nextElementSibling; }
    return out;
  }

  function makeAccordion(trigger, answers) {
    if (!trigger || !answers || !answers.length || trigger.dataset.faqAcc) return;
    trigger.dataset.faqAcc = '1';
    var open = false;
    answers.forEach(function (a) { a.style.display = 'none'; });
    trigger.style.cursor = 'pointer';
    trigger.style.display = 'block';
    trigger.style.position = 'relative';
    trigger.style.paddingRight = '28px';
    trigger.setAttribute('role', 'button');
    trigger.setAttribute('tabindex', '0');
    trigger.setAttribute('aria-expanded', 'false');

    var chev = document.createElement('span');
    chev.setAttribute('aria-hidden', 'true');
    chev.textContent = '＋';
    chev.style.cssText = 'position:absolute;right:2px;top:50%;transform:translateY(-50%);font-weight:400;opacity:.5;transition:opacity .2s;';
    trigger.appendChild(chev);

    function toggle() {
      open = !open;
      answers.forEach(function (a) { a.style.display = open ? '' : 'none'; });
      chev.textContent = open ? '－' : '＋';
      trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    trigger.addEventListener('click', toggle);
    trigger.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
    });
  }

  function init() {
    // A. Question 微資料
    document.querySelectorAll('[itemtype$="/Question"]').forEach(function (q) {
      var t = q.querySelector('[itemprop="name"]');
      var a = q.querySelector('[itemprop="acceptedAnswer"]');
      if (t && a) makeAccordion(t, [a]);
    });
    // C. info-box FAQ
    document.querySelectorAll('.info-box').forEach(function (box) {
      var t = box.querySelector('.box-title');
      if (t && QRE.test((t.textContent || '').trim())) makeAccordion(t, siblingsAfter(t));
    });
    // B. num-card FAQ（生命靈數）
    document.querySelectorAll('.num-card').forEach(function (card) {
      var s = card.firstElementChild;
      if (s && s.tagName === 'STRONG' && QRE.test((s.textContent || '').trim())) {
        makeAccordion(s, siblingsAfter(s));
      }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
