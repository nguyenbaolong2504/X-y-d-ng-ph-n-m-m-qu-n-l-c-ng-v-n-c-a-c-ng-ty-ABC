from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap
import pyodbc
import hashlib
import sys

from Utils.user_session import UserSession

class LoginWindow(QWidget):
    login_successful = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        self.session = None
        self.setWindowTitle("Đăng nhập - Hệ thống Quản lý Công văn ABC")
        self.setFixedSize(1100, 650)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Database connection
        self.conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=congtyabc;"
            "Trusted_Connection=yes;"
        )

        self.setup_ui()

    def setup_ui(self):
        # Main container
        container = QFrame()
        container.setObjectName("container")
        container.setStyleSheet("""
            QFrame#container {
                background-color: white;
                border-radius: 25px;
            }
        """)
        
        # Main layout for container
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Close button row (top right)
        close_widget = QWidget()
        close_widget.setFixedHeight(55)
        close_layout = QHBoxLayout(close_widget)
        close_layout.setContentsMargins(20, 15, 20, 0)
        close_layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(38, 38)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #7f8c8d;
                border: none;
                border-radius: 19px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e74c3c;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.close_app)
        close_layout.addWidget(close_btn)

        container_layout.addWidget(close_widget)

        # Two-column layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ========== LEFT PANEL (WELCOME) ==========
        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-top-left-radius: 25px;
                border-bottom-left-radius: 25px;
            }
        """)
        left_panel.setFixedWidth(480)

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(50, 100, 50, 100)
        left_layout.setSpacing(25)

        # Welcome text
        welcome_title = QLabel("WELCOME!")
        welcome_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_title.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            color: white;
            letter-spacing: 3px;
        """)
        left_layout.addWidget(welcome_title)

        welcome_sub = QLabel("Login to continue")
        welcome_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_sub.setStyleSheet("""
            font-size: 18px;
            color: rgba(255,255,255,0.85);
        """)
        left_layout.addWidget(welcome_sub)

        left_layout.addStretch()

        # Decorative elements
        decor_text = QLabel("📑")
        decor_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        decor_text.setStyleSheet("""
            font-size: 90px;
            opacity: 0.25;
        """)
        left_layout.addWidget(decor_text)

        left_layout.addStretch()

        # ========== RIGHT PANEL (LOGIN FORM) ==========
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-top-right-radius: 25px;
                border-bottom-right-radius: 25px;
            }
        """)

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(60, 100, 60, 100)
        right_layout.setSpacing(30)

        # Login title
        login_title = QLabel("Login")
        login_title.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #2d3436;
        """)
        right_layout.addWidget(login_title)

        login_sub = QLabel("Please login to your account")
        login_sub.setStyleSheet("""
            font-size: 15px;
            color: #7f8c8d;
            margin-bottom: 25px;
        """)
        right_layout.addWidget(login_sub)

        # Username field
        user_label = QLabel("")
        user_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2d3436;
            margin-bottom: 5px;
        """)
        right_layout.addWidget(user_label)

        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("Enter your username...")
        self.txt_user.setMinimumHeight(52)
        self.txt_user.setStyleSheet("""
            QLineEdit {
                border: 1px solid #dfe6e9;
                border-radius: 12px;
                padding: 14px 18px;
                font-size: 15px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border-color: #6c5ce7;
                background-color: white;
            }
        """)
        right_layout.addWidget(self.txt_user)

        # Password field
        pass_label = QLabel("")
        pass_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #2d3436;
            margin-bottom: 5px;
            margin-top: 10px;
        """)
        right_layout.addWidget(pass_label)

        self.txt_pass = QLineEdit()
        self.txt_pass.setPlaceholderText("Enter your password...")
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_pass.setMinimumHeight(52)
        self.txt_pass.setStyleSheet("""
            QLineEdit {
                border: 1px solid #dfe6e9;
                border-radius: 12px;
                padding: 14px 18px;
                font-size: 15px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border-color: #6c5ce7;
                background-color: white;
            }
        """)
        right_layout.addWidget(self.txt_pass)

        # Forgot password
        forgot_btn = QPushButton(".")
        forgot_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        forgot_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #6c5ce7;
                border: none;
                text-align: right;
                font-size: 13px;
                padding: 8px 5px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        forgot_btn.clicked.connect(self.forgot_password)
        
        forgot_layout = QHBoxLayout()
        forgot_layout.addStretch()
        forgot_layout.addWidget(forgot_btn)
        right_layout.addLayout(forgot_layout)

        # Login button
        btn_login = QPushButton("Login")
        btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_login.setMinimumHeight(55)
        btn_login.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6c5ce7, stop:1 #a363d9);
                color: white;
                border: none;
                border-radius: 28px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 15px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
        """)
        btn_login.clicked.connect(self.login)
        right_layout.addWidget(btn_login)

        right_layout.addStretch()

        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

        container_layout.addLayout(main_layout)

        # Set container as main widget
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(12, 12, 12, 12)
        outer_layout.addWidget(container)

        # Enter key shortcut
        self.txt_user.returnPressed.connect(btn_login.click)
        self.txt_pass.returnPressed.connect(btn_login.click)

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def login(self):
        username = self.txt_user.text().strip()
        password = self.txt_pass.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu")
            return

        cursor = self.conn.cursor()
        hashed_password = self.hash_password(password)

        sql = """
            SELECT
                cb.Id,
                cb.HoTen,
                cb.IsAdmin,
                cb.DonViId,
                dv.TenDonVi,
                cb.NhomQuyenId
            FROM CanBo cb
            LEFT JOIN DonViTrucThuoc dv ON cb.DonViId = dv.Id
            WHERE cb.Username = ? AND cb.Password = ?
        """

        cursor.execute(sql, (username, hashed_password))
        row = cursor.fetchone()

        if not row:
            cursor.execute(sql, (username, password))
            row = cursor.fetchone()
            if row:
                cursor.execute("UPDATE CanBo SET Password = ? WHERE Id = ?", (hashed_password, row[0]))
                self.conn.commit()

        if not row:
            QMessageBox.critical(self, "Lỗi đăng nhập", "Sai tên đăng nhập hoặc mật khẩu!")
            return

        user_id = row[0]
        ho_ten = row[1]
        is_admin = bool(row[2])
        don_vi_id = row[3]
        ten_don_vi = row[4] if row[4] else ""
        nhom_quyen_id = row[5]

        if is_admin:
            role = "Admin"
        elif nhom_quyen_id == 1:
            role = "Giám đốc"
        elif nhom_quyen_id == 2:
            role = "Trưởng phòng"
        else:
            role = "Nhân viên"

        self.session = UserSession()
        self.session.set_user(user_id, username, ho_ten, don_vi_id, is_admin, role, ten_don_vi)

        QMessageBox.information(self, "Đăng nhập thành công", f"Xin chào {ho_ten}\nVai trò: {role}")
        self.close()

    def get_session(self):
        return self.session

    def forgot_password(self):
        QMessageBox.information(self, "Quên mật khẩu", "Vui lòng liên hệ quản trị viên để được hỗ trợ!")

    def close_app(self):
        reply = QMessageBox.question(self, "Xác nhận thoát", "Bạn có chắc muốn thoát chương trình?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            sys.exit(0)