/** /oil/[id] datasheet → 對應完整指南 /oil-X/ 的 canonical 收編表。
 *  共用於 app/oil/[id]/page.tsx（canonical/麵包屑/導流按鈕）與 app/sitemap.ts（排除非 canonical URL）。
 *  來源：手動對照 oils.json 與 46 個 oil-*.html 完整指南。 */
export const CANONICAL_OVERRIDES: Record<string, string> = {
  // 柑橘類
  '34': 'oil-lemon', '310': 'oil-lemon',
  '144': 'oil-lemon-eucalyptus',
  '159': 'oil-petitgrain',
  '160': 'oil-bergamot',
  '218': 'oil-neroli',
  '311': 'oil-grapefruit',
  // 花朵類
  '182': 'oil-jasmine',
  '192': 'oil-rose', '234': 'oil-rose',
  '207': 'oil-helichrysum',
  // 菊科
  '92': 'oil-yarrow',
  '108': 'oil-german-chamomile',
  '157': 'oil-roman-chamomile',
  // 薰衣草系
  '82': 'oil-spike-lavender',
  '165': 'oil-lavender', '209': 'oil-lavender',
  '166': 'oil-lavandin',
  // 香草類
  '47': 'oil-rosemary', '87': 'oil-rosemary',
  '150': 'oil-melissa',
  '171': 'oil-clary-sage',
  '222': 'oil-palmarosa',
  '230': 'oil-sweet-basil',
  '233': 'oil-geranium',
  '238': 'oil-thyme',
  // 薄荷類
  '41': 'oil-spearmint',
  '42': 'oil-peppermint', '226': 'oil-peppermint',
  // 呼吸類
  '72': 'oil-bay',
  '73': 'oil-ravintsara',
  '76': 'oil-eucalyptus',
  '224': 'oil-tea-tree',
  // 木質/松柏
  '102': 'oil-myrrh',
  '201': 'oil-cedarwood',
  '285': 'oil-patchouli',
  '287': 'oil-sandalwood',
  '292': 'oil-vetiver',
  '315': 'oil-cypress',
  '320': 'oil-juniper',
  '325': 'oil-black-spruce',
  // 辛香類
  '120': 'oil-ginger',
  '143': 'oil-citronella',
  '252': 'oil-clove',
  '330': 'oil-black-pepper',
  // 樹脂・其他
  '124': 'oil-sweet-fennel',
  '301': 'oil-frankincense',
  // 柑橘類
  '97': 'oil-ylang-ylang',
};
