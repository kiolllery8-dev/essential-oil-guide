const assert = require('node:assert/strict');
const { chromium } = require(process.env.PLAYWRIGHT_PACKAGE || 'playwright');

(async () => {
  const browser = await chromium.launch({ headless: true,
    executablePath: process.env.PLAYWRIGHT_BROWSER || chromium.executablePath() });
  try {
    for (const width of [375, 1280]) {
      const context = await browser.newContext({ viewport: { width, height: 900 } });
      await context.route('**/*', route => new URL(route.request().url()).hostname === '127.0.0.1'
        ? route.continue() : route.abort());
      const page = await context.newPage();
      page.on('dialog', dialog => dialog.accept());
      await page.goto('http://127.0.0.1:8873/numerology/');
      await page.waitForFunction(() => window.__ivSiteEventsInstalled);
      await page.evaluate(() => {
        window.__capturedEvents = [];
        window.gtag = (...args) => window.__capturedEvents.push(args);
      });
      await page.locator('#num-y').fill('1992');
      await page.locator('#num-m').selectOption('2');
      await page.locator('#num-d').selectOption('3');
      await page.locator('#num-go').click();
      await page.waitForFunction(() => window.__capturedEvents.some(e => e[1] === 'numerology_calculate'));
      // Put only the first result title near the viewport bottom. The next card's
      // heading must remain below the viewport when the view event is emitted.
      await page.locator('#num-result > :first-child > :first-child').evaluate(element => {
        window.scrollTo(0, element.getBoundingClientRect().top + window.scrollY - window.innerHeight + 110);
      });
      await page.waitForFunction(() => window.__capturedEvents.some(e => e[1] === 'numerology_result_view'));
      assert(await page.locator('#num-result h3').first().evaluate(element =>
        element.getBoundingClientRect().top >= window.innerHeight), 'First result counts before the second card is visible');
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.locator('#num-result > :first-child > :first-child').scrollIntoViewIfNeeded();
      assert.equal(await page.evaluate(() => window.__capturedEvents.filter(e => e[1] === 'numerology_result_view').length),
        1, 'Repeated exposure must not duplicate the view event');
      const count = () => page.evaluate(() => window.__capturedEvents.filter(e => e[1] === 'numerology_calculate').length);
      assert.equal(await count(), 1, 'One successful calculation emits one event');
      await page.locator('#num-go').click();
      await page.waitForFunction(() => window.__capturedEvents.filter(e => e[1] === 'numerology_calculate').length === 2);
      await page.locator('#num-y').fill('');
      await page.locator('#num-go').click();
      await page.waitForTimeout(250);
      assert.equal(await count(), 2, 'Invalid input must not count the previous result');
      await page.evaluate(() => document.addEventListener('click', event => {
        if (event.target.closest('a')) event.preventDefault();
      }));
      await page.locator('a[href^="/oil-"]').first().click();
      await page.locator('a[href^="/article-"]').first().click();
      await page.evaluate(() => {
        for (const [id, href] of [['numeric-oil', '/oil/25/?test=secret#section'],
          ['external-oil', 'https://example.invalid/oil-lavender/']]) {
          const link = document.createElement('a');
          link.id = id; link.href = href; link.textContent = id;
          document.body.appendChild(link);
        }
      });
      await page.locator('#numeric-oil').click();
      const beforeExternal = await page.evaluate(() => window.__capturedEvents.length);
      await page.locator('#external-oil').click();
      assert.equal(await page.evaluate(() => window.__capturedEvents.length), beforeExternal,
        'Cross-origin links must not emit related-reading events');
      const events = await page.evaluate(() => window.__capturedEvents);
      assert(events.some(e => e[1] === 'related_oil_click'));
      assert(events.some(e => e[1] === 'related_article_click'));
      assert(events.some(e => e[2].target_path === '/oil/25/'), 'Numeric routes exclude query and fragment');
      for (const event of events) {
        assert.equal(event[0], 'event');
        assert(Object.keys(event[2]).every(k => ['page_path', 'tool', 'target_path'].includes(k)));
        assert(!JSON.stringify(event).includes('1992'), 'No birthday may be transmitted');
        assert(!JSON.stringify(event).includes('secret'), 'No query may be transmitted');
      }
      await page.evaluate(() => { window.gtag = undefined; window.dataLayer = []; });
      await page.locator('#numeric-oil').click();
      assert(await page.evaluate(() => window.dataLayer.some(e => e[1] === 'related_oil_click'
        && e[2].target_path === '/oil/25/')), 'dataLayer fallback queues the event');
      console.log(`PASS ${width}px: calculation deduplication, invalid input, visible results, related links, privacy`);
      await context.close();
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
