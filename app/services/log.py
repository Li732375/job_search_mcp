import os
import json
from typing import Any
from time import strftime

from app.config import _ERROR_LOG_URL


def log_error(**kwargs:Any) -> None:
    """將錯誤訊息與原始資料寫入 JSON 檔案"""

    error_entry = {
            'timestamp': strftime("%Y-%m-%d %H:%M:%S"), 
            **kwargs}
    
    # 讀取現有紀錄並更新
    data = []

    # 若檔案存在則讀取現有資料
    if os.path.exists(_ERROR_LOG_URL):
        with open(_ERROR_LOG_URL, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
    
    # 新增錯誤紀錄(Dict)
    data.append(error_entry)

    # 寫回檔案或者直接建立新檔案
    with open(_ERROR_LOG_URL, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def clear_error_log() -> None:
    """清除錯誤紀錄檔案"""

    if os.path.exists(_ERROR_LOG_URL):
        os.remove(_ERROR_LOG_URL)


def is_log_exists() -> bool:
    """檢查錯誤紀錄檔案是否存在"""

    return os.path.exists(_ERROR_LOG_URL)