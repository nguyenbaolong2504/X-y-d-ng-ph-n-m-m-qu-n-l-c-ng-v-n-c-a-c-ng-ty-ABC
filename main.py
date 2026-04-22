import sys
import os
# Thêm QMessageBox vào danh sách import
from PyQt6.QtWidgets import (QApplication, QLabel, QMainWindow, QWidget, 
                             QVBoxLayout, QHBoxLayout, QListWidget, QStackedWidget, 
                             QListWidgetItem, QFrame, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

sys.path.insert(0, os.getcwd())

# === THIẾT LẬP CHUỖI KẾT NỐI SQL SERVER DÙNG CHUNG ===
# Đã thêm chữ 'r' để sửa lỗi "\S"
CONN_STR = r"DRIVER={SQL Server};SERVER=.\SQLEXPRESS;DATABASE=congtyadc;Trusted_Connection=yes;"

# === Import các module với cơ chế kiểm tra an toàn ===
def safe_import(module_name, class_name):
    try:
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name), True
    except Exception as e:
        print(f"⚠️ Lỗi import {class_name}: {e}")
        return None, False

# Import các thành phần hệ thống
TrangChuView, TRANGCHU_OK = safe_import("View.trangchu", "TrangChuView")
TrangChuController, _ = safe_import("Controller.trangchu_controller", "TrangChuController")

from Model.congvan_model import CongVanModel
from View.quanlycongvanden import MainWindow as MainWindowDen
from Controller.congvan_controller import CongVanController

from Model.congvandi_model import CongVanDiModel
from View.quanlycongvandi import MainWindowDi
from Controller.congvandi_controller import CongVanDiController

ModelNoiBo, NOIBO_OK = safe_import("Model.model_noibo", "ModelNoiBo")
MainWindowNoiBo, _ = safe_import("View.view_noibo", "MainWindowNoiBo")
ControllerNoiBo, _ = safe_import("Controller.controller_noibo", "ControllerNoiBo")

CanBoModel, CANBO_OK = safe_import("Model.canbo_model", "CanBoModel")
CanBoWindow, _ = safe_import("View.quanlycanbo", "CanBoWindow")
CanBoController, _ = safe_import("Controller.canbo_controller", "CanBoController")

ChucVuModel, CHUCVU_OK = safe_import("Model.chucvu_model", "ChucVuModel")
ChucVuWindow, _ = safe_import("View.quanlychucvu", "ChucVuWindow")
ChucVuController, _ = safe_import("Controller.chucvu_controller", "ChucVuController")

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ Thống Quản Lý Văn Bản - Công Ty ABC")
        self.setGeometry(100, 100, 1500, 850)
        self.setStyleSheet("QMainWindow { background-color: #ffffff; }")
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. HEADER
        header = QFrame()
        header.setFixedHeight(65)
        header.setStyleSheet("background-color: #0c2461; border: none;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 0, 20, 0)
            
        lbl_logo = QLabel("📑")
        lbl_logo.setStyleSheet("font-size: 32px; color: white; background: white; padding: 5px; border-radius: 5px;")
        
        lbl_title_main = QLabel("HỆ THỐNG QUẢN LÝ CÔNG VĂN ABC")
        lbl_title_main.setStyleSheet("color: white; font-weight: bold; font-size: 18px;")
        lbl_title_sub = QLabel("Hệ thống quản lý văn bản, cán bộ chuyên nghiệp")
        lbl_title_sub.setStyleSheet("color: #dcdde1; font-size: 12px;")
        
        title_layout = QVBoxLayout()
        title_layout.addWidget(lbl_title_main)
        title_layout.addWidget(lbl_title_sub)
        
        lbl_admin = QLabel("Administrator 🧑‍💼")
        lbl_admin.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        
        header_layout.addWidget(lbl_logo)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(lbl_admin)
        main_layout.addWidget(header)

        # 2. BODY
        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # --- SIDEBAR ---
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(240)
        self.sidebar.setStyleSheet("""
            QListWidget { background-color: #f4f5f7; border-right: 1px solid #dcdde1; outline: none; }
            QListWidget::item { height: 50px; padding-left: 10px; border-bottom: 1px solid #e1e2e6; color: #2f3640; font-size: 14px; }
            QListWidget::item:selected { background-color: #ffffff; color: #0c2461; font-weight: bold; border-left: 4px solid #e67e22; }
        """)

        hamburger_item = QListWidgetItem(" ☰ ")
        hamburger_item.setFlags(Qt.ItemFlag.NoItemFlags) 
        self.sidebar.addItem(hamburger_item)

        menu_items = ["🏠 Tổng quan hệ thống", "📥 Văn bản đến", "📤 Văn bản đi", "📄 Văn bản nội bộ", "👥 Danh sách cán bộ", "📂 Danh mục chức vụ"]
        for text in menu_items:
            self.sidebar.addItem(QListWidgetItem(text))

        # --- QSTACKEDWIDGET ---
        self.stacked_widget = QStackedWidget()
        self.setup_pages()
        
        self.sidebar.currentRowChanged.connect(self.change_page)
        self.sidebar.setCurrentRow(1)

        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(body_widget)

    def setup_pages(self):
        # 0. Trang chủ
        if TRANGCHU_OK:
            self.tab_home = TrangChuView()
            self.home_controller = TrangChuController(self.tab_home)
            self.stacked_widget.addWidget(self.tab_home)
        else:
            self.stacked_widget.addWidget(QLabel("Trang chủ chưa sẵn sàng"))

        # 1. Công văn đến
        self.tab_den = MainWindowDen()
        self.stacked_widget.addWidget(self.tab_den)

        # 2. Công văn đi
        self.tab_di = MainWindowDi()
        self.stacked_widget.addWidget(self.tab_di)

        # 3. Công văn nội bộ
        if NOIBO_OK:
            self.tab_noibo = MainWindowNoiBo()
            self.stacked_widget.addWidget(self.tab_noibo)
        else:
            self.stacked_widget.addWidget(QLabel("Nội bộ chưa sẵn sàng"))

        # 4. Danh sách cán bộ
        if CANBO_OK:
            try:
                self.tab_canbo = CanBoWindow()
                model = CanBoModel()
                model.conn_str = CONN_STR
                self.canbo_controller = CanBoController(model, self.tab_canbo)
                self.stacked_widget.addWidget(self.tab_canbo)
            except Exception as e:
                self.stacked_widget.addWidget(QLabel(f"❌ Lỗi nạp dữ liệu Cán bộ: {str(e)}"))
        else:
            self.stacked_widget.addWidget(QLabel("Module Cán bộ chưa sẵn sàng"))

        # 5. Danh mục chức vụ
        if CHUCVU_OK:
            try:
                self.tab_chucvu = ChucVuWindow()
                cv_model = ChucVuModel(CONN_STR)
                self.chucvu_controller = ChucVuController(cv_model, self.tab_chucvu)
                self.stacked_widget.addWidget(self.tab_chucvu)
            except Exception as e:
                self.stacked_widget.addWidget(QLabel(f"❌ Lỗi module Chức vụ: {str(e)}"))
        else:
            self.stacked_widget.addWidget(QLabel("Module Chức vụ chưa sẵn sàng"))

        # Khởi tạo các Controller
        try:
            self.den_controller = CongVanController(CongVanModel(), self.tab_den)
            self.di_controller = CongVanDiController(CongVanDiModel(), self.tab_di)
            if NOIBO_OK:
                self.noibo_controller = ControllerNoiBo(ModelNoiBo(), self.tab_noibo)
            
            # --- ĐÃ SỬA: KẾT NỐI THÔNG QUA TAB_DEN ---
            # Chỉ kết nối nếu nút tồn tại trong tab_den
            if hasattr(self.tab_den, 'btn_refresh'):
                self.tab_den.btn_refresh.clicked.connect(self.tab_den.nap_dulieu_signal.emit)
            
            if hasattr(self.tab_den, 'btn_in'):
                self.tab_den.btn_in.clicked.connect(self.tab_den.print_table)
                
        except Exception as e:
            print(f"Lưu ý kết nối controller: {e}")

    def change_page(self, index):
        if index > 0:
            self.stacked_widget.setCurrentIndex(index - 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = MainApp()
    window.show()
    sys.exit(app.exec())