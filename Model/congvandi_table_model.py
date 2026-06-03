import os
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from typing import List, Dict

class CongVanDiTableModel(QAbstractTableModel):
    def __init__(self, data: List[Dict], headers: List[str]):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        if row < 0 or row >= len(self._data):
            return None
        record = self._data[row]
        key = self._headers[col]

        if role == Qt.ItemDataRole.DisplayRole:
            if key == "Trạng thái":
                # SỬA: Chỉ 3 trạng thái
                tt_map = {1: "Chờ ký", 2: "Đã ký", 3: "Đã phát hành"}
                val = record.get("TrangThaiChuyen", 1)
                return tt_map.get(val, "Chờ ký")
            elif key == "Mức độ":
                return record.get("MucDo", "Thường")
            elif key == "File":
                file_path = record.get("FilePath", "")
                if file_path and isinstance(file_path, str):
                    return os.path.basename(file_path) if os.path.exists(file_path) else "File không tồn tại"
                return "Chưa có file"
            elif key == "ID":
                return record.get("Id", record.get("id", ""))
            elif key == "Số đi":
                return record.get("SoPhatHanh", "")
            elif key == "Năm":
                return record.get("Nam", "")
            elif key == "Ký hiệu":
                return record.get("KyHieu", "")
            elif key == "Ngày ký":
                ngay = record.get("NgayKy", "")
                if ngay and len(str(ngay)) > 10:
                    return str(ngay)[:10]
                return str(ngay) if ngay else ""
            elif key == "Nơi nhận":
                return record.get("NoiNhan", "")
            elif key == "Trích yếu":
                return record.get("TrichYeu", "")
            else:
                return record.get(key, "")

        elif role == Qt.ItemDataRole.UserRole:
            if key == "File":
                return record.get("FilePath", "")
            return None

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if section < len(self._headers):
                return self._headers[section]
        return None

    def get_row(self, row: int) -> Dict:
        if 0 <= row < len(self._data):
            return self._data[row]
        return {}

    def get_data(self) -> List[Dict]:
        return self._data