import pyodbc

class ChucVuModel:
    def __init__(self, connection_string):
        self.conn_str = connection_string

    def get_all(self):
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                # Đảm bảo tên bảng viết đúng như trong SQL (dbo.ChucVu)
                cursor.execute("SELECT Id, TenChucVu, TrangThai, GhiChu FROM dbo.ChucVu")
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except pyodbc.Error as e:
            print(f"Lỗi truy vấn SQL: {e}")
            return [] 
        
    def add(self, data):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ChucVu (TenChucVu, TrangThai, GhiChu)
                VALUES (?, ?, ?)
            """, (data['TenChucVu'], data['TrangThai'], data['GhiChu']))
            conn.commit()

    def update(self, data):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE ChucVu 
                SET TenChucVu = ?, TrangThai = ?, GhiChu = ?
                WHERE Id = ?
            """, (data['TenChucVu'], data['TrangThai'], data['GhiChu'], data['Id']))
            conn.commit()

    def delete(self, id_chucvu):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ChucVu WHERE Id = ?", (id_chucvu,))
            conn.commit()