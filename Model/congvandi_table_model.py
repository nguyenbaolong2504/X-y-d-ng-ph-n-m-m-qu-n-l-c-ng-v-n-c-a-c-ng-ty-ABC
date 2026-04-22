from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from typing import List, Dict

class CongVanDiTableModel(QAbstractTableModel):
    def __init__(self, data: List[Dict], headers: List[str]):
        super().__init__()
        self._data = data
        self._headers = headers
        # QUAN TRỌNG: Các key này phải khớp chính xác với tên cột trong SQL SELECT
        self._col_keys = [
            "Id",               # Cột 0 (Ẩn)
            "SoPhatHanh",       # Cột 1
            "Nam",              # Cột 2
            "KyHieu",           # Cột 3
            "NgayKy",           # Cột 4
            "NoiNhan",          # Cột 5
            "TrichYeu",         # Cột 6
            "TrangThaiChuyen"   # Cột 7
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
            
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            col = index.column()
            
            # Kiểm tra nếu column index vượt quá danh sách keys
            if col >= len(self._col_keys):
                return None
                
            key = self._col_keys[col]
            value = self._data[row].get(key, "")

            # Xử lý riêng cho cột Trạng thái để hiển thị chữ thay vì số 0/1
            if key == "TrangThaiChuyen":
                return "Đã chuyển" if value == 1 else "Chưa chuyển"
            
            # Cột ID (col 0) thường để trống hoặc trả về giá trị nếu muốn hiện
            if col == 0:
                return str(value) if value is not None else ""

            return str(value) if value is not None else ""
            
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            if section < len(self._headers):
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