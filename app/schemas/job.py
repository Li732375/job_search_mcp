# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field

# 定義每筆職缺資料的結構
class JobSchema(BaseModel):
    # 識別
    source: str = Field(default="e04", description="資料來源")
    job_id: str
    url: str

    # 職缺資訊
    title: str
    company_name: str
    location: Optional[str]
    salary_text: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    experience: Optional[str]
    education: Optional[str]
    description: str

    # 時間
    posted_date: Optional[str]
    crawled_at: str