from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from typing import List, Dict
import os

class CongVanTableModel(QAbstractTableModel):
    def __init__(self, data: List[Dict], headers: List[str]):
        super().__init__()
        self._data = data
        self._headers = headers
        self._keys = [
            "id", "tac_vu", "ngay_den", "so_den", "tac_gia", "so_ky_hieu",
            "ngay_van_ban", "trich_yeu", "nguoi_xu_ly",
            "trang_thai", "ten_loai", "muc_do", "file_dinh_kem", "ghi_chu"
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        if col >= len(self._keys):
            return None
        key = self._keys[col]
        item = self._data[row]

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return ""
            if col == 1:
                return "📝"
            value = item.get(key)
            if key == "trang_thai":
                mapping = {0: "Mới tiếp nhận", 1: "Chờ sếp phân công", 2: "Đang xử lý", 3: "Hoàn thành"}
                return mapping.get(value, "Mới tiếp nhận")
            if key in ("ngay_den", "ngay_van_ban") and value:
                return str(value).split()[0]
            if key == "file_dinh_kem":
                return os.path.basename(str(value)) if value else ""
            if key == "muc_do":
                return value if value else "Thường"
            return str(value) if value is not None else ""
            
        if role == Qt.ItemDataRole.UserRole and col == 12:
            return item.get("file_dinh_kem")
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return None

    def get_row(self, row: int) -> Dict:
        if 0 <= row < len(self._data):
            return self._data[row]
        return {}