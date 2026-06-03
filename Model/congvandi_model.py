import pyodbc
from typing import List, Dict
from config import DB_CONFIG
from datetime import datetime
import os

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
            raise Exception(f"Lỗi truy vấn: {str(e)}")

    def get_max_so_phat_hanh(self) -> int:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ISNULL(MAX(SoPhatHanh), 0) FROM CongVanPhatHanh")
                result = cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            return 0

    def get_all(self, tu_ngay=None, den_ngay=None, keyword=None,
                is_admin=None, role=None, ten_don_vi=None, nguoi_tao_id=None, **kwargs):
        sql = """
            SELECT Id, SoPhatHanh, Nam, KyHieu, NgayKy,
                   NoiNhan, TrichYeu, TrangThaiChuyen, GhiChu, FilePath,
                   PhanLoaiId, DonViSoanId, NguoiKyId, VanBanDenGocId, MucDo
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

        if not is_admin and nguoi_tao_id is not None:
            sql += " AND NguoiTaoId = ?"
            params.append(nguoi_tao_id)

        sql += " ORDER BY Id DESC"
        return self._execute_query(sql, tuple(params))

    def add(self, data: Dict) -> int:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                new_so = self.get_max_so_phat_hanh() + 1

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

                muc_do = data.get('MucDo', 'Thường')
                trang_thai = data.get('TrangThaiChuyen', 0)
                nguoi_tao_id = data.get('NguoiTaoId', 1)

                cursor.execute("""
                    INSERT INTO CongVanPhatHanh
                    (SoPhatHanh, Nam, KyHieu, NgayKy, TrichYeu, NoiNhan, TrangThaiChuyen,
                     GhiChu, FilePath, NgayChuyen, PhanLoaiId, DonViSoanId, NguoiKyId,
                     VanBanDenGocId, NguoiTaoId, MucDo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), ?, ?, ?, ?, ?, ?)
                """, (
                    new_so, data.get('Nam'), data.get('KyHieu'), data.get('NgayKy'),
                    data.get('TrichYeu'), data.get('NoiNhan'), trang_thai,
                    data.get('GhiChu'), data.get('FilePath'),
                    phan_loai_id, don_vi_soan_id, nguoi_ky_id,
                    van_ban_den_goc_id, nguoi_tao_id, muc_do
                ))
                conn.commit()
                cursor.execute("SELECT @@IDENTITY")
                new_id = int(cursor.fetchone()[0])
                return new_id
        except Exception as e:
            raise Exception(f"Lỗi thêm: {str(e)}")

    def update(self, id_cv: int, data: Dict):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT FilePath FROM CongVanPhatHanh WHERE Id = ?", (id_cv,))
                old_row = cursor.fetchone()
                old_file = old_row[0] if old_row else None

                new_file = data.get('FilePath')
                if new_file and old_file and new_file != old_file and os.path.exists(old_file):
                    try:
                        os.remove(old_file)
                    except:
                        pass
                if not new_file and old_file and os.path.exists(old_file):
                    try:
                        os.remove(old_file)
                    except:
                        pass

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

                muc_do = data.get('MucDo', 'Thường')
                trang_thai = data.get('TrangThaiChuyen', 0)

                cursor.execute("""
                    UPDATE CongVanPhatHanh SET
                        Nam=?, KyHieu=?, NgayKy=?, TrichYeu=?, NoiNhan=?,
                        TrangThaiChuyen=?, GhiChu=?, FilePath=?,
                        PhanLoaiId=?, DonViSoanId=?, NguoiKyId=?,
                        VanBanDenGocId=?, MucDo=?
                    WHERE Id=?
                """, (
                    data.get('Nam'), data.get('KyHieu'), data.get('NgayKy'),
                    data.get('TrichYeu'), data.get('NoiNhan'), trang_thai,
                    data.get('GhiChu'), new_file,
                    phan_loai_id, don_vi_soan_id, nguoi_ky_id,
                    van_ban_den_goc_id, muc_do, id_cv
                ))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi cập nhật: {str(e)}")

    def delete(self, id_cv: int):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT FilePath FROM CongVanPhatHanh WHERE Id = ?", (id_cv,))
                row = cursor.fetchone()
                if row and row[0] and os.path.exists(row[0]):
                    try:
                        os.remove(row[0])
                    except:
                        pass
                cursor.execute("DELETE FROM CongVanPhatHanh WHERE Id = ?", (id_cv,))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi xóa: {str(e)}")
    def update_trang_thai(self, id_cv: int, trang_thai: int):
        sql = "UPDATE CongVanPhatHanh SET TrangThaiChuyen = ? WHERE Id = ?"
        self._execute_query(sql, (trang_thai, id_cv))