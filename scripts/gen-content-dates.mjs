/**
 * gen-content-dates.mjs — 從 git 歷史產出每頁「真實內容更新日期」
 * 輸出 data/content-dates.json：{ "<slug>": "YYYY-MM-DD", "data/oils.json": "YYYY-MM-DD" }
 * 供 sitemap lastmod 與 Article dateModified 使用（取代「每次 build 都是今天」的假更新訊號）。
 *
 * 淺 clone（CI fetch-depth=1）時 git 日期全部等於 HEAD，會失真 → 直接沿用已 commit 的 JSON。
 * deploy workflow 已設 fetch-depth: 0，CI 端也能精確重算。
 */
import { execSync } from 'node:child_process';
import { readdirSync, writeFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const OUT = join(ROOT, 'data', 'content-dates.json');

function sh(cmd) {
  return execSync(cmd, { cwd: ROOT, encoding: 'utf8' }).trim();
}

let depth = 0;
try { depth = parseInt(sh('git rev-list --count HEAD'), 10); } catch { /* 無 git */ }
if (!depth || depth <= 1) {
  console.log(`[content-dates] git 歷史不足（depth=${depth}），沿用既有 JSON`);
  if (!existsSync(OUT)) writeFileSync(OUT, '{}\n');
  process.exit(0);
}

const dates = {};
const files = readdirSync(join(ROOT, 'html-source')).filter((f) => f.endsWith('.html'));
for (const f of files) {
  try {
    const iso = sh(`git log -1 --format=%cI -- "html-source/${f}"`);
    if (iso) dates[f.replace(/\.html$/, '')] = iso.slice(0, 10);
  } catch { /* 未入 git 的新檔跳過 */ }
}
try { dates['data/oils.json'] = sh('git log -1 --format=%cI -- "data/oils.json"').slice(0, 10); } catch {}

writeFileSync(OUT, JSON.stringify(dates, null, 2) + '\n');
console.log(`[content-dates] 寫出 ${Object.keys(dates).length} 筆 → data/content-dates.json`);
