# -*- coding: utf-8 -*-
from app.services.spyE04 import SpyE04
from app.services.job_crawl_flow import crawl_E04_jobs
from app.services.log import clear_error_log
    

def crawl_E04():
    '''純本地測試/執行用，可以在不啟動 MCP 伺服器時直接執行爬蟲流程'''
    
    spider = SpyE04()
    crawl_E04_jobs(spider)

def init():
    """初始化"""
    
    clear_error_log()  # 清空錯誤紀錄


if __name__ == "__main__":
    init()
    crawl_E04()
