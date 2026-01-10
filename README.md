# I-Want-Jobs-All

## 專案簡介

一個建立於 FastMCP 的職缺服務 MCP。透過在本機啟動 MCP Server，提供工具給代理（Agent）呼叫，提供 **謀職** 相關服務。

---

## 功能列表

1. **MCP 介面**（對，目前僅一個！）

    - 職缺資料抓取
        - 搜刮自數字網站
        - 透過自行修改 config.py 設定條件（條件參見 [wiki](https://github.com/Li732375/JobE04_spider/wiki)）。

            > 就是網址那段冗長條件參數內容啦！

        - 支援單一或複合條件篩選職缺（學歷、經驗、工作型態、薪資、地區等）。
        - 取得職缺詳細資訊（薪資範圍、公司、地址、福利、擅長要求等）。
        - 輸出 CSV，可自訂欄位順序。
        - 錯誤將自動寫入 `error_message.json`，檢查抓取異常或反爬機制阻擋。

    - 新功能持續開發中...

---

## 安裝依賴套件

```bash
pip install -r requirements.txt
```

---

## 專案架構

```
.
│  .gitignore
│  agent_tools.py               # MCP 介面、伺服器
│  main.py 
│  README.md
│  requirements.txt             # 依賴套件
│
└─app 
    │ config.py                 # 條件、欄位順序
    │
    ├─extractors
    ├─schemas
    │  └─ job_schema.py         # 職缺資料格式
    │
    └─services
       │  job_crawl_flow.py     # 流程封裝
       └─ spyE04.py             # 介面功能實作
```

---

## 使用說明

### 1️⃣ 啟動 MCP 伺服器（本地）

```bash
python agent_tools.py
```

### 2️⃣ 連接 Agent 程式

參見各平台 MCP Server 添加辦法

---

## 注意事項

1. 請勿頻繁抓取，以免 IP 被網站封鎖。
2. 若 CSV 格子過高，可取消 Excel 的「自動換行」。
3. 抓取大量職缺（>4000 筆）可能耗時數小時。
