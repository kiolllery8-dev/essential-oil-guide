# 全站自動維護

啟用日期：2026-10-08，Asia/Taipei。

全站既有 416 個正式內容路由已建立 `data/maintenance-baseline.json`。每次部署在 build 後檢查既有 title、description、canonical、robots、URL 與受保護精油資料／生命靈數生成器／安全頁；不通過就不能上傳或部署。

正常自動維護不得修改基準檔或檢查程式來繞過驗證。新增頁可以增加，不得刪除或取代原頁；新頁也需有完整 metadata。使用者提供的原文不得删減，安全建議與算法變更不屬一般內容自動修改。

主機 worker：`/home/user/essential-oil-agent/bin/agent.py`。
主機狀態：`/home/user/essential-oil-agent/state/{health,full}.json`。
主機報告：`/home/user/essential-oil-agent/reports/latest.md`。

`essential-oil-health.timer` 每 15 分鐘巡檢核心頁；`essential-oil-full.timer` 每天台灣時間 03:20 掃描全部基準頁、sitemap 頁與站內連結發現的頁面，檢查 HTTP、metadata 漂移、站內連結、anchor 及圖片資源。動態產生的 anchor 可能不在伺服器 HTML，需功能驗證後再判為錯誤。HTTP 巡檢不能代表桌機／手機 UI 或計算器功能通過。

Codex 聊天室巡檢接手全站待辦與後續建置，平常無變化保持安靜。主機巡檢不依賴桌面 App；Codex 後續程式修復、內容製作及通知仍依賴其排程可執行、登入與額度有效。

自動發布需先完成獨立審核、正式 build、全站基準比較、變更影響的功能／版面驗證與回復演練。不能把此文件當成已完成所有驗收的證明。不得 force push；遠端更新先同步重驗；GitHub Pages 回復需確認不撤銷他人後續修改。

停止主機掃描：`sudo systemctl stop essential-oil-health.timer essential-oil-full.timer`。
暫停 worker：將私有 `state/config.json` 的 `paused` 設為 true。
恢復依相同 timer 及原始基準，不能重建基準來接受漂移。
