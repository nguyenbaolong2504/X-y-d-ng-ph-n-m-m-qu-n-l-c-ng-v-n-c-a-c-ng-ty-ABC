from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QGridLayout, QLineEdit, 
                             QRadioButton, QPushButton, QHBoxLayout, QLabel)
from PyQt6.QtCore import Qt

class DonViDialog(QDialog):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.setWindowTitle("Cập nhật Đơn vị / Bộ phận")
        self.setFixedWidth(650) 
        self.setup_ui()
        self.apply_styles()
        if data:
            self.fill_data()

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog { background-color: #ffffff; font-family: 'Segoe UI', Arial; }
            QLabel { color: #2c3e50; font-size: 13px; font-weight: bold; margin-bottom: 2px;}
            QLineEdit { 
                min-height: 32px; border: 1px solid #bdc3c7; border-radius: 4px; 
                padding: 0px 10px; font-size: 14px; background-color: #ffffff; color: #2c3e50;
            }
            QLineEdit:focus { border: 1px solid #3498db; }
            QRadioButton { font-size: 14px; color: #2c3e50; }
            
            QPushButton#BtnSave { background-color: #0097e6; color: white; font-weight: bold; border-radius: 4px; padding: 8px 15px; border: none; }
            QPushButton#BtnSave:hover { background-color: #00a8ff; }
            QPushButton#BtnCancel { background-color: #e84118; color: white; font-weight: bold; border-radius: 4px; padding: 8px 15px; border: none; }
            QPushButton#BtnCancel:hover { background-color: #c23616; }
        """)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        grid = QGridLayout()
        grid.setHorizontalSpacing(30) 
        grid.setVerticalSpacing(15)   

        # Dòng 1: Tên đơn vị | Địa chỉ
        grid.addWidget(QLabel("Tên đơn vị"), 0, 0)
        self.txt_ten = QLineEdit()
        grid.addWidget(self.txt_ten, 1, 0)

        grid.addWidget(QLabel("Địa chỉ"), 0, 1)
        self.txt_diachi = QLineEdit()
        grid.addWidget(self.txt_diachi, 1, 1)

        # Dòng 2: Điện thoại | Email
        grid.addWidget(QLabel("Điện thoại"), 2, 0)
        self.txt_sdt = QLineEdit()
        grid.addWidget(self.txt_sdt, 3, 0)

        grid.addWidget(QLabel("Email"), 2, 1)
        self.txt_email = QLineEdit()
        grid.addWidget(self.txt_email, 3, 1)

        # Dòng 3: Website | Trạng thái
        grid.addWidget(QLabel("Website"), 4, 0)
        self.txt_web = QLineEdit()
        self.txt_web.setPlaceholderText("VD: https://...")
        grid.addWidget(self.txt_web, 5, 0)

        grid.addWidget(QLabel("Trạng thái"), 4, 1)
        radio_layout = QHBoxLayout()
        radio_layout.setContentsMargins(0, 0, 0, 0)
        self.radio_hienthi = QRadioButton("Hiển thị")
        self.radio_an = QRadioButton("Không hiển thị")
        self.radio_hienthi.setChecked(True)
        radio_layout.addWidget(self.radio_hienthi)
        radio_layout.addWidget(self.radio_an)
        radio_layout.addStretch()
        grid.addLayout(radio_layout, 5, 1)

        layout.addLayout(grid)

        # Nút bấm
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("💾 Lưu & Đóng")
        self.btn_save.setObjectName("BtnSave")
        self.btn_cancel = QPushButton("✖ Đóng")
        self.btn_cancel.setObjectName("BtnCancel")
        
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

    def fill_data(self):
        self.txt_ten.setText(str(self.data.get('TenDonVi', '')))
        self.txt_diachi.setText(str(self.data.get('DiaChi', '') or ''))
        self.txt_sdt.setText(str(self.data.get('DienThoai', '') or ''))
        self.txt_email.setText(str(self.data.get('Email', '') or ''))
        self.txt_web.setText(str(self.data.get('Website', '') or ''))
        
        tt_val = str(self.data.get('TrangThai', '1'))
        if tt_val == '0' or tt_val.lower() == 'false':
            self.radio_an.setChecked(True)
        else:
            self.radio_hienthi.setChecked(True)

    def get_data(self):
        res = {
            "TenDonVi": self.txt_ten.text().strip(),
            "DiaChi": self.txt_diachi.text().strip(),
            "DienThoai": self.txt_sdt.text().strip(),
            "Email": self.txt_email.text().strip(),
            "Website": self.txt_web.text().strip(),
            "TrangThai": 1 if self.radio_hienthi.isChecked() else 0
        }
        if self.data: res["Id"] = self.data["Id"]
        return res