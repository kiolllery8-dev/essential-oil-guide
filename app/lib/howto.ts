/** HowTo schema for aromatherapy page */

const CDN = 'https://cdn.jsdelivr.net/gh/kiolllery8-dev/essential-oil-cdn@main/images/';

export interface HowToStep {
  name: string;
  text: string;
  image?: string;
}

export function howToSchema(opts: {
  name: string;
  description: string;
  totalTime: string; // ISO 8601 duration e.g. "PT10M"
  image?: string;
  tools?: string[];
  supplies?: string[];
  steps: HowToStep[];
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'HowTo',
    name: opts.name,
    description: opts.description,
    totalTime: opts.totalTime,
    ...(opts.image ? { image: opts.image } : {}),
    ...(opts.tools ? {
      tool: opts.tools.map((t) => ({ '@type': 'HowToTool', name: t })),
    } : {}),
    ...(opts.supplies ? {
      supply: opts.supplies.map((s) => ({ '@type': 'HowToSupply', name: s })),
    } : {}),
    step: opts.steps.map((s, i) => ({
      '@type': 'HowToStep',
      position: i + 1,
      name: s.name,
      text: s.text,
      ...(s.image ? { image: s.image } : {}),
    })),
  };
}

export const AROMATHERAPY_HOWTOS = [
  howToSchema({
    name: '如何用超聲波水氧機擴香精油',
    description: '正確使用水氧機擴香，讓精油分子均勻擴散至室內空氣，達到情緒調節與空氣淨化效果。',
    totalTime: 'PT5M',
    image: `${CDN}hero-aroma.png`,
    tools: ['超聲波水氧機', '量杯'],
    supplies: ['純水或蒸餾水', '精油（3-5 滴）'],
    steps: [
      { name: '準備純水', text: '量取 50-100ml 純水或蒸餾水，避免使用自來水以防礦物質堵塞噴霧孔。' },
      { name: '倒入水箱', text: '將水倒入水氧機水箱，不超過 MAX 標線。' },
      { name: '滴入精油', text: '每 100ml 水滴 3-5 滴精油；10 坪以內空間 3 滴，超過 10 坪可增至 5-8 滴。' },
      { name: '蓋上蓋子啟動', text: '蓋緊水箱蓋，按下啟動鍵，選擇連續霧化或間歇模式。' },
      { name: '控制時間', text: '單次建議 30-60 分鐘後休息，避免長時間在密閉空間高濃度吸入；孕婦、嬰幼兒、寵物在場時請降低劑量或離開。' },
    ],
  }),
  howToSchema({
    name: '如何調配精油按摩油（稀釋）',
    description: '將純精油安全稀釋成按摩油，適合日常皮膚保養、肌肉放鬆、舒緩不適。',
    totalTime: 'PT3M',
    image: `${CDN}hero-aroma.png`,
    tools: ['10ml 深色玻璃瓶', '滴管'],
    supplies: ['基底油 10ml（荷荷芭 / 甜杏仁 / 椰子分餾油）', '精油 3-6 滴'],
    steps: [
      { name: '選擇基底油', text: '10ml 基底油建議首選荷荷芭油（最接近皮脂、保存久）；敏感肌用甜杏仁；油性肌用椰子分餾油。' },
      { name: '決定稀釋比例', text: '成人一般 3%（10ml + 6 滴）；臉部 1%（2 滴）；兒童 0.5-1%；懷孕 1% 以下。' },
      { name: '倒入深色玻璃瓶', text: '將基底油倒入 10ml 深色玻璃瓶（琥珀色或鈷藍色避免光照氧化）。' },
      { name: '滴入精油', text: '依稀釋比例滴入精油，蓋緊後緩慢翻轉搖勻 30 秒。' },
      { name: '貼膚測試', text: '首次使用取少量塗抹手肘內側，24 小時觀察是否紅腫、癢、疹；無反應才可正式使用。' },
    ],
  }),
  howToSchema({
    name: '如何正確使用精油泡澡',
    description: '精油泡澡能協助肌肉放鬆、促進循環、改善睡眠，但需先乳化避免直接刺激皮膚。',
    totalTime: 'PT25M',
    image: `${CDN}hero-aroma.png`,
    supplies: ['乳化劑（全脂牛奶 / 蜂蜜 / 基底油）1 湯匙', '精油 5-8 滴'],
    steps: [
      { name: '放溫水', text: '放好 37-40°C 溫水（過熱會加速精油蒸發與皮膚刺激）。' },
      { name: '調製乳化劑', text: '在小碗內加 1 湯匙全脂牛奶、蜂蜜或基底油，滴入 5-8 滴精油充分攪拌（精油不溶於水，必須先乳化）。' },
      { name: '倒入浴缸', text: '將乳化後的精油倒入水中，用手輕撥攪散 10 秒。' },
      { name: '浸泡', text: '浸泡 15-20 分鐘；避免泡到水面下的精油直接接觸黏膜（眼、口、會陰）。' },
      { name: '起身清潔', text: '起身後以溫水快速沖淨，用毛巾拍乾（不要搓），可再擦一層保濕乳液。' },
    ],
  }),
  howToSchema({
    name: '如何製作隨身滾珠精油瓶',
    description: '自製 10ml 滾珠瓶隨身精油，太陽穴舒緩頭痛、手腕提神、頸後放鬆。',
    totalTime: 'PT3M',
    image: `${CDN}hero-aroma.png`,
    tools: ['10ml 滾珠瓶', '小漏斗'],
    supplies: ['基底油 9ml（荷荷芭最佳）', '精油 6-10 滴'],
    steps: [
      { name: '準備滾珠瓶', text: '使用 10ml 不鏽鋼滾珠瓶（抗氧化、不易污染）；深色玻璃保存久。' },
      { name: '倒入基底油', text: '用漏斗將 9ml 基底油倒入瓶中，預留 1ml 空間給精油。' },
      { name: '滴入精油', text: '依目的配方滴入 6-10 滴精油（3-5% 濃度）：提神 = 薄荷 3 + 迷迭香 3；放鬆 = 薰衣草 4 + 甜橙 3。' },
      { name: '裝回滾珠蓋', text: '將滾珠頭壓回瓶口，蓋上外蓋，倒轉搖勻 30 秒。' },
      { name: '使用', text: '塗抹太陽穴（頭痛）、手腕（情緒）、頸後（提神）、胸口（呼吸）。一天 3-5 次皆可。' },
    ],
  }),
];
