# I-Want-Jobs-All

## 專案簡介

一個基於 FastMCP 的職缺爬蟲服務。本專案可在本機啟動 MCP Server，提供工具給 ChatGPT（MCP Client） 呼叫，由 AI 觸發職缺蒐集並輸出成 CSV 檔案。

特色：

* 支援單一或複合條件篩選職缺。
* 提供 MCP 介面，可讓 AI 或其他程式呼叫。

---

## 功能列表

1. **職缺資料抓取**

   * 支援單一或複合條件篩選職缺（學歷、經驗、工作型態、薪資、地區等）。
   * 可取得職缺詳細資訊（薪資範圍、公司、地址、福利、擅長要求等）。
   * CSV 輸出，可自訂欄位順序。

2. **MCP 介面**

   * 透過 FastMCP 將爬蟲方法提供給 AI 代理呼叫。
   * 可呼叫方法（對，目前僅一個！）：
        - `crawl_e04_jobs()`：抓取多個職缺。

3. **錯誤紀錄**

   * 自動將爬蟲錯誤寫入 `error_message.json`。
   * 可用於檢查抓取異常或反爬機制阻擋。

---

## 安裝與依賴

```bash
pip install -r requirements.txt
```

`requirements.txt` 內容：

```
fastmcp==2.14.2
playwright==1.57.0
playwright_stealth==2.0.0
pydantic==2.12.5
Requests==2.32.5
```

---

## 專案架構

```
dev/
│  main.py                  
│  agent_tools.py           # MCP 工具介面
│  README.md
│
└─app/
    │  config.py            # 篩選條件設定、欄位順序
    │  agent_tools.py       # MCP 介面
    │
    ├─extractors/           
    ├─schemas/
    │      job_schema.py    # 職缺資料結構
    │
    └─services/
           job_crawl_flow.py # 爬蟲流程封裝
           spyE04.py         # 職缺爬蟲實作
```

---

## 使用說明

### 1️⃣ 啟動 MCP 伺服器（本地）

```bash
python agent_tools.py
```

### 2️⃣ 呼叫介面抓取職缺

* 透過 MCP 或 FastMCP 提供的 API，代理 AI 可呼叫：

```python
crawl_e04_jobs():
"""
爬取 E04 全部職缺，執行後會抓取職缺並生成 CSV
"""
```
存檔：
```
job_list_YYYY-MM-DD-HH-MM.csv
```

---

## 注意事項

1. 請勿頻繁抓取，以免 IP 被網站封鎖。
2. CSV 若出現亂碼，可用文字編輯器另存為 ANSI。
3. 若 CSV 格子過高，可取消 Excel 的「自動換行」。
4. 爬取大量職缺（>4000 筆）可能耗時數小時。
