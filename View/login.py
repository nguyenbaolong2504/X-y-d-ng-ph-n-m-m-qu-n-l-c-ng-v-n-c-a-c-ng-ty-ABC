from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import pyodbc
<<<<<<< HEAD
from Utils.user_session import UserSession   # <-- THÊM DÒNG NÀY
=======
from Utils.user_session import UserSession

>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng nhập hệ thống")
<<<<<<< HEAD
=======
        self.resize(450, 300)


>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
        self.resize(450, 300)

        self.conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=congtyadc;"
<<<<<<< HEAD
=======
        )

        self.conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=congtyadc;"
>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
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
<<<<<<< HEAD
=======
            QPushButton:hover{
                background:#5a4fcf;
            }
>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
        """)

        layout = QVBoxLayout(self)
<<<<<<< HEAD
=======
        layout.setContentsMargins(40,40,40,40)
        layout.setSpacing(15)

>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
        layout.setContentsMargins(40,40,40,40)
        layout.setSpacing(15)

        title = QLabel("ĐĂNG NHẬP HỆ THỐNG")
        title.setStyleSheet("font-size:28px; font-weight:bold; color:#6c5ce7; padding:20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("Tên đăng nhập")
        layout.addWidget(self.txt_user)

        self.txt_pass = QLineEdit()
<<<<<<< HEAD
=======

        self.txt_pass.setPlaceholderText(
            "Mật khẩu"
        )

        self.txt_pass.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.txt_user.setPlaceholderText("Tên đăng nhập")
        layout.addWidget(self.txt_user)

        self.txt_pass = QLineEdit()
>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
        self.txt_pass.setPlaceholderText("Mật khẩu")
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.txt_pass)

        btn = QPushButton("Đăng nhập")
        btn.clicked.connect(self.login)
        layout.addWidget(btn)

    def login(self):
<<<<<<< HEAD
=======
        user = self.txt_user.text().strip()
        password = self.txt_pass.text().strip()

>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
        user = self.txt_user.text().strip()
        password = self.txt_pass.text().strip()

        if user == "" or password == "":
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ tài khoản và mật khẩu")
            return

<<<<<<< HEAD
        cursor = self.conn.cursor()
=======
        # =====================================================
        # QUERY
        # =====================================================
        if user == "" or password == "":
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ tài khoản và mật khẩu")
            return

        cursor = self.conn.cursor()
        sql = """
            SELECT cb.Id, cb.HoTen, cb.IsAdmin, cb.DonViId, dv.TenDonVi, cb.NhomQuyenId
            FROM CanBo cb
            LEFT JOIN DonViTrucThuoc dv ON cb.DonViId = dv.Id
            WHERE Username = ? AND Password = ?
        """
        cursor.execute(sql, (user, password))
        row = cursor.fetchone()

>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
        sql = """
            SELECT cb.Id, cb.HoTen, cb.IsAdmin, cb.DonViId, dv.TenDonVi, cb.NhomQuyenId
            FROM CanBo cb
            LEFT JOIN DonViTrucThuoc dv ON cb.DonViId = dv.Id
            WHERE Username = ? AND Password = ?
        """
        cursor.execute(sql, (user, password))
        row = cursor.fetchone()

        if row:
            self.user_id = row[0]
            self.hoten = row[1]
            is_admin = row[2]
            don_vi_id = row[3]
            ten_don_vi = row[4] if row[4] else ""
            nhom_quyen_id = row[5] if len(row) > 5 else None

            if is_admin:
                self.vaitro = "Admin"
            else:
                if nhom_quyen_id == 1:
                    self.vaitro = "GiamDoc"
                elif nhom_quyen_id == 2:
                    self.vaitro = "TruongPhong"
                else:
                    self.vaitro = "NhanVien"

<<<<<<< HEAD
            session = UserSession()
            session.set_user(self.user_id, user, self.hoten, don_vi_id, is_admin, self.vaitro, ten_don_vi)

            QMessageBox.information(self, "Đăng nhập thành công", f"Xin chào {self.hoten}\nVai trò: {self.vaitro}")
            self.close()
        else:
            QMessageBox.critical(self, "Lỗi", "Sai tài khoản hoặc mật khẩu")
=======
            QMessageBox.information(

                self,

                "Đăng nhập thành công",

                f"Xin chào {self.hoten}\n"

                f"Vai trò: {self.vaitro}"
            )
        if row:
            self.user_id = row[0]
            self.hoten = row[1]
            is_admin = row[2]
            don_vi_id = row[3]
            ten_don_vi = row[4] if row[4] else ""
            nhom_quyen_id = row[5] if len(row) > 5 else None

            if is_admin:
                self.vaitro = "Admin"
            else:
                if nhom_quyen_id == 1:
                    self.vaitro = "GiamDoc"
                elif nhom_quyen_id == 2:
                    self.vaitro = "TruongPhong"
                else:
                    self.vaitro = "NhanVien"

            session = UserSession()
            # SỬA DÒNG NÀY: thêm self.hoten vào vị trí thứ 3
            session.set_user(self.user_id, user, self.hoten, don_vi_id, is_admin, self.vaitro, ten_don_vi)

            QMessageBox.information(self, "Đăng nhập thành công", f"Xin chào {self.hoten}\nVai trò: {self.vaitro}")
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

>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
