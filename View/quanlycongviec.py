from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import pyodbc


class QuanLyCongViec(QWidget):

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
        # STYLE
        # =====================================================

        self.setStyleSheet("""
            QWidget{
                background:#f5f6fa;
                font-family:Segoe UI;
            }

            QLineEdit{
                background:white;
                border:1px solid #dcdde1;
                border-radius:10px;
                padding:10px;
                font-size:14px;
            }

            QPushButton{
                border:none;
                border-radius:10px;
                color:white;
                font-weight:bold;
                padding:10px;
                font-size:14px;
            }

            QTableWidget{
                background:white;
                border-radius:10px;
                border:1px solid #dcdde1;
            }

            QHeaderView::section{
                background:#3498db;
                color:white;
                padding:13px;
                border:none;
                font-weight:bold;
            }
        """)

        layout = QVBoxLayout(self)

        # =====================================================
        # TITLE
        # =====================================================

        title = QLabel("QUẢN LÝ CÔNG VIỆC")

        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#3498db;
            padding:10px;
        """)

        layout.addWidget(title)

        # =====================================================
        # FORM
        # =====================================================

        form = QHBoxLayout()

        self.txt_ten = QLineEdit()
        self.txt_ten.setPlaceholderText(
            "Tên workflow..."
        )

        self.txt_yeucau = QLineEdit()
        self.txt_yeucau.setPlaceholderText(
            "Yêu cầu xử lý..."
        )

        form.addWidget(self.txt_ten)
        form.addWidget(self.txt_yeucau)

        layout.addLayout(form)

        # =====================================================
        # BUTTON
        # =====================================================

        btn_layout = QHBoxLayout()

        btn_add = QPushButton("+ Thêm")
        btn_add.setStyleSheet("""
            background:#27ae60;
        """)

        btn_update = QPushButton("✏️ Sửa")
        btn_update.setStyleSheet("""
            background:#f39c12;
        """)

        btn_delete = QPushButton("🗑 Xóa")
        btn_delete.setStyleSheet("""
            background:#e74c3c;
        """)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_delete)

        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        # =====================================================
        # TABLE
        # =====================================================

        self.table = QTableWidget()

        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Tên Workflow",
            "Yêu cầu xử lý"
        ])

        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.verticalHeader().setVisible(False)

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        layout.addWidget(self.table)

        # =====================================================
        # SIGNAL
        # =====================================================

        btn_add.clicked.connect(self.them)
        btn_update.clicked.connect(self.sua)
        btn_delete.clicked.connect(self.xoa)

        self.table.cellClicked.connect(self.chon)

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
                TenWorkflow,
                YeuCauXuLy
            FROM Workflow
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

        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO Workflow
            (
                SoDen,
                TenWorkflow,
                LoaiWorkflow,
                VanBanId,
                TrangThaiGiaiQuyet,
                NguoiTaoId,
                NgayTao,
                YeuCauXuLy
            )
            VALUES (?,?,?,?,?,?,GETDATE(),?)
        """,(
            1,
            self.txt_ten.text(),
            1,
            1,
            0,
            1,
            self.txt_yeucau.text()
        ))

        self.conn.commit()

        self.load_data()

        self.txt_ten.clear()
        self.txt_yeucau.clear()

    # =========================================================
    # CHỌN
    # =========================================================

    def chon(self,row,column):

        self.id_selected = self.table.item(row,0).text()

        self.txt_ten.setText(
            self.table.item(row,1).text()
        )

        self.txt_yeucau.setText(
            self.table.item(row,2).text()
        )

    # =========================================================
    # SỬA
    # =========================================================

    def sua(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE Workflow
            SET
                TenWorkflow=?,
                YeuCauXuLy=?
            WHERE Id=?
        """,(
            self.txt_ten.text(),
            self.txt_yeucau.text(),
            self.id_selected
        ))

        self.conn.commit()

        self.load_data()

    # =========================================================
    # XÓA
    # =========================================================

    def xoa(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            DELETE FROM Workflow
            WHERE Id=?
        """,(self.id_selected))

        self.conn.commit()

        self.load_data()