import pyodbc

class HanBaoQuanModel:
    def __init__(self, connection_string):
        self.conn_str = connection_string

    def get_all(self):
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, TenHanBaoQuan, GhiChu FROM dbo.HanBaoQuan")
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except pyodbc.Error as e:
            print(f"Lỗi truy vấn SQL: {e}")
            return [] 
        
    def search(self, keyword):
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                sql = """
                    SELECT Id, TenHanBaoQuan, GhiChu 
                    FROM dbo.HanBaoQuan 
                    WHERE TenHanBaoQuan LIKE ? OR GhiChu LIKE ?
                    ORDER BY Id DESC
                """
                like_val = f"%{keyword}%"
                cursor.execute(sql, (like_val, like_val))
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except pyodbc.Error as e:
            print(f"Lỗi tìm kiếm SQL: {e}")
            return []
        
    def add(self, data):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO HanBaoQuan (TenHanBaoQuan, GhiChu)
                VALUES (?, ?)
            """, (data['TenHanBaoQuan'], data['GhiChu']))
            conn.commit()

    def update(self, data):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE HanBaoQuan 
                SET TenHanBaoQuan = ?, GhiChu = ?
                WHERE Id = ?
            """, (data['TenHanBaoQuan'], data['GhiChu'], data['Id']))
            conn.commit()

    def delete(self, id_hbq):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM HanBaoQuan WHERE Id = ?", (id_hbq,))
            conn.commit()