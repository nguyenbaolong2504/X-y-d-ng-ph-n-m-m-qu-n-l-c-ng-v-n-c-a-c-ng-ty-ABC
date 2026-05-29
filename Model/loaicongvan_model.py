import pyodbc
from datetime import datetime

class LoaiCongVanModel:
    def __init__(self, connection_string):
        self.conn_str = connection_string

    def get_all(self, trang_thai=None):
        """Lấy danh sách loại công văn (1: đến, 2: đi, 3: dùng chung cho cả 2)"""
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                if trang_thai == 1:
                    sql = "SELECT Id, MaLoai, TenLoai, MoTa, TrangThai, NgayTao FROM dbo.LoaiCongVan WHERE TrangThai IN (1, 3) ORDER BY Id ASC"
                    cursor.execute(sql)
                elif trang_thai == 2:
                    # Lấy loại ĐI (2) và DÙNG CHUNG (3)
                    sql = "SELECT Id, MaLoai, TenLoai, MoTa, TrangThai, NgayTao FROM dbo.LoaiCongVan WHERE TrangThai IN (2, 3) ORDER BY Id ASC"
                    cursor.execute(sql)
                else:
                    sql = "SELECT Id, MaLoai, TenLoai, MoTa, TrangThai, NgayTao FROM dbo.LoaiCongVan ORDER BY Id ASC"
                    cursor.execute(sql)
                
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