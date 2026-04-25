from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QTextEdit, QPushButton, QHBoxLayout, QLabel)
from PyQt6.QtCore import Qt

class LoaiVanBanDialog(QDialog):
    def __init__(self, title="Cập nhật Loại văn bản", data=None):
        super().__init__()
        self.data = data
        self.setWindowTitle(title)
        self.setFixedWidth(450)
        self.setup_ui()
        self.apply_styles()
        if data:
            self.fill_data()

    def apply_styles(self):
        # Thiết kế Premium: Nền trắng, chữ đậm, ô nhập liệu có bo góc
        self.setStyleSheet("""
            QDialog { 
                background-color: #ffffff; 
                font-family: 'Segoe UI', Arial; 
            }
            QLabel { 
                font-weight: bold; 
                color: #34495e; 
                font-size: 14px; 
            }
            /* Fix lỗi tàng hình chữ bằng cách set min-height và color rõ ràng */
            QLineEdit {
                min-height: 35px;
                padding: 0px 10px;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                font-size: 14px;
                background-color: #fdfdfd;
                color: #2c3e50;
            }
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                background-color: #fdfdfd;
                color: #2c3e50;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #3498db;
                background-color: #ffffff;
            }
            QPushButton {
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton#BtnSave {
                background-color: #2ecc71; 
                color: white;
            }
            QPushButton#BtnSave:hover { background-color: #27ae60; }
            
            QPushButton#BtnCancel {
                background-color: #ecf0f1; 
                color: #7f8c8d;
            }
            QPushButton#BtnCancel:hover { background-color: #bdc3c7; color: white; }
        """)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Tiêu đề nhỏ bên trong form
        info_lbl = QLabel("Thông tin loại văn bản")
        info_lbl.setStyleSheet("color: #7f8c8d; font-size: 12px; text-transform: uppercase;")
        layout.addWidget(info_lbl)

        # Layout form nhập liệu
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.txt_ma = QLineEdit()
        self.txt_ma.setPlaceholderText("VD: CV, QD, TB...")
        
        self.txt_ten = QLineEdit()
        self.txt_ten.setPlaceholderText("Nhập tên loại văn bản...")
        
        self.txt_ghichu = QTextEdit()
        self.txt_ghichu.setPlaceholderText("Ghi chú thêm (nếu có)...")
        self.txt_ghichu.setFixedHeight(100)

        form_layout.addRow("Mã loại:", self.txt_ma)
        form_layout.addRow("Tên loại:", self.txt_ten)
        form_layout.addRow("Ghi chú:", self.txt_ghichu)

        layout.addLayout(form_layout)

        # Hàng nút bấm phía dưới
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
        # Đổ dữ liệu cũ vào form khi thực hiện Sửa
        self.txt_ma.setText(str(self.data.get('MaCongVan', '') or ''))
        self.txt_ten.setText(str(self.data.get('TenHinhThuc', '')))
        self.txt_ghichu.setPlainText(str(self.data.get('GhiChu', '') or ''))

    def get_data(self):
        # Gom dữ liệu để Controller ném xuống Model
        res = {
            "MaCongVan": self.txt_ma.text().strip(),
            "TenHinhThuc": self.txt_ten.text().strip(),
            "GhiChu": self.txt_ghichu.toPlainText().strip()
        }
        if self.data:
            res["Id"] = self.data["Id"]
        return res