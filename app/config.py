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

# 欄位名稱順序
FIELD_NAMES_ORDER = [
    '更新日期', '工作型態', '工作時段', '薪資類型', '最低薪資',
    '最高薪資', '職缺名稱', '學歷', '工作經驗', '工作縣市',
    '工作里區', '工作地址', '公司名稱', '職缺描述', '其他描述',
    '擅長要求', '證照', '駕駛執照', '出差', '104 職缺網址', 
    '公司產業類別', '法定福利'
]

# 職缺欄位對應表
JOB_FIELD_MAPPING = {
    "posted_date": "更新日期",
    "work_type": "工作型態",
    "work_shift": "工作時段",
    "salary_type": "薪資類型",
    "salary_min": "最低薪資",
    "salary_max": "最高薪資",
    "job_name": "職缺名稱",
    "education": "學歷",
    "experience": "工作經驗",
    "address_area": "工作縣市",
    "job_area": "工作里區",
    "address_detail": "工作地址",
    "company_name": "公司名稱",
    "job_description": "職缺描述",
    "other_description": "其他描述",
    "specialty": "擅長要求",
    "certificate": "證照",
    "driver_license": "駕駛執照",
    "business_trip": "出差",
    "job_url": "104 職缺網址",
    "industry": "公司產業類別",
    "legal_welfare": "法定福利",
}
