import pyodbc

class LoaiVanBanModel:
    def __init__(self, connection_string, table_name):
        self.conn_str = connection_string
        self.table_name = table_name # 'PhanLoaiCongVanDen' hoặc 'PhanLoaiCongVanPhatHanh'

    def get_all(self):
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT Id, MaCongVan, TenHinhThuc, GhiChu FROM dbo.{self.table_name} ORDER BY Id ASC")
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except pyodbc.Error as e:
            print(f"Lỗi truy vấn SQL ({self.table_name}): {e}")
            return [] 
            
    def search(self, keyword):
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                sql = f"SELECT Id, MaCongVan, TenHinhThuc, GhiChu FROM dbo.{self.table_name} WHERE MaCongVan LIKE ? OR TenHinhThuc LIKE ? ORDER BY Id DESC"
                like_val = f"%{keyword}%"
                cursor.execute(sql, (like_val, like_val))
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except pyodbc.Error as e:
            print(f"Lỗi tìm kiếm ({self.table_name}): {e}")
            return []

    def add(self, data):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {self.table_name} (MaCongVan, TenHinhThuc, GhiChu) VALUES (?, ?, ?)", 
                           (data['MaCongVan'], data['TenHinhThuc'], data['GhiChu']))
            conn.commit()

    def update(self, data):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {self.table_name} SET MaCongVan = ?, TenHinhThuc = ?, GhiChu = ? WHERE Id = ?", 
                           (data['MaCongVan'], data['TenHinhThuc'], data['GhiChu'], data['Id']))
            conn.commit()

    def delete(self, id_val):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {self.table_name} WHERE Id = ?", (id_val,))
            conn.commit()