import pyodbc
from typing import List, Dict
from config import DB_CONFIG

class CongVanModel:
    def __init__(self):
        # Tự động cấu hình chuỗi kết nối linh hoạt
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
        """Hàm nội bộ để thực thi truy vấn và trả về danh sách Dictionary"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                # Lấy tên cột từ mô tả của cursor
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            raise Exception(f"Lỗi truy vấn cơ sở dữ liệu: {str(e)}")

    # --- 1. LẤY DANH MỤC PHÒNG BAN ---
    def get_phong_ban(self) -> List[str]:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT TenDonVi FROM DonViTrucThuoc WHERE TrangThai = 1")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Lỗi nạp danh mục đơn vị: {e}")
            return []

    # --- 2. LẤY TẤT CẢ (MẶC ĐỊNH KHI MỞ APP) ---
    def get_all(self) -> List[Dict]:
        sql = """
            SELECT Id as id, NgayDen as ngay_den, SoDen as so_den, 
                   NoiPhatHanh as tac_gia, KyHieu as so_ky_hieu, 
                   NgayKy as ngay_van_ban, TrichYeu as trich_yeu, 
                   NoiNhan as don_vi_nhan, NgayChuyen as ngay_chuyen, 
                   TrangThaiChuyen as trang_thai, GhiChu as ghi_chu
            FROM CongVanDen
            ORDER BY NgayDen DESC
        """
        return self._execute_query(sql)

    # --- 3. TÌM KIẾM THEO TÁC GIẢ HOẶC SỐ ĐẾN ---
    def search_by_author_or_number(self, keyword: str) -> List[Dict]:
        sql = """
            SELECT Id as id, NgayDen as ngay_den, SoDen as so_den, 
                   NoiPhatHanh as tac_gia, KyHieu as so_ky_hieu, 
                   NgayKy as ngay_van_ban, TrichYeu as trich_yeu, 
                   NoiNhan as don_vi_nhan, NgayChuyen as ngay_chuyen, 
                   TrangThaiChuyen as trang_thai, GhiChu as ghi_chu
            FROM CongVanDen
            WHERE NoiPhatHanh LIKE ? OR SoDen LIKE ? OR KyHieu LIKE ?
            ORDER BY NgayDen DESC
        """
        like_val = f"%{keyword}%"
        return self._execute_query(sql, (like_val, like_val, like_val))

    # --- 4. LỌC THEO NGÀY ĐẾN ---
    def filter_by_ngay_den(self, tu_ngay: str, den_ngay: str) -> List[Dict]:
        sql = """
            SELECT Id as id, NgayDen as ngay_den, SoDen as so_den, 
                   NoiPhatHanh as tac_gia, KyHieu as so_ky_hieu, 
                   NgayKy as ngay_van_ban, TrichYeu as trich_yeu, 
                   NoiNhan as don_vi_nhan, NgayChuyen as ngay_chuyen, 
                   TrangThaiChuyen as trang_thai, GhiChu as ghi_chu
            FROM CongVanDen
            WHERE NgayDen BETWEEN ? AND ?
            ORDER BY NgayDen DESC
        """
        return self._execute_query(sql, (tu_ngay, den_ngay))

    # --- 5. CÁC THAO TÁC NGHIỆP VỤ (THÊM/SỬA/XÓA) ---
    def add(self, data: Dict) -> int:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO CongVanDen (Nam, SoDen, KyHieu, NgayDen, NgayKy, NoiPhatHanh, 
                                           TrichYeu, NoiNhan, NgayChuyen, GhiChu)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data['ngay_den'][:4], # Tự lấy năm từ chuỗi ngày
                    data.get('so_den'), data['so_ky_hieu'], data['ngay_den'], data['ngay_van_ban'],
                    data['tac_gia'], data['trich_yeu'], data['don_vi_nhan'], data['ngay_chuyen'], data.get('ghi_chu')
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
                        TrichYeu = ?, NoiNhan = ?, NgayChuyen = ?, GhiChu = ?
                    WHERE Id = ?
                """, (
                    data.get('so_den'), data['so_ky_hieu'], data['ngay_den'], data['ngay_van_ban'],
                    data['tac_gia'], data['trich_yeu'], data['don_vi_nhan'], data['ngay_chuyen'], data.get('ghi_chu'), id
                ))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi cập nhật dữ liệu: {str(e)}")

    def delete(self, id: int):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM CongVanDen WHERE Id = ?", (id,))
                conn.commit()
        except Exception as e:
            raise Exception(f"Lỗi xóa dữ liệu: {str(e)}")