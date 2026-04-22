from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from typing import List, Dict

class CongVanTableModel(QAbstractTableModel):
    def __init__(self, data: List[Dict], headers: List[str]):
        super().__init__()
        self._data = data
        self._headers = headers
        self._col_keys = [
            "id", "tac_vu", "ngay_den", "so_den", "tac_gia", "so_ky_hieu",
            "ngay_van_ban", "trich_yeu", "don_vi_nhan", "ngay_chuyen",
            "trang_thai", "ghi_chu"
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
        
        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0: return "" # Cột Checkbox (ẩn text)
            if col == 1: return "🖨️ / 📝" # Icon Tác vụ
            
            key = self._col_keys[col]
            value = self._data[row].get(key, "")
            
            # Xử lý hiển thị ngày tháng bỏ phần thời gian nếu có
            if key in ["ngay_den", "ngay_van_ban", "ngay_chuyen"] and value:
                return str(value).split()[0]
                
            return str(value) if value is not None else ""
            
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return None

    def refresh_data(self, new_data: List[Dict]):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

    def get_row(self, row: int) -> Dict:
        if 0 <= row < len(self._data):
            return self._data[row]
        return {}