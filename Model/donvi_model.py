import pyodbc

class DonViModel:
    def __init__(self, connection_string):
        self.conn_str = connection_string

    def get_all(self):
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, ParentId, CapDo, TenDonVi, Email, Website, DiaChi, DienThoai, TrangThai FROM dbo.DonViTrucThuoc ORDER BY Id ASC")
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except pyodbc.Error as e:
            print(f"Lỗi SQL Đơn vị: {e}")
            return [] 
            
    def search(self, keyword):
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                sql = """
                    SELECT Id, ParentId, CapDo, TenDonVi, Email, Website, DiaChi, DienThoai, TrangThai 
                    FROM dbo.DonViTrucThuoc 
                    WHERE TenDonVi LIKE ? OR DienThoai LIKE ? OR Email LIKE ? OR Website LIKE ?
                    ORDER BY Id ASC
                """
                like_val = f"%{keyword}%"
                cursor.execute(sql, (like_val, like_val, like_val, like_val))
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except pyodbc.Error as e:
            print(f"Lỗi tìm kiếm Đơn vị: {e}")
            return []

    def add(self, data):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO DonViTrucThuoc (TenDonVi, DiaChi, DienThoai, Email, Website, TrangThai) VALUES (?, ?, ?, ?, ?, ?)", 
                           (data['TenDonVi'], data['DiaChi'], data['DienThoai'], data['Email'], data['Website'], data['TrangThai']))
            conn.commit()

    def update(self, data):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE DonViTrucThuoc SET TenDonVi = ?, DiaChi = ?, DienThoai = ?, Email = ?, Website = ?, TrangThai = ? WHERE Id = ?", 
                           (data['TenDonVi'], data['DiaChi'], data['DienThoai'], data['Email'], data['Website'], data['TrangThai'], data['Id']))
            conn.commit()

    def delete(self, id_val):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM DonViTrucThuoc WHERE Id = ?", (id_val,))
            conn.commit()