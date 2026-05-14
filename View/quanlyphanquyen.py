from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import pyodbc


class QuanLyPhanQuyen(QWidget):

    def __init__(self):

        super().__init__()

        # =====================================================
        # SQL
        # =====================================================

        self.conn = pyodbc.connect(

            "DRIVER={ODBC Driver 17 for SQL Server};"

            "SERVER=localhost\\SQLEXPRESS;"

            "DATABASE=congtyadc;"

            "Trusted_Connection=yes;"
        )

        # =====================================================
        # LAYOUT
        # =====================================================

        layout = QVBoxLayout(self)

        # =====================================================
        # STYLE
        # =====================================================

        self.setStyleSheet("""

        QWidget{
            background:#f5f6fa;
            font-family:Segoe UI;
        }

        QLabel{
            color:#2d3436;
        }

        QFrame{
            background:white;
            border-radius:15px;
        }

        QPushButton{
            background:#6c5ce7;
            color:white;
            border:none;
            padding:10px 18px;
            border-radius:10px;
            font-size:14px;
            font-weight:bold;
        }

        QPushButton:hover{
            background:#5848c2;
        }

        QLineEdit{
            padding:10px;
            border:1px solid #dcdde1;
            border-radius:10px;
            background:white;
        }

        QTableWidget{
            background:white;
            border:none;
            border-radius:10px;
            gridline-color:#ecf0f1;
            font-size:13px;
        }

        QHeaderView::section{
            background:#6c5ce7;
            color:white;
            padding:12px;
            border:none;
            font-weight:bold;
        }

        """)

        # =====================================================
        # TITLE
        # =====================================================

        title = QLabel("🔐 QUẢN LÝ PHÂN QUYỀN HỆ THỐNG")

        title.setStyleSheet("""

            font-size:28px;
            font-weight:bold;
            color:#6c5ce7;
            padding:15px;

        """)

        layout.addWidget(title)

        # =====================================================
        # TOOLBAR
        # =====================================================

        toolbar = QHBoxLayout()

        self.txt_search = QLineEdit()

        self.txt_search.setPlaceholderText(
            "Nhập tên đăng nhập..."
        )

        btn_reload = QPushButton("🔄 Làm mới")

        btn_reload.clicked.connect(self.load_data)

        toolbar.addWidget(self.txt_search)

        toolbar.addWidget(btn_reload)

        layout.addLayout(toolbar)

        # =====================================================
        # TABLE
        # =====================================================

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([

            "Tên đăng nhập",

            "Mật khẩu",

            "Vai trò",

            "Họ tên"

        ])

        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.verticalHeader().setVisible(False)

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)

        # =====================================================
        # INFO PANEL
        # =====================================================

        info = QFrame()

        info_layout = QVBoxLayout(info)

        lbl = QLabel("""


""")

        lbl.setStyleSheet("""

            font-size:16px;
            line-height:30px;
            padding:15px;

        """)

        info_layout.addWidget(lbl)

        layout.addWidget(info)

        # =====================================================
        # LOAD DATA
        # =====================================================

        self.load_data()

    # =========================================================
    # LOAD DATA
    # =========================================================

    def load_data(self):

        cursor = self.conn.cursor()

        sql = """

        SELECT

            Username,

            Password,

            CASE

                WHEN IsAdmin = 1 THEN N'Admin'

                WHEN NhomQuyenId = 1 THEN N'Giám đốc'

                WHEN NhomQuyenId = 2 THEN N'Trưởng phòng'

                ELSE N'Nhân viên'

            END AS VaiTro,

            HoTen

        FROM CanBo

        WHERE Username IS NOT NULL

        """

        keyword = self.txt_search.text().strip()

        if keyword != "":

            sql += " AND Username LIKE ? "

            cursor.execute(sql, ('%' + keyword + '%',))

        else:

            cursor.execute(sql)

        data = cursor.fetchall()

        self.table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):

            for col_idx, value in enumerate(row_data):

                item = QTableWidgetItem(str(value))

                self.table.setItem(row_idx, col_idx, item)