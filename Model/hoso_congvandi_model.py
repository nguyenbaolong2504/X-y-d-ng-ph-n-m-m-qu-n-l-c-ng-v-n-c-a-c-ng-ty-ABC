import pyodbc

class HoSoCongVanDiModel:
    def __init__(self, conn_str):
        self.conn_str = conn_str

    def luu_cong_van_vao_hoso(self, hoso_id, congvan_id, hanbaoquan_id=None):
        sql = """
            INSERT INTO HoSo_CongVanDi (HoSoId, CongVanDiId, HanBaoQuanId, NgayLuu)
            VALUES (?, ?, ?, GETDATE())
        """
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (hoso_id, congvan_id, hanbaoquan_id))
            conn.commit()

    def da_luu_chua(self, hoso_id, congvan_id):
        sql = "SELECT COUNT(*) FROM HoSo_CongVanDi WHERE HoSoId = ? AND CongVanDiId = ?"
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (hoso_id, congvan_id))
            return cursor.fetchone()[0] > 0

    def get_congvan_by_hoso(self, hoso_id):
        sql = """
            SELECT cv.Id, cv.SoPhatHanh, cv.KyHieu, cv.NgayKy, cv.TrichYeu, cv.MucDo, cv.TrangThaiChuyen,
                   hbq.TenHanBaoQuan
            FROM CongVanPhatHanh cv
            JOIN HoSo_CongVanDi hs ON cv.Id = hs.CongVanDiId
            LEFT JOIN HanBaoQuan hbq ON hs.HanBaoQuanId = hbq.Id
            WHERE hs.HoSoId = ?
            ORDER BY hs.NgayLuu DESC
        """
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (hoso_id,))
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]