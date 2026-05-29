# -*- coding: utf-8 -*-
"""
gsc_report.py — intelliverse.tw 的 GSC 搜尋表現報告（透過 Maton gateway，不走 MCP）

繞過不穩的 MCP，直接打 Maton 的 GSC searchAnalytics API。
認證沿用 gsc-coverage skill 的 Maton key（env MATON_API_KEY 或 ~/.gcp/maton-api-key.txt）。

模式：
  --mode total      整站 clicks/impressions/ctr/position
  --mode queries    top 關鍵字
  --mode pages      top 頁面
  --mode striking   ⭐「臨門一腳」分析：page×query，排名 8-20 + 有曝光
                    = 推一把就能上第 1 頁的精準目標（附「該頁針對哪個詞優化」）
  --mode all        全部（預設）

  --days N          時間窗（預設 90）
  --site S          GSC property（預設自動偵測 url-prefix / sc-domain）
"""
import os, json, sys, argparse, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

sys.stdout.reconfigure(encoding='utf-8')
GATEWAY = "https://gateway.maton.ai"


def maton_key():
    k = os.environ.get("MATON_API_KEY", "").strip()
    if k:
        return k
    p = os.path.expanduser("~/.gcp/maton-api-key.txt")
    if os.path.exists(p):
        return open(p).read().strip()
    raise SystemExit("Maton API key 缺（env MATON_API_KEY 或 ~/.gcp/maton-api-key.txt）")


def query(site, dims, days=90, limit=1000, filters=None):
    site_enc = urllib.parse.quote(site, safe="")
    url = f"{GATEWAY}/google-search-console/webmasters/v3/sites/{site_enc}/searchAnalytics/query"
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=days)
    body = {"startDate": start.isoformat(), "endDate": end.isoformat(),
            "dimensions": dims, "rowLimit": limit}
    if filters:
        body["dimensionFilterGroups"] = filters
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {maton_key()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode()).get("rows", [])


def detect_site():
    for cand in ["https://intelliverse.tw/", "sc-domain:intelliverse.tw"]:
        try:
            query(cand, [], 30, 1)
            return cand
        except Exception:
            continue
    raise SystemExit("無法連到 intelliverse.tw 的 GSC property（檢查授權）")


def short(u):
    return u.replace("https://intelliverse.tw", "") or "/"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="all",
                    choices=["total", "queries", "pages", "striking", "all"])
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--site", default=None)
    ap.add_argument("--pos-min", type=float, default=8.0, help="striking 排名下限")
    ap.add_argument("--pos-max", type=float, default=20.5, help="striking 排名上限")
    ap.add_argument("--min-impr", type=int, default=3, help="striking 最低曝光")
    args = ap.parse_args()

    site = args.site or detect_site()
    d = args.days
    print(f"# GSC 報告 — {site}（近 {d} 天）\n")

    if args.mode in ("total", "all"):
        rows = query(site, [], d, 1)
        if rows:
            r = rows[0]
            print(f"## 整站\n點擊 {int(r.get('clicks',0))}　曝光 {int(r.get('impressions',0))}　"
                  f"CTR {r.get('ctr',0)*100:.1f}%　平均排名 {r.get('position',0):.1f}\n")

    if args.mode in ("queries", "all"):
        print(f"## Top 關鍵字（by 曝光）")
        for r in sorted(query(site, ["query"], d, 50), key=lambda x: -x["impressions"])[:25]:
            print(f"  曝光{int(r['impressions']):>4} 點擊{int(r['clicks']):>3} "
                  f"CTR{r['ctr']*100:>4.0f}% 排名{r['position']:>5.1f}  {r['keys'][0]}")
        print()

    if args.mode in ("pages", "all"):
        print(f"## Top 頁面（by 曝光）")
        for r in sorted(query(site, ["page"], d, 50), key=lambda x: -x["impressions"])[:20]:
            print(f"  曝光{int(r['impressions']):>4} 點擊{int(r['clicks']):>3} "
                  f"排名{r['position']:>5.1f}  {short(r['keys'][0])}")
        print()

    if args.mode in ("striking", "all"):
        print(f"## ⭐ 臨門一腳（排名 {args.pos_min}-{args.pos_max}，曝光 ≥{args.min_impr}）")
        print(f"   推一把就上第 1 頁的 page×query 組合：")
        rows = query(site, ["page", "query"], d, 2000)
        strike = [r for r in rows
                  if args.pos_min <= r["position"] <= args.pos_max
                  and r["impressions"] >= args.min_impr]
        strike.sort(key=lambda x: -x["impressions"])
        if not strike:
            print("   （目前無符合條件的組合；資料量還在累積）")
        for r in strike[:30]:
            pg = short(r["keys"][0]); kw = r["keys"][1]
            print(f"  曝光{int(r['impressions']):>4} 排名{r['position']:>5.1f} CTR{r['ctr']*100:>4.0f}%  "
                  f"[{kw}] → {pg}")
        # 彙整：每頁的機會關鍵字
        bypage = {}
        for r in strike:
            bypage.setdefault(short(r["keys"][0]), []).append((r["keys"][1], int(r["impressions"]), r["position"]))
        print(f"\n## 機會頁面彙整（該優化哪頁、針對哪些詞）")
        for pg, kws in sorted(bypage.items(), key=lambda x: -sum(k[1] for k in x[1]))[:15]:
            tot = sum(k[1] for k in kws)
            top = "、".join(k[0] for k in sorted(kws, key=lambda x: -x[1])[:4])
            print(f"  {pg}　(總曝光{tot})　關鍵詞：{top}")


if __name__ == "__main__":
    main()
