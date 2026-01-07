# -*- coding: utf-8 -*-
from app.services.E04 import E04Spy
from app.services.job_crawl_flow import crawl_all_jobs


def main():
    spider = E04Spy()
    jobs = crawl_all_jobs(spider)

    print(f"共取得 {len(jobs)} 筆職缺")


if __name__ == "__main__":
    main()
