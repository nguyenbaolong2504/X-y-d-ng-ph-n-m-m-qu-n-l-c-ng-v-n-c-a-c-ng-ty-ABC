from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import pyodbc


class LoginWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Đăng nhập hệ thống")

        self.resize(450, 300)

        # =====================================================
        # CONNECT SQL
        # =====================================================

        self.conn = pyodbc.connect(

            "DRIVER={ODBC Driver 17 for SQL Server};"

            "SERVER=localhost\\SQLEXPRESS;"

            "DATABASE=congtyadc;"

            "Trusted_Connection=yes;"
        )

        # =====================================================
        # STYLE
        # =====================================================

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

        # =====================================================
        # LAYOUT
        # =====================================================

        layout = QVBoxLayout(self)

        layout.setContentsMargins(40,40,40,40)

        layout.setSpacing(15)

        # =====================================================
        # TITLE
        # =====================================================

        title = QLabel("ĐĂNG NHẬP HỆ THỐNG")

        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:#6c5ce7;
            padding:20px;
        """)

        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)

        # =====================================================
        # USERNAME
        # =====================================================

        self.txt_user = QLineEdit()

        self.txt_user.setPlaceholderText(
            "Tên đăng nhập"
        )

        layout.addWidget(self.txt_user)

        # =====================================================
        # PASSWORD
        # =====================================================

        self.txt_pass = QLineEdit()

        self.txt_pass.setPlaceholderText(
            "Mật khẩu"
        )

        self.txt_pass.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        layout.addWidget(self.txt_pass)

        # =====================================================
        # BUTTON LOGIN
        # =====================================================

        btn = QPushButton("Đăng nhập")

        btn.clicked.connect(self.login)

        layout.addWidget(btn)

    # =========================================================
    # LOGIN
    # =========================================================

    def login(self):

        user = self.txt_user.text().strip()

        password = self.txt_pass.text().strip()

        # =====================================================
        # VALIDATE
        # =====================================================

        if user == "" or password == "":

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng nhập đầy đủ tài khoản và mật khẩu"
            )

            return

        # =====================================================
        # QUERY
        # =====================================================

        cursor = self.conn.cursor()

        sql = """

        SELECT *

        FROM CanBo

        WHERE Username = ?

        AND Password = ?

        """

        cursor.execute(sql, (user, password))

        row = cursor.fetchone()

        # =====================================================
        # LOGIN SUCCESS
        # =====================================================

        if row:

            self.user_id = row.Id

            self.hoten = row.HoTen

            # =================================================
            # ADMIN
            # =================================================

            if row.IsAdmin == True:

                self.vaitro = "Admin"

            else:

                # =============================================
                # ROLE
                # =============================================

                if row.NhomQuyenId == 1:

                    self.vaitro = "GiamDoc"

                elif row.NhomQuyenId == 2:

                    self.vaitro = "TruongPhong"

                else:

                    self.vaitro = "NhanVien"

            QMessageBox.information(

                self,

                "Đăng nhập thành công",

                f"Xin chào {self.hoten}\n"

                f"Vai trò: {self.vaitro}"
            )

            self.close()

        # =====================================================
        # LOGIN FAIL
        # =====================================================

        else:

            QMessageBox.critical(

                self,

                "Lỗi",

                "Sai tài khoản hoặc mật khẩu"
            )