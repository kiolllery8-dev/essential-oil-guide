/* Mobile hamburger menu — left-slide drawer with backdrop below header */
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.querySelector('.menu-toggle');
    var nav = document.querySelector('header nav');
    var header = document.querySelector('header');
    if (!btn || !nav) return;

    // Create backdrop
    var backdrop = document.querySelector('.nav-backdrop');
    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.className = 'nav-backdrop';
      document.body.appendChild(backdrop);
    }

    // Compute drawer top offset to match header bottom
    function syncDrawerTop() {
      if (!header) return;
      var rect = header.getBoundingClientRect();
      var top = Math.max(0, rect.bottom);
      document.documentElement.style.setProperty('--drawer-top', top + 'px');
    }
    syncDrawerTop();
    window.addEventListener('resize', syncDrawerTop);
    window.addEventListener('scroll', syncDrawerTop, { passive: true });

    function open() {
      syncDrawerTop();
      nav.classList.add('open');
      document.body.classList.add('menu-open');
      btn.setAttribute('aria-expanded', 'true');
    }
    function close() {
      nav.classList.remove('open');
      document.body.classList.remove('menu-open');
      btn.setAttribute('aria-expanded', 'false');
    }
    function toggle() {
      if (nav.classList.contains('open')) close(); else open();
    }

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      toggle();
    });
    backdrop.addEventListener('click', close);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', close);
    });
  });
})();
