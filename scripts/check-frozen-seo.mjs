/**
 * check-frozen-seo.mjs — 凍結指定頁面的 SEO 招牌欄位，任何改動都擋下來。
 *
 * 起因：2026-08-09 玉玲要求 /numerology/ 的 title 一個字元都不能動
 * （該頁是全站流量第一：30 天 115 次點擊、平均第 4.85 名，30 個關鍵字）。
 * 這些字串是靠比對「精確內容」而非 hash，出錯時能直接看出差在哪。
 *
 * 用法：node scripts/check-frozen-seo.mjs
 * 回傳碼 0 = 全部沒動；1 = 有欄位被改（印出 expected / actual 逐項對照）。
 */
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

/** 凍結清單：檔案 → 欄位 → 必須完全相符的字串 */
const FROZEN = [
  {
    file: 'html-source/numerology.html',
    url: '/numerology/',
    reason: '全站流量第一頁，30 個關鍵字在排（生命靈數配對計算 #1、九宮格免費算 #3）',
    fields: {
      title:
        '生命靈數計算機｜免費算主命數＋1-9號人解析、配對與九宮格 | 精油能量圖譜',
      description:
        '輸入西元生日，免費計算你的生命靈數主命數、九宮格連線與空缺數，並附 1-9 號人完整性格解析、生命靈數配對速配表與對應精油方向。源自畢達哥拉斯占數，結合芳香療法的自我探索工具。',
    },
  },
];

const extract = {
  title: (raw) => raw.match(/<title>([\s\S]*?)<\/title>/)?.[1],
  description: (raw) =>
    raw.match(/<meta\s+name="description"\s+content="([\s\S]*?)"/)?.[1],
};

let failed = 0;

for (const entry of FROZEN) {
  let raw;
  try {
    raw = readFileSync(join(ROOT, entry.file), 'utf-8');
  } catch {
    console.error(`✗ ${entry.file} 讀不到——凍結頁不該被刪除或改名`);
    failed++;
    continue;
  }

  for (const [field, expected] of Object.entries(entry.fields)) {
    const actual = extract[field](raw);
    if (actual === expected) {
      console.log(`✓ ${entry.url} ${field} 未變動`);
      continue;
    }
    failed++;
    console.error(`\n✗ ${entry.url} 的 ${field} 被改了`);
    console.error(`  原因：${entry.reason}`);
    console.error(`  應為：${expected}`);
    console.error(`  現為：${actual ?? '（找不到這個欄位）'}`);
    if (actual) {
      // 指出第一個不同的字元位置，避免肉眼比對全形／半形符號
      const n = Math.min(expected.length, actual.length);
      let i = 0;
      while (i < n && expected[i] === actual[i]) i++;
      const cp = (s) =>
        s[i] === undefined
          ? '（結束）'
          : `U+${s.codePointAt(i).toString(16).toUpperCase().padStart(4, '0')} ${JSON.stringify(s[i])}`;
      console.error(`  第 ${i + 1} 個字元起不同： 應為 ${cp(expected)}／現為 ${cp(actual)}`);
    }
  }
}

if (failed) {
  console.error(`\n凍結檢查失敗：${failed} 個欄位被改動。`);
  console.error('這些欄位是刻意鎖住的。真的要改，請先跟玉玲確認，再更新本檔的 FROZEN 清單。');
  process.exit(1);
}
console.log('\n凍結檢查通過：招牌欄位全部原封不動。');
