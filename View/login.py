from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import pyodbc

from Utils.user_session import UserSession

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.session = None

        self.setWindowTitle("Đăng nhập hệ thống")
        self.resize(450, 300)

        self.conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
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
            QPushButton:hover{
                background:#5a4fcf;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40,40,40,40)
        layout.setSpacing(15)

        title = QLabel("ĐĂNG NHẬP HỆ THỐNG")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:#6c5ce7;
            padding:20px;
        """)
        layout.addWidget(title)

        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("Tên đăng nhập")
        layout.addWidget(self.txt_user)

        self.txt_pass = QLineEdit()
        self.txt_pass.setPlaceholderText("Mật khẩu")
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.txt_pass)

        btn = QPushButton("Đăng nhập")
        btn.clicked.connect(self.login)
        layout.addWidget(btn)

    def login(self):

        username = self.txt_user.text().strip()
        password = self.txt_pass.text().strip()

        if not username or not password:
            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng nhập đầy đủ tài khoản và mật khẩu"
            )
            return

        cursor = self.conn.cursor()

        sql = """
            SELECT
                cb.Id,
                cb.HoTen,
                cb.IsAdmin,
                cb.DonViId,
                dv.TenDonVi,
                cb.NhomQuyenId
            FROM CanBo cb
            LEFT JOIN DonViTrucThuoc dv
                ON cb.DonViId = dv.Id
            WHERE cb.Username = ?
            AND cb.Password = ?
        """

        cursor.execute(sql, (username, password))

        row = cursor.fetchone()

        if not row:

            QMessageBox.critical(
                self,
                "Lỗi",
                "Sai tài khoản hoặc mật khẩu"
            )
            return

        user_id = row.Id
        ho_ten = row.HoTen
        is_admin = bool(row.IsAdmin)

        don_vi_id = row.DonViId
        ten_don_vi = row.TenDonVi if row.TenDonVi else ""

        nhom_quyen_id = row.NhomQuyenId

        if is_admin:
            role = "Admin"

        elif nhom_quyen_id == 1:
            role = "GiamDoc"

        elif nhom_quyen_id == 2:
            role = "TruongPhong"

        else:
            role = "NhanVien"

        session = UserSession()

        session.set_user(
            user_id,
            username,
            ho_ten,
            don_vi_id,
            is_admin,
            role,
            ten_don_vi
        )

        self.session = session

        QMessageBox.information(
            self,
            "Đăng nhập thành công",
            f"Xin chào {ho_ten}\nVai trò: {role}"
        )

        self.close()