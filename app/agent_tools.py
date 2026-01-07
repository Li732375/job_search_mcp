# -*- coding: utf-8 -*-
from typing import List
from app.schemas.job import JobSchema
from app.services.E04 import SpyE04
from app.services.job_crawl_flow import crawl_all_jobs

from fastmcp import FastMCP
    

app = FastMCP("I-Want-Jobs-All")

@app.tool()
def crawl_e04_jobs() -> List[dict]:
    """
    爬取 e04 全部職缺，回傳結構化資料
    """
    spider = SpyE04()
    jobs: List[JobSchema] = crawl_all_jobs(spider)

    # MCP 只能傳 JSON-friendly 結構
    return [job.model_dump() for job in jobs]