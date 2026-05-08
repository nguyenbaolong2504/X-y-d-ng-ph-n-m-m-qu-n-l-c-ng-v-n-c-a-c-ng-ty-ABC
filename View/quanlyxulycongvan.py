from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# ==========================================================
# 1. DIALOG: FORM NHẬP/SỬA THÔNG TIN (ĐÃ CẢI TIẾN)
# ==========================================================
class XuLyCongVanDialog(QDialog):
    def __init__(self, parent=None, data=None, lists=None):
        super().__init__(parent)
        self.data = data    # Dữ liệu để sửa (nếu có)
        self.lists = lists  # Danh sách cán bộ, đơn vị, công văn từ DB
        self.setWindowTitle("📝 Phân công xử lý công văn")
        self.setFixedWidth(500)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # Sử dụng QComboBox thay cho QLineEdit để chọn tên thay vì nhập ID
        self.cb_canbo_nhan = QComboBox()
        self.cb_congvan = QComboBox()
        self.cb_donvi = QComboBox()
        self.cb_canbo_chuyen = QComboBox()
        
        self.date_chuyen = QDateEdit(calendarPopup=True)
        self.date_chuyen.setDate(QDate.currentDate())
        
        self.txt_noidung = QTextEdit()
        self.txt_noidung.setMaximumHeight(100)
        self.txt_noidung.setPlaceholderText("Nhập nội dung yêu cầu xử lý...")

        # Đổ dữ liệu từ 'lists' vào các ComboBox (Tên hiển thị, Id ẩn bên dưới)
        if self.lists:
            # Load danh sách cán bộ
            for id_cb, name in self.lists.get('canbo', []):
                self.cb_canbo_nhan.addItem(name, id_cb)
                self.cb_canbo_chuyen.addItem(name, id_cb)
            
            # Load danh sách công văn
            for id_cv, trich_yeu in self.lists.get('congvan', []):
                # Hiển thị 50 ký tự đầu của trích yếu
                display_text = (trich_yeu[:50] + '...') if len(trich_yeu) > 50 else trich_yeu
                self.cb_congvan.addItem(display_text, id_cv)
                
            # Load danh sách đơn vị
            for id_dv, ten_dv in self.lists.get('donvi', []):
                self.cb_donvi.addItem(ten_dv, id_dv)

        # Thêm các thành phần vào Form
        form_layout.addRow("Cán bộ nhận:", self.cb_canbo_nhan)
        form_layout.addRow("Công văn gốc:", self.cb_congvan)
        form_layout.addRow("Đơn vị chuyển:", self.cb_donvi)
        form_layout.addRow("Ngày chuyển:", self.date_chuyen)
        form_layout.addRow("Nội dung chỉ đạo:", self.txt_noidung)
        form_layout.addRow("Cán bộ chuyển:", self.cb_canbo_chuyen)

        # Chế độ Sửa: Tự động chọn đúng các mục cũ
        if self.data:
            self.cb_canbo_nhan.setCurrentIndex(self.cb_canbo_nhan.findData(self.data.get('CanBoId')))
            self.cb_congvan.setCurrentIndex(self.cb_congvan.findData(self.data.get('VanBanDenId')))
            self.cb_donvi.setCurrentIndex(self.cb_donvi.findData(self.data.get('DonViChuyenId')))
            self.cb_canbo_chuyen.setCurrentIndex(self.cb_canbo_chuyen.findData(self.data.get('CanBoChuyenId')))
            
            if self.data.get('NgayChuyen'):
                d = self.data['NgayChuyen']
                self.date_chuyen.setDate(QDate(d.year, d.month, d.day))
            
            self.txt_noidung.setPlainText(self.data.get('NoiDungYeuCau', ''))

        self.btn_save = QPushButton("💾 LƯU THÔNG TIN")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #28A745; color: white; border-radius: 5px;
                padding: 10px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background-color: #218838; }
        """)
        self.btn_save.clicked.connect(self.accept)

        layout.addLayout(form_layout)
        layout.addSpacing(10)
        layout.addWidget(self.btn_save)

    def get_values(self):
        """Lấy ID thực tế từ ComboBox để gửi về cho Controller"""
        return {
            'CanBoId': self.cb_canbo_nhan.currentData(),
            'VanBanDenId': self.cb_congvan.currentData(),
            'DonViChuyenId': self.cb_donvi.currentData(),
            'NgayChuyen': self.date_chuyen.date().toPyDate(),
            'NoiDungYeuCau': self.txt_noidung.toPlainText(),
            'CanBoChuyenId': self.cb_canbo_chuyen.currentData()
        }

# ==========================================================
# 2. VIEW CHÍNH: QUẢN LÝ XỬ LÝ CÔNG VĂN
# ==========================================================
class QuanLyXuLyCongVanView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget { background-color: #F4F6F9; font-family: 'Segoe UI', Arial; font-size: 13px; }
            QGroupBox { background-color: white; border: 1px solid #DFE4EA; border-radius: 8px; margin-top: 15px; }
            QGroupBox::title { subcontrol-origin: margin; padding: 5px 15px; color: #2C3E50; font-weight: bold; font-size: 16px; }
            QLineEdit { border: 1px solid #CED4DA; border-radius: 4px; padding: 6px; background: white; }
            QComboBox { border: 1px solid #CED4DA; border-radius: 4px; padding: 5px; background: white; min-height: 25px; }
            QTableWidget { background-color: white; border: 1px solid #DEE2E6; gridline-color: #F1F3F5; }
            QHeaderView::section { background-color: #F8F9FA; font-weight: bold; color: #495057; border: 1px solid #DEE2E6; padding: 10px; }
        """)

        layout_main = QVBoxLayout(self)
        self.group_box = QGroupBox("📁 HỆ THỐNG XỬ LÝ CÔNG VĂN ĐẾN")
        layout_group = QVBoxLayout(self.group_box)
        layout_group.setContentsMargins(20, 30, 20, 20)

        # Thanh công cụ
        layout_top = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Tìm theo nội dung yêu cầu, cán bộ...")
        self.txt_search.setFixedWidth(350)

        self.btn_search = QPushButton("Tìm kiếm")
        self.btn_search.setStyleSheet("background-color: #FFC107; font-weight: bold; padding: 6px 15px;")

        self.btn_refresh = QPushButton("↻ Làm mới")
        self.btn_refresh.setStyleSheet("background-color: #6C757D; color: white; padding: 6px 15px;")

        self.btn_add = QPushButton("+ Thêm phân công")
        self.btn_add.setStyleSheet("background-color: #28A745; color: white; font-weight: bold; padding: 6px 20px;")

        layout_top.addWidget(self.txt_search)
        layout_top.addWidget(self.btn_search)
        layout_top.addWidget(self.btn_refresh)
        layout_top.addStretch()
        layout_top.addWidget(self.btn_add)
        layout_group.addLayout(layout_top)

        # Bảng dữ liệu
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "STT", "Cán bộ nhận", "Công văn đến", "Đơn vị chuyển", 
            "Ngày chuyển", "Nội dung yêu cầu", "Cán bộ chuyển", "Thao tác"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch) 
        
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        layout_group.addWidget(self.table)
        layout_main.addWidget(self.group_box)

    def add_row_to_table(self, row_idx, data):
        ngay = data.get('NgayChuyen')
        str_ngay = ngay.strftime("%d/%m/%Y") if ngay else ""

        self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_idx + 1)))
        self.table.setItem(row_idx, 1, QTableWidgetItem(str(data.get('TenCanBoNhan') or "")))
        self.table.setItem(row_idx, 2, QTableWidgetItem(str(data.get('TieuDeCongVan') or "")))
        self.table.setItem(row_idx, 3, QTableWidgetItem(str(data.get('TenDonViChuyen') or "")))
        self.table.setItem(row_idx, 4, QTableWidgetItem(str_ngay))
        self.table.setItem(row_idx, 5, QTableWidgetItem(str(data.get('NoiDungYeuCau') or "")))
        self.table.setItem(row_idx, 6, QTableWidgetItem(str(data.get('TenCanBoChuyen') or "")))

        self.table.item(row_idx, 0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.item(row_idx, 4).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(5, 2, 5, 2)
        btn_layout.setSpacing(10)

        btn_edit = QPushButton("Sửa")
        btn_edit.setStyleSheet("background-color: #FFC107; border-radius: 3px; padding: 3px 8px; font-weight: bold;")

        btn_delete = QPushButton("Xóa")
        btn_delete.setStyleSheet("background-color: #DC3545; color: white; border-radius: 3px; padding: 3px 8px; font-weight: bold;")

        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        
        self.table.setCellWidget(row_idx, 7, btn_container)
        self.table.setRowHeight(row_idx, 40)

        return btn_edit, btn_delete