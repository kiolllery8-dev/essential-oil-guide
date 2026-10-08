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
      await page.locator('#num-result h2, #num-result h3').first().scrollIntoViewIfNeeded();
      await page.waitForFunction(() => window.__capturedEvents.some(e => e[1] === 'numerology_result_view'));
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
      const events = await page.evaluate(() => window.__capturedEvents);
      assert(events.some(e => e[1] === 'related_oil_click'));
      for (const event of events) {
        assert.equal(event[0], 'event');
        assert(Object.keys(event[2]).every(k => ['page_path', 'tool', 'target_path'].includes(k)));
        assert(!JSON.stringify(event).includes('1992'), 'No birthday may be transmitted');
      }
      console.log(`PASS ${width}px: calculation deduplication, invalid input, visible results, related links, privacy`);
      await context.close();
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
