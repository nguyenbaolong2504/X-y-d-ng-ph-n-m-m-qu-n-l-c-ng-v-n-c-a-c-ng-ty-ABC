import pyodbc
from typing import List, Dict
from config import DB_CONFIG
import os

class CongVanModel:
    def __init__(self):
        if DB_CONFIG.get('trusted_connection') in ('yes', True):
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

    def _execute_query(self, sql: str, params: tuple = ()) -> List[Dict]:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                if cursor.description is None:
                    return []
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            raise Exception(f"Lỗi truy vấn CSDL: {str(e)}")

    def get_danh_sach_can_bo(self) -> List[Dict]:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, HoTen FROM CanBo ORDER BY HoTen")
                return [{"id": row[0], "ho_ten": row[1]} for row in cursor.fetchall()]
        except Exception as e:
            print(f"Lỗi nạp danh sách cán bộ: {e}")
            return []

    def get_loai_van_ban(self) -> List[Dict]:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, TenLoai FROM LoaiCongVan ORDER BY Id")
                return [dict(id=row[0], ten_loai=row[1]) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Lỗi nạp loại văn bản: {e}")
            return []

    def get_max_so_den(self) -> int:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ISNULL(MAX(SoDen), 0) FROM CongVanDen")
                result = cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            print(f"Lỗi lấy số đến lớn nhất: {e}")
            return 0

    def get_all(self, is_admin=False, role=None, ten_don_vi=None) -> List[Dict]:
        sql = """
            SELECT 
                cv.Id as id,
                cv.NgayDen as ngay_den,
                cv.SoDen as so_den,
                cv.NoiPhatHanh as tac_gia,
                cv.KyHieu as so_ky_hieu,
                cv.NgayKy as ngay_van_ban,
                cv.TrichYeu as trich_yeu,
                ISNULL(cb.HoTen, cv.NoiNhan) as nguoi_xu_ly,
                cv.TrangThaiChuyen as trang_thai,
                cv.GhiChu as ghi_chu,
                cv.FileDinhKem as file_dinh_kem,
                cv.PhanLoaiId as phan_loai_id,
                pl.TenLoai as ten_loai,
                cv.MucDo as muc_do
            FROM CongVanDen cv
            LEFT JOIN LoaiCongVan pl ON cv.PhanLoaiId = pl.Id
            LEFT JOIN CanBo cb ON TRY_CAST(cv.NoiNhan AS INT) = cb.Id
        """
        conditions = []
        params = []
        if not is_admin:
            if role == 'NhanVien' and ten_don_vi == 'IT':
                conditions.append("cv.NoiPhatHanh LIKE N'%Giám đốc%'")
                conditions.append("cv.NoiNhan = ?")
                params.append(ten_don_vi)
            elif role in ('TruongPhong', 'NhanVien'):
                conditions.append("cv.NoiNhan = ?")
                params.append(ten_don_vi)
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY cv.NgayDen DESC"
        return self._execute_query(sql, tuple(params))

    def search_by_author_or_number(self, keyword: str, is_admin=False, role=None, ten_don_vi=None) -> List[Dict]:
        sql = """
            SELECT cv.Id as id, cv.NgayDen as ngay_den, cv.SoDen as so_den,
                   cv.NoiPhatHanh as tac_gia, cv.KyHieu as so_ky_hieu,
                   cv.NgayKy as ngay_van_ban, cv.TrichYeu as trich_yeu,
                   ISNULL(cb.HoTen, cv.NoiNhan) as nguoi_xu_ly, cv.TrangThaiChuyen as trang_thai, 
                   cv.GhiChu as ghi_chu, cv.FileDinhKem as file_dinh_kem,
                   cv.PhanLoaiId as phan_loai_id, cv.MucDo as muc_do,
                   pl.TenLoai as ten_loai
            FROM CongVanDen cv
            LEFT JOIN LoaiCongVan pl ON cv.PhanLoaiId = pl.Id
            LEFT JOIN CanBo cb ON (TRY_CAST(cv.NoiNhan AS INT) = cb.Id)
            WHERE (cv.NoiPhatHanh LIKE ? OR cv.SoDen LIKE ? OR cv.KyHieu LIKE ?)
        """
        params = [f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"]
        conditions = []
        if not is_admin:
            if role == 'NhanVien' and ten_don_vi == 'IT':
                conditions.append("cv.NoiPhatHanh LIKE N'%Giám đốc%'")
                conditions.append("cv.NoiNhan = ?")
                params.append(ten_don_vi)
            elif role in ('TruongPhong', 'NhanVien'):
                conditions.append("cv.NoiNhan = ?")
                params.append(ten_don_vi)
        if conditions:
            sql += " AND " + " AND ".join(conditions)
        sql += " ORDER BY cv.NgayDen DESC"
        return self._execute_query(sql, tuple(params))

    def filter_by_criteria(self, tu_ngay: str = None, den_ngay: str = None, loai_id: int = None,
                           muc_do: str = None,
                           is_admin=False, role=None, ten_don_vi=None) -> List[Dict]:
        base_sql = """
            SELECT cv.Id as id, cv.NgayDen as ngay_den, cv.SoDen as so_den,
                   cv.NoiPhatHanh as tac_gia, cv.KyHieu as so_ky_hieu,
                   cv.NgayKy as ngay_van_ban, cv.TrichYeu as trich_yeu,
                   ISNULL(cb.HoTen, cv.NoiNhan) as nguoi_xu_ly, cv.TrangThaiChuyen as trang_thai, 
                   cv.GhiChu as ghi_chu, cv.FileDinhKem as file_dinh_kem,
                   cv.PhanLoaiId as phan_loai_id, cv.MucDo as muc_do,
                   pl.TenLoai as ten_loai
            FROM CongVanDen cv
            LEFT JOIN LoaiCongVan pl ON cv.PhanLoaiId = pl.Id
            LEFT JOIN CanBo cb ON (TRY_CAST(cv.NoiNhan AS INT) = cb.Id)
            WHERE 1=1
        """
        params = []
        if tu_ngay and den_ngay:
            base_sql += " AND cv.NgayDen BETWEEN ? AND ?"
            params.extend([tu_ngay, den_ngay])
        if loai_id is not None:
            base_sql += " AND cv.PhanLoaiId = ?"
            params.append(loai_id)
        if muc_do and muc_do != "Tất cả":
            base_sql += " AND cv.MucDo = ?"
            params.append(muc_do)
        conditions = []
        if not is_admin:
            if role == 'NhanVien' and ten_don_vi == 'IT':
                conditions.append("cv.NoiPhatHanh LIKE N'%Giám đốc%'")
                conditions.append("cv.NoiNhan = ?")
                params.append(ten_don_vi)
            elif role in ('TruongPhong', 'NhanVien'):
                conditions.append("cv.NoiNhan = ?")
                params.append(ten_don_vi)
        if conditions:
            base_sql += " AND " + " AND ".join(conditions)
        base_sql += " ORDER BY cv.NgayDen DESC"
        return self._execute_query(base_sql, tuple(params))

    def add(self, data: Dict) -> int:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                max_so_den = self.get_max_so_den()
                new_so_den = max_so_den + 1
                ngay_den_val = data.get('ngay_den')
                nam = str(ngay_den_val)[:4] if ngay_den_val else ""
                # Mặc định trạng thái = 1 (Chờ phân công)
                trang_thai_value = data.get('trang_thai', 1)
                cursor.execute("""
                    INSERT INTO CongVanDen
                    (Nam, SoDen, KyHieu, NgayDen, NgayKy, NoiPhatHanh, TrichYeu, NoiNhan, GhiChu, FileDinhKem, TrangThaiChuyen, PhanLoaiId, TrangThaiXuLy, MucDo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (nam, new_so_den, data.get('so_ky_hieu'), data.get('ngay_den'),
                      data.get('ngay_van_ban'), data.get('tac_gia'), data.get('trich_yeu'),
                      data.get('nguoi_xu_ly'), data.get('ghi_chu'), data.get('file_dinh_kem'),
                      trang_thai_value, data.get('phan_loai_id'), 0, data.get('muc_do', 'Thường')))
                conn.commit()
                cursor.execute("SELECT @@IDENTITY")
                return int(cursor.fetchone()[0])
        except Exception as e:
            raise Exception(f"Lỗi thêm mới: {str(e)}")

    def update(self, id: int, data: Dict):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE CongVanDen
                    SET KyHieu = ?, NgayDen = ?, NgayKy = ?, NoiPhatHanh = ?, TrichYeu = ?,
                        NoiNhan = ?, GhiChu = ?, FileDinhKem = ?, TrangThaiChuyen = ?, PhanLoaiId = ?, MucDo = ?
                    WHERE Id = ?
                """, (data.get('so_ky_hieu'), data.get('ngay_den'), data.get('ngay_van_ban'),
                      data.get('tac_gia'), data.get('trich_yeu'), data.get('nguoi_xu_ly'),
                      data.get('ghi_chu'), data.get('file_dinh_kem'), data.get('trang_thai', 1),
                      data.get('phan_loai_id'), data.get('muc_do', 'Thường'), id))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi cập nhật: {str(e)}")

    def update_nguoi_xu_ly(self, id_cv: int, nguoi_id: int):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE CongVanDen SET NoiNhan = ? WHERE Id = ?", (nguoi_id, id_cv))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi cập nhật người xử lý: {str(e)}")

    def update_trang_thai_cv(self, id_cv: int, trang_thai: int):
        """Cập nhật trạng thái công văn (1: Chờ phân công, 2: Đang xử lý, 3: Hoàn thành)"""
        sql = "UPDATE CongVanDen SET TrangThaiChuyen = ? WHERE Id = ?"
        self._execute_query(sql, (trang_thai, id_cv))

    def delete(self, id: int):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM LichSuXuLy WHERE CongVanDenId = ?", (id,))
                cursor.execute("DELETE FROM PhanCongXuLy WHERE CongVanDenId = ?", (id,))
                try:
                    cursor.execute("DELETE FROM CongVanDen_CanBo WHERE VanBanDenId = ?", (id,))
                except:
                    pass
                cursor.execute("SELECT FileDinhKem FROM CongVanDen WHERE Id = ?", (id,))
                row = cursor.fetchone()
                if row and row[0] and os.path.exists(row[0]):
                    try:
                        os.remove(row[0])
                    except OSError:
                        pass
                cursor.execute("DELETE FROM CongVanDen WHERE Id = ?", (id,))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi xóa: {str(e)}")

    def get_by_id(self, cv_id: int) -> Dict:
        sql = """
            SELECT Id, KyHieu, TrichYeu, NoiPhatHanh, NgayDen, FileDinhKem,
                   NgayKy, GhiChu, TrangThaiChuyen, PhanLoaiId, MucDo
            FROM CongVanDen WHERE Id = ?
        """
        rows = self._execute_query(sql, (cv_id,))
        return rows[0] if rows else {}

    def get_connection_string(self) -> str:
        return self.conn_str