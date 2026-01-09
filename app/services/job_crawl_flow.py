# -*- coding: utf-8 -*-
from dev.app.services.spyE04 import SpyE04

import time
import json


def crawl_E04_jobs(spider: SpyE04) -> None:
    """爬取 E04 職缺主流程"""
    
    spider = SpyE04()

    # 取得篩選條件
    uni_params = spider.uni_filter_params
    mul_params = spider.mul_filter_params

    # 產生組合
    keys, combinations = spider.generate_filter_combinations(mul_params)
    print(f"開始搜尋職缺 ID（組合數：{len(combinations)}）")

    # 搜尋職缺 ID
    job_ids = spider.collect_job_ids(
        uni_filter_param = uni_params,
        keys = keys,
        combinations = combinations,
    )
    print(f"共取得 {len(job_ids)} 筆職缺")

    # 抓詳情並寫入 CSV (格式 2026-01-05-13-45)
    output_file = f"job_list_{time.strftime('%Y-%m-%d-%H-%M')}.csv"
    spider.fetch_jobs_and_write_csv(job_ids, output_file)

    # 依是否有錯誤紀錄，調整輸出結果
    with open('error_message.json', 'r', encoding='utf-8-sig') as f:
        errors = json.load(f)
    if errors:
        print(f"\n任務完成！\n資料已寫入 {output_file}\n[錯誤] 請查看 error_message.json")
    else:
        print(f"\n任務完成！\n資料已寫入 {output_file}")