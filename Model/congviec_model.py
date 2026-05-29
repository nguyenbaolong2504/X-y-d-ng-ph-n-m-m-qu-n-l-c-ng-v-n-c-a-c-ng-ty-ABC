import pyodbc
from datetime import datetime

class CongViecModel:
    def __init__(self, conn_str):
        self.conn_str = conn_str

    def _get_connection(self):
        return pyodbc.connect(self.conn_str)

    def get_cong_viec_cua_toi(self, nguoi_dung_id, vai_tro):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Gộp Admin và Giám đốc thành nhóm có quyền xem toàn bộ công việc
        if vai_tro in ["Giám đốc", "Admin"]:
            sql = """
                SELECT pc.Id, pc.NoiDung, cb_g.HoTen AS NguoiGiao, cb_n.HoTen AS NguoiNhan,
                       pc.TrangThai, pc.HanXuLy, pc.NgayTao
                FROM PhanCongXuLy pc
                LEFT JOIN CanBo cb_g ON pc.NguoiGiaoId = cb_g.Id
                LEFT JOIN CanBo cb_n ON pc.NguoiDuocGiaoId = cb_n.Id
                ORDER BY pc.NgayTao DESC
            """
            cursor.execute(sql)
        else:
            # Các vai trò khác (Trưởng phòng, Nhân viên) chỉ xem việc của mình (nhận hoặc giao)
            sql = """
                SELECT pc.Id, pc.NoiDung, cb_g.HoTen AS NguoiGiao, cb_n.HoTen AS NguoiNhan,
                       pc.TrangThai, pc.HanXuLy, pc.NgayTao
                FROM PhanCongXuLy pc
                LEFT JOIN CanBo cb_g ON pc.NguoiGiaoId = cb_g.Id
                LEFT JOIN CanBo cb_n ON pc.NguoiDuocGiaoId = cb_n.Id
                WHERE pc.NguoiDuocGiaoId = ? OR pc.NguoiGiaoId = ?
                ORDER BY pc.NgayTao DESC
            """
            cursor.execute(sql, (nguoi_dung_id, nguoi_dung_id))
            
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_chi_tiet(self, cv_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Id, CongVanDenId, DonViDuocGiaoId, NguoiDuocGiaoId, HanXuLy, NoiDung,
                   NguoiGiaoId, TrangThai, KetQua, FileKetQua, YKienDuyet, NgayNop, NgayTao
            FROM PhanCongXuLy WHERE Id = ?
        """, cv_id)
        row = cursor.fetchone()
        conn.close()
        return row

    def them(self, id_cv_den, noi_dung, nguoi_giao, nguoi_nhan, han_xu_ly):
        conn = self._get_connection()
        cursor = conn.cursor()
        ngay_tao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO PhanCongXuLy (CongVanDenId, NguoiDuocGiaoId, HanXuLy, NoiDung, NguoiGiaoId, TrangThai, NgayTao, NgayNop)
            VALUES (?, ?, ?, ?, ?, 1, ?, NULL)
        """, (id_cv_den, nguoi_nhan, han_xu_ly, noi_dung, nguoi_giao, ngay_tao))
        conn.commit()
        new_id = cursor.execute("SELECT @@IDENTITY").fetchval()
        conn.close()
        return new_id

    def cap_nhat_nguoi_nhan(self, cv_id, nguoi_nhan_id, trang_thai, y_kien_duyet=""):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE PhanCongXuLy
            SET NguoiDuocGiaoId = ?, TrangThai = ?, YKienDuyet = ?
            WHERE Id = ?
        """, (nguoi_nhan_id, trang_thai, y_kien_duyet, cv_id))
        conn.commit()
        conn.close()

    def cap_nhat_trang_thai(self, cv_id, trang_thai, y_kien_duyet=""):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE PhanCongXuLy SET TrangThai = ?, YKienDuyet = ? WHERE Id = ?
        """, (trang_thai, y_kien_duyet, cv_id))
        conn.commit()
        conn.close()

    def cap_nhat_file_ket_qua(self, cv_id, file_path):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE PhanCongXuLy SET FileKetQua = ? WHERE Id = ?
        """, (file_path, cv_id))
        conn.commit()
        conn.close()

    def cap_nhat_ngay_nop(self, cv_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE PhanCongXuLy SET NgayNop = ? WHERE Id = ?
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cv_id))
        conn.commit()
        conn.close()

    def them_lich_su(self, cv_id, nguoi_id, hanh_dong, chi_tiet):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT CongVanDenId FROM PhanCongXuLy WHERE Id = ?", cv_id)
        row = cursor.fetchone()
        if not row:
            conn.close()
            return
        cv_den_id = row[0]
        thoi_gian = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO LichSuXuLy (CongVanDenId, NguoiThuChienId, ThaiGian, HanhDong, ChiTiet)
            VALUES (?, ?, ?, ?, ?)
        """, (cv_den_id, nguoi_id, thoi_gian, hanh_dong, chi_tiet))
        conn.commit()
        conn.close()

    def get_lich_su(self, cv_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ls.HanhDong, ls.ChiTiet, ls.ThaiGian, cb.HoTen
            FROM LichSuXuLy ls
            JOIN CanBo cb ON ls.NguoiThuChienId = cb.Id
            WHERE ls.CongVanDenId = (SELECT CongVanDenId FROM PhanCongXuLy WHERE Id = ?)
            ORDER BY ls.ThaiGian
        """, cv_id)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_file_chung(self, cv_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT TOP 1 FileKetQua FROM PhanCongXuLy 
            WHERE CongVanDenId = (SELECT CongVanDenId FROM PhanCongXuLy WHERE Id = ?)
            AND FileKetQua IS NOT NULL AND FileKetQua != ''
            ORDER BY Id DESC
        """, cv_id)
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def get_phan_hoi_moi_cho_nguoi(self, nguoi_dung_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT pc.Id, pc.NoiDung, ls.HanhDong, ls.ChiTiet, ls.ThaiGian, cb.HoTen as NguoiPhanHoi
            FROM PhanCongXuLy pc
            JOIN LichSuXuLy ls ON ls.CongVanDenId = pc.CongVanDenId
            JOIN CanBo cb ON ls.NguoiThuChienId = cb.Id
            WHERE (pc.NguoiDuocGiaoId = ? OR pc.NguoiGiaoId = ?)
              AND ls.HanhDong = 'Phản hồi'
              AND ls.ThaiGian > DATEADD(day, -7, GETDATE())
            ORDER BY ls.ThaiGian DESC
        """
        cursor.execute(sql, (nguoi_dung_id, nguoi_dung_id))
        rows = cursor.fetchall()
        conn.close()
        return rows


# =======================================================
# KHÔI PHỤC LẠI 2 CLASS BỊ MẤT
# =======================================================
class CongVanDenModel:
    def __init__(self, conn_str):
        self.conn_str = conn_str

    def get_all(self):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT Id, KyHieu, NgayNhan, TrichYeu FROM CongVanDen ORDER BY NgayNhan DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

class CongVanDiModel:
    def __init__(self, conn_str):
        self.conn_str = conn_str

    def tao(self, id_cong_van_den, so_ky_hieu, noi_nhan, trich_yeu, file_path):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        ngay_ky = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO CongVanPhatHanh (SoKyHieu, NgayKy, NoiNhan, TrichYeu, FilePath, CongVanDenId)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (so_ky_hieu, ngay_ky, noi_nhan, trich_yeu, file_path, id_cong_van_den))
        conn.commit()
        conn.close()