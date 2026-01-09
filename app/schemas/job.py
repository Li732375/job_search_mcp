# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


# 定義每筆職缺資料的結構
class JobSchema(BaseModel):
    """定義職缺資料的結構"""
    posted_date: datetime = Field(description = "更新日期")
    work_type: str = Field(description = "工作型態")
    work_shift: str = Field(description = "工作時段")
    salary_type: str = Field(description = "薪資類型")    
    salary_min: Optional[int] = Field(default = None, description = "最低薪資")
    salary_max: Optional[int] = Field(default = None, description = "最高薪資")
    job_name: str = Field(description = "職缺名稱")
    education: str = Field(description = "學歷")
    experience: str = Field(description = "工作經驗")
    addressArea: str = Field(description = "工作縣市")
    job_area: str = Field(description = "工作里區")
    address_detail: Optional[str] = Field(default = None, description = "工作地址")
    company_name: str = Field(description = "公司名稱")
    job_description: Optional[str] = Field(default = None, description = "職缺描述")
    other_description: Optional[str] = Field(default = None, description = "其他描述")
    specialty: Optional[str] = Field(default = None, description = "擅長要求")
    certificate: Optional[str] = Field(default = None, description = "證照")
    driver_license: Optional[str] = Field(default = None, description = "駕駛執照")
    business_trip: Optional[str] = Field(default = None, description = "出差")
    job_url: str = Field(description = "104 職缺網址")
    industry: str = Field(description = "公司產業類別")
    legal_welfare: Optional[str] = Field(default = None, description = "法定福利")