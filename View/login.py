from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import pyodbc


class LoginWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Đăng nhập hệ thống")

        self.resize(450,300)

        self.conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=.\\SQLEXPRESS;"
            "DATABASE=congtyadc;"
            "Trusted_Connection=yes;"
        )

        self.setStyleSheet("""

            QWidget{
                background:#f5f6fa;
                font-family:Segoe UI;
            }

            QLineEdit{
                padding:12px;
                border-radius:10px;
                border:1px solid #dcdde1;
                font-size:14px;
                background:white;
            }

            QPushButton{
                background:#6c5ce7;
                color:white;
                border:none;
                border-radius:10px;
                padding:12px;
                font-size:15px;
                font-weight:bold;
            }

        """)

        layout = QVBoxLayout(self)

        title = QLabel("ĐĂNG NHẬP HỆ THỐNG")

        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:#6c5ce7;
            padding:20px;
        """)

        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)

        self.txt_user = QLineEdit()

        self.txt_user.setPlaceholderText(
            "Tên đăng nhập"
        )

        self.txt_pass = QLineEdit()

        self.txt_pass.setPlaceholderText(
            "Mật khẩu"
        )

        self.txt_pass.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        layout.addWidget(self.txt_user)

        layout.addWidget(self.txt_pass)

        btn = QPushButton("Đăng nhập")

        btn.clicked.connect(self.login)

        layout.addWidget(btn)

    def login(self):

        user = self.txt_user.text()

        password = self.txt_pass.text()

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                HoTen,
                VaiTro
            FROM TaiKhoan
            WHERE TenDangNhap=?
            AND MatKhau=?
        """,(user,password))

        data = cursor.fetchone()

        if data:

            self.hoten = data[0]

            self.vaitro = data[1]

            QMessageBox.information(
                self,
                "OK",
                f"Xin chào {self.hoten}\nVai trò: {self.vaitro}"
            )

            self.close()

        else:

            QMessageBox.critical(
                self,
                "Lỗi",
                "Sai tài khoản hoặc mật khẩu"
            )