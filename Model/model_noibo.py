import pyodbc
import os
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from typing import List, Dict
from config import DB_CONFIG

class ModelNoiBo:
    def __init__(self):
        if DB_CONFIG.get('trusted_connection') in ('yes', True):
            self.conn_str = (
                f"DRIVER={DB_CONFIG['driver']};"
                f"SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};"
                f"Trusted_Connection=yes;"
            )
        else:
            self.conn_str = (
                f"DRIVER={DB_CONFIG['driver']};"
                f"SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};"
                f"UID={DB_CONFIG['username']};"
                f"PWD={DB_CONFIG['password']};"
            )

    def _get_connection(self):
        return pyodbc.connect(self.conn_str)

    def get_all(self, keyword="", user_id=None, is_admin=False):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT 
                    vb.Id,
                    vb.KyHieu,
                    vb.NgayBanHanh,
                    loai.TenLoai AS LoaiVanBan,
                    vb.TrichYeu,
                    donvi.TenDonVi AS DonViSoan,
                    nguoiky.HoTen AS NguoiKy,
                    vb.GhiChu,
                    vb.FileDinhKem
                FROM CongVanNoiBo vb
                LEFT JOIN LoaiCongVan loai ON vb.LoaiCongVanId = loai.Id
                LEFT JOIN DonViTrucThuoc donvi ON vb.DonViSoanId = donvi.Id
                LEFT JOIN CanBo nguoiky ON vb.NguoiKyId = nguoiky.Id
                WHERE 1=1
            """
            params = []
            if keyword:
                query += " AND (vb.KyHieu LIKE ? OR vb.TrichYeu LIKE ?)"
                params.extend([f"%{keyword}%", f"%{keyword}%"])
            if not is_admin and user_id:
                query += " AND vb.NguoiTaoId = ?"
                params.append(user_id)
            query += " ORDER BY vb.NgayBanHanh DESC"
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    def add(self, data: Dict, nguoi_tao_id=1):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                loai_id = self._get_loai_id(data.get("LoaiVanBan"))
                donvi_id = self._get_donvi_id(data.get("DonViSoan"))
                nguoiky_id = self._get_canbo_id(data.get("NguoiKy"))
                ngay_ban_hanh = data.get("NgayBanHanh")
                nam = ngay_ban_hanh[:4] if ngay_ban_hanh else ""
                file_path = data.get("FileDinhKem")
                sql = """
                    INSERT INTO CongVanNoiBo
                    (KyHieu, NgayBanHanh, LoaiCongVanId, TrichYeu, DonViSoanId, 
                     NguoiKyId, GhiChu, Nam, NguoiTaoId, NguoiSoanId, TrangThaiChuyen, 
                     NguoiNhan, FileDinhKem, NguoiDuyetId, NoiDungTrinh, NgayChuyen, SoTrang)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, NULL, NULL, NULL, NULL)
                """
                default_nguoi_nhan = "Đã chọn trong danh sách chi tiết"
                cursor.execute(sql, (
                    data.get("KyHieu"),
                    ngay_ban_hanh,
                    loai_id,
                    data.get("TrichYeu"),
                    donvi_id,
                    nguoiky_id,
                    data.get("GhiChu"),
                    nam,
                    nguoi_tao_id,
                    nguoi_tao_id,
                    default_nguoi_nhan,
                    file_path
                ))
                new_id = cursor.execute("SELECT @@IDENTITY").fetchval()
                nguoi_nhan_ids = data.get("NguoiNhanList", [])
                if nguoi_nhan_ids:
                    for nid in nguoi_nhan_ids:
                        cursor.execute("INSERT INTO CongVanNoBao_NguoiNhan (CongVanNoiBoId, NguoiNhanId, DaXem) VALUES (?, ?, 0)", (new_id, nid))
                    self._tao_cong_viec_noi_bo(new_id, nguoi_nhan_ids, cursor)
                conn.commit()
                return new_id
        except Exception as e:
            print(f"[ERROR] add: {e}")
            import traceback
            traceback.print_exc()
            raise

    def _tao_cong_viec_noi_bo(self, noibo_id, nguoi_nhan_ids, cursor):
        try:
            for nid in nguoi_nhan_ids:
                cursor.execute("SELECT Id FROM CongViecNoiBo WHERE NoiBoId=? AND NguoiNhanId=?", (noibo_id, nid))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO CongViecNoiBo (NoiBoId, NguoiNhanId, TrangThai, NgayTao) VALUES (?, ?, 0, GETDATE())", (noibo_id, nid))
        except Exception as e:
            print(f"[ERROR] _tao_cong_viec_noi_bo: {e}")

    def update(self, id: int, data: Dict):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                loai_id = self._get_loai_id(data.get("LoaiVanBan"))
                donvi_id = self._get_donvi_id(data.get("DonViSoan"))
                nguoiky_id = self._get_canbo_id(data.get("NguoiKy"))
                ngay_ban_hanh = data.get("NgayBanHanh")
                file_path = data.get("FileDinhKem")
                sql = """
                    UPDATE CongVanNoiBo
                    SET KyHieu=?, NgayBanHanh=?, LoaiCongVanId=?, TrichYeu=?, 
                        DonViSoanId=?, NguoiKyId=?, GhiChu=?, FileDinhKem=?
                    WHERE Id=?
                """
                cursor.execute(sql, (
                    data.get("KyHieu"),
                    ngay_ban_hanh,
                    loai_id,
                    data.get("TrichYeu"),
                    donvi_id,
                    nguoiky_id,
                    data.get("GhiChu"),
                    file_path,
                    id
                ))
                cursor.execute("DELETE FROM CongVanNoBao_NguoiNhan WHERE CongVanNoiBoId=?", (id,))
                cursor.execute("DELETE FROM CongViecNoiBo WHERE NoiBoId=?", (id,))
                nguoi_nhan_ids = data.get("NguoiNhanList", [])
                if nguoi_nhan_ids:
                    for nid in nguoi_nhan_ids:
                        cursor.execute("INSERT INTO CongVanNoBao_NguoiNhan (CongVanNoiBoId, NguoiNhanId, DaXem) VALUES (?, ?, 0)", (id, nid))
                        cursor.execute("INSERT INTO CongViecNoiBo (NoiBoId, NguoiNhanId, TrangThai, NgayTao) VALUES (?, ?, 0, GETDATE())", (id, nid))
                conn.commit()
        except Exception as e:
            print(f"[ERROR] update: {e}")
            import traceback
            traceback.print_exc()
            raise

    def delete(self, id: int):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM CongVanNoiBo WHERE Id=?", (id,))
                conn.commit()
        except Exception as e:
            print(f"[ERROR] delete: {e}")

    def get_nguoi_nhan_list(self, noibo_id):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT cb.Id, cb.HoTen FROM CongVanNoBao_NguoiNhan nn
                    JOIN CanBo cb ON nn.NguoiNhanId = cb.Id
                    WHERE nn.CongVanNoiBoId = ?
                """, noibo_id)
                rows = cursor.fetchall()
                return [{"id": row[0], "ten": row[1]} for row in rows]
        except Exception as e:
            print(f"[ERROR] get_nguoi_nhan_list: {e}")
            return []

    def get_van_ban_noi_bo_cua_toi(self, nguoi_dung_id, chi_chua_xem=False):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                sql = """
                    SELECT vb.Id, vb.KyHieu, vb.NgayBanHanh, loai.TenLoai AS LoaiVanBan,
                           vb.TrichYeu, donvi.TenDonVi AS DonViSoan, nguoiky.HoTen AS NguoiKy,
                           vb.GhiChu, vb.FileDinhKem, cv.TrangThai, cv.NgayXem, cv.NgayTao
                    FROM CongVanNoiBo vb
                    LEFT JOIN LoaiCongVan loai ON vb.LoaiCongVanId = loai.Id
                    LEFT JOIN DonViTrucThuoc donvi ON vb.DonViSoanId = donvi.Id
                    LEFT JOIN CanBo nguoiky ON vb.NguoiKyId = nguoiky.Id
                    JOIN CongViecNoiBo cv ON cv.NoiBoId = vb.Id
                    WHERE cv.NguoiNhanId = ?
                """
                params = [nguoi_dung_id]
                if chi_chua_xem:
                    sql += " AND cv.TrangThai = 0"
                sql += " ORDER BY vb.NgayBanHanh DESC"
                cursor.execute(sql, params)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"[ERROR] get_van_ban_noi_bo_cua_toi: {e}")
            return []

    def get_chi_tiet_van_ban_noi_bo(self, noibo_id, nguoi_dung_id):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT vb.Id, vb.KyHieu, vb.NgayBanHanh, loai.TenLoai AS LoaiVanBan,
                           vb.TrichYeu, donvi.TenDonVi AS DonViSoan, nguoiky.HoTen AS NguoiKy,
                           vb.GhiChu, vb.FileDinhKem, cv.TrangThai, cv.NgayXem, cv.NgayTao
                    FROM CongVanNoiBo vb
                    LEFT JOIN LoaiCongVan loai ON vb.LoaiCongVanId = loai.Id
                    LEFT JOIN DonViTrucThuoc donvi ON vb.DonViSoanId = donvi.Id
                    LEFT JOIN CanBo nguoiky ON vb.NguoiKyId = nguoiky.Id
                    LEFT JOIN CongViecNoiBo cv ON cv.NoiBoId = vb.Id AND cv.NguoiNhanId = ?
                    WHERE vb.Id = ?
                """, (nguoi_dung_id, noibo_id))
                row = cursor.fetchone()
                if not row:
                    return None
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
        except Exception as e:
            print(f"[ERROR] get_chi_tiet: {e}")
            return None

    def danh_dau_da_xem(self, noibo_id, nguoi_dung_id):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE CongViecNoiBo
                    SET TrangThai = 1, NgayXem = GETDATE()
                    WHERE NoiBoId = ? AND NguoiNhanId = ?
                """, (noibo_id, nguoi_dung_id))
                conn.commit()
        except Exception as e:
            print(f"[ERROR] danh_dau_da_xem: {e}")

    # ========== Các hàm lấy danh mục ==========
    def get_loai_list(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Id, TenLoai FROM LoaiCongVan ORDER BY TenLoai")
            return [{"id": row[0], "ten": row[1]} for row in cursor.fetchall()]

    def get_donvi_list(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Id, TenDonVi FROM DonViTrucThuoc ORDER BY TenDonVi")
            return [{"id": row[0], "ten": row[1]} for row in cursor.fetchall()]

    def get_canbo_list(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Id, HoTen FROM CanBo ORDER BY HoTen")
            return [{"id": row[0], "ten": row[1]} for row in cursor.fetchall()]

    def get_canbo_by_donvi(self, donvi_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Id, HoTen FROM CanBo WHERE DonViId = ? ORDER BY HoTen", (donvi_id,))
            return [{"id": row[0], "ten": row[1]} for row in cursor.fetchall()]

    def get_all_canbo(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Id, HoTen FROM CanBo ORDER BY HoTen")
            return [{"id": row[0], "ten": row[1]} for row in cursor.fetchall()]

    def get_all_truongphong(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cb.Id, cb.HoTen FROM CanBo cb
                JOIN ChucVu cv ON cb.ChucVuId = cv.Id
                WHERE cv.TenChucVu = N'Trưởng phòng'
            """)
            return [{"id": row[0], "ten": row[1]} for row in cursor.fetchall()]

    def _get_loai_id(self, ten_loai):
        if not ten_loai: return None
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Id FROM LoaiCongVan WHERE TenLoai = ?", (ten_loai,))
            row = cursor.fetchone()
            return row[0] if row else None

    def _get_donvi_id(self, ten_donvi):
        if not ten_donvi: return None
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Id FROM DonViTrucThuoc WHERE TenDonVi = ?", (ten_donvi,))
            row = cursor.fetchone()
            return row[0] if row else None

    def _get_canbo_id(self, ten_cb):
        if not ten_cb: return None
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Id FROM CanBo WHERE HoTen = ?", (ten_cb,))
            row = cursor.fetchone()
            return row[0] if row else None


class NoiBoTableModel(QAbstractTableModel):
    def __init__(self, data: List[Dict]):
        super().__init__()
        self._data = data
        self._headers = ["ID", "Ký hiệu", "Ngày ban hành", "Loại văn bản", "Trích yếu", 
                         "Đơn vị soạn", "Người ký", "Ghi chú", "File đính kèm"]
        self._keys = ["Id", "KyHieu", "NgayBanHanh", "LoaiVanBan", "TrichYeu", 
                      "DonViSoan", "NguoiKy", "GhiChu", "FileDinhKem"]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        row = self._data[index.row()]
        key = self._keys[index.column()]
        value = row.get(key, "")
        if key == "FileDinhKem" and value:
            return os.path.basename(value)
        return str(value) if value is not None else ""

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._headers[section]
        return None

    def get_row(self, row):
        return self._data[row] if row < len(self._data) else {}