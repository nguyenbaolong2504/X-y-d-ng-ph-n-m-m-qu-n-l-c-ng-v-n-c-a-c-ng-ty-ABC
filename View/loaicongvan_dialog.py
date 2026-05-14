from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QTextEdit, QPushButton, QHBoxLayout, QLabel)
from PyQt6.QtCore import Qt

class LoaiCongVanDialog(QDialog):
    def __init__(self, title="Cập nhật Loại công văn", data=None, default_trangthai=1):
        super().__init__()
        self.data = data
        self.trangthai_hidden = default_trangthai
        self.setWindowTitle(title)
        self.setFixedWidth(450)
        self.setup_ui()
        self.apply_styles()
        
        if data:
            self.fill_data()

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog { background-color: #ffffff; font-family: 'Segoe UI', Arial; }
            QLabel { font-weight: bold; color: #34495e; font-size: 14px; }
            QLineEdit { min-height: 35px; padding: 0px 10px; border: 1px solid #bdc3c7; border-radius: 6px; font-size: 14px; background-color: #fdfdfd; color: #2c3e50; }
            QTextEdit { border: 1px solid #bdc3c7; border-radius: 6px; padding: 10px; font-size: 14px; background-color: #fdfdfd; color: #2c3e50; }
            QLineEdit:focus, QTextEdit:focus { border: 2px solid #3498db; background-color: #ffffff; }
            QPushButton { border-radius: 6px; padding: 10px 20px; font-weight: bold; font-size: 14px; border: none; }
            QPushButton#BtnSave { background-color: #2ecc71; color: white; }
            QPushButton#BtnSave:hover { background-color: #27ae60; }
            QPushButton#BtnCancel { background-color: #ecf0f1; color: #7f8c8d; }
            QPushButton#BtnCancel:hover { background-color: #bdc3c7; color: white; }
        """)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        info_lbl = QLabel("Thông tin loại công văn")
        info_lbl.setStyleSheet("color: #7f8c8d; font-size: 12px; text-transform: uppercase;")
        layout.addWidget(info_lbl)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.txt_ma = QLineEdit()
        self.txt_ma.setPlaceholderText("VD: CV, QD, TB...")
        
        self.txt_ten = QLineEdit()
        self.txt_ten.setPlaceholderText("Nhập tên loại công văn...")

        self.txt_mota = QTextEdit()
        self.txt_mota.setPlaceholderText("Mô tả chi tiết (nếu có)...")
        self.txt_mota.setFixedHeight(100)

        form_layout.addRow("Mã loại:", self.txt_ma)
        form_layout.addRow("Tên loại:", self.txt_ten)
        form_layout.addRow("Mô tả:", self.txt_mota)

        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Lưu dữ liệu")
        self.btn_save.setObjectName("BtnSave")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_cancel = QPushButton("Hủy bỏ")
        self.btn_cancel.setObjectName("BtnCancel")
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

    def fill_data(self):
        self.txt_ma.setText(str(self.data.get('MaLoai', '') or ''))
        self.txt_ten.setText(str(self.data.get('TenLoai', '')))
        self.txt_mota.setPlainText(str(self.data.get('MoTa', '') or ''))
        self.trangthai_hidden = self.data.get('TrangThai', 1)

    def get_data(self):
        res = {
            "MaLoai": self.txt_ma.text().strip(),
            "TenLoai": self.txt_ten.text().strip(),
            "MoTa": self.txt_mota.toPlainText().strip(),
            "TrangThai": self.trangthai_hidden 
        }
        if self.data:
            res["Id"] = self.data["Id"]
        return res