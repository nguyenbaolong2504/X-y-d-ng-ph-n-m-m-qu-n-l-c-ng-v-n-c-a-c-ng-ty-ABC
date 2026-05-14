import pyodbc
from datetime import datetime

class LoaiCongVanModel:
    def __init__(self, connection_string):
        self.conn_str = connection_string

    def get_all(self):
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, MaLoai, TenLoai, MoTa, TrangThai, NgayTao FROM dbo.LoaiCongVan ORDER BY Id ASC")
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except pyodbc.Error as e:
            print(f"Lỗi truy vấn SQL (LoaiCongVan): {e}")
            return [] 
            
    def search(self, keyword):
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                sql = "SELECT Id, MaLoai, TenLoai, MoTa, TrangThai, NgayTao FROM dbo.LoaiCongVan WHERE MaLoai LIKE ? OR TenLoai LIKE ? ORDER BY Id DESC"
                like_val = f"%{keyword}%"
                cursor.execute(sql, (like_val, like_val))
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except pyodbc.Error as e:
            print(f"Lỗi tìm kiếm (LoaiCongVan): {e}")
            return []

    def add(self, data):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            ngay_tao = datetime.now()
            cursor.execute("INSERT INTO LoaiCongVan (MaLoai, TenLoai, MoTa, TrangThai, NgayTao) VALUES (?, ?, ?, ?, ?)", 
                           (data['MaLoai'], data['TenLoai'], data['MoTa'], data['TrangThai'], ngay_tao))
            conn.commit()

    def update(self, data):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE LoaiCongVan SET MaLoai = ?, TenLoai = ?, MoTa = ?, TrangThai = ? WHERE Id = ?", 
                           (data['MaLoai'], data['TenLoai'], data['MoTa'], data['TrangThai'], data['Id']))
            conn.commit()

    def delete(self, id_val):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM LoaiCongVan WHERE Id = ?", (id_val,))
            conn.commit()