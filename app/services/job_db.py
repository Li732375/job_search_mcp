from app.config import JOB_DATA_LOCAL_URL

import uuid
import sqlite3


class JobDB:
    def __init__(self, db_url: str = JOB_DATA_LOCAL_URL) -> None:
        """初始化職缺資料庫連線"""
        
        # 建立資料庫連線（若不存在則建立）
        self.db_url = db_url
        self.conn = sqlite3.connect(db_url)
        self.cursor = self.conn.cursor()
        self.conn.close()
        
    def add_table(self, table_name: str, schema: type) -> None:
        """建立職缺資料表"""
        
        # 取得 schema 欄位定義
        cols = []

        for name, field in schema.model_fields.items():
            t = field.annotation
            sql_type = "TEXT"

            if t is int:
                sql_type = "INTEGER"

            cols.append(f"{name} {sql_type}")

        cols_sql = ",\n    ".join(cols)
        
        # 建立資料表
        self.conn = sqlite3.connect(self.db_url)
        
        self.cursor.execute(f"""
                            CREATE TABLE IF NOT EXISTS {table_name} (
                                data_id TEXT PRIMARY KEY,
                                {cols_sql}
                            )
                            """)
        self.conn.commit()
        self.conn.close()
        print(f"成功建立資料表 {table_name} ！")

    def insert(self, table_name: str, schema: type) -> None:
        """插入資料"""
        
        # 取得 schema 欄位名稱
        field_names = [name for name in schema.model_fields.keys()]
        placeholders = ", ".join(["?"] * (len(field_names) + 1))  # 多一個 data_id
        
        # 插入資料
        self.conn = sqlite3.connect(self.db_url)

        self.cursor.execute(f"""
                            INSERT INTO {table_name} (data_id, {', '.join(field_names)})
                            VALUES ({placeholders})
                            """, 
                            (str(uuid.uuid4()), *[getattr(schema, name) for name in field_names])
                           )
        self.conn.commit()
        self.conn.close()
        print(f"成功寫入資料進資料表 {table_name} ！")