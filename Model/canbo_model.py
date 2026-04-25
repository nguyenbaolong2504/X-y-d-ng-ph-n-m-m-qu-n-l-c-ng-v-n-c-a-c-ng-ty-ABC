import pyodbc
from typing import List, Dict
from config import DB_CONFIG

class CanBoModel:
    def __init__(self):
        # THAY THẾ CHUỖI KẾT NỐI CŨ BẰNG ĐOẠN NÀY:
        if DB_CONFIG.get('trusted_connection') == 'yes' or DB_CONFIG.get('trusted_connection') is True:
            self.conn_str = (
                f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};Trusted_Connection=yes;"
            )
        else:
            self.conn_str = (
                f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};UID={DB_CONFIG['username']};PWD={DB_CONFIG['password']};"
            )
    def _get_connection(self):
        return pyodbc.connect(self.conn_str)

    def get_all(self) -> List[Dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Join với bảng DonVi và ChucVu để lấy tên hiển thị
            sql = """
                SELECT cb.Id, cb.HoTen, cb.NgaySinh, cb.GioiTinh, 
                       dv.TenDonVi, cv.TenChucVu, cb.Username, cb.Email, 
                       cb.Mobile, cb.KiVanBan, cb.IsAdmin
                FROM CanBo cb
                LEFT JOIN DonViTrucThuoc dv ON cb.DonViId = dv.Id
                LEFT JOIN ChucVu cv ON cb.ChucVuId = cv.Id
                ORDER BY cb.Id DESC
            """
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_don_vi(self):
        with self._get_connection() as conn:
            return conn.cursor().execute("SELECT Id, TenDonVi FROM DonViTrucThuoc").fetchall()

    def get_chuc_vu(self):
        with self._get_connection() as conn:
            return conn.cursor().execute("SELECT Id, TenChucVu FROM ChucVu").fetchall()

    def add(self, data: Dict):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            sql = """
                INSERT INTO CanBo (HoTen, NgaySinh, GioiTinh, DonViId, ChucVuId, Username, Password, Email, Mobile, KiVanBan, IsAdmin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(sql, (
                data['HoTen'], data['NgaySinh'], data['GioiTinh'], data['DonViId'],
                data['ChucVuId'], data['Username'], data['Password'], data['Email'],
                data['Mobile'], data['KiVanBan'], data['IsAdmin']
            ))
            conn.commit()
    
    def update(self, data: Dict):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            sql = """
                UPDATE CanBo 
                SET HoTen=?, NgaySinh=?, GioiTinh=?, DonViId=?, ChucVuId=?, 
                    Username=?, Email=?, Mobile=?, KiVanBan=?, IsAdmin=?
                WHERE Id=?
            """
            cursor.execute(sql, (
                data['HoTen'], data['NgaySinh'], data['GioiTinh'], data['DonViId'],
                data['ChucVuId'], data['Username'], data['Email'],
                data['Mobile'], data['KiVanBan'], data['IsAdmin'], data['Id']
            ))
            conn.commit()
            
    def delete(self, id_canbo: int):
        with self._get_connection() as conn:
            conn.cursor().execute("DELETE FROM CanBo WHERE Id = ?", (id_canbo,))
            conn.commit()