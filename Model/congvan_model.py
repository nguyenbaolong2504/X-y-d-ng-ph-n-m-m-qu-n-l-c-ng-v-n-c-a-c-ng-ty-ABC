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
            raise Exception(f"Lỗi truy vấn cơ sở dữ liệu: {str(e)}")

<<<<<<< HEAD
    def get_danh_sach_can_bo(self) -> List[Dict]:
=======
    def get_phong_ban(self) -> List[str]:
>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
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

<<<<<<< HEAD
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

=======
>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
    def get_all(self, is_admin=False, role=None, ten_don_vi=None) -> List[Dict]:
        sql = """
            SELECT cv.Id as id, cv.NgayDen as ngay_den, cv.SoDen as so_den,
                   cv.NoiPhatHanh as tac_gia, cv.KyHieu as so_ky_hieu,
                   cv.NgayKy as ngay_van_ban, cv.TrichYeu as trich_yeu,
<<<<<<< HEAD
                   ISNULL(cb.HoTen, cv.NoiNhan) as nguoi_xu_ly, cv.TrangThaiChuyen as trang_thai, 
                   cv.GhiChu as ghi_chu, cv.FileDinhKem as file_dinh_kem,
                   cv.PhanLoaiId as phan_loai_id, cv.MucDo as muc_do,
                   pl.TenLoai as ten_loai
            FROM CongVanDen cv
            LEFT JOIN LoaiCongVan pl ON cv.PhanLoaiId = pl.Id
            LEFT JOIN CanBo cb ON (TRY_CAST(cv.NoiNhan AS INT) = cb.Id)
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

=======
                   cv.NoiNhan as don_vi_nhan,
                   cv.TrangThaiChuyen as trang_thai, cv.GhiChu as ghi_chu,
                   cv.FileDinhKem as file_dinh_kem,
                   cv.PhanLoaiId as phan_loai_id,
                   pl.TenHinhThuc as ten_loai
            FROM CongVanDen cv
            LEFT JOIN PhanLoaiCongVanDen pl ON cv.PhanLoaiId = pl.Id
        """
        conditions = []
        params = []

        if not is_admin:
            if role == 'NhanVien' and ten_don_vi == 'IT':
                conditions.append("(cv.NoiPhatHanh LIKE N'%Giám đốc%' OR cv.NoiPhatHanh LIKE N'%Giám đốc%')")
                conditions.append("cv.NoiNhan = ?")
                params.append(ten_don_vi)
            elif role in ('TruongPhong', 'NhanVien'):
                conditions.append("cv.NoiNhan = ?")
                params.append(ten_don_vi)

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += " ORDER BY cv.NgayDen DESC"
        return self._execute_query(sql, tuple(params))

>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
    def search_by_author_or_number(self, keyword: str, is_admin=False, role=None, ten_don_vi=None) -> List[Dict]:
        sql = """
            SELECT cv.Id as id, cv.NgayDen as ngay_den, cv.SoDen as so_den,
                   cv.NoiPhatHanh as tac_gia, cv.KyHieu as so_ky_hieu,
                   cv.NgayKy as ngay_van_ban, cv.TrichYeu as trich_yeu,
<<<<<<< HEAD
                   ISNULL(cb.HoTen, cv.NoiNhan) as nguoi_xu_ly, cv.TrangThaiChuyen as trang_thai, 
                   cv.GhiChu as ghi_chu, cv.FileDinhKem as file_dinh_kem,
                   cv.PhanLoaiId as phan_loai_id, cv.MucDo as muc_do,
                   pl.TenLoai as ten_loai
            FROM CongVanDen cv
            LEFT JOIN LoaiCongVan pl ON cv.PhanLoaiId = pl.Id
            LEFT JOIN CanBo cb ON (TRY_CAST(cv.NoiNhan AS INT) = cb.Id)
=======
                   cv.NoiNhan as don_vi_nhan,
                   cv.TrangThaiChuyen as trang_thai, cv.GhiChu as ghi_chu,
                   cv.FileDinhKem as file_dinh_kem,
                   cv.PhanLoaiId as phan_loai_id,
                   pl.TenHinhThuc as ten_loai
            FROM CongVanDen cv
            LEFT JOIN PhanLoaiCongVanDen pl ON cv.PhanLoaiId = pl.Id
>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
            WHERE (cv.NoiPhatHanh LIKE ? OR cv.SoDen LIKE ? OR cv.KyHieu LIKE ?)
        """
        params = [f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"]
        conditions = []
<<<<<<< HEAD
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

=======

        if not is_admin:
            if role == 'NhanVien' and ten_don_vi == 'IT':
                conditions.append("(cv.NoiPhatHanh LIKE N'%Giám đốc%' OR cv.NoiPhatHanh LIKE N'%Giám đốc%')")
                conditions.append("cv.NoiNhan = ?")
                params.append(ten_don_vi)
            elif role in ('TruongPhong', 'NhanVien'):
                conditions.append("cv.NoiNhan = ?")
                params.append(ten_don_vi)

        if conditions:
            sql += " AND " + " AND ".join(conditions)

        sql += " ORDER BY cv.NgayDen DESC"
        return self._execute_query(sql, tuple(params))

>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
    def filter_by_criteria(self, tu_ngay: str = None, den_ngay: str = None, loai_id: int = None,
                           is_admin=False, role=None, ten_don_vi=None) -> List[Dict]:
        base_sql = """
            SELECT cv.Id as id, cv.NgayDen as ngay_den, cv.SoDen as so_den,
                   cv.NoiPhatHanh as tac_gia, cv.KyHieu as so_ky_hieu,
                   cv.NgayKy as ngay_van_ban, cv.TrichYeu as trich_yeu,
<<<<<<< HEAD
                   ISNULL(cb.HoTen, cv.NoiNhan) as nguoi_xu_ly, cv.TrangThaiChuyen as trang_thai, 
                   cv.GhiChu as ghi_chu, cv.FileDinhKem as file_dinh_kem,
                   cv.PhanLoaiId as phan_loai_id, cv.MucDo as muc_do,
                   pl.TenLoai as ten_loai
=======
                   cv.NoiNhan as don_vi_nhan,
                   cv.TrangThaiChuyen as trang_thai, cv.GhiChu as ghi_chu,
                   cv.FileDinhKem as file_dinh_kem,
                   cv.PhanLoaiId as phan_loai_id,
                   pl.TenHinhThuc as ten_loai
>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
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

        conditions = []
        if not is_admin:
            if role == 'NhanVien' and ten_don_vi == 'IT':
<<<<<<< HEAD
                conditions.append("cv.NoiPhatHanh LIKE N'%Giám đốc%'")
=======
                conditions.append("(cv.NoiPhatHanh LIKE N'%Giám đốc%' OR cv.NoiPhatHanh LIKE N'%Giám đốc%')")
>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
                conditions.append("cv.NoiNhan = ?")
                params.append(ten_don_vi)
            elif role in ('TruongPhong', 'NhanVien'):
                conditions.append("cv.NoiNhan = ?")
                params.append(ten_don_vi)
<<<<<<< HEAD
        if conditions:
            base_sql += " AND " + " AND ".join(conditions)
=======

        if conditions:
            base_sql += " AND " + " AND ".join(conditions)

>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
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
                cursor.execute("""
<<<<<<< HEAD
                    INSERT INTO CongVanDen 
                    (Nam, SoDen, KyHieu, NgayDen, NgayKy, NoiPhatHanh,
                     TrichYeu, NoiNhan, GhiChu, FileDinhKem,
                     TrangThaiChuyen, PhanLoaiId, TrangThaiXuLy, MucDo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
                """, (
                    nam, new_so_den, data.get('so_ky_hieu'),
                    data.get('ngay_den'), data.get('ngay_van_ban'), data.get('tac_gia'),
                    data.get('trich_yeu'), data.get('nguoi_xu_ly'), data.get('ghi_chu'),
                    data.get('file_dinh_kem'), data.get('trang_thai', 0),
                    data.get('phan_loai_id'), data.get('muc_do')
=======
                    INSERT INTO CongVanDen (
                        Nam,
                        SoDen,
                        KyHieu,
                        NgayDen,
                        NgayKy,
                        NoiPhatHanh,
                        TrichYeu,
                        NoiNhan,
                        NgayChuyen,
                        GhiChu,
                        FileDinhKem,
                        TrangThaiChuyen,
                        PhanLoaiId,
                        TrangThaiXuLy,
                        TrangThaiDuyet,
                        IsKhan,
                        IsMat,
                        DonViNhapId,
                        NguoiTaoId
                    )

                    VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        0,
                        0,
                        0,
                        0,
                        1,
                        1
                    )

                    INSERT INTO CongVanDen (Nam, SoDen, KyHieu, NgayDen, NgayKy, NoiPhatHanh,
                                            TrichYeu, NoiNhan, GhiChu, FileDinhKem,
                                            TrangThaiChuyen, PhanLoaiId, TrangThaiXuLy)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                """, (
                    data['ngay_den'][:4], data.get('so_den'), data['so_ky_hieu'], 
                    data['ngay_den'], data['ngay_van_ban'], data['tac_gia'], 
                    data['trich_yeu'], data['don_vi_nhan'], data.get('ghi_chu'), 
                    data.get('file_dinh_kem'), data.get('trang_thai', 0), 
                    data.get('phan_loai_id')
>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
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
<<<<<<< HEAD
                        KyHieu = ?, NgayDen = ?, NgayKy = ?, NoiPhatHanh = ?,
                        TrichYeu = ?, NoiNhan = ?, GhiChu = ?, FileDinhKem = ?,
                        TrangThaiChuyen = ?, PhanLoaiId = ?, MucDo = ?
                    WHERE Id = ?
                """, (
                    data.get('so_ky_hieu'), data.get('ngay_den'), data.get('ngay_van_ban'),
                    data.get('tac_gia'), data.get('trich_yeu'), data.get('nguoi_xu_ly'),
                    data.get('ghi_chu'), data.get('file_dinh_kem'),
                    data.get('trang_thai', 0), data.get('phan_loai_id'), data.get('muc_do'), id
=======
                        SoDen = ?, KyHieu = ?, NgayDen = ?, NgayKy = ?, NoiPhatHanh = ?,
                        TrichYeu = ?, NoiNhan = ?, GhiChu = ?, FileDinhKem = ?,
                        TrangThaiChuyen = ?, PhanLoaiId = ?
                    WHERE Id = ?
                """, (
                    data.get('so_den'), data['so_ky_hieu'], data['ngay_den'], data['ngay_van_ban'],
                    data['tac_gia'], data['trich_yeu'], data['don_vi_nhan'],
                    data.get('ghi_chu'), data.get('file_dinh_kem'),
                    data.get('trang_thai', 0), data.get('phan_loai_id'), id
>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
                ))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi cập nhật dữ liệu: {str(e)}")

    def chuyen_xu_ly_van_ban(self, id_cv: int, data: Dict):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                chu_tri_ten = data.get('chu_tri_ten', '')
                tham_gia_ten = ", ".join(data.get('tham_gia_ten', []))
                noi_dung = data.get('noi_dung', '')
                yeu_cau = data.get('yeu_cau_xu_ly', '')
                ngay_xl = data.get('ngay_xu_ly', '')
                ghi_chu_phan_cong = (
                    f"Nội dung: {noi_dung}\n"
                    f"Yêu cầu: {yeu_cau}\n"
                    f"Người tham gia: {tham_gia_ten}\n"
                    f"Hạn xử lý: {ngay_xl}"
                )
                cursor.execute("""
                    UPDATE CongVanDen 
                    SET NoiNhan = ?, GhiChu = ?, TrangThaiChuyen = 2 
                    WHERE Id = ?
                """, (chu_tri_ten, ghi_chu_phan_cong, id_cv))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi phân công xử lý: {str(e)}")

    def delete(self, id: int):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT FileDinhKem FROM CongVanDen WHERE Id = ?", (id,))
                row = cursor.fetchone()
                if row and row[0] and os.path.exists(row[0]):
                    try: os.remove(row[0])
<<<<<<< HEAD
                    except OSError: pass 
=======
                    except: pass
>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
                cursor.execute("DELETE FROM CongVanDen WHERE Id = ?", (id,))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi xóa dữ liệu: {str(e)}")

    def get_by_id(self, cv_id: int) -> Dict:
        sql = """
            SELECT Id, KyHieu, TrichYeu, NoiPhatHanh, NgayDen, FileDinhKem
            FROM CongVanDen WHERE Id = ?
        """
        rows = self._execute_query(sql, (cv_id,))
        return rows[0] if rows else {}

    def get_connection_string(self) -> str:
        return self.conn_str

    def update_trang_thai(self, cv_id: int, trang_thai: int):
        sql = "UPDATE CongVanDen SET TrangThaiXuLy = ? WHERE Id = ?"
        self._execute_query(sql, (trang_thai, cv_id))