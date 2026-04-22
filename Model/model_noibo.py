import pyodbc
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from typing import List, Dict
from config import DB_CONFIG # Đảm bảo file config này chứa thông tin SQL Server

class ModelNoiBo:
    def __init__(self):
        # Kết nối SQL Server (dùng chung cấu hình với Văn bản đi/đến)
        if 'trusted_connection' in DB_CONFIG:
            self.conn_str = (
                f"DRIVER={DB_CONFIG['driver']};"
                f"SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};"
                f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
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

    def get_all(self, keyword="") -> List[Dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Câu lệnh SELECT phải khớp với các cột trong ảnh image_5e5448.png
            query = """
                SELECT Id, KyHieu, NgayBanHanh, LoaiCongVanId, TrichYeu, 
                       DonViSoanId, NguoiKyId, NguoiNhan, GhiChu
                FROM CongVanNoiBo
            """
            if keyword:
                query += " WHERE KyHieu LIKE ? OR TrichYeu LIKE ?"
                cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
            else:
                query += " ORDER BY Id DESC"
                cursor.execute(query)
            
            rows = cursor.fetchall()
            # Biến đổi kết quả thành list các dictionary
            return [dict(zip([col[0] for col in cursor.description], row)) for row in rows]

class NoiBoTableModel(QAbstractTableModel):
    def __init__(self, data: List[Dict]):
        super().__init__()
        self._data = data
        # Header hiển thị trên giao diện
        self._headers = ["ID", "Ký hiệu", "Ngày ban hành", "Loại văn bản", 
                         "Trích yếu, thông báo", "Đơn vị soạn", "Người ký", 
                         "Đơn vị nhận", "Ghi chú"]
        # Key phải khớp CHÍNH XÁC với tên cột trong SQL Server (PascalCase)
        self._keys = ["Id", "KyHieu", "NgayBanHanh", "LoaiCongVanId", 
                      "TrichYeu", "DonViSoanId", "NguoiKyId", 
                      "NguoiNhan", "GhiChu"]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
            
        if role == Qt.ItemDataRole.DisplayRole:
            row = self._data[index.row()]
            col = index.column()
            key = self._keys[col]
            value = row.get(key, "")
            
            # Xử lý giá trị None để tránh lỗi str()
            return str(value) if value is not None else ""
        return None

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return None