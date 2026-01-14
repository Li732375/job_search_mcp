from app.services.spyE04 import SpyE04
from app.services.log import is_log_exists


def crawl_E04_jobs(spider: SpyE04) -> None:
    """爬取 E04 職缺主流程"""

    # 產生組合
    keys, combinations = spider.generate_filter_combinations()
    print(f"開始搜尋職缺 ID（組合數：{len(combinations)}）")

    # 搜尋職缺 ID
    job_id_set = spider.collect_job_ids(
        keys = keys,
        combinations = combinations,
    )
    print(f"共取得 {len(job_id_set)} 筆職缺")

    # 抓詳情並寫入資料庫
    spider.fetch_jobs_and_write_sqlite(job_id_set)

    # 依是否有錯誤紀錄，調整輸出結果
    if is_log_exists():
        print(f"\n任務完成！\n[錯誤] 請查看錯誤紀錄檔案以了解詳情。")
    else:
        print(f"\n任務完成！")
        