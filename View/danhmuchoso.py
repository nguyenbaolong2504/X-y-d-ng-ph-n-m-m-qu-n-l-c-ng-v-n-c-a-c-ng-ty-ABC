from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pyodbc


# =========================================================
# FORM POPUP - DÙNG CHO THÊM/SỬA
# =========================================================

class FormQuanLyHoSo(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Thông tin hồ sơ")

        self.resize(650, 500)

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

        title = QLabel("🗂️ THÔNG TIN HỒ SƠ")

        title.setStyleSheet("""

            font-size:28px;
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

        self.txt_so = QLineEdit()

        self.spin_nam = QSpinBox()

        self.spin_nam.setMaximum(9999)

        self.spin_nam.setValue(2026)

        self.txt_ghichu = QTextEdit()

        self.txt_ghichu.setMinimumHeight(120)

        form.addRow(
            "Tên hồ sơ:",
            self.txt_ten
        )

        form.addRow(
            "Số ký hiệu:",
            self.txt_so
        )

        form.addRow(
            "Năm:",
            self.spin_nam
        )

        form.addRow(
            "Ghi chú:",
            self.txt_ghichu
        )

        main.addWidget(form_frame)

        # =================================================
        # BUTTON
        # =================================================

        bottom = QHBoxLayout()

        bottom.addStretch()

        btn_ok = QPushButton("💾 Lưu")

        btn_cancel = QPushButton("❌ Hủy")

        btn_cancel.setStyleSheet("""

            QPushButton{

                background:#d63031;

            }

            QPushButton:hover{

                background:#b71c1c;

            }

        """)

        btn_ok.clicked.connect(self.accept)

        btn_cancel.clicked.connect(self.reject)

        bottom.addWidget(btn_ok)

        bottom.addWidget(btn_cancel)

        main.addLayout(bottom)


# =========================================================
# WIDGET CHÍNH - QUẢN LÝ HỒ SƠ
# =========================================================

class QuanLyHoSo(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("🗂️ QUẢN LÝ HỒ SƠ")
        self.resize(1000, 700)

        # =================================================
        # SQL CONNECTION
        # =================================================

        self.conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=congtyabc;"
            "Trusted_Connection=yes;"
        )

        self.current_id = None  # Lưu ID đang sửa

        # =================================================
        # STYLE TOÀN BỘ
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

        QLineEdit,
        QTextEdit,
        QSpinBox{

            border:1px solid #dfe6e9;
            border-radius:10px;
            padding:10px;
            font-size:14px;
            background:white;

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
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # =================================================
        # TITLE
        # =================================================

        title = QLabel("🗂️ QUẢN LÝ HỒ SƠ")
        title.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
            color:#6c5ce7;
            padding:10px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # =================================================
        # FORM NHẬP LIỆU
        # =================================================

        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:15px;
                padding:20px;
                border:1px solid #dfe6e9;
            }
        """)

        form_layout = QVBoxLayout(form_frame)

        form_title = QLabel("📝 THÔNG TIN HỒ SƠ")
        form_title.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            color:#6c5ce7;
            padding-bottom:10px;
        """)
        form_layout.addWidget(form_title)

        # Grid form
        grid = QGridLayout()
        grid.setSpacing(15)

        # Tên hồ sơ
        grid.addWidget(QLabel("Tên hồ sơ:"), 0, 0)
        self.txt_ten = QLineEdit()
        self.txt_ten.setPlaceholderText("Nhập tên hồ sơ...")
        grid.addWidget(self.txt_ten, 0, 1)

        # Số ký hiệu
        grid.addWidget(QLabel("Số ký hiệu:"), 0, 2)
        self.txt_so = QLineEdit()
        self.txt_so.setPlaceholderText("Nhập số ký hiệu...")
        grid.addWidget(self.txt_so, 0, 3)

        # Năm
        grid.addWidget(QLabel("Năm:"), 1, 0)
        self.spin_nam = QSpinBox()
        self.spin_nam.setMaximum(9999)
        self.spin_nam.setValue(2026)
        grid.addWidget(self.spin_nam, 1, 1)

        # Ghi chú
        grid.addWidget(QLabel("Ghi chú:"), 1, 2)
        self.txt_ghichu = QTextEdit()
        self.txt_ghichu.setMaximumHeight(80)
        self.txt_ghichu.setPlaceholderText("Nhập ghi chú...")
        grid.addWidget(self.txt_ghichu, 1, 3)

        form_layout.addLayout(grid)

        # Buttons form
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
                min-width:120px;
            }
            QPushButton:hover{
                background:#00a381;
            }
        """)

        self.btn_sua = QPushButton("✏️ Cập nhật hồ sơ")
        self.btn_sua.setStyleSheet("""
            QPushButton{
                background:#fdcb6e;
                color:white;
                border:none;
                border-radius:10px;
                padding:12px;
                font-size:14px;
                font-weight:bold;
                min-width:120px;
            }
            QPushButton:hover{
                background:#f0b840;
            }
        """)

        self.btn_xoa_form = QPushButton("🗑️ Xóa hồ sơ")
        self.btn_xoa_form.setStyleSheet("""
            QPushButton{
                background:#d63031;
                color:white;
                border:none;
                border-radius:10px;
                padding:12px;
                font-size:14px;
                font-weight:bold;
                min-width:120px;
            }
            QPushButton:hover{
                background:#b71c1c;
            }
        """)

        self.btn_clear = QPushButton("🔄 Làm mới form")
        self.btn_clear.setStyleSheet("""
            QPushButton{
                background:#636e72;
                color:white;
                border:none;
                border-radius:10px;
                padding:12px;
                font-size:14px;
                font-weight:bold;
                min-width:120px;
            }
            QPushButton:hover{
                background:#4a5458;
            }
        """)

        btn_layout.addWidget(self.btn_them)
        btn_layout.addWidget(self.btn_sua)
        btn_layout.addWidget(self.btn_xoa_form)
        btn_layout.addWidget(self.btn_clear)
        form_layout.addLayout(btn_layout)

        main_layout.addWidget(form_frame)

        # =================================================
        # SEARCH BAR
        # =================================================

        search_frame = QFrame()
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(0, 0, 0, 0)

        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("font-size:20px;")
        search_layout.addWidget(search_icon)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Tìm kiếm hồ sơ theo tên...")
        self.txt_search.setStyleSheet("""
            QLineEdit{
                border:1px solid #dfe6e9;
                border-radius:10px;
                padding:12px;
                font-size:14px;
                background:white;
            }
        """)
        search_layout.addWidget(self.txt_search)

        self.btn_reload = QPushButton("🔄 Làm mới danh sách")
        search_layout.addWidget(self.btn_reload)

        main_layout.addWidget(search_frame)

        # =================================================
        # TABLE
        # =================================================

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Tên hồ sơ",
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
        header.setFixedHeight(45)
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.verticalHeader().setDefaultSectionSize(45)

        main_layout.addWidget(self.table)

        # =================================================
        # EVENTS
        # =================================================

        self.btn_them.clicked.connect(self.them_ho_so)
        self.btn_sua.clicked.connect(self.sua_ho_so)
        self.btn_xoa_form.clicked.connect(self.xoa_ho_so)
        self.btn_clear.clicked.connect(self.clear_form)
        self.btn_reload.clicked.connect(self.load_data)
        self.txt_search.textChanged.connect(self.tim_kiem_ho_so)
        self.table.clicked.connect(self.on_table_click)

        # Load data ban đầu
        self.load_data()

    # =================================================
    # CLEAR FORM
    # =================================================

    def clear_form(self):
        self.current_id = None
        self.txt_ten.clear()
        self.txt_so.clear()
        self.spin_nam.setValue(2026)
        self.txt_ghichu.clear()
        self.table.clearSelection()

    # =================================================
    # CLICK TABLE -> ĐIỀN FORM
    # =================================================

    def on_table_click(self, index):
        row = index.row()

        id_item = self.table.item(row, 0)
        ten_item = self.table.item(row, 1)
        nam_item = self.table.item(row, 2)
        ghichu_item = self.table.item(row, 3)

        if id_item:
            self.current_id = id_item.text()

        if ten_item:
            self.txt_ten.setText(ten_item.text())

        if nam_item:
            try:
                self.spin_nam.setValue(int(nam_item.text()))
            except:
                self.spin_nam.setValue(2026)

        if ghichu_item:
            self.txt_ghichu.setText(ghichu_item.text())

        # Lấy số ký hiệu từ database
        if self.current_id:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT SoKyHieu FROM QuanLyHoSo WHERE Id=?",
                (self.current_id,)
            )
            result = cursor.fetchone()
            if result and result[0]:
                self.txt_so.setText(str(result[0]))
            else:
                self.txt_so.clear()

    # =================================================
    # LOAD DATA
    # =================================================

    def load_data(self):

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                Id,
                TieuDeHoSo,
                Nam,
                GhiChu
            FROM QuanLyHoSo
            ORDER BY Id DESC
        """)

        data = cursor.fetchall()

        self.table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                self.table.setItem(
                    row_idx,
                    col_idx,
                    QTableWidgetItem(str(value))
                )

    # =================================================
    # SEARCH
    # =================================================

    def tim_kiem_ho_so(self):

        keyword = self.txt_search.text().strip()

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                Id,
                TieuDeHoSo,
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
                self.table.setItem(
                    row_idx,
                    col_idx,
                    QTableWidgetItem(str(value))
                )

    # =================================================
    # THÊM HỒ SƠ
    # =================================================

    def them_ho_so(self):

        ten = self.txt_ten.text().strip()
        so = self.txt_so.text().strip()
        nam = self.spin_nam.value()
        ghichu = self.txt_ghichu.toPlainText().strip()

        if not ten:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên hồ sơ!")
            self.txt_ten.setFocus()
            return

        if not so:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập số ký hiệu!")
            self.txt_so.setFocus()
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
            """, (ten, so, nam, ghichu))

            self.conn.commit()

            QMessageBox.information(self, "Thành công", "Thêm hồ sơ thành công!")

            self.clear_form()
            self.load_data()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Thêm hồ sơ thất bại!\n{str(e)}")

    # =================================================
    # SỬA HỒ SƠ
    # =================================================

    def sua_ho_so(self):

        if not self.current_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn hồ sơ cần sửa từ bảng!")
            return

        ten = self.txt_ten.text().strip()
        so = self.txt_so.text().strip()
        nam = self.spin_nam.value()
        ghichu = self.txt_ghichu.toPlainText().strip()

        if not ten:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên hồ sơ!")
            self.txt_ten.setFocus()
            return

        if not so:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập số ký hiệu!")
            self.txt_so.setFocus()
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
                """, (ten, so, nam, ghichu, self.current_id))

                self.conn.commit()

                QMessageBox.information(self, "Thành công", "Cập nhật hồ sơ thành công!")

                self.clear_form()
                self.load_data()

            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Cập nhật hồ sơ thất bại!\n{str(e)}")

    # =================================================
    # XÓA HỒ SƠ
    # =================================================

    def xoa_ho_so(self):

        if not self.current_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn hồ sơ cần xóa từ bảng!")
            return

        confirm = QMessageBox.question(
            self,
            "Xác nhận xóa",
            "Bạn có chắc muốn xóa hồ sơ này?\nHành động này không thể hoàn tác!"
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "DELETE FROM QuanLyHoSo WHERE Id=?",
                    (self.current_id,)
                )

                self.conn.commit()

                QMessageBox.information(self, "Thành công", "Xóa hồ sơ thành công!")

                self.clear_form()
                self.load_data()

            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Xóa hồ sơ thất bại!\n{str(e)}")