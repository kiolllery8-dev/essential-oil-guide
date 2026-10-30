import { parseFragment, type DefaultTreeAdapterTypes } from 'parse5';

/** Existing inbound fragments must keep reaching their original subject.
 * Add only IDs to exact, unique existing headings; never rewrite prose or links.
 * Source safety/knowledge files remain byte-for-byte protected by the baseline.
 */
const ANCHORS: Record<string, [string, string][]> = {
  'safety.html': [
    ['buying', '🏷️ 精油品質選購指南'],
    ['children', '👶 嬰幼兒安全'],
    ['dilution', '🛡️ 五大黃金安全原則'],
  ],
  'article-tcm-aromatherapy.html': [
    ['四寒熱屬性對照表', '四、寒熱屬性對照表（精油的「四性」）'],
    ['二十二經絡與對應精油', '二、十二經絡與對應精油'],
    ['三五行金木水火土與精油五大類', '三、五行（金木水火土）與精油五大類'],
  ],
  'oil-bergamot.html': [['四光敏性與12小時避光原則', '⚠️ 重要安全提醒：光敏性']],
  'oil-rose.html': [['三奧圖vs原精兩種萃取的差異', '🌹 玫瑰奧圖 vs 玫瑰原精 vs 玫瑰果油：三者完整比較']],
  'oil-myrrh.html': [['二紅沒藥-vs-沒藥', '四、沒藥 vs 紅沒藥 vs 乳香 — 三者差異']],
  'article-hydrosols.html': [['三5-大主流純露推薦', '三、5 大主流純露推薦']],
  'article-conifers.html': [
    ['三化學成分輪廓比較', '三、化學成分輪廓比較'],
    ['五適用情境快速對照', '五、適用情境快速對照'],
  ],
  'article-spiritual-aromatherapy.html': [
    ['二七個脈輪與精油對應表', '二、七個脈輪與精油對應表'],
    ['四冥想擴香配方', '四、冥想擴香配方（5 種冥想類型）'],
  ],
  'oil-grapefruit.html': [
    ['二化學成分輪廓', '二、化學成分輪廓'],
    ['四藥物交互作用葡萄柚效應', '⚠️ 重要安全資訊：葡萄柚精油與藥物交互作用（「葡萄柚效應」）'],
  ],
  'oil-geranium.html': [['二三大產地比較', '🌏 三大產地完整比較']],
};

const escapeRegex = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

export function addLegacyAnchors(filename: string, html: string): string {
  if (!ANCHORS[filename]) return html;
  // HTML parsing handles attribute case, whitespace, unquoted values and
  // character references exactly before comparing DOM IDs. Never serialize:
  // only the original matching opening tag receives the additional attributes.
  const existingIds = new Set<string>();
  function collect(node: DefaultTreeAdapterTypes.Node) {
    if ('attrs' in node) {
      for (const attr of node.attrs) if (attr.name === 'id') existingIds.add(attr.value);
    }
    if ('childNodes' in node) node.childNodes.forEach(collect);
    if ('content' in node) collect(node.content);
  }
  collect(parseFragment(html));
  for (const [id, text] of ANCHORS[filename] || []) {
    const target = new RegExp(`(<(h[2-4]|div)\\b[^>]*)(>)${escapeRegex(text)}(</\\2>)`, 'g');
    const matches = [...html.matchAll(target)];
    if (matches.length !== 1 || /\bid\s*=/i.test(matches[0][1]) ||
        existingIds.has(id)) {
      throw new Error(`Legacy anchor target changed: ${filename}#${id}`);
    }
    html = html.replace(target, (_whole, open, _tag, close, end) => `${open} id="${id}" data-legacy-anchor${close}${text}${end}`);
  }
  return html;
}
