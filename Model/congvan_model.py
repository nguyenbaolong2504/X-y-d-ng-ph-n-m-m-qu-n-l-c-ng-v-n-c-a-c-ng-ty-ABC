import pyodbc
from typing import List, Dict
from config import DB_CONFIG
import os


class CongVanModel:
    def __init__(self):
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
            raise Exception(f"Lỗi truy vấn cơ sở dữ liệu: {str(e)}")

    # ========== DANH MỤC ==========
    def get_phong_ban(self) -> List[str]:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT TenDonVi FROM DonViTrucThuoc WHERE TrangThai = 1")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Lỗi nạp danh mục đơn vị: {e}")
            return []

    def get_loai_van_ban(self) -> List[Dict]:
        """Trả về list dict: {'id': ..., 'ten_loai': ...} từ PhanLoaiCongVanDen"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, TenHinhThuc FROM PhanLoaiCongVanDen ORDER BY Id")
                return [dict(id=row[0], ten_loai=row[1]) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Lỗi nạp loại văn bản: {e}")
            return []

    # ========== TRUY VẤN ==========
    def get_all(self) -> List[Dict]:
        sql = """
            SELECT cv.Id as id, cv.NgayDen as ngay_den, cv.SoDen as so_den,
                   cv.NoiPhatHanh as tac_gia, cv.KyHieu as so_ky_hieu,
                   cv.NgayKy as ngay_van_ban, cv.TrichYeu as trich_yeu,
                   cv.NoiNhan as don_vi_nhan, cv.NgayChuyen as ngay_chuyen,
                   cv.TrangThaiChuyen as trang_thai, cv.GhiChu as ghi_chu,
                   cv.FileDinhKem as file_dinh_kem,
                   cv.PhanLoaiId as phan_loai_id,
                   pl.TenHinhThuc as ten_loai
            FROM CongVanDen cv
            LEFT JOIN PhanLoaiCongVanDen pl ON cv.PhanLoaiId = pl.Id
            ORDER BY cv.NgayDen DESC
        """
        return self._execute_query(sql)

    def search_by_author_or_number(self, keyword: str) -> List[Dict]:
        sql = """
            SELECT cv.Id as id, cv.NgayDen as ngay_den, cv.SoDen as so_den,
                   cv.NoiPhatHanh as tac_gia, cv.KyHieu as so_ky_hieu,
                   cv.NgayKy as ngay_van_ban, cv.TrichYeu as trich_yeu,
                   cv.NoiNhan as don_vi_nhan, cv.NgayChuyen as ngay_chuyen,
                   cv.TrangThaiChuyen as trang_thai, cv.GhiChu as ghi_chu,
                   cv.FileDinhKem as file_dinh_kem,
                   cv.PhanLoaiId as phan_loai_id,
                   pl.TenHinhThuc as ten_loai
            FROM CongVanDen cv
            LEFT JOIN PhanLoaiCongVanDen pl ON cv.PhanLoaiId = pl.Id
            WHERE cv.NoiPhatHanh LIKE ? OR cv.SoDen LIKE ? OR cv.KyHieu LIKE ?
            ORDER BY cv.NgayDen DESC
        """
        like_val = f"%{keyword}%"
        return self._execute_query(sql, (like_val, like_val, like_val))

    def filter_by_ngay_den(self, tu_ngay: str, den_ngay: str) -> List[Dict]:
        sql = """
            SELECT cv.Id as id, cv.NgayDen as ngay_den, cv.SoDen as so_den,
                   cv.NoiPhatHanh as tac_gia, cv.KyHieu as so_ky_hieu,
                   cv.NgayKy as ngay_van_ban, cv.TrichYeu as trich_yeu,
                   cv.NoiNhan as don_vi_nhan, cv.NgayChuyen as ngay_chuyen,
                   cv.TrangThaiChuyen as trang_thai, cv.GhiChu as ghi_chu,
                   cv.FileDinhKem as file_dinh_kem,
                   cv.PhanLoaiId as phan_loai_id,
                   pl.TenHinhThuc as ten_loai
            FROM CongVanDen cv
            LEFT JOIN PhanLoaiCongVanDen pl ON cv.PhanLoaiId = pl.Id
            WHERE cv.NgayDen BETWEEN ? AND ?
            ORDER BY cv.NgayDen DESC
        """
        return self._execute_query(sql, (tu_ngay, den_ngay))

    # ========== LỌC KẾT HỢP (MỚI) ==========
    def filter_by_criteria(self, tu_ngay: str = None, den_ngay: str = None, loai_id: int = None) -> List[Dict]:
        """Lọc theo ngày (có thể bỏ trống) và loại văn bản (None = tất cả)"""
        base_sql = """
            SELECT cv.Id as id, cv.NgayDen as ngay_den, cv.SoDen as so_den,
                   cv.NoiPhatHanh as tac_gia, cv.KyHieu as so_ky_hieu,
                   cv.NgayKy as ngay_van_ban, cv.TrichYeu as trich_yeu,
                   cv.NoiNhan as don_vi_nhan, cv.NgayChuyen as ngay_chuyen,
                   cv.TrangThaiChuyen as trang_thai, cv.GhiChu as ghi_chu,
                   cv.FileDinhKem as file_dinh_kem,
                   cv.PhanLoaiId as phan_loai_id,
                   pl.TenHinhThuc as ten_loai
            FROM CongVanDen cv
            LEFT JOIN PhanLoaiCongVanDen pl ON cv.PhanLoaiId = pl.Id
            WHERE 1=1
        """
        params = []
        if tu_ngay and den_ngay:
            base_sql += " AND cv.NgayDen BETWEEN ? AND ?"
            params += [tu_ngay, den_ngay]
        if loai_id is not None:
            base_sql += " AND cv.PhanLoaiId = ?"
            params.append(loai_id)
        base_sql += " ORDER BY cv.NgayDen DESC"
        return self._execute_query(base_sql, tuple(params))

    # ========== THÊM / SỬA / XÓA ==========
    def add(self, data: Dict) -> int:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO CongVanDen (Nam, SoDen, KyHieu, NgayDen, NgayKy, NoiPhatHanh,
                                           TrichYeu, NoiNhan, NgayChuyen, GhiChu, FileDinhKem,
                                           TrangThaiChuyen, PhanLoaiId)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data['ngay_den'][:4],
                    data.get('so_den'), data['so_ky_hieu'], data['ngay_den'], data['ngay_van_ban'],
                    data['tac_gia'], data['trich_yeu'], data['don_vi_nhan'], data['ngay_chuyen'],
                    data.get('ghi_chu'), data.get('file_dinh_kem'),
                    data.get('trang_thai', 0),
                    data.get('phan_loai_id')
                ))
                conn.commit()
                cursor.execute("SELECT @@IDENTITY")
                return int(cursor.fetchone()[0])
        except Exception as e:
            raise Exception(f"Lỗi thêm mới dữ liệu: {str(e)}")

    def update(self, id: int, data: Dict):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE CongVanDen SET
                        SoDen = ?, KyHieu = ?, NgayDen = ?, NgayKy = ?, NoiPhatHanh = ?,
                        TrichYeu = ?, NoiNhan = ?, NgayChuyen = ?, GhiChu = ?, FileDinhKem = ?,
                        TrangThaiChuyen = ?, PhanLoaiId = ?
                    WHERE Id = ?
                """, (
                    data.get('so_den'), data['so_ky_hieu'], data['ngay_den'], data['ngay_van_ban'],
                    data['tac_gia'], data['trich_yeu'], data['don_vi_nhan'], data['ngay_chuyen'],
                    data.get('ghi_chu'), data.get('file_dinh_kem'),
                    data.get('trang_thai', 0),
                    data.get('phan_loai_id'), id
                ))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi cập nhật dữ liệu: {str(e)}")

    def delete(self, id: int):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT FileDinhKem FROM CongVanDen WHERE Id = ?", (id,))
                row = cursor.fetchone()
                if row and row[0] and os.path.exists(row[0]):
                    os.remove(row[0])
                cursor.execute("DELETE FROM CongVanDen WHERE Id = ?", (id,))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi xóa dữ liệu: {str(e)}")