from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, Qt
import textwrap # Import thư viện ngắt dòng tự động

class TableWidgetGeneric(QFrame): 
    them_signal = pyqtSignal()
    sua_signal = pyqtSignal(dict)
    xoa_signal = pyqtSignal(int)
    lam_moi_signal = pyqtSignal()
    timkiem_signal = pyqtSignal(str)

    def __init__(self, title_text):
        super().__init__()
        self.title_text = title_text
        self.setObjectName("TableContainer")
        self.setup_ui()

    def setup_ui(self):
        # YÊU CẦU 1: Ép cứng nền trắng cho khung bao ngoài
        self.setStyleSheet("""
            QFrame#TableContainer { 
                background-color: #ffffff; 
                border: 1px solid #dcdde1; 
                border-radius: 8px; 
            }
            /* YÊU CẦU 3: Tooltip hộp vuông nền trắng, chữ đen */
            QToolTip {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #7f8c8d;
                border-radius: 4px;
                padding: 6px;
                font-size: 13px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15) 
        layout.setSpacing(10)
        
        # Header & Toolbar
        header = QHBoxLayout()
        lbl = QLabel(f"📂 {self.title_text.upper()}")
        lbl.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; border: none;")
        btn_add = QPushButton("+ Thêm")
        btn_add.setFixedSize(70, 30)
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setStyleSheet("background-color: #27ae60; color: white; border-radius: 4px; font-weight: bold; border: none;")
        btn_add.clicked.connect(self.them_signal.emit)
        header.addWidget(lbl)
        header.addStretch()
        header.addWidget(btn_add)
        layout.addLayout(header)

        toolbar = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Tìm theo mã hoặc tên...")
        self.txt_search.setStyleSheet("min-height: 32px; padding: 0 10px; border-radius: 4px; border: 1px solid #bdc3c7; background: #ffffff; color: #2c3e50;")
        btn_search = QPushButton("🔍")
        btn_search.setFixedSize(35, 32)
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setStyleSheet("background-color: #f39c12; color: white; border-radius: 4px; border: none;")
        btn_search.clicked.connect(lambda: self.timkiem_signal.emit(self.txt_search.text()))
        self.txt_search.returnPressed.connect(lambda: self.timkiem_signal.emit(self.txt_search.text()))
        toolbar.addWidget(self.txt_search)
        toolbar.addWidget(btn_search)
        layout.addLayout(toolbar)

        # ================= CẤU HÌNH BẢNG =================
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["STT", "Mã", "Tên loại văn bản", "Ghi chú", "Thao tác"])
        
        self.table.setWordWrap(False) 
        
        # YÊU CẦU 2: Tăng chiều cao hàng lên 50px để nút không bị khuyết
        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        
        header_h = self.table.horizontalHeader()
        header_h.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header_h.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 50)
        
        # YÊU CẦU 2: Nới rộng cột thao tác ra 150px
        header_h.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 150) 
        
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(True)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setStyleSheet("""
            QTableWidget { 
                border: 1px solid #ecf0f1; 
                gridline-color: #f1f2f6; 
                background-color: #ffffff;
                color: #2c3e50;
            }
            QHeaderView::section { 
                background-color: #f8f9fa; 
                color: #2c3e50; 
                font-weight: bold; 
                border: 1px solid #ecf0f1; 
                padding: 8px;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        layout.addWidget(self.table)

    def load_data(self, data):
        self.table.setRowCount(0)
        for i, r in enumerate(data):
            self.table.insertRow(i)
            
            stt = QTableWidgetItem(str(i+1))
            stt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 0, stt)
            
            ma = QTableWidgetItem(str(r.get('MaLoai', '') or ''))
            ma.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 1, ma)
            
            ten = QTableWidgetItem(str(r.get('TenLoai', '')))
            self.table.setItem(i, 2, ten)
            
            # GHI CHÚ
            gc_text = str(r.get('MoTa', '') or '')
            gc = QTableWidgetItem(gc_text)
            gc.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            
            # YÊU CẦU 3: Ngắt dòng văn bản mỗi 50 ký tự để tạo thành khối hình vuông/chữ nhật
            if gc_text.strip() != "":
                wrapped_tooltip = "<br>".join(textwrap.wrap(gc_text, width=50))
                gc.setToolTip(wrapped_tooltip) 
            
            self.table.setItem(i, 3, gc)
            
            # YÊU CẦU 2: Xóa lề (Margins) của layout chứa nút để nó bung tối đa
            btns = QWidget()
            btns.setStyleSheet("background: transparent; border: none;")
            l = QHBoxLayout(btns)
            l.setContentsMargins(0, 0, 0, 0) # Ép sát lề
            l.setSpacing(8)
            
            b_edit = QPushButton("Sửa")
            b_edit.setFixedSize(55, 30)
            b_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            b_edit.setStyleSheet("background-color: #f1c40f; color: #2c3e50; font-weight: bold; border-radius: 4px; border: none;")
            b_edit.clicked.connect(lambda ch, row=r: self.sua_signal.emit(row))
            
            b_del = QPushButton("Xóa")
            b_del.setFixedSize(55, 30)
            b_del.setCursor(Qt.CursorShape.PointingHandCursor)
            b_del.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; border-radius: 4px; border: none;")
            b_del.clicked.connect(lambda ch, id_v=r['Id']: self.xoa_signal.emit(id_v))
            
            l.addStretch()
            l.addWidget(b_edit)
            l.addWidget(b_del)
            l.addStretch()
            
            self.table.setCellWidget(i, 4, btns)

class LoaiCongVanWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #f4f6f9;") 
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(25)

        self.view_den = TableWidgetGeneric("Loại công văn đến")
        self.view_di = TableWidgetGeneric("Loại công văn đi")

        main_layout.addWidget(self.view_den)
        main_layout.addWidget(self.view_di)