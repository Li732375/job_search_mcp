from typing import Dict, List, Optional, Tuple, Any, Set
from app.schemas.job import JobSchema
from config import UNI_FILTER_PARAMS, MUL_FILTER_PARAMS, FIELD_NAMES_ORDER

import time
import random
import requests
from itertools import product
import csv
import json
import sys
import os
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

# 設定標準輸出編碼
sys.stdout.reconfigure(encoding='utf-8-sig')


class E04Spy():
    def __init__(self):
        self.session = requests.Session()
        self.headers_user_agent: str = ""
        self.error_log_file: str = 'error_message.json'

        self._uni_filter_params: Dict[str, str] = UNI_FILTER_PARAMS
        self._mul_filter_params: Dict[str, str] = MUL_FILTER_PARAMS
        self._field_names_order: List[str] = FIELD_NAMES_ORDER


        # 寫入空列表，清空舊紀錄
        with open(self.error_log_file, 'w', encoding='utf-8-sig') as f:
            json.dump("", f)

        self.refresh_session()

    @property
    def uni_filter_params(self) -> Dict[str, str]:
        return self._uni_filter_params
    
    @uni_filter_params.setter
    def uni_filter_params(self, value: Dict[str, str]) -> None:
        if not isinstance(value, dict):
            raise TypeError("uni_filter_params 必須是 dict")
        self._uni_filter_params = value
    
    @property
    def mul_filter_params(self) -> Dict[str, str]:
        return self._mul_filter_params
    
    @mul_filter_params.setter
    def mul_filter_params(self, value: Dict[str, str]) -> None:
        if not isinstance(value, dict):
            raise TypeError("mul_filter_params 必須是 dict")
        self._mul_filter_params = value

    @property
    def field_names_order(self) -> Dict[str]:
        return self._field_names_order
    
    @field_names_order.setter
    def field_names_order(self, value: Dict[str]) -> None:
        if not isinstance(value, dict):
            raise TypeError("field_names_order 必須是 dict")
        self._field_names_order = value

    def log_error(self, 
                  job_id: str, 
                  message: Any, 
                  raw_data: Optional[Any]=None) -> None:
        """將錯誤訊息與原始資料存入 JSON 檔案"""
        error_entry = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'job_id': job_id,
            'error_message': str(message),
            'raw_data': raw_data
        }
        
        # 讀取現有紀錄並更新
        data = []
        if os.path.exists(self.error_log_file):
            try:
                with open(self.error_log_file, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
            except:
                data = []
        
        data.append(error_entry)
        with open(self.error_log_file, 'w', encoding='utf-8-sig') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def refresh_session(self) -> None:
        print("正在啟動隱身瀏覽器通過驗證...", end='', flush=True)
        with Stealth().use_sync(sync_playwright()) as p:
            browser = p.chromium.launch(headless=True)
            
            # 模擬主流解析度，規避自動化偵測並確保網頁完整載入
            context = browser.new_context(viewport={'width': 1920, 
                                                    'height': 1080})
            page = context.new_page()
            
            try:
                page.goto('https://www.104.com.tw/', 
                          wait_until="domcontentloaded",  # 避免 networkidle 超時
                          timeout=60000  # 最多等待 60 秒
                          )
                # 短暫隨機等待(JavaScript 初始化完成，cookie/session 可用以及模擬真人停留時間)
                time.sleep(random.uniform(0.5, 3))
                self.headers_user_agent = page.evaluate("navigator.userAgent")
                cookies = context.cookies()
                for cookie in cookies:
                    self.session.cookies.set(cookie['name'], cookie['value'], 
                                             domain=cookie['domain'])
                print("已更新憑證")
            except Exception as e:
                self.log_error("SYSTEM", f"驗證失敗: {e}")
            finally:
                browser.close()

    def fetch_with_retry(self, url: str, 
                         headers: Optional[Dict[str, str]]=None, 
                         params: Optional[Any]=None, 
                         max_retries: int = 3
                         ) -> Optional[requests.Response]:
        attempt = 0
        if headers is None: headers = {}
        headers['User-Agent'] = self.headers_user_agent
        headers['Referer'] = 'https://www.104.com.tw/'

        while attempt < max_retries:
            try:
                r = self.session.get(url, headers=headers, params=params, 
                                     timeout=15)
                if r.status_code == 200: return r

                if r.status_code in (429, 403):
                    self.refresh_session()
                    time.sleep(random.uniform(5, 10))
                    attempt += 1
                    continue
                return None
            
            except Exception as e:
                attempt += 1
                time.sleep(2)
        return None

    def search(self, 
               max_num: int =150, 
               filter_params: Optional[Dict[str, str]]=None) -> List[str]: 
        jobs = []
        query_parts = ['jobsource=index_s', 'mode=s']

        if filter_params:
            for k, v in filter_params.items():
                query_parts.append(f'{k}={v}')

        query = '&'.join(query_parts)
        url = 'https://www.104.com.tw/jobs/search/api/jobs'
        headers = {'Accept': 'application/json, text/plain, */*'}
        page = 1
        
        while max_num == -1 or len(jobs) < max_num:
            full_params = f'{query}&page={page}&pagesize=20'
            r = self.fetch_with_retry(url, headers=headers, params=full_params)
            if r is None: break

            try:
                datas = r.json()
                if 'data' not in datas: break
                jobs.extend(data['link']['job'].split('/job/')[-1] for data in datas['data'])
                if page >= datas['metadata']['pagination']['lastPage']: break
                time.sleep(random.uniform(1, 2))
                page += 1
                
            except Exception as e:
                self.log_error("SEARCH", e)
                break

        return jobs[:max_num]

    def get_job(self, job_id: str) -> Optional[JobSchema]:
        url = f'https://www.104.com.tw/job/ajax/content/{job_id}'
        headers = {'Referer': f'https://www.104.com.tw/job/{job_id}', 
                   'Accept': 'application/json'}
        
        r = self.fetch_with_retry(url, headers=headers)
        if r is None: return None
        job_data = None

        try:
            resp_json = r.json()
            job_data = resp_json.get('data')
            if not job_data or job_data.get('switch') == 'off': return None

            salary_map = {
                10: '面議', 
                20: '論件計酬', 
                30: '時薪', 
                40: '日薪', 
                50: '有薪', 
                60: '年薪', 
                70: '其他',
                }
            header = job_data.get('header', {})
            job_detail = job_data.get('jobDetail', {})
            condition = job_data.get('condition', {})
            welfare = job_data.get('welfare', {})
            workType = ', '.join(job_detail.get('workType', [])) or '全職'
            raw_area = job_detail.get('addressRegion', "")
            jobArea = raw_area if len(raw_area) == 3 else raw_area[3:]
            workPeriod = job_detail.get('workPeriod', {})
            work_shift = ' '.join(workPeriod.get('shifts', {}).keys())
            duty_time = workPeriod.get('note', '')
            
            data_info = JobSchema(
                    id = job_id,
                    posted_date = header.get('appearDate'), 
                    work_type = workType,
                    work_shift = f"{work_shift} {duty_time}".strip() or '無',
                    salary_type = salary_map.get(job_detail.get('salaryType'), '其他'),
                    salary_min = int(job_detail.get('salaryMin', 0)),
                    salary_max = int(job_detail.get('salaryMax', 0)),
                    job_name = header.get('jobName'),
                    education = condition.get('edu'),
                    experience = condition.get('workExp'),
                    addressArea = job_detail.get('addressArea'),
                    job_area = jobArea,
                    address_detail = job_detail.get('addressDetail') or '無',
                    company_name = header.get('custName'),
                    job_description = job_detail.get('jobDescription') or '無',
                    other_description = condition.get('other') or '無',
                    specialt = ', '.join(item.get('description', '') for item in condition.get('specialty', [])) or '無',
                    certificate = ', '.join(item.get('name', '') for item in condition.get('certificate', [])) or '無',
                    driver_license = ', '.join(condition.get('driverLicense', [])) or '無',
                    business_trip = job_detail.get('businessTrip') or '無',
                    job_url = f'https://www.104.com.tw/job/{job_id}?apply=form',
                    industry = job_data.get('industry'),
                    legal_welfare = ', '.join(welfare.get('legalTag', [])) or '無',
            )
            
            return data_info
        
        except Exception as e:
            self.log_error(job_id, e, raw_data=job_data)
            return None

    def generate_filter_combinations(self, 
                                     mul_filter_params: Dict[str, str]
                                     ) -> Tuple[List[str], List[Tuple[str, ...]]]:
        keys: List[str] = list(mul_filter_params.keys())
        values: List[List[str]] = [v.split(',') for v in mul_filter_params.values()]
        combinations: List[Tuple[str, ...]] = list(product(*values))
        return keys, combinations
    
    def collect_job_ids(self, 
                        uni_filter_params: Dict[str, str], 
                        keys: List[str], 
                        combinations: List[Tuple[str, ...]]
                        , max_num: int = 20
                        ) -> Set[str]:
        alljobs_set: Set[str] = set()

        for idx, combo in enumerate(combinations, 1):
            filter_params: Dict[str, str] = {
                **uni_filter_params,
                **dict(zip(keys, combo))
            }
            jobs: List[str] = self.search(max_num=max_num, filter_params=filter_params)
            alljobs_set.update(jobs)
            print(f"進度：{(idx/len(combinations))*100:6.2f} % | 累計職缺：{len(alljobs_set)}", end='\r')

        return alljobs_set
    
    def fetch_jobs_and_write_csv(self, 
                                 job_ids: Set[str], 
                                 output_file: str) -> None:
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self._field_names_order)
            writer.writeheader()

            for idx, job_id in enumerate(job_ids, 1):
                info = self.get_job(job_id)
                if info:
                    writer.writerow({k: info.get(k, '無') for k in self._field_names_order})
                    f.flush()
                print(f"進度：{(idx/len(job_ids))*100:6.2f} % ({idx}/{len(job_ids)})", end='\r')
                time.sleep(random.uniform(0.1, 1))
