from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pyodbc


# =========================================================
# FORM POPUP - CỬA SỔ THÊM/SỬA HỒ SƠ
# =========================================================

class FormHoSo(QDialog):

    def __init__(self, parent=None, ho_so_data=None):

        super().__init__(parent)

        self.ho_so_data = ho_so_data  # None = Thêm mới, có data = Sửa

        if ho_so_data:
            self.setWindowTitle("✏️ CẬP NHẬT HỒ SƠ")
        else:
            self.setWindowTitle("➕ THÊM HỒ SƠ MỚI")

        self.resize(600, 450)

        self.setStyleSheet("""

        QDialog{
            background:white;
            font-family:Segoe UI;
        }

        QLabel{
            font-size:14px;
            font-weight:600;
            color:#2d3436;
        }

        QLineEdit,
        QTextEdit,
        QSpinBox{

            border:1px solid #dfe6e9;
            border-radius:10px;
            padding:10px;
            font-size:14px;
            background:#fdfdfd;
        }

        QLineEdit:focus,
        QTextEdit:focus{

            border:2px solid #6c5ce7;
        }

        QPushButton{

            background:#6c5ce7;
            color:white;
            border:none;
            border-radius:10px;
            padding:12px;
            font-size:14px;
            font-weight:bold;
            min-width:120px;
        }

        QPushButton:hover{

            background:#5848c2;
        }

        """)

        main = QVBoxLayout(self)

        # =================================================
        # TITLE
        # =================================================

        if ho_so_data:
            title = QLabel("✏️ CẬP NHẬT THÔNG TIN HỒ SƠ")
        else:
            title = QLabel("➕ THÊM HỒ SƠ MỚI")

        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#6c5ce7;
            padding-bottom:15px;
        """)

        main.addWidget(title)

        # =================================================
        # FORM
        # =================================================

        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame{
                background:#f8f9fa;
                border-radius:15px;
                padding:20px;
            }
        """)

        form = QFormLayout(form_frame)
        form.setSpacing(20)

        self.txt_ten = QLineEdit()
        self.txt_ten.setPlaceholderText("Nhập tên hồ sơ...")

        self.txt_so = QLineEdit()
        self.txt_so.setPlaceholderText("Nhập số ký hiệu...")

        self.spin_nam = QSpinBox()
        self.spin_nam.setMaximum(9999)
        self.spin_nam.setValue(2026)

        self.txt_ghichu = QTextEdit()
        self.txt_ghichu.setMinimumHeight(100)
        self.txt_ghichu.setPlaceholderText("Nhập ghi chú...")

        form.addRow("Tên hồ sơ:", self.txt_ten)
        form.addRow("Số ký hiệu:", self.txt_so)
        form.addRow("Năm:", self.spin_nam)
        form.addRow("Ghi chú:", self.txt_ghichu)

        main.addWidget(form_frame)

        # Nếu là sửa, điền dữ liệu cũ vào form
        if ho_so_data:
            self.txt_ten.setText(ho_so_data.get("ten", ""))
            self.txt_so.setText(ho_so_data.get("so", ""))
            self.spin_nam.setValue(ho_so_data.get("nam", 2026))
            self.txt_ghichu.setText(ho_so_data.get("ghichu", ""))

        # =================================================
        # BUTTON
        # =================================================

        bottom = QHBoxLayout()
        bottom.addStretch()

        btn_luu = QPushButton("💾 Lưu")
        btn_huy = QPushButton("❌ Hủy")

        btn_huy.setStyleSheet("""
            QPushButton{
                background:#d63031;
            }
            QPushButton:hover{
                background:#b71c1c;
            }
        """)

        btn_luu.clicked.connect(self.accept)
        btn_huy.clicked.connect(self.reject)

        bottom.addWidget(btn_luu)
        bottom.addWidget(btn_huy)

        main.addLayout(bottom)

    def get_data(self):
        """Trả về dữ liệu từ form"""
        return {
            "ten": self.txt_ten.text().strip(),
            "so": self.txt_so.text().strip(),
            "nam": self.spin_nam.value(),
            "ghichu": self.txt_ghichu.toPlainText().strip()
        }


# =========================================================
# WIDGET CHÍNH - QUẢN LÝ HỒ SƠ
# =========================================================

class QuanLyHoSo(QWidget):

    def __init__(self):

        super().__init__()

        # =================================================
        # SQL CONNECTION
        # =================================================

        self.conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=congtyabc;"
            "Trusted_Connection=yes;"
        )

        # =================================================
        # STYLE
        # =================================================

        self.setStyleSheet("""

        QWidget{
            background:#f5f6fa;
            font-family:Segoe UI;
        }

        QLabel{
            font-size:14px;
            font-weight:600;
            color:#2d3436;
        }

        QLineEdit{

            border:1px solid #dfe6e9;
            border-radius:10px;
            padding:12px;
            font-size:14px;
            background:white;
        }

        QLineEdit:focus{

            border:2px solid #6c5ce7;
        }

        QPushButton{

            background:#6c5ce7;
            color:white;
            border:none;
            border-radius:10px;
            padding:12px;
            font-size:14px;
            font-weight:bold;
            min-width:120px;
        }

        QPushButton:hover{

            background:#5848c2;
        }

        QTableWidget{

            background:white;
            border:1px solid #dfe6e9;
            border-radius:15px;
            font-size:14px;
            gridline-color:#ecf0f1;
        }

        QTableWidget::item{

            padding:12px;
        }

        QTableWidget::item:selected{

            background:#dfe6e9;
            color:black;
        }

        QHeaderView::section{

            background:white;
            color:#2d3436;
            border:1px solid #ecf0f1;
            padding:14px;
            font-size:14px;
            font-weight:bold;
        }

        """)

        # =================================================
        # LAYOUT CHÍNH
        # =================================================

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # =================================================
        # TITLE
        # =================================================

        title = QLabel("🗂️ QUẢN LÝ HỒ SƠ")
        title.setStyleSheet("""
            font-size:32px;
            font-weight:bold;
            color:#6c5ce7;
            padding:10px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # =================================================
        # TOOLBAR (TÌM KIẾM + NÚT CHỨC NĂNG)
        # =================================================

        toolbar_frame = QFrame()
        toolbar_frame.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:15px;
                padding:15px;
                border:1px solid #dfe6e9;
            }
        """)

        toolbar_layout = QVBoxLayout(toolbar_frame)
        toolbar_layout.setSpacing(15)

        # Hàng 1: Tìm kiếm
        search_layout = QHBoxLayout()

        lbl_search = QLabel("🔍")
        lbl_search.setStyleSheet("font-size:20px;")

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Nhập tên hồ sơ cần tìm...")
        self.txt_search.setMinimumHeight(45)

        self.btn_search = QPushButton("🔍 Tìm kiếm")
        self.btn_search.setMinimumHeight(45)

        self.btn_reload = QPushButton("🔄 Làm mới")
        self.btn_reload.setMinimumHeight(45)

        search_layout.addWidget(lbl_search)
        search_layout.addWidget(self.txt_search)
        search_layout.addWidget(self.btn_search)
        search_layout.addWidget(self.btn_reload)

        toolbar_layout.addLayout(search_layout)

        # Hàng 2: Các nút chức năng
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_them = QPushButton("➕ Thêm hồ sơ")
        self.btn_them.setStyleSheet("""
            QPushButton{
                background:#00b894;
                color:white;
                border:none;
                border-radius:10px;
                padding:12px;
                font-size:14px;
                font-weight:bold;
                min-width:140px;
            }
            QPushButton:hover{
                background:#00a381;
            }
        """)

        self.btn_sua = QPushButton("✏️ Sửa hồ sơ")
        self.btn_sua.setStyleSheet("""
            QPushButton{
                background:#fdcb6e;
                color:white;
                border:none;
                border-radius:10px;
                padding:12px;
                font-size:14px;
                font-weight:bold;
                min-width:140px;
            }
            QPushButton:hover{
                background:#f0b840;
            }
        """)

        self.btn_xoa = QPushButton("🗑️ Xóa hồ sơ")
        self.btn_xoa.setStyleSheet("""
            QPushButton{
                background:#d63031;
                color:white;
                border:none;
                border-radius:10px;
                padding:12px;
                font-size:14px;
                font-weight:bold;
                min-width:140px;
            }
            QPushButton:hover{
                background:#b71c1c;
            }
        """)

        btn_layout.addWidget(self.btn_them)
        btn_layout.addWidget(self.btn_sua)
        btn_layout.addWidget(self.btn_xoa)

        toolbar_layout.addLayout(btn_layout)

        main_layout.addWidget(toolbar_frame)

        # =================================================
        # TABLE
        # =================================================

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Tên hồ sơ",
            "Số ký hiệu",
            "Năm",
            "Ghi chú"
        ])

        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        header.setFixedHeight(50)
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.verticalHeader().setDefaultSectionSize(50)

        main_layout.addWidget(self.table)

        # =================================================
        # EVENTS
        # =================================================

        self.btn_them.clicked.connect(self.them_ho_so)
        self.btn_sua.clicked.connect(self.sua_ho_so)
        self.btn_xoa.clicked.connect(self.xoa_ho_so)
        self.btn_search.clicked.connect(self.tim_kiem_ho_so)
        self.btn_reload.clicked.connect(self.load_data)
        self.txt_search.returnPressed.connect(self.tim_kiem_ho_so)  # Nhấn Enter để tìm

        # Load data ban đầu
        self.load_data()

    # =================================================
    # LOAD DATA
    # =================================================

    def load_data(self):

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                Id,
                TieuDeHoSo,
                SoKyHieu,
                Nam,
                GhiChu
            FROM QuanLyHoSo
            ORDER BY Id DESC
        """)

        data = cursor.fetchall()

        self.table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value if value is not None else ""))
                self.table.setItem(row_idx, col_idx, item)

    # =================================================
    # TÌM KIẾM
    # =================================================

    def tim_kiem_ho_so(self):

        keyword = self.txt_search.text().strip()

        if not keyword:
            self.load_data()
            return

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                Id,
                TieuDeHoSo,
                SoKyHieu,
                Nam,
                GhiChu
            FROM QuanLyHoSo
            WHERE TieuDeHoSo LIKE ?
            ORDER BY Id DESC
        """, (f"%{keyword}%",))

        data = cursor.fetchall()

        self.table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value if value is not None else ""))
                self.table.setItem(row_idx, col_idx, item)

    # =================================================
    # THÊM HỒ SƠ
    # =================================================

    def them_ho_so(self):

        dlg = FormHoSo(self)  # Mở cửa sổ popup thêm mới

        if dlg.exec():
            data = dlg.get_data()

            # Validate
            if not data["ten"]:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên hồ sơ!")
                return

            if not data["so"]:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập số ký hiệu!")
                return

            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    INSERT INTO QuanLyHoSo
                    (
                        TieuDeHoSo,
                        SoKyHieu,
                        Nam,
                        NguoiLapId,
                        HanNopLuu,
                        TrangThaiDong,
                        GhiChu
                    )
                    VALUES
                    (
                        ?,
                        ?,
                        ?,
                        1,
                        GETDATE(),
                        0,
                        ?
                    )
                """, (
                    data["ten"],
                    data["so"],
                    data["nam"],
                    data["ghichu"]
                ))

                self.conn.commit()

                QMessageBox.information(self, "Thành công", "Thêm hồ sơ thành công!")
                self.load_data()

            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Thêm hồ sơ thất bại!\n{str(e)}")

    # =================================================
    # SỬA HỒ SƠ
    # =================================================

    def sua_ho_so(self):

        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn hồ sơ cần sửa!")
            return

        # Lấy dữ liệu từ bảng
        ho_so_data = {
            "id": self.table.item(row, 0).text(),
            "ten": self.table.item(row, 1).text(),
            "so": self.table.item(row, 2).text(),
            "nam": int(self.table.item(row, 3).text()),
            "ghichu": self.table.item(row, 4).text()
        }

        dlg = FormHoSo(self, ho_so_data)  # Mở cửa sổ popup sửa

        if dlg.exec():
            data = dlg.get_data()

            # Validate
            if not data["ten"]:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên hồ sơ!")
                return

            if not data["so"]:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập số ký hiệu!")
                return

            confirm = QMessageBox.question(
                self,
                "Xác nhận",
                "Bạn có chắc muốn cập nhật hồ sơ này?"
            )

            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("""
                        UPDATE QuanLyHoSo
                        SET
                            TieuDeHoSo=?,
                            SoKyHieu=?,
                            Nam=?,
                            GhiChu=?
                        WHERE Id=?
                    """, (
                        data["ten"],
                        data["so"],
                        data["nam"],
                        data["ghichu"],
                        ho_so_data["id"]
                    ))

                    self.conn.commit()

                    QMessageBox.information(self, "Thành công", "Cập nhật hồ sơ thành công!")
                    self.load_data()

                except Exception as e:
                    QMessageBox.critical(self, "Lỗi", f"Cập nhật hồ sơ thất bại!\n{str(e)}")

    # =================================================
    # XÓA HỒ SƠ
    # =================================================

    def xoa_ho_so(self):

        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn hồ sơ cần xóa!")
            return

        id = self.table.item(row, 0).text()
        ten = self.table.item(row, 1).text()

        confirm = QMessageBox.question(
            self,
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa hồ sơ:\n\n\"{ten}\"?\n\nHành động này không thể hoàn tác!"
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "DELETE FROM QuanLyHoSo WHERE Id=?",
                    (id,)
                )

                self.conn.commit()

                QMessageBox.information(self, "Thành công", "Xóa hồ sơ thành công!")
                self.load_data()

            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Xóa hồ sơ thất bại!\n{str(e)}")