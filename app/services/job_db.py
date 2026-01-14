import uuid
import sqlite3
from types import TracebackType
from typing import Optional, Type, Any

from app.config import _JOB_DB_LOCAL_URL
from app.services.log import log_error


class JobDB:
    def __init__(self, db_url: str = _JOB_DB_LOCAL_URL) -> None:
        """初始化職缺資料庫連線"""
        
        self.db_url = db_url
        self.conn: Optional[sqlite3.Connection] = None
        self._it_cursor = None  # 記錄走訪指針

    def __enter__(self) -> "JobDB":
        """進入 with 區塊時自動執行，並回傳一個資料庫連線物件"""

        # 建立資料庫連線（若不存在則建立）
        self.conn = sqlite3.connect(self.db_url)
        return self

    def __exit__(self, 
                 exc_type: Optional[Type[BaseException]], 
                 exc_val: Optional[BaseException], 
                 exc_tb: Optional[TracebackType]) -> Optional[bool]:
        """
        離開 with 區塊時（無論是否報錯）都會自動執行

        當程式在 with 區塊內發生錯誤（例外）時，捕捉錯誤的詳細資訊。
        當錯誤發生時，這三個變數分別代表：
        - exc_type (Exception Type): 錯誤的類別（例如 ValueError 或 sqlite3.OperationalError）。
        - exc_val (Exception Value): 錯誤的實例物件，通常包含錯誤訊息（例如 "no such table: users"）。
        - exc_tb (Exception Traceback): 回溯物件（Traceback object），記錄了錯誤發生在哪一行、哪個函式中。
        """

        if self.conn:
            # 離開時若有錯誤發生
            if exc_type:
                self.log_error("__EXIT__", f"執行 SQL 階段錯誤:{exc_type}\n{exc_val}\n{exc_tb}")
                print(f"執行 SQL 階段錯誤")

                # 復原到修改前
                self.conn.rollback()
            else:
                self.conn.commit()
            
            self.conn.close()
            return False
            
    def add_table(self, table_name: str, data_schema: type) -> None:
        """
        新增資料表

        資料表最左欄固定是 data_id (TEXT PRIMARY KEY)
        往右其他欄位依 data_schema 定義自動產生
        """
        
        # 取得 data_schema 欄位定義
        cols = []

        for name, field in data_schema.model_fields.items():
            t = field.annotation
            sql_type = "TEXT"

            if t is int:
                sql_type = "INTEGER"

            cols.append(f"{name} {sql_type}")

        cols_sql = ",\n    ".join(cols)
        
        # 建立資料表
        cursor = self.conn.cursor()  # 取得游標

        cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {table_name} (
                            data_id TEXT PRIMARY KEY,
                            {cols_sql}
                        )
                        """)
        
        print(f"成功建立資料表 {table_name}", end='\r' )

    def is_table_exists(self, table_name: str) -> bool:
        """檢查資料表存在"""

        # 取得游標
        cursor = self.conn.cursor()
        
        # 查詢 SQLite 的系統表 sqlite_master
        sql = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?"
        cursor.execute(sql, (table_name,))
        
        # 如果傳回結果為 1，代表存在；0 代表不存在
        exists = cursor.fetchone()[0] == 1
        
        return exists

    def insert(self, table_name: str, data_schema: type) -> None:
        """寫入資料"""

        # 取得 data_schema 欄位名稱
        field_names = [name for name in data_schema.model_fields.keys()]
        placeholders = ", ".join(["?"] * (len(field_names) + 1))  # 多一個 data_id
        
        # 寫入資料
        cursor = self.conn.cursor()  # 取得游標

        # 確認資料表存在
        if self.is_table_exists(table_name):
            cursor.execute(f"""
                           INSERT INTO {table_name} (data_id, {', '.join(field_names)}) 
                           VALUES ({placeholders})
                           """, 
                           (str(uuid.uuid4()), *[getattr(data_schema, name) for name in field_names])
                           )
        else:
            print(f"[錯誤]資料表 {table_name} 不存在於 {self.db_url}", end='\r')
            return None
    
    def walk(self, table_name: str, id_start: str = None) -> Any:
        """
        指定 ID 開頭（模糊篩選）的逐筆走訪（維持該物件不滅）

        1. 若無 id_start：進入走訪模式，每次執行回傳下一筆完整資料。
        2. 若有 id_start：
           - 僅一筆：回傳該完整資料。
           - 2~5 筆：回傳 (序位, 前六碼, 整筆資料) 的元組清單。
           - 超過 5 筆：回傳提示訊息。
        """
        cursor = self.conn.cursor()
        
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
        id_col = cursor.description[0][0]

        if not id_start:
            if self._it_cursor is None:
                self._it_cursor = self.conn.cursor()
                self._it_cursor.execute(f"SELECT * FROM {table_name} ORDER BY {id_col} ASC")
            
            row = self._it_cursor.fetchone()  # 取得指標下一筆資料
            
            if row is None:
                self._it_cursor = None  # 走訪結束，重設狀態
                print("已達表尾，無更多資料。")
                return None
            
            return row  # tuple

        # 每次指定 ID 都會重設走訪指標
        self._it_cursor = None 

        # 先計算符合數
        count_sql = f"SELECT count(*) FROM {table_name} WHERE {id_col} LIKE ?"
        cursor.execute(count_sql, (f"{id_start}%",))
        total_count = cursor.fetchone()[0]

        if total_count == 0:
            print(f"找不到符合的資料。")
            return None

        if total_count > 5:
            print(f"資料表 ({total_count}) 中符合數大於五筆，請提供更多 ID 資訊。")
            return None
        
        """
        考量不小心輸入一個非常常見的 ID 開頭（例如 1），
        而資料庫裡有 100 萬筆符合此 ID 開頭的資料（高重複性），
        程式會試圖一次把 100 萬筆完整資料（含所有欄位）塞進記憶體。
        會導致程式瞬間卡死，引發 MemoryError。

        故採「先確認量級，再決定行為」防禦性設計(Defensive Programming)
        多寫一次查詢，換來系統的強健性 (Robustness)，避免在大數據情境下發生不可預測的崩潰。
        """

        # 取得所有符合條件的資料
        sql = f"SELECT * FROM {table_name} WHERE {id_col} LIKE ? ORDER BY {id_col} ASC"
        cursor.execute(sql, (f"{id_start}%",))
        results = cursor.fetchall()

        if total_count == 1:
            return results[0]  # 回傳完整資料，tuple
        else:
            output = tuple(
                (idx, str(row[0])[:6], row) 
                for idx, row in enumerate(results, start = 1)
            )
            print(f"多項相符資料，請提供更多 ID 資訊。")
            
            return output  # 回傳少量相符清單，數筆 tuple 集合的 list
    
    def log_error(self, fun_name: str, message: Any) -> None:
        """錯誤紀錄"""

        log_error(
            function = fun_name,
            message = message,
        )