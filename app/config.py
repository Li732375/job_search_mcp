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
    '更新日期': 'posted_date',
    '工作型態': 'work_type',
    '工作時段': 'work_shift',
    '薪資類型': 'salary_type',
    '最低薪資': 'salary_min',
    '最高薪資': 'salary_max',
    '職缺名稱': 'job_name',
    '學歷': 'education',
    '工作經驗': 'experience',
    '工作縣市': 'address_area',
    '工作里區': 'job_area',
    '工作地址': 'address_detail',
    '公司名稱': 'company_name',
    '職缺描述': 'job_description',
    '其他描述': 'other_description',
    '擅長要求': 'specialty',
    '證照': 'certificate',
    '駕駛執照': 'driver_license',
    '出差': 'business_trip',
    '104 職缺網址': 'job_url',
    '公司產業類別': 'industry',
    '法定福利': 'legal_welfare'
}