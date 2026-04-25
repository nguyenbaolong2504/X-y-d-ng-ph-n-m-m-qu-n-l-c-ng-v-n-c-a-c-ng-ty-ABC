from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, Qt

class TableWidgetGeneric(QFrame): 
    them_signal = pyqtSignal()
    sua_signal = pyqtSignal(dict)
    xoa_signal = pyqtSignal(int)
    lam_moi_signal = pyqtSignal()
    timkiem_signal = pyqtSignal(str)

    def __init__(self, title_text):
        super().__init__()
        self.title_text = title_text
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: white; border: 1px solid #dcdde1; border-radius: 8px;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Header
        header = QHBoxLayout()
        lbl = QLabel(f"📂 {self.title_text.upper()}")
        lbl.setStyleSheet("font-weight: bold; font-size: 14px; border: none; color: #2c3e50;")
        btn_add = QPushButton("+ Thêm")
        btn_add.setFixedSize(70, 30)
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setStyleSheet("background-color: #27ae60; color: white; border-radius: 4px; font-weight: bold; border: none;")
        btn_add.clicked.connect(self.them_signal.emit)
        header.addWidget(lbl); header.addStretch(); header.addWidget(btn_add)
        layout.addLayout(header)

        # Toolbar Tìm kiếm
        toolbar = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Tìm theo mã hoặc tên...")
        self.txt_search.setStyleSheet("min-height: 32px; padding: 0 10px; border-radius: 4px; border: 1px solid #bdc3c7; background: #fdfdfd; color: #2c3e50;")
        
        btn_search = QPushButton("🔍")
        btn_search.setFixedSize(35, 32)
        btn_search.setStyleSheet("background-color: #f39c12; color: white; border-radius: 4px; font-size: 14px; border: none;")
        btn_search.clicked.connect(lambda: self.timkiem_signal.emit(self.txt_search.text()))
        self.txt_search.returnPressed.connect(lambda: self.timkiem_signal.emit(self.txt_search.text()))
        
        btn_refresh = QPushButton("↻")
        btn_refresh.setFixedSize(35, 32)
        btn_refresh.setStyleSheet("background-color: #95a5a6; color: white; border-radius: 4px; font-size: 18px; border: none;")
        btn_refresh.clicked.connect(self.lam_moi_signal.emit)

        toolbar.addWidget(self.txt_search); toolbar.addWidget(btn_search); toolbar.addWidget(btn_refresh)
        layout.addLayout(toolbar)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["STT", "Mã", "Tên loại", "Ghi chú", "Thao tác"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 40)
        
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 130)
        
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(True)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        # === CÁC DÒNG CODE MỚI ĐỂ HIỂN THỊ FULL TEXT GHI CHÚ ===
        self.table.setWordWrap(True) # Cho phép văn bản tự động xuống dòng
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents) # Tự động giãn chiều cao hàng theo nội dung
        self.table.verticalHeader().setMinimumSectionSize(45) # Ép chiều cao tối thiểu là 45px cho đẹp
        # =========================================================

        self.table.setStyleSheet("""
            QTableWidget { 
                border: none; 
                gridline-color: #ecf0f1; 
                color: #2c3e50; 
            } 
            QHeaderView::section { 
                background-color: #f8f9fa; 
                color: #2c3e50; 
                font-weight: bold; 
                border: 1px solid #ecf0f1; 
                padding: 5px;
            }
        """)
        layout.addWidget(self.table)

    def load_data(self, data):
        self.table.setRowCount(0)
        for i, r in enumerate(data):
            self.table.insertRow(i)
            # ĐÃ XÓA DÒNG: self.table.setRowHeight(i, 40) (vì đã thiết lập tự động co giãn ở trên)
            
            stt = QTableWidgetItem(str(i+1))
            stt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 0, stt)
            
            ma = QTableWidgetItem(str(r['MaCongVan'] or ""))
            ma.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 1, ma)
            
            ten = QTableWidgetItem(str(r['TenHinhThuc'] or ""))
            ten.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 2, ten)
            
            gc = QTableWidgetItem(str(r['GhiChu'] or ""))
            gc.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 3, gc)
            
            btns = QWidget()
            btns.setObjectName("ActionContainer")
            btns.setStyleSheet("QWidget#ActionContainer { background: transparent; border: none; }")
            
            l = QHBoxLayout(btns)
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(6)
            
            b_edit = QPushButton("Sửa")
            b_edit.setFixedSize(55, 26)
            b_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            b_edit.setStyleSheet("background-color: #f1c40f; color: #2c3e50; font-weight: bold; border-radius: 4px; border: none;")
            b_edit.clicked.connect(lambda ch, row=r: self.sua_signal.emit(row))
            
            b_del = QPushButton("Xóa")
            b_del.setFixedSize(55, 26)
            b_del.setCursor(Qt.CursorShape.PointingHandCursor)
            b_del.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; border-radius: 4px; border: none;")
            b_del.clicked.connect(lambda ch, id_v=r['Id']: self.xoa_signal.emit(id_v))
            
            l.addStretch()
            l.addWidget(b_edit)
            l.addWidget(b_del)
            l.addStretch()
            
            self.table.setCellWidget(i, 4, btns)

class LoaiVanBanWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #f4f6f9;")
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(25)

        self.view_den = TableWidgetGeneric("Loại văn bản đến")
        self.view_di = TableWidgetGeneric("Loại văn bản đi")

        main_layout.addWidget(self.view_den)
        main_layout.addWidget(self.view_di)