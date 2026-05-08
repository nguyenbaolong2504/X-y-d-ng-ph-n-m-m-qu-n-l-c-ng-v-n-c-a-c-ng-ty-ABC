import pyodbc

class XuLyCongVanModel:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_all_xuly(self):
        cursor = self.db.cursor()
        # Đã sửa: DonVi -> DonViTrucThuoc (Khớp với cấu trúc CSDL của bạn)
        query = """
            SELECT 
                t.Id, 
                cb.HoTen AS TenCanBoNhan, 
                vbd.TrichYeu AS TieuDeCongVan, 
                dv.TenDonVi AS TenDonViChuyen, 
                t.NgayChuyen, 
                t.NoiDungYeuCau, 
                cbc.HoTen AS TenCanBoChuyen
            FROM CongVanDen_CanBo t
            LEFT JOIN CanBo cb ON t.CanBoId = cb.Id
            LEFT JOIN CongVanDen vbd ON t.VanBanDenId = vbd.Id
            LEFT JOIN DonViTrucThuoc dv ON t.DonViChuyenId = dv.Id
            LEFT JOIN CanBo cbc ON t.CanBoChuyenId = cbc.Id
            ORDER BY t.Id DESC
        """
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def add_xuly(self, data):
        cursor = self.db.cursor()
        query = """
            INSERT INTO CongVanDen_CanBo (CanBoId, VanBanDenId, DonViChuyenId, NgayChuyen, NoiDungYeuCau, CanBoChuyenId)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (data['CanBoId'], data['VanBanDenId'], data['DonViChuyenId'], 
                               data['NgayChuyen'], data['NoiDungYeuCau'], data['CanBoChuyenId']))
        self.db.commit()
        return True

    def update_xuly(self, data):
        cursor = self.db.cursor()
        query = """
            UPDATE CongVanDen_CanBo 
            SET CanBoId = ?, VanBanDenId = ?, DonViChuyenId = ?, 
                NgayChuyen = ?, NoiDungYeuCau = ?, CanBoChuyenId = ?
            WHERE Id = ?
        """
        cursor.execute(query, (
            data['CanBoId'], data['VanBanDenId'], data['DonViChuyenId'], 
            data['NgayChuyen'], data['NoiDungYeuCau'], data['CanBoChuyenId'], data['Id']
        ))
        self.db.commit()
        return True

    def delete_xuly(self, id_xuly):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM CongVanDen_CanBo WHERE Id = ?", (id_xuly,))
        self.db.commit()
        return cursor.rowcount > 0

    # --- CÁC HÀM LẤY DANH MỤC (ĐÃ ĐƯA VÀO TRONG CLASS) ---
    
    def get_list_canbo(self):
        """Lấy danh sách cán bộ từ bảng CanBo"""
        cursor = self.db.cursor()
        cursor.execute("SELECT Id, HoTen FROM CanBo")
        return cursor.fetchall()

    def get_list_donvi(self):
        """Lấy danh sách đơn vị từ bảng DonViTrucThuoc"""
        cursor = self.db.cursor()
        # Đảm bảo dùng tên bảng 'DonViTrucThuoc' để tránh lỗi Invalid Object Name
        cursor.execute("SELECT Id, TenDonVi FROM DonViTrucThuoc")
        return cursor.fetchall()

    def get_list_congvan(self):
        """Lấy danh sách trích yếu công văn từ bảng CongVanDen"""
        cursor = self.db.cursor()
        cursor.execute("SELECT Id, TrichYeu FROM CongVanDen")
        return cursor.fetchall()