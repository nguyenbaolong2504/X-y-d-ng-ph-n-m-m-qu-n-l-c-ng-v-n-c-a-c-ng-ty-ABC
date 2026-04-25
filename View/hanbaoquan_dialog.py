from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, 
                             QLineEdit, QTextEdit, QPushButton, QHBoxLayout, QLabel)
from PyQt6.QtCore import Qt

class HanBaoQuanDialog(QDialog):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.setWindowTitle("Cập nhật Thời hạn bảo quản")
        self.setFixedWidth(450)
        self.setup_ui()
        self.apply_styles()
        if data:
            self.fill_data()

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog { background-color: #ffffff; font-family: 'Segoe UI'; }
            QLabel { 
                font-weight: bold; 
                color: #34495e; 
                font-size: 14px; 
            }
            QLineEdit, QTextEdit {
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background-color: #fcfcfc;
                color: #2c3e50;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #3498db;
                background-color: #ffffff;
            }
            QPushButton {
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
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
            QPushButton#BtnCancel:hover { background-color: #bdc3c7; color: white;}
        """)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Form nhập liệu
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.txt_ten = QLineEdit()
        self.txt_ten.setPlaceholderText("Nhập tên thời hạn (VD: 5 năm, Vĩnh viễn...)")
        
        self.txt_ghichu = QTextEdit()
        self.txt_ghichu.setPlaceholderText("Nhập ghi chú chi tiết nếu có...")
        self.txt_ghichu.setFixedHeight(100)

        form_layout.addRow(QLabel("Tên thời hạn:"), self.txt_ten)
        form_layout.addRow(QLabel("Ghi chú:"), self.txt_ghichu)

        layout.addLayout(form_layout)

        # Nút bấm
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("💾 Lưu Dữ Liệu")
        self.btn_save.setObjectName("BtnSave")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_cancel = QPushButton("❌ Hủy")
        self.btn_cancel.setObjectName("BtnCancel")
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

    def fill_data(self):
        self.txt_ten.setText(str(self.data.get('TenHanBaoQuan', '')))
        self.txt_ghichu.setPlainText(str(self.data.get('GhiChu', '') or ''))

    def get_data(self):
        res = {
            "TenHanBaoQuan": self.txt_ten.text(),
            "GhiChu": self.txt_ghichu.toPlainText()
        }
        if self.data:
            res["Id"] = self.data["Id"]
        return res