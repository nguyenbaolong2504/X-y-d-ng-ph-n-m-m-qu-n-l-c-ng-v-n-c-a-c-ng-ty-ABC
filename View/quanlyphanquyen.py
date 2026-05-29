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
            "SERVER=DESKTOP-MRSI227\\SQLEXPRESS;"
            "DATABASE=congtyabc;"
            "Trusted_Connection=yes;"
        )

        cursor = self.conn.cursor()

        cursor.execute("SELECT @@SERVERNAME")
        print("SERVER =", cursor.fetchone()[0])

        cursor.execute("SELECT DB_NAME()")
        print("DATABASE =", cursor.fetchone()[0])

        cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_NAME='QuyenMenu'
        """)

        print("QUYENMENU =", cursor.fetchall())

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
        # PHÂN QUYỀN MENU
        # =====================================================

        permission_frame = QFrame()

        permission_layout = QVBoxLayout(permission_frame)

        title_permission = QLabel("📋 Menu được phép sử dụng")

        title_permission.setStyleSheet("""
        font-size:18px;
        font-weight:bold;
        padding:10px;
        """)

        permission_layout.addWidget(title_permission)

        self.menu_list = QListWidget()

        self.all_menus = [

            "Tổng quan hệ thống",
            "Văn bản đến",
            "Văn bản đi",
            "Văn bản nội bộ",
            "Văn bản nội bộ của tôi",
            "Danh sách cán bộ",
            "Danh mục chức vụ",
            "Thời hạn bảo quản",
            "Loại công văn",
            "Đơn vị, bộ phận",
            "Phân quyền sử dụng",
            "Mục lục hồ sơ",
            "Danh mục hồ sơ",
            "Công việc"

        ]

        for menu in self.all_menus:

            item = QListWidgetItem(menu)

            item.setFlags(
                item.flags() |
                Qt.ItemFlag.ItemIsUserCheckable
            )

            item.setCheckState(
                Qt.CheckState.Unchecked
            )

            self.menu_list.addItem(item)

        permission_layout.addWidget(self.menu_list)

        self.btn_save_permission = QPushButton(
            "💾 Lưu phân quyền"
        )
        self.table.itemSelectionChanged.connect( 
            self.load_permission 
        ) 
        self.btn_save_permission.clicked.connect( 
            self.save_permission 
        )

        permission_layout.addWidget(
            self.btn_save_permission
        )

        layout.addWidget(permission_frame)

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

    def load_permission(self):

        try:

            row = self.table.currentRow()

            if row < 0:
                return

            item = self.table.item(row, 0)

            if item is None:
                return

            username = item.text()

            cursor = self.conn.cursor()

            # Lấy CanBoId
            cursor.execute("""
                SELECT Id
                FROM CanBo
                WHERE Username = ?
            """, (username,))

            canbo = cursor.fetchone()

            if not canbo:
                return

            canbo_id = canbo[0]

            # Bỏ tick toàn bộ trước
            for i in range(self.menu_list.count()):
                self.menu_list.item(i).setCheckState(
                    Qt.CheckState.Unchecked
                )

            # Lấy quyền đã cấp
            cursor.execute("""
                SELECT m.TenMenu
                FROM dbo.QuyenMenu q
                INNER JOIN dbo.MenuHeThong m
                    ON q.MenuId = m.Id
                WHERE q.CanBoId = ?
                AND q.DuocXem = 1
            """, (canbo_id,))

            menus = [row[0] for row in cursor.fetchall()]

            for i in range(self.menu_list.count()):

                item = self.menu_list.item(i)

                if item.text() in menus:

                    item.setCheckState(
                        Qt.CheckState.Checked
                    )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Lỗi",
                str(e)
            )


    def save_permission(self):

        try:

            row = self.table.currentRow()

            if row < 0:

                QMessageBox.warning(
                    self,
                    "Thông báo",
                    "Vui lòng chọn người dùng"
                )

                return

            username = self.table.item(row, 0).text()

            cursor = self.conn.cursor()

            # Lấy CanBoId
            cursor.execute("""
                SELECT Id
                FROM CanBo
                WHERE Username = ?
            """, (username,))

            canbo = cursor.fetchone()

            if not canbo:

                QMessageBox.warning(
                    self,
                    "Lỗi",
                    "Không tìm thấy cán bộ"
                )

                return

            canbo_id = canbo[0]

            # Xóa quyền cũ
            cursor.execute("""
                DELETE FROM dbo.QuyenMenu
                WHERE CanBoId = ?
            """, (canbo_id,))

            # Thêm quyền mới
            for i in range(self.menu_list.count()):

                item = self.menu_list.item(i)

                if item.checkState() == Qt.CheckState.Checked:

                    cursor.execute("""
                        SELECT Id
                        FROM dbo.MenuHeThong
                        WHERE TenMenu = ?
                    """, (item.text(),))

                    menu = cursor.fetchone()

                    if menu:

                        menu_id = menu[0]

                        cursor.execute("""
                            INSERT INTO dbo.QuyenMenu
                            (
                                CanBoId,
                                MenuId,
                                DuocXem
                            )
                            VALUES
                            (
                                ?, ?, 1
                            )
                        """,
                        (
                            canbo_id,
                            menu_id
                        ))

            self.conn.commit()

            QMessageBox.information(
                self,
                "Thành công",
                f"Đã lưu phân quyền cho {username}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Lỗi",
                str(e)
            )