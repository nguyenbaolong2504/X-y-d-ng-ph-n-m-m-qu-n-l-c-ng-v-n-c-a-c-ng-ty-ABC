from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, Qt
import textwrap # Import thư viện ngắt dòng tự động cho Tooltip

class DonViWindow(QWidget):
    them_signal = pyqtSignal()
    sua_signal = pyqtSignal(dict)
    xoa_signal = pyqtSignal(int)
    lam_moi_signal = pyqtSignal()
    timkiem_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ffffff;") 
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        lbl_title = QLabel("🏢 DANH MỤC ĐƠN VỊ, BỘ PHẬN")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(lbl_title)

        toolbar = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Tìm kiếm theo tên, SĐT, Email, Web...")
        self.txt_search.setStyleSheet("min-height: 35px; padding: 0 15px; border-radius: 6px; border: 1px solid #bdc3c7; color: #2c3e50;")
        self.txt_search.setFixedWidth(300)
        
        btn_search = QPushButton("🔍")
        btn_search.setFixedSize(40, 37)
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setStyleSheet("background-color: #f39c12; color: white; border-radius: 6px; border: none;")
        
        btn_refresh = QPushButton("↻")
        btn_refresh.setFixedSize(40, 37)
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setStyleSheet("background-color: #95a5a6; color: white; border-radius: 6px; font-size: 18px; border: none;")

        btn_them = QPushButton("+ Cập nhật đơn vị")
        btn_them.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_them.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 8px 15px; border-radius: 6px; border: none;")
        
        toolbar.addWidget(self.txt_search); toolbar.addWidget(btn_search); toolbar.addWidget(btn_refresh)
        toolbar.addStretch(); toolbar.addWidget(btn_them)
        layout.addLayout(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["STT", "Đơn vị, bộ phận", "Địa chỉ", "Điện thoại", "Email", "Website", "Trạng thái", "Thao tác"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 50) 
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 110) 
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(6, 120) 
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(7, 120) 
        
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(True)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        # Tắt tự động xuống dòng và ép chiều cao cố định để bảng gọn gàng, hiện dấu ...
        self.table.setWordWrap(False)
        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        
        # Thêm CSS cho Tooltip vuông vắn nền trắng chữ đen
        self.table.setStyleSheet("""
            QTableWidget { border: 1px solid #dcdde1; gridline-color: #ecf0f1; color: #2c3e50; font-size: 13px;} 
            QHeaderView::section { background-color: #f8f9fa; color: #2c3e50; font-weight: bold; border: 1px solid #ecf0f1; padding: 10px;}
            QTableWidget::item { padding: 5px; }
            QToolTip {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #7f8c8d;
                border-radius: 4px;
                padding: 6px;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.table)

        btn_them.clicked.connect(self.them_signal.emit)
        btn_refresh.clicked.connect(self.lam_moi_signal.emit)
        btn_search.clicked.connect(lambda: self.timkiem_signal.emit(self.txt_search.text()))
        self.txt_search.returnPressed.connect(lambda: self.timkiem_signal.emit(self.txt_search.text()))

    def load_data(self, data):
        self.table.setRowCount(0)
        for i, r in enumerate(data):
            self.table.insertRow(i)
            
            # STT
            stt = QTableWidgetItem(str(i+1))
            stt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 0, stt)
            
            # Tên đơn vị (Thêm Tooltip)
            ten_str = str(r['TenDonVi'] or "")
            ten = QTableWidgetItem(ten_str)
            if ten_str.strip():
                ten.setToolTip("<br>".join(textwrap.wrap(ten_str, width=50)))
            self.table.setItem(i, 1, ten)
            
            # Địa chỉ (Thêm Tooltip)
            dc_str = str(r['DiaChi'] or "")
            dc = QTableWidgetItem(dc_str)
            if dc_str.strip():
                dc.setToolTip("<br>".join(textwrap.wrap(dc_str, width=50)))
            self.table.setItem(i, 2, dc)
            
            # Điện thoại
            sdt = QTableWidgetItem(str(r['DienThoai'] or ""))
            sdt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 3, sdt)
            
            # Email (Thêm Tooltip)
            email_str = str(r['Email'] or "")
            email = QTableWidgetItem(email_str)
            if email_str.strip():
                email.setToolTip("<br>".join(textwrap.wrap(email_str, width=50)))
            self.table.setItem(i, 4, email)
            
            # Website (Thêm Tooltip)
            web_url = str(r['Website'] or "").strip()
            if web_url:
                href_url = web_url if web_url.startswith('http') else 'http://' + web_url
                lbl_web = QLabel(f'<a href="{href_url}" style="color: #3498db; text-decoration: none;">{web_url}</a>')
                lbl_web.setOpenExternalLinks(True) 
                lbl_web.setAlignment(Qt.AlignmentFlag.AlignVCenter)
                lbl_web.setStyleSheet("padding-left: 5px; background: transparent;")
                lbl_web.setToolTip(web_url) # Tooltip cho link web
                self.table.setCellWidget(i, 5, lbl_web)
            else:
                self.table.setItem(i, 5, QTableWidgetItem(""))
            
            # Trạng thái
            tt_val = str(r.get('TrangThai', '1'))
            if tt_val == '1' or tt_val.lower() == 'true':
                lbl_text = "Hiển thị"; color = "#2ecc71" 
            else:
                lbl_text = "Không hiển thị"; color = "#e74c3c"

            lbl_badge = QLabel(lbl_text)
            lbl_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_badge.setStyleSheet(f"background-color: {color}; color: white; font-weight: bold; border-radius: 4px; padding: 4px;")
            
            badge_container = QWidget()
            badge_container.setStyleSheet("background: transparent;")
            bc_layout = QHBoxLayout(badge_container)
            bc_layout.setContentsMargins(10, 10, 10, 10)
            bc_layout.addWidget(lbl_badge)
            self.table.setCellWidget(i, 6, badge_container)

            # Thao tác
            btns = QWidget()
            btns.setStyleSheet("background: transparent; border: none;")
            l = QHBoxLayout(btns)
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(8)
            
            b_edit = QPushButton("Sửa")
            b_edit.setFixedSize(50, 30)
            b_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            b_edit.setStyleSheet("background-color: #f1c40f; color: #2c3e50; font-weight: bold; border-radius: 4px;")
            b_edit.clicked.connect(lambda ch, row=r: self.sua_signal.emit(row))
            
            b_del = QPushButton("Xóa")
            b_del.setFixedSize(50, 30)
            b_del.setCursor(Qt.CursorShape.PointingHandCursor)
            b_del.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; border-radius: 4px;")
            b_del.clicked.connect(lambda ch, id_v=r['Id']: self.xoa_signal.emit(id_v))
            
            l.addStretch(); l.addWidget(b_edit); l.addWidget(b_del); l.addStretch()
            self.table.setCellWidget(i, 7, btns)