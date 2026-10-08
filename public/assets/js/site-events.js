/* Aggregate tool and related-reading events. Never transmit form values or result numbers. */
(function () {
  'use strict';
  if (window.__ivSiteEventsInstalled) return;
  window.__ivSiteEventsInstalled = true;
  var calculationObserver = null;
  var viewObserver = null;
  function safePath(path) {
    return /^\/(?:[a-z0-9-]+\/|oil\/[0-9]+\/)?$/.test(path) ? path : '/';
  }
  function emit(name, fields) {
    var send = window.gtag || function () {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(arguments);
    };
    send('event', name, Object.assign({ page_path: safePath(location.pathname) }, fields));
  }
  document.addEventListener('click', function (event) {
    if (!event.isTrusted || !(event.target instanceof Element)) return;
    if (event.target.closest('#num-go')) {
      if (calculationObserver) calculationObserver.disconnect();
      if (viewObserver) viewObserver.disconnect();
      var result = document.getElementById('num-result');
      if (!result) return;
      calculationObserver = new MutationObserver(function () {
        if (result.innerText.trim().length < 100 || !result.getClientRects().length) return;
        calculationObserver.disconnect();
        emit('numerology_calculate', { tool: 'numerology' });
        var heading = result.querySelector('h2, h3') || result.firstElementChild || result;
        viewObserver = new IntersectionObserver(function (entries) {
          if (!entries.some(function (entry) { return entry.isIntersecting; })) return;
          viewObserver.disconnect();
          emit('numerology_result_view', { tool: 'numerology' });
        });
        viewObserver.observe(heading);
      });
      calculationObserver.observe(result, { childList: true });
      var pendingObserver = calculationObserver;
      setTimeout(function () { pendingObserver.disconnect(); }, 1000);
    }
    var anchor = event.target.closest('a[href]');
    if (!anchor) return;
    var target;
    try { target = new URL(anchor.href, location.href); } catch (_) { return; }
    if (target.origin !== location.origin) return;
    if (/^\/oil(?:-[a-z0-9-]+|\/[0-9]+)\/$/.test(target.pathname)) {
      emit('related_oil_click', { target_path: safePath(target.pathname) });
    } else if (/^\/article-[a-z0-9-]+\/$/.test(target.pathname)) {
      emit('related_article_click', { target_path: safePath(target.pathname) });
    }
  }, true);
}());
