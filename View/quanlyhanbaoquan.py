from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, Qt

class HanBaoQuanWindow(QWidget):
    them_signal = pyqtSignal()
    sua_signal = pyqtSignal(dict)
    xoa_signal = pyqtSignal(int)
    lam_moi_signal = pyqtSignal()
    timkiem_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ffffff;") 
        self.setup_ui()
        self.apply_premium_styles()

    def apply_premium_styles(self):
        style = """
            QLabel#HeaderTitle {
                font-size: 20px; 
                font-weight: bold; 
                color: #2c3e50;
                padding: 10px 0px;
                background-color: transparent;
            }
            
            QLineEdit#SearchBox {
                min-height: 38px;
                padding: 0px 15px; 
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                font-size: 14px;
                color: #2c3e50;
                background-color: #ffffff;
            }
            QLineEdit#SearchBox:focus { border: 2px solid #3498db; }
            
            QPushButton#BtnThem { 
                background-color: #3498db; 
                color: white; 
                border-radius: 6px; 
                padding: 8px 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#BtnThem:hover { background-color: #2980b9; }

            QPushButton.IconBtn {
                border-radius: 6px; 
                font-size: 18px; 
                font-weight: bold;
                border: none;
            }
            
            QPushButton#BtnSearch { background-color: #f39c12; color: white; }
            QPushButton#BtnSearch:hover { background-color: #e67e22; }
            
            QPushButton#BtnRefresh { background-color: #95a5a6; color: white; }
            QPushButton#BtnRefresh:hover { background-color: #7f8c8d; }
            
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #dcdde1;
                gridline-color: #ecf0f1; 
                selection-background-color: #e3f2fd;
                selection-color: #2c3e50;
                color: #2c3e50;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #34495e;
                font-weight: bold;
                font-size: 14px;
                padding: 12px;
                border: 1px solid #dcdde1;
            }
        """
        self.table.setStyleSheet(style)
        self.btn_them.setStyleSheet(style)
        self.btn_search.setStyleSheet(style)
        self.btn_refresh.setStyleSheet(style)
        self.txt_search.setStyleSheet(style)
        self.lbl_title.setStyleSheet(style)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.lbl_title = QLabel("DANH MỤC THỜI HẠN BẢO QUẢN")
        self.lbl_title.setObjectName("HeaderTitle")
        layout.addWidget(self.lbl_title)

        toolbar_layout = QHBoxLayout()
        
        self.txt_search = QLineEdit()
        self.txt_search.setObjectName("SearchBox")
        self.txt_search.setPlaceholderText("Nhập từ khóa tìm kiếm...")
        self.txt_search.setFixedWidth(300)
        
        self.btn_search = QPushButton("🔍")
        self.btn_search.setObjectName("BtnSearch")
        self.btn_search.setProperty("class", "IconBtn")
        self.btn_search.setFixedSize(40, 40)
        self.btn_search.setToolTip("Tìm kiếm (Enter)")
        self.btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_refresh = QPushButton("↻")
        self.btn_refresh.setObjectName("BtnRefresh")
        self.btn_refresh.setProperty("class", "IconBtn")
        self.btn_refresh.setFixedSize(40, 40)
        self.btn_refresh.setToolTip("Làm mới dữ liệu")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_them = QPushButton("+ Thêm thời hạn")
        self.btn_them.setObjectName("BtnThem")
        self.btn_them.setCursor(Qt.CursorShape.PointingHandCursor)
        
        toolbar_layout.addWidget(self.txt_search)
        toolbar_layout.addWidget(self.btn_search)
        toolbar_layout.addWidget(self.btn_refresh)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.btn_them)
        
        layout.addLayout(toolbar_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["STT", "Tên thời hạn", "Ghi chú", "Thao tác"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # NỚI RỘNG CỘT THAO TÁC LÊN 160 ĐỂ ĐỦ CHỖ CHO 2 NÚT CÓ CHỮ
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 160) 
        self.table.verticalHeader().setVisible(False) 
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setShowGrid(True) 
        
        layout.addWidget(self.table)

        self.btn_them.clicked.connect(self.them_signal.emit)
        self.btn_refresh.clicked.connect(self.lam_moi_signal.emit)
        self.btn_search.clicked.connect(lambda: self.timkiem_signal.emit(self.txt_search.text()))
        self.txt_search.returnPressed.connect(lambda: self.timkiem_signal.emit(self.txt_search.text()))

    def load_data(self, data_list):
        self.table.setRowCount(0)
        for i, row in enumerate(data_list):
            self.table.insertRow(i)
            self.table.setRowHeight(i, 45) 

            item_stt = QTableWidgetItem(str(i + 1))
            item_stt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 0, item_stt)
            
            item_ten = QTableWidgetItem(str(row['TenHanBaoQuan']))
            item_ten.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 1, item_ten)

            item_gc = QTableWidgetItem(str(row['GhiChu'] or ""))
            item_gc.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 2, item_gc)

            btn_widget = QWidget()
            btn_widget.setObjectName("CellWidget")
            btn_widget.setStyleSheet("QWidget#CellWidget { background-color: transparent; }") 
            
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setSpacing(8)
            
            # TRẢ LẠI CHỮ "SỬA" VÀ TĂNG KÍCH THƯỚC LÊN 70px
            btn_edit = QPushButton("Sửa")
            btn_edit.setFixedSize(70, 30)
            btn_edit.setToolTip("Sửa thông tin")
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.setStyleSheet("""
                QPushButton { background-color: #f1c40f; color: #2c3e50; border-radius: 4px; font-weight: bold; font-size: 13px; border: none; }
                QPushButton:hover { background-color: #f39c12; }
            """)
            btn_edit.clicked.connect(lambda ch, r=row: self.sua_signal.emit(r))
            
            # TRẢ LẠI CHỮ "XÓA" VÀ TĂNG KÍCH THƯỚC LÊN 70px
            btn_del = QPushButton("Xóa")
            btn_del.setFixedSize(70, 30)
            btn_del.setToolTip("Xóa mục này")
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.setStyleSheet("""
                QPushButton { background-color: #e74c3c; color: white; border-radius: 4px; font-weight: bold; font-size: 13px; border: none; }
                QPushButton:hover { background-color: #c0392b; }
            """)
            btn_del.clicked.connect(lambda ch, id_hbq=row['Id']: self.xoa_signal.emit(id_hbq))
            
            btn_layout.addStretch()
            btn_layout.addWidget(btn_edit)
            btn_layout.addWidget(btn_del)
            btn_layout.addStretch()

            self.table.setCellWidget(i, 3, btn_widget)