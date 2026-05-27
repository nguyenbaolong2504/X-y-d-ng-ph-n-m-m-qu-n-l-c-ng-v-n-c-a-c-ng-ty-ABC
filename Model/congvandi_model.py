import pyodbc
from typing import List, Dict
from config import DB_CONFIG
from datetime import datetime

class CongVanDiModel:
    def __init__(self, conn_str=None):
        if conn_str:
            self.conn_str = conn_str
        else:
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

    def get_max_so_phat_hanh(self) -> int:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ISNULL(MAX(SoPhatHanh), 0) FROM CongVanPhatHanh")
                result = cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            print(f"Lỗi lấy số phát hành lớn nhất: {e}")
            return 0

    def get_all(self, tu_ngay=None, den_ngay=None, keyword=None, is_admin=False, role=None, ten_don_vi=None) -> List[Dict]:
        sql = """
            SELECT Id, SoPhatHanh, Nam, KyHieu, NgayKy, 
                   NoiNhan, TrichYeu, TrangThaiChuyen, GhiChu, FilePath, 
                   MucDo, PhanLoaiId, DonViSoanId, NguoiKyId, VanBanDenGocId
            FROM CongVanPhatHanh
            WHERE 1=1
        """
        params = []

        if tu_ngay and den_ngay:
            sql += " AND NgayKy BETWEEN ? AND ?"
            params.extend([tu_ngay, den_ngay])

        if keyword:
            sql += " AND (KyHieu LIKE ? OR NoiNhan LIKE ? OR TrichYeu LIKE ?)"
            kw = f"%{keyword}%"
            params.extend([kw, kw, kw])

        if not is_admin:
            if role in ('TruongPhong', 'NhanVien'):
                sql += " AND NoiNhan = ?"
                params.append(ten_don_vi)

        sql += " ORDER BY Id DESC"
        return self._execute_query(sql, tuple(params))

    def tao(self, van_ban_den_goc_id: int, so_ky_hieu: str, noi_nhan: str, trich_yeu: str, file_path: str, nguoi_tao_id=1):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                new_so = self.get_max_so_phat_hanh() + 1
                nam = datetime.now().year
                ngay_ky = datetime.now().date().isoformat()
                cursor.execute("""
                    INSERT INTO CongVanPhatHanh 
                    (SoPhatHanh, Nam, KyHieu, NgayKy, TrichYeu, NoiNhan, TrangThaiChuyen, 
                     FilePath, NgayChuyen, VanBanDenGocId, NguoiTaoId)
                    VALUES (?, ?, ?, ?, ?, ?, 1, ?, GETDATE(), ?, ?)
                """, (
                    new_so, nam, so_ky_hieu, ngay_ky, trich_yeu, noi_nhan, 
                    file_path, van_ban_den_goc_id, nguoi_tao_id
                ))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi thêm công văn đi: {str(e)}")

    def add(self, data: Dict):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                new_so = self.get_max_so_phat_hanh() + 1

                # Xử lý PhanLoaiId
                phan_loai_id = data.get('PhanLoaiId')
                if phan_loai_id is not None:
                    try:
                        phan_loai_id = int(phan_loai_id)
                    except (ValueError, TypeError):
                        phan_loai_id = None

                # Xử lý DonViSoanId - QUAN TRỌNG: gán 1 nếu None
                don_vi_soan_id = data.get('DonViSoanId')
                if don_vi_soan_id is not None:
                    try:
                        don_vi_soan_id = int(don_vi_soan_id)
                    except (ValueError, TypeError):
                        don_vi_soan_id = 1
                else:
                    don_vi_soan_id = 1  # ID đơn vị mặc định (Ban Giám Đốc)

                # Xử lý NguoiKyId
                nguoi_ky_id = data.get('NguoiKyId')
                if nguoi_ky_id is not None:
                    try:
                        nguoi_ky_id = int(nguoi_ky_id)
                    except (ValueError, TypeError):
                        nguoi_ky_id = None

                # Xử lý VanBanDenGocId
                van_ban_den_goc_id = data.get('VanBanDenGocId')
                if van_ban_den_goc_id is not None:
                    try:
                        van_ban_den_goc_id = int(van_ban_den_goc_id)
                    except (ValueError, TypeError):
                        van_ban_den_goc_id = None

                cursor.execute("""
                    INSERT INTO CongVanPhatHanh 
                    (SoPhatHanh, Nam, KyHieu, NgayKy, TrichYeu, NoiNhan, TrangThaiChuyen, 
                     GhiChu, FilePath, NgayChuyen, MucDo, PhanLoaiId, DonViSoanId, NguoiKyId, VanBanDenGocId, NguoiTaoId)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), ?, ?, ?, ?, ?, ?)
                """, (
                    new_so, data.get('Nam'), data.get('KyHieu'), data.get('NgayKy'), 
                    data.get('TrichYeu'), data.get('NoiNhan'), data.get('TrangThaiChuyen', 0), 
                    data.get('GhiChu'), data.get('FilePath'), data.get('MucDo'),
                    phan_loai_id, don_vi_soan_id, nguoi_ky_id,
                    van_ban_den_goc_id, data.get('NguoiTaoId', 1)
                ))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi thêm công văn đi: {str(e)}")

    def update(self, id_cv: int, data: Dict):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                phan_loai_id = data.get('PhanLoaiId')
                if phan_loai_id is not None:
                    try:
                        phan_loai_id = int(phan_loai_id)
                    except (ValueError, TypeError):
                        phan_loai_id = None

                don_vi_soan_id = data.get('DonViSoanId')
                if don_vi_soan_id is not None:
                    try:
                        don_vi_soan_id = int(don_vi_soan_id)
                    except (ValueError, TypeError):
                        don_vi_soan_id = 1
                else:
                    don_vi_soan_id = 1

                nguoi_ky_id = data.get('NguoiKyId')
                if nguoi_ky_id is not None:
                    try:
                        nguoi_ky_id = int(nguoi_ky_id)
                    except (ValueError, TypeError):
                        nguoi_ky_id = None

                van_ban_den_goc_id = data.get('VanBanDenGocId')
                if van_ban_den_goc_id is not None:
                    try:
                        van_ban_den_goc_id = int(van_ban_den_goc_id)
                    except (ValueError, TypeError):
                        van_ban_den_goc_id = None

                cursor.execute("""
                    UPDATE CongVanPhatHanh SET
                        Nam=?, KyHieu=?, NgayKy=?, TrichYeu=?, NoiNhan=?, 
                        TrangThaiChuyen=?, GhiChu=?, FilePath=?, MucDo=?,
                        PhanLoaiId=?, DonViSoanId=?, NguoiKyId=?, VanBanDenGocId=?
                    WHERE Id=?
                """, (
                    data.get('Nam'), data.get('KyHieu'), data.get('NgayKy'), 
                    data.get('TrichYeu'), data.get('NoiNhan'), data.get('TrangThaiChuyen', 0), 
                    data.get('GhiChu'), data.get('FilePath'), data.get('MucDo'),
                    phan_loai_id, don_vi_soan_id, nguoi_ky_id,
                    van_ban_den_goc_id, id_cv
                ))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi cập nhật công văn đi: {str(e)}")

    def delete(self, id_cv: int):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM CongVanPhatHanh WHERE Id = ?", (id_cv,))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi xóa công văn đi: {str(e)}")