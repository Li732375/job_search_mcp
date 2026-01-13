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

# 職缺資料庫路徑
JOB_DATA_LOCAL_URL = 'app/database/job_data.db'