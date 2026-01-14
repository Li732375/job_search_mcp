# -*- coding: utf-8 -*-
from app.services.spyE04 import SpyE04
from app.services.job_crawl_flow import crawl_E04_jobs
from app.services.log import clear_error_log
    

app = FastMCP("I-Want-Jobs-All")

@app.tool()
def crawl_e04_jobs() -> None:
    """
    依據 config.py 條件設定，爬取 e04 全部職缺
    """
    
    spider = SpyE04()
    crawl_E04_jobs(spider)

@app.tool()
def clear_logs() -> None:
    """清除錯誤紀錄檔案"""
    
    clear_error_log()


def init():
    """初始化"""
    
    clear_error_log()  # 清空錯誤紀錄


if __name__ == "__main__":
    init()
    app.run()
