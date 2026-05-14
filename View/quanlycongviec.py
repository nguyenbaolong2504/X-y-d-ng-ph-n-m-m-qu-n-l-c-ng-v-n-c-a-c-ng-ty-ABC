from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pyodbc


# =========================================================
# FORM CÔNG VIỆC
# =========================================================

class FormCongViec(QDialog):

    def __init__(self,parent=None):

        super().__init__(parent)

        self.setWindowTitle("Thông tin công việc")

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
        QComboBox,
        QDateEdit{

            border:1px solid #dfe6e9;

            border-radius:10px;

            padding:10px;

            font-size:14px;

            background:#fdfdfd;

        }

        QLineEdit:focus,
        QTextEdit:focus,
        QComboBox:focus{

            border:2px solid #00b894;

        }

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

            background:#019875;

        }

        """)

        main = QVBoxLayout(self)

        # =====================================================
        # TITLE
        # =====================================================

        title = QLabel("✅ THÔNG TIN CÔNG VIỆC")

        title.setStyleSheet("""

            font-size:28px;
            font-weight:bold;
            color:#00b894;
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

        self.cbo_nguoi = QComboBox()

        self.cbo_nguoi.addItems([
            "Nguyễn Văn A",
            "Trần Văn B",
            "Lê Văn C"
        ])

        self.cbo_trangthai = QComboBox()

        self.cbo_trangthai.addItems([
            "Chưa xử lý",
            "Đang xử lý",
            "Hoàn thành"
        ])

        self.date_han = QDateEdit()

        self.date_han.setCalendarPopup(True)

        self.date_han.setDate(QDate.currentDate())

        self.txt_ghichu = QTextEdit()

        self.txt_ghichu.setMinimumHeight(120)

        form.addRow(
            "Tên công việc:",
            self.txt_ten
        )

        form.addRow(
            "Người xử lý:",
            self.cbo_nguoi
        )

        form.addRow(
            "Trạng thái:",
            self.cbo_trangthai
        )

        form.addRow(
            "Hạn xử lý:",
            self.date_han
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

class QuanLyCongViec(QWidget):

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

            background:#00b894;

            color:white;

            border:none;

            border-radius:10px;

            padding:12px;

            font-size:14px;

            font-weight:bold;

        }

        QPushButton:hover{

            background:#019875;

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

        title = QLabel("✅ QUẢN LÝ CÔNG VIỆC")

        title.setStyleSheet("""

            font-size:30px;

            font-weight:bold;

            color:#00b894;

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

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "Tên công việc",
            "Người xử lý",
            "Ngày tạo",
            "Trạng thái",
            "Hạn xử lý"
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

        self.table.setRowCount(0)

    # =====================================================
    # THEM
    # =====================================================

    def them(self):

        dlg = FormCongViec(self)

        if dlg.exec():

            row = self.table.rowCount()

            self.table.insertRow(row)

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    dlg.txt_ten.text()
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    dlg.cbo_nguoi.currentText()
                )
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    QDate.currentDate().toString(
                        "yyyy-MM-dd"
                    )
                )
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    dlg.cbo_trangthai.currentText()
                )
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    dlg.date_han.date().toString(
                        "yyyy-MM-dd"
                    )
                )
            )