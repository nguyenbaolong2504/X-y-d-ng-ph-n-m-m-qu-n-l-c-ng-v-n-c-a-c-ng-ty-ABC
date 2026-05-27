from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from typing import List, Dict
import os

class CongVanDiTableModel(QAbstractTableModel):
    def __init__(self, data: List[Dict], headers: List[str]):
        super().__init__()
        self._data = data
        self._headers = headers
        self._col_keys = [
            "Id",               # 0
            "SoPhatHanh",       # 1
            "Nam",              # 2
            "KyHieu",           # 3
            "NgayKy",           # 4
            "NoiNhan",          # 5
            "TrichYeu",         # 6
            "TrangThaiChuyen",  # 7
            "MucDo",            # 8
            "FilePath"          # 9
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
            if col >= len(self._col_keys):
                return None
            key = self._col_keys[col]
            value = self._data[row].get(key, "")
            if key == "TrangThaiChuyen":
                return "Đã chuyển" if value == 1 else "Chưa chuyển"
            if key == "NgayKy" and value:
                return str(value).split(' ')[0]
            if key == "FilePath" and value:
                return os.path.basename(value)
            return str(value) if value is not None else ""
        if role == Qt.ItemDataRole.UserRole and index.column() == 9:
            file_path = self._data[index.row()].get("FilePath")
            if file_path:
                return file_path
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            if section < len(self._headers):
                return self._headers[section]
        return None

    def get_row(self, row: int) -> Dict:
        if 0 <= row < len(self._data):
            return self._data[row]
        return {}