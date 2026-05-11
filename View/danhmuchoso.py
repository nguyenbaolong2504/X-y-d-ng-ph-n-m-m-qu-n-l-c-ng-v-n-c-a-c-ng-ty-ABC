from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import pyodbc


class DanhMucHoSo(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        # =====================================================
        # SQL
        # =====================================================

        self.conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=.\\SQLEXPRESS;"
            "DATABASE=congtyadc;"
            "Trusted_Connection=yes;"
        )

        # =====================================================
        # UI
        # =====================================================

        layout = QVBoxLayout(self)

        title = QLabel("MỤC LỤC HỒ SƠ")

        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#27ae60;
            padding:10px;
        """)

        layout.addWidget(title)

        self.txt_ten = QLineEdit()

        self.txt_ten.setPlaceholderText(
            "Tên hồ sơ..."
        )

        layout.addWidget(self.txt_ten)

        # =====================================================
        # BUTTON
        # =====================================================

        btn_layout = QHBoxLayout()

        btn_add = QPushButton("+ Thêm")
        btn_update = QPushButton("✏️ Sửa")
        btn_delete = QPushButton("🗑 Xóa")

        btn_add.clicked.connect(self.them)
        btn_update.clicked.connect(self.sua)
        btn_delete.clicked.connect(self.xoa)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_delete)

        layout.addLayout(btn_layout)

        # =====================================================
        # TABLE
        # =====================================================

        self.table = QTableWidget()

        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Tiêu đề hồ sơ"
        ])

        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.cellClicked.connect(self.chon)

        layout.addWidget(self.table)

        # =====================================================
        # LOAD
        # =====================================================

        self.load_data()

    # =========================================================
    # LOAD
    # =========================================================

    def load_data(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                Id,
                TieuDeHoSo
            FROM DanhMucHoSo
        """)

        data = cursor.fetchall()

        self.table.setRowCount(len(data))

        for r,row in enumerate(data):

            for c,val in enumerate(row):

                item = QTableWidgetItem(str(val))

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.table.setItem(r,c,item)

    # =========================================================
    # THÊM
    # =========================================================

    def them(self):

        try:

            cursor = self.conn.cursor()

            cursor.execute("""
                INSERT INTO DanhMucHoSo
                (
                    TieuDeHoSo,
                    SoKyHieu,
                    Nam,
                    HanBaoQuanId,
                    NguoiLapId,
                    HanNopLuu,
                    TrangThaiDong
                )
                VALUES (?,?,?,?,?,?,?)
            """,(
                self.txt_ten.text(),
                "HS001",
                2026,
                1,
                1,
                "2026-12-31",
                0
            ))

            self.conn.commit()

            self.load_data()

            QMessageBox.information(
                self,
                "Thông báo",
                "Thêm thành công"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Lỗi",
                str(e)
            )

    # =========================================================
    # CHỌN
    # =========================================================

    def chon(self,row,column):

        self.id_selected = self.table.item(row,0).text()

        self.txt_ten.setText(
            self.table.item(row,1).text()
        )

    # =========================================================
    # SỬA
    # =========================================================

    def sua(self):

        try:

            cursor = self.conn.cursor()

            cursor.execute("""
                UPDATE DanhMucHoSo
                SET
                    TieuDeHoSo=?
                WHERE Id=?
            """,(
                self.txt_ten.text(),
                self.id_selected
            ))

            self.conn.commit()

            self.load_data()

            QMessageBox.information(
                self,
                "Thông báo",
                "Sửa thành công"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Lỗi",
                str(e)
            )

    # =========================================================
    # XÓA
    # =========================================================

    def xoa(self):

        try:

            cursor = self.conn.cursor()

            cursor.execute("""
                DELETE FROM DanhMucHoSo
                WHERE Id=?
            """,(self.id_selected))

            self.conn.commit()

            self.load_data()

            QMessageBox.information(
                self,
                "Thông báo",
                "Xóa thành công"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Lỗi",
                str(e)
            )