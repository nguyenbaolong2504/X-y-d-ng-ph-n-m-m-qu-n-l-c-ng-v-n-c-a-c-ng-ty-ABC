from PyQt6.QtCore import Qt, QAbstractTableModel

class CanBoTableModel(QAbstractTableModel):
    def __init__(self, data=None, headers=None):
        super().__init__()
        self._data = data or []
        self._headers = headers or []

    def rowCount(self, parent=None): return len(self._data)
    def columnCount(self, parent=None): return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            row_data = self._data[index.row()]
            col = index.column()
            # Logic hiển thị theo cột
            if col == 0: return index.row() + 1 # STT
            if col == 1: return row_data.get('HoTen')
            if col == 2: return str(row_data.get('NgaySinh'))
            if col == 3: return "Nam" if row_data.get('GioiTinh') == 1 else "Nữ"
            if col == 4: return row_data.get('TenChucVu')
            if col == 5: return row_data.get('TenDonVi')
            if col == 6: return row_data.get('Username')
            if col == 7: return row_data.get('Email')
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return None

    def get_row_data(self, row_index):
        return self._data[row_index]