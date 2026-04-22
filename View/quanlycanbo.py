from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, Qt

class CanBoWindow(QWidget):
    them_signal = pyqtSignal()
    sua_signal = pyqtSignal(dict)  # Nhận data để sửa
    xoa_signal = pyqtSignal(int)   # Nhận Id để xóa
    lam_moi_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Toolbar
        toolbar = QHBoxLayout()
        self.btn_them = QPushButton("➕ Thêm cán bộ")
        self.btn_them.setStyleSheet("background-color: #27ae60; color: white; padding: 8px;")
        self.btn_lam_moi = QPushButton("🔄 Làm mới")
        toolbar.addWidget(self.btn_them)
        toolbar.addWidget(self.btn_lam_moi)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # Table - Sử dụng QTableWidget để dễ chèn nút bấm Sửa/Xóa
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "STT", "Họ và tên", "Ngày sinh", "Chức vụ", "Đơn vị", "Tên truy cập", "Email", "Thao tác"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Kết nối nút bấm chính
        self.btn_them.clicked.connect(self.them_signal.emit)
        self.btn_lam_moi.clicked.connect(self.lam_moi_signal.emit)

    # ĐỊNH NGHĨA HÀM NÀY ĐỂ HẾT LỖI
    def set_table_model(self, model):
        """Hàm này nhận dữ liệu và hiển thị lên QTableWidget"""
        # Lưu ý: Vì bạn đang dùng QTableWidget nên ta lấy data từ model để load
        data = model._data if hasattr(model, '_data') else []
        self.load_data_to_table(data)

    def load_data_to_table(self, data_list):
        self.table.setRowCount(0)
        for i, row in enumerate(data_list):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.table.setItem(i, 1, QTableWidgetItem(str(row.get('HoTen', ''))))
            self.table.setItem(i, 2, QTableWidgetItem(str(row.get('NgaySinh', ''))))
            self.table.setItem(i, 3, QTableWidgetItem(str(row.get('TenChucVu', ''))))
            self.table.setItem(i, 4, QTableWidgetItem(str(row.get('TenDonVi', ''))))
            self.table.setItem(i, 5, QTableWidgetItem(str(row.get('Username', ''))))
            self.table.setItem(i, 6, QTableWidgetItem(str(row.get('Email', ''))))

            # Nút Sửa/Xóa
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(2, 2, 2, 2)
            
            btn_edit = QPushButton("📝")
            btn_edit.setFixedWidth(30)
            btn_edit.clicked.connect(lambda ch, r=row: self.sua_signal.emit(r))
            
            btn_del = QPushButton("🗑️")
            btn_del.setFixedWidth(30)
            btn_del.setStyleSheet("color: red;")
            btn_del.clicked.connect(lambda ch, id_cb=row['Id']: self.xoa_signal.emit(id_cb))
            
            btn_layout.addWidget(btn_edit)
            btn_layout.addWidget(btn_del)
            self.table.setCellWidget(i, 7, btn_widget)