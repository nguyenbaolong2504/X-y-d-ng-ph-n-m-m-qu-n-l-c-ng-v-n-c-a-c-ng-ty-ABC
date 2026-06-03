import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, Qt

class ChiTietNoiBoNhanDialog(QDialog):
    def __init__(self, data, conn_str, parent=None):
        super().__init__(parent)
        self.data = data
        self.conn_str = conn_str
        self.setWindowTitle("Chi tiết văn bản nội bộ")
        self.setMinimumSize(600, 400)
        layout = QVBoxLayout()
        info = f"""
        <b>Ký hiệu:</b> {data.get('KyHieu', '')}<br>
        <b>Ngày ban hành:</b> {data.get('NgayBanHanh', '')}<br>
        <b>Loại văn bản:</b> {data.get('LoaiVanBan', '')}<br>
        <b>Trích yếu:</b> {data.get('TrichYeu', '')}<br>
        <b>Đơn vị soạn:</b> {data.get('DonViSoan', '')}<br>
        <b>Người ký:</b> {data.get('NguoiKy', '')}<br>
        <b>Ghi chú:</b> {data.get('GhiChu', '')}<br>
        <b>Trạng thái:</b> {'Đã xem' if data.get('TrangThai') == 1 else 'Chưa xem'}<br>
        <b>Ngày nhận:</b> {data.get('NgayTao', '')}<br>
        """
        if data.get('NgayXem'):
            info += f"<b>Ngày xem:</b> {data['NgayXem']}<br>"
        label = QLabel(info)
        label.setWordWrap(True)
        layout.addWidget(label)

        if data.get('FileDinhKem') and os.path.exists(data['FileDinhKem']):
            btn_xem = QPushButton("📄 Xem file đính kèm")
            btn_xem.clicked.connect(lambda: os.startfile(data['FileDinhKem']))
            layout.addWidget(btn_xem)

        if data.get('TrangThai') == 0:
            btn_doc = QPushButton("✅ Đánh dấu đã đọc")
            btn_doc.clicked.connect(self.accept)
            layout.addWidget(btn_doc)

        btn_close = QPushButton("Đóng")
        btn_close.clicked.connect(self.reject)
        layout.addWidget(btn_close)
        self.setLayout(layout)


class NoiBoNhanWidget(QWidget):
    da_xem_signal = pyqtSignal(int)

    def __init__(self, user_session, conn_str, model, parent=None):
        super().__init__(parent)
        self.user_id = user_session.user_id
        self.conn_str = conn_str
        self.model = model
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        toolbar = QHBoxLayout()
        self.btn_refresh = QPushButton("🔄 Làm mới")
        self.btn_refresh.clicked.connect(self.load_data)
        self.chk_chua_xem = QCheckBox("Chỉ hiển thị chưa xem")
        self.chk_chua_xem.stateChanged.connect(self.load_data)
        toolbar.addWidget(self.btn_refresh)
        toolbar.addWidget(self.chk_chua_xem)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["ID", "Ký hiệu", "Ngày ban hành", "Loại VB", "Trích yếu",
                                              "Đơn vị soạn", "Người ký", "Trạng thái", "Ngày nhận"])
        self.table.setColumnHidden(0, True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.xem_chi_tiet)
        layout.addWidget(self.table)

    def load_data(self):
        chi_chua_xem = self.chk_chua_xem.isChecked()
        data = self.model.get_van_ban_noi_bo_cua_toi(self.user_id, chi_chua_xem)
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(str(row.get('Id', ''))))
            self.table.setItem(i, 1, QTableWidgetItem(row.get('KyHieu', '')))
            self.table.setItem(i, 2, QTableWidgetItem(str(row.get('NgayBanHanh', ''))))
            self.table.setItem(i, 3, QTableWidgetItem(row.get('LoaiVanBan', '')))
            self.table.setItem(i, 4, QTableWidgetItem(row.get('TrichYeu', '')))
            self.table.setItem(i, 5, QTableWidgetItem(row.get('DonViSoan', '')))
            self.table.setItem(i, 6, QTableWidgetItem(row.get('NguoiKy', '')))
            trangthai = "Đã xem" if row.get('TrangThai') == 1 else "Chưa xem"
            self.table.setItem(i, 7, QTableWidgetItem(trangthai))
            self.table.setItem(i, 8, QTableWidgetItem(str(row.get('NgayTao', ''))))
        self.table.resizeColumnsToContents()

    def xem_chi_tiet(self):
        row = self.table.currentRow()
        if row < 0:
            return
        noibo_id = int(self.table.item(row, 0).text())
        data = self.model.get_chi_tiet_van_ban_noi_bo(noibo_id, self.user_id)
        if not data:
            QMessageBox.warning(self, "Lỗi", "Không thể tải chi tiết văn bản")
            return
        dlg = ChiTietNoiBoNhanDialog(data, self.conn_str, self)
        if dlg.exec() == QDialog.DialogCode.Accepted and data.get('TrangThai') == 0:
            self.model.danh_dau_da_xem(noibo_id, self.user_id)
            self.da_xem_signal.emit(noibo_id)
            self.load_data()