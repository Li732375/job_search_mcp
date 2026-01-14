# 獨立篩選條件
E04_UNI_FILTER_PARAMS = { 
    's5': '0',
    'isnew': '3',
    'wktm': '1',
    'ro': '1', 
}

# 複合篩選條件
E04_MUL_FILTER_PARAMS = {
    'area': '6001001000,6001016000,6001002011',
    'jobexp': '1,3',
    'edu': '3,4,5',
    'jobcat': '2007001004,2007001020',
}

### 以下變數不建議改動

# 預設資料庫路徑
_JOB_DATA_LOCAL_URL = 'app/database/job_data.db'

# 預設資料表名稱
_JOB_DATA_TABLE = 'jobs' 
_BLACKLIST_TABLE = 'blacklist'

# 預設錯誤訊息紀錄檔案
_ERROR_LOG_URL = 'error_message.json'