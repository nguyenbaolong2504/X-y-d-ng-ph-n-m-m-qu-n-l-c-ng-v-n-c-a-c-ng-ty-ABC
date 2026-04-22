from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, Qt

class ChucVuWindow(QWidget):
    them_signal = pyqtSignal()
    sua_signal = pyqtSignal(dict)
    xoa_signal = pyqtSignal(int)
    lam_moi_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Tiêu đề và nút Thêm
        header_layout = QHBoxLayout()
        header_lbl = QLabel("📂 DANH MỤC CHỨC VỤ")
        header_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        
        self.btn_them = QPushButton("➕ Thêm chức vụ")
        self.btn_them.setStyleSheet("background-color: #27ae60; color: white; padding: 6px 12px;")
        
        header_layout.addWidget(header_lbl)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_them)
        layout.addLayout(header_layout)

        # Bảng hiển thị
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["STT", "Tên chức vụ", "Trạng thái", "Ghi chú", "Thao tác"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.btn_them.clicked.connect(self.them_signal.emit)

    def load_data(self, data_list):
        self.table.setRowCount(0)
        for i, row in enumerate(data_list):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.table.setItem(i, 1, QTableWidgetItem(str(row['TenChucVu'])))
            
            # Hiển thị trạng thái bằng Label màu sắc cho giống hình mẫu
            status_text = "Hiển thị" if row['TrangThai'] == 1 else "Đang ẩn"
            status_color = "#2ecc71" if row['TrangThai'] == 1 else "#e67e22"
            lbl_status = QLabel(status_text)
            lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_status.setStyleSheet(f"background-color: {status_color}; color: white; border-radius: 4px; margin: 4px;")
            self.table.setCellWidget(i, 2, lbl_status)
            
            self.table.setItem(i, 3, QTableWidgetItem(str(row['GhiChu'] or "")))

            # Nút Thao tác
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            
            btn_edit = QPushButton("📝")
            btn_edit.setFixedWidth(30)
            btn_edit.clicked.connect(lambda ch, r=row: self.sua_signal.emit(r))
            
            btn_del = QPushButton("🗑️")
            btn_del.setFixedWidth(30)
            btn_del.setStyleSheet("color: red;")
            btn_del.clicked.connect(lambda ch, id_cv=row['Id']: self.xoa_signal.emit(id_cv))
            
            btn_layout.addWidget(btn_edit)
            btn_layout.addWidget(btn_del)
            self.table.setCellWidget(i, 4, btn_widget)