/* Mobile hamburger menu toggle (shared across all pages) */
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.querySelector('.menu-toggle');
    var nav = document.querySelector('header nav');
    if (!btn || !nav) return;
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', nav.classList.contains('open') ? 'true' : 'false');
    });
    // Close when clicking outside
    document.addEventListener('click', function (e) {
      if (!nav.contains(e.target) && e.target !== btn) {
        nav.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
    // Close when a link is tapped
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      });
    });
  });
})();
