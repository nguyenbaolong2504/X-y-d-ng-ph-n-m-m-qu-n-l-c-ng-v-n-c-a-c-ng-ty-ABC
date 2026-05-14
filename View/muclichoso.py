from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pyodbc


# =========================================================
# FORM
# =========================================================

class FormMucLuc(QDialog):

    def __init__(self,parent=None):

        super().__init__(parent)

        self.setWindowTitle("Thông tin mục lục hồ sơ")

        self.resize(700,550)

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

        # =====================================================
        # TITLE
        # =====================================================

        title = QLabel("📁 THÔNG TIN MỤC LỤC")

        title.setStyleSheet("""

            font-size:28px;
            font-weight:bold;
            color:#6c5ce7;
            padding-bottom:15px;

        """)

        main.addWidget(title)

        # =====================================================
        # FORM
        # =====================================================

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
            "Tiêu đề hồ sơ:",
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

        # =====================================================
        # BUTTON
        # =====================================================

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
# MAIN
# =========================================================

class MucLucHoSo(QWidget):

    def __init__(self):

        super().__init__()

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

        QPushButton{

            background:#6c5ce7;

            color:white;

            border:none;

            border-radius:10px;

            padding:12px;

            font-size:14px;

            font-weight:bold;

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

        QHeaderView::section{

            background:white;

            border:1px solid #ecf0f1;

            padding:14px;

            font-size:14px;

            font-weight:bold;

        }

        """)

        layout = QVBoxLayout(self)

        # =====================================================
        # TITLE
        # =====================================================

        title = QLabel("📁 MỤC LỤC HỒ SƠ")

        title.setStyleSheet("""

            font-size:30px;

            font-weight:bold;

            color:#6c5ce7;

            padding:10px;

        """)

        layout.addWidget(title)

        # =====================================================
        # TOOLBAR
        # =====================================================

        top = QHBoxLayout()

        btn_add = QPushButton("➕ Thêm")

        btn_edit = QPushButton("✏️ Sửa")

        btn_delete = QPushButton("🗑️ Xóa")

        btn_reload = QPushButton("🔄 Làm mới")

        top.addWidget(btn_add)

        top.addWidget(btn_edit)

        top.addWidget(btn_delete)

        top.addWidget(btn_reload)

        layout.addLayout(top)

        # =====================================================
        # TABLE
        # =====================================================

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Tiêu đề hồ sơ",
            "Số ký hiệu",
            "Năm"
        ])

        self.table.verticalHeader().setVisible(False)

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()

        header.setFixedHeight(45)

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.verticalHeader().setDefaultSectionSize(45)

        layout.addWidget(self.table)

        # =====================================================
        # EVENT
        # =====================================================

        btn_add.clicked.connect(self.them)

        btn_reload.clicked.connect(self.load_data)

        self.load_data()

    # =====================================================
    # LOAD DATA
    # =====================================================

    def load_data(self):

        cursor = self.conn.cursor()

        cursor.execute("""

            SELECT
                Id,
                TieuDeHoSo,
                SoKyHieu,
                Nam

            FROM DanhMucHoSo

        """)

        data = cursor.fetchall()

        self.table.setRowCount(len(data))

        for r,row in enumerate(data):

            for c,val in enumerate(row):

                self.table.setItem(
                    r,
                    c,
                    QTableWidgetItem(str(val))
                )

    # =====================================================
    # THEM
    # =====================================================

    def them(self):

        dlg = FormMucLuc(self)

        if dlg.exec():

            cursor = self.conn.cursor()

            cursor.execute("""

                INSERT INTO DanhMucHoSo
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

            """,(

                dlg.txt_ten.text(),

                dlg.txt_so.text(),

                dlg.spin_nam.value(),

                dlg.txt_ghichu.toPlainText()

            ))

            self.conn.commit()

            self.load_data()