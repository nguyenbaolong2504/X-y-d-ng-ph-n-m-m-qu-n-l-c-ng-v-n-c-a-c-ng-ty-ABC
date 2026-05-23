import pyodbc
from typing import List, Dict
from config import DB_CONFIG

class CongVanDiModel:
    def __init__(self):
        self.conn_str = (
            f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};Trusted_Connection=yes;"
        )

    def _get_connection(self):
        return pyodbc.connect(self.conn_str)

    def get_all(self, is_admin=False, role=None, ten_don_vi=None) -> List[Dict]:
        sql = """
            SELECT Id, SoPhatHanh, Nam, KyHieu, NgayKy, 
                   NoiNhan, TrichYeu, TrangThaiChuyen, GhiChu, FilePath
            FROM CongVanPhatHanh
        """
        conditions = []
        params = []
        if not is_admin:
            if role in ('TruongPhong', 'NhanVien'):
                conditions.append("NoiNhan = ?")
                params.append(ten_don_vi)
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY Id DESC"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(zip([col[0] for col in cursor.description], row)) for row in rows]

    def add(self, data: Dict):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            sql = """
                INSERT INTO CongVanPhatHanh 
                (SoPhatHanh, Nam, KyHieu, NgayKy, TrichYeu, NoiNhan, TrangThaiChuyen, GhiChu, FilePath, NgayChuyen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())
            """
            cursor.execute(sql, (
                data.get('SoPhatHanh'), data.get('Nam'), data.get('KyHieu'), 
                data.get('NgayKy'), data.get('TrichYeu'), data.get('NoiNhan'), 
                data.get('TrangThaiChuyen', 0), data.get('GhiChu'), data.get('FilePath')
            ))
            conn.commit()

    def update(self, id: int, data: Dict):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            sql = """
                UPDATE CongVanPhatHanh SET
                    SoPhatHanh=?, Nam=?, KyHieu=?, NgayKy=?, TrichYeu=?, 
                    NoiNhan=?, TrangThaiChuyen=?, GhiChu=?, FilePath=?
                WHERE Id=?
            """
            cursor.execute(sql, (
                data.get('SoPhatHanh'), data.get('Nam'), data.get('KyHieu'), 
                data.get('NgayKy'), data.get('TrichYeu'), data.get('NoiNhan'), 
                data.get('TrangThaiChuyen', 0), data.get('GhiChu'), data.get('FilePath'), id
            ))
            conn.commit()

    def delete(self, id: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM CongVanPhatHanh WHERE Id = ?", (id,))
            conn.commit()

    def get_data_for_export(self, start_date=None, end_date=None) -> List[Dict]:
        if start_date and end_date:
            return self.filter_by_date(start_date, end_date)
        return self.get_all()