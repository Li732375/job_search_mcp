# -*- coding: utf-8 -*-
from .services.spyE04 import SpyE04
from .services.job_crawl_flow import crawl_E04_jobs


from fastmcp import FastMCP
    

app = FastMCP("I-Want-Jobs-All")

@app.tool()
def crawl_e04_jobs() -> None:
    """
    爬取 e04 全部職缺
    """
    
    spider = SpyE04()
    crawl_E04_jobs(spider)
