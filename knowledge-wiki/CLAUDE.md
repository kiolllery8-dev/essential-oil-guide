# 精油能量圖譜知識庫 — Schema

這是一個 Karpathy-pattern LLM wiki，整合 5 本 IFA 芳療經典書籍的知識。

## 知識來源（raw/）

1. IFA 芳療課程 - Joanna Hoare（英系 IFA 標準教材）
2. 破解精油 - Essential Oils Handbook（英法系整合）
3. 天然驅蟲配方手冊 - Naturally Bug Free（75 配方）
4. 方療應用全書 - 呂秀齡（應用實務）
5. 綜合 IFA 芳療聖經教材

## 節點類型

- `oil` — 精油單品（學名、科屬、化學分類、應用）
- `chemistry` — 化學分類（14 大類）
- `molecule` — 化學分子（沉香醇、檸檬烯等）
- `family` — 植物科屬
- `technique` — 芳療技法
- `safety` — 安全知識
- `person` — 芳療史人物
- `school` — 芳療學派與概念
- `usecase` — 應用情境

## 連結語意

- 精油 → 化學分類 / 分子 / 植物科 / 應用 / 學派
- 化學分類 → 分子 / 精油
- 應用情境 → 推薦精油
- 安全知識 → 相關精油
