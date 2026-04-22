from PyQt6.QtWidgets import *

class ChucVuDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin Chức vụ")
        self.setFixedWidth(350)
        self.data = data
        self.setup_ui()
        if data: self.fill_data()

    def setup_ui(self):
        layout = QFormLayout(self)
        self.txt_ten = QLineEdit()
        self.cmb_status = QComboBox()
        self.cmb_status.addItem("Ẩn", 0)
        self.cmb_status.addItem("Hiển thị", 1)
        self.txt_ghichu = QTextEdit()
        self.txt_ghichu.setFixedHeight(60)

        layout.addRow("Tên chức vụ (*):", self.txt_ten)
        layout.addRow("Trạng thái:", self.cmb_status)
        layout.addRow("Ghi chú:", self.txt_ghichu)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)

    def fill_data(self):
        self.txt_ten.setText(self.data['TenChucVu'])
        self.cmb_status.setCurrentIndex(1 if self.data['TrangThai'] == 1 else 0)
        self.txt_ghichu.setPlainText(str(self.data['GhiChu'] or ""))

    def get_data(self):
        return {
            "Id": self.data['Id'] if self.data else None,
            "TenChucVu": self.txt_ten.text(),
            "TrangThai": self.cmb_status.currentData(),
            "GhiChu": self.txt_ghichu.toPlainText()
        }