# -*- coding: utf-8 -*-
from app.services.spyE04 import SpyE04
from app.services.job_crawl_flow import crawl_E04_jobs


def main():
    spider = SpyE04()
    crawl_E04_jobs(spider)

if __name__ == "__main__":
    main()
