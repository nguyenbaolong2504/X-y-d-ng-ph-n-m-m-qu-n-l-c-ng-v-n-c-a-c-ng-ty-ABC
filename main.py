import sys, os, pyodbc
_original_pyodbc_connect = pyodbc.connect
def _intercept_connect(*args, **kwargs):
    # TRẢ VỀ LOCALHOST VÌ MÁY BẠN DÙNG TÊN NÀY MỚI CHẠY ĐƯỢC
    my_local_conn_str = ( 
        "DRIVER={ODBC Driver 17 for SQL Server};" 
        "SERVER=localhost\\SQLEXPRESS;" 
        "DATABASE=master;" 
        "Trusted_Connection=yes;" 
        )

    return _original_pyodbc_connect(my_local_conn_str)

pyodbc.connect = _intercept_connect

from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
sys.path.insert(0, os.getcwd())

# =====================================================================
# CHUỖI KẾT NỐI
# =====================================================================

CONN_STR = r""" 
DRIVER={ODBC Driver 17 for SQL Server}; 
SERVER=localhost; 
DATABASE=master; 
Trusted_Connection=yes; 
"""

# =====================================================================
# IMPORT SAFE
# =====================================================================

def safe_import(module_name, class_name):
    try:
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name), True
    except Exception as e:
        print(f"⚠️ Lỗi import {class_name}: {e}")
        return None, False

TrangChuView, TRANGCHU_OK = safe_import("View.trangchu", "TrangChuView")
TrangChuController, _ = safe_import("Controller.trangchu_controller", "TrangChuController")
from Model.congvan_model import CongVanModel
from View.quanlycongvanden import MainWindow as MainWindowDen
from Controller.congvan_controller import CongVanController
from Model.congvandi_model import CongVanDiModel
from View.quanlycongvandi import MainWindowDi
from Controller.congvandi_controller import CongVanDiController
from View.login import LoginWindow
from View.quanlyphanquyen import QuanLyPhanQuyen
from View.muclichoso import MucLucHoSo
from View.danhmuchoso import DanhMucHoSo
from View.quanlycongviec import QuanLyCongViec
ModelNoiBo, NOIBO_OK = safe_import("Model.model_noibo", "ModelNoiBo")
MainWindowNoiBo, _ = safe_import("View.view_noibo", "MainWindowNoiBo")
DonViModel, DV_OK = safe_import("Model.donvi_model", "DonViModel")
DonViWindow, _ = safe_import("View.quanlydonvi", "DonViWindow")
DonViController, _ = safe_import("Controller.donvi_controller", "DonViController")
ControllerNoiBo, _ = safe_import(
    "Controller.controller_noibo",
    "ControllerNoiBo"
)

CanBoModel, CANBO_OK = safe_import(
    "Model.canbo_model",
    "CanBoModel"
)

CanBoWindow, _ = safe_import(
    "View.quanlycanbo",
    "CanBoWindow"
)

CanBoController, _ = safe_import(
    "Controller.canbo_controller",
    "CanBoController"
)

ChucVuModel, CHUCVU_OK = safe_import(
    "Model.chucvu_model",
    "ChucVuModel"
)

ChucVuWindow, _ = safe_import(
    "View.quanlychucvu",
    "ChucVuWindow"
)

ChucVuController, _ = safe_import(
    "Controller.chucvu_controller",
    "ChucVuController"
)

HanBaoQuanModel, HBQ_OK = safe_import(
    "Model.hanbaoquan_model",
    "HanBaoQuanModel"
)

HanBaoQuanWindow, _ = safe_import(
    "View.quanlyhanbaoquan",
    "HanBaoQuanWindow"
)

HanBaoQuanController, _ = safe_import(
    "Controller.hanbaoquan_controller",
    "HanBaoQuanController"
)

# === ĐÃ SỬA: SỬ DỤNG LOAICONGVAN ===
LoaiCongVanModel, LCV_OK = safe_import(
    "Model.loaicongvan_model",
    "LoaiCongVanModel"
)

LoaiCongVanWindow, _ = safe_import(
    "View.quanlyloaicongvan",
    "LoaiCongVanWindow"
)

LoaiCongVanController, _ = safe_import(
    "Controller.loaicongvan_controller",
    "LoaiCongVanController"
)

# =====================================================================
# ĐƠN VỊ
# =====================================================================

DonViModel, DV_OK = safe_import(
    "Model.donvi_model",
    "DonViModel"
)

DonViWindow, _ = safe_import(
    "View.quanlydonvi",
    "DonViWindow"
)

DonViController, _ = safe_import(
    "Controller.donvi_controller",
    "DonViController"
)

# =====================================================================
# MAIN WINDOW
# =====================================================================

# --- THÊM MỚI: IMPORT MODULE XỬ LÝ CÔNG VĂN ---
XuLyCongVanModel, XULY_OK = safe_import("Model.xulycongvan_model", "XuLyCongVanModel")
QuanLyXuLyCongVanView, _ = safe_import("View.quanlyxulycongvan", "QuanLyXuLyCongVanView")
CongVanControllerCustom, _ = safe_import("Controller.xulycongvan_controller", "CongVanController")
from Utils.user_session import UserSession

class MainApp(QMainWindow):
    def __init__(self, user_session):
        super().__init__()
        self.user_session = user_session
        self.logout_requested = False          # THÊM DÒNG NÀY
        self.setWindowTitle("Hệ Thống Quản Lý Văn Bản - Công Ty ABC")
        self.setGeometry(100, 100, 1500, 850)
        self.setStyleSheet("QMainWindow { background-color: #ffffff; }")
        self.setup_ui()

    def logout(self):
        self.logout_requested = True
        self.close()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        
        # ================= HEADER =================
        header = QFrame()
        header.setFixedHeight(65)
        header.setStyleSheet("background-color: #0c2461; border: none;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15,0,20,0)
        
        lbl_logo = QLabel("📑")
        lbl_logo.setStyleSheet("font-size: 32px; color: white; background: white; padding: 5px; border-radius: 5px;")
        lbl_title_main = QLabel("HỆ THỐNG QUẢN LÝ CÔNG VĂN ABC")
        lbl_title_main.setStyleSheet("color: white; font-weight: bold; font-size: 18px;")
        lbl_title_sub = QLabel("Hệ thống quản lý văn bản, cán bộ chuyên nghiệp")
        lbl_title_sub.setStyleSheet("color: #dcdde1; font-size: 12px;")
        title_layout = QVBoxLayout()
        title_layout.addWidget(lbl_title_main)
        title_layout.addWidget(lbl_title_sub)
        
        # Thay vì "Administrator", hiển thị tên người dùng + nút đăng xuất
        user_widget = QWidget()
        user_layout = QHBoxLayout(user_widget)
        user_layout.setContentsMargins(0, 0, 0, 0)
        user_layout.setSpacing(10)

        hoten = self.user_session.get_hoten() if hasattr(self.user_session, 'get_hoten') else "Người dùng"
        lbl_user = QLabel(f"{hoten} 🧑‍💼")
        lbl_user.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")

        btn_logout = QPushButton("Đăng xuất")
        btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self.logout)

        user_layout.addWidget(lbl_user)
        user_layout.addWidget(btn_logout)

        header_layout.addWidget(lbl_logo)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(user_widget)
        main_layout.addWidget(header)
        
        # ================= BODY =================
        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(0,0,0,0)
        body_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(240)
        self.sidebar.setStyleSheet("""
            QListWidget { background-color: #f4f5f7; border-right: 1px solid #dcdde1; outline: none; }
            QListWidget::item { height: 50px; padding-left: 10px; border-bottom: 1px solid #e1e2e6; color: #2f3640; font-size: 14px; }
            QListWidget::item:selected { background-color: #ffffff; color: #0c2461; font-weight: bold; border-left: 4px solid #e67e22; }
        """)
        self.sidebar.addItem(QListWidgetItem(" ☰ "))
        menu_items = [
            "🏠 Tổng quan hệ thống",
            "📥 Văn bản đến",
            "📤 Văn bản đi",
            "📄 Văn bản nội bộ",
            "📥 Văn bản nội bộ của tôi",   # Thêm dòng này
            "👥 Danh sách cán bộ",
            "📂 Danh mục chức vụ",
            "⏳ Thời hạn bảo quản",
            "🏷️ Loại công văn",
            "🏢 Đơn vị, bộ phận",
            "⚙️ Xử lý công văn",
            "🔐 Phân quyền sử dụng",
            "🗂️ Mục lục hồ sơ",
            "📁 Danh mục hồ sơ",
            "✅ Công việc"
        ]
        for text in menu_items:
            self.sidebar.addItem(QListWidgetItem(text))
        
        self.stacked_widget = QStackedWidget()
        self.setup_pages()
        self.sidebar.currentRowChanged.connect(self.change_page)
        self.sidebar.setCurrentRow(1)
        
        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(body_widget)

    def setup_pages(self):
        if TRANGCHU_OK:
            self.tab_home = TrangChuView()
            self.home_controller = TrangChuController(self.tab_home, self.user_session)
            self.stacked_widget.addWidget(self.tab_home)
        else:
            self.stacked_widget.addWidget(QLabel("Trang chủ chưa sẵn sàng"))
        
        self.tab_den = MainWindowDen()
        self.den_controller = CongVanController(CongVanModel(), self.tab_den, self.user_session)
        self.stacked_widget.addWidget(self.tab_den)
        
        self.tab_di = MainWindowDi()
        self.di_controller = CongVanDiController(CongVanDiModel(), self.tab_di, self.user_session)
        self.stacked_widget.addWidget(self.tab_di)
        
        if NOIBO_OK:
            self.tab_noibo = MainWindowNoiBo()
            self.noibo_controller = ControllerNoiBo(ModelNoiBo(), self.tab_noibo)
            self.stacked_widget.addWidget(self.tab_noibo)
        else:
            self.stacked_widget.addWidget(QLabel("Nội bộ chưa sẵn sàng"))
        
        if CANBO_OK:
            try:
                self.tab_canbo = CanBoWindow()
                model = CanBoModel()
                model.conn_str = CONN_STR
                self.canbo_controller = CanBoController(model, self.tab_canbo)
                self.stacked_widget.addWidget(self.tab_canbo)
            except Exception as e:
                self.stacked_widget.addWidget(QLabel(f"❌ Lỗi cán bộ: {str(e)}"))
        else:
            self.stacked_widget.addWidget(QLabel("Module cán bộ chưa sẵn sàng"))
        
        if CHUCVU_OK:
            try:
                self.tab_chucvu = ChucVuWindow()
                cv_model = ChucVuModel(CONN_STR)
                self.chucvu_controller = ChucVuController(cv_model, self.tab_chucvu)
                self.stacked_widget.addWidget(self.tab_chucvu)
            except Exception as e:
                self.stacked_widget.addWidget(QLabel(f"❌ Lỗi chức vụ: {str(e)}"))
        else:
            self.stacked_widget.addWidget(QLabel("Module chức vụ chưa sẵn sàng"))
        
        if HBQ_OK:
            try:
                self.tab_hbq = HanBaoQuanWindow()
                hbq_model = HanBaoQuanModel(CONN_STR)
                self.hbq_controller = HanBaoQuanController(hbq_model, self.tab_hbq)
                self.stacked_widget.addWidget(self.tab_hbq)
            except Exception as e:
                self.stacked_widget.addWidget(QLabel(f"❌ Lỗi HBQ: {str(e)}"))
        else:
            self.stacked_widget.addWidget(
                QLabel("Module HBQ chưa sẵn sàng")
            )

        # =============================================================
        # 7. LOẠI CÔNG VĂN (ĐÃ FIX THEO CODE MỚI)
        # =============================================================

        if LCV_OK:
            try:
                self.tab_lvb = LoaiCongVanWindow()
                self.ctrl_lvb = LoaiCongVanController(
                    LoaiCongVanModel(CONN_STR),
                    self.tab_lvb.view_den,
                    self.tab_lvb.view_di
                )
                self.stacked_widget.addWidget(self.tab_lvb)
            except Exception as e:
                self.stacked_widget.addWidget(QLabel(f"❌ Lỗi Loại công văn: {str(e)}"))
        else:
            self.stacked_widget.addWidget(QLabel("Module Loại công văn chưa sẵn sàng"))

        # =============================================================
        # 8. ĐƠN VỊ
        # =============================================================

        if DV_OK:
            try:
                self.tab_dv = DonViWindow()
                dv_model = DonViModel(CONN_STR)
                self.dv_controller = DonViController(dv_model, self.tab_dv)
                self.stacked_widget.addWidget(self.tab_dv)
            except Exception as e:
                self.stacked_widget.addWidget(QLabel(f"❌ Lỗi đơn vị: {str(e)}"))
        else:
            self.stacked_widget.addWidget(QLabel("Module đơn vị chưa sẵn sàng"))
        
        if XULY_OK:
            try:
                self.tab_xuly = QuanLyXuLyCongVanView()
                db_conn = pyodbc.connect(CONN_STR)
                xl_model = XuLyCongVanModel(db_conn)
                self.xuly_controller = CongVanControllerCustom(self.tab_xuly, xl_model)
                self.stacked_widget.addWidget(self.tab_xuly)
            except Exception as e:
                self.stacked_widget.addWidget(QLabel(f"❌ Lỗi module Xử lý công văn: {str(e)}"))
        else:
            self.stacked_widget.addWidget(QLabel("Module Xử lý công văn chưa sẵn sàng"))

        # =============================================================
        # 10. PHÂN QUYỀN
        # =============================================================

        try:
            self.tab_phanquyen = QuanLyPhanQuyen()
            self.stacked_widget.addWidget(self.tab_phanquyen)
        except Exception as e:
            self.stacked_widget.addWidget(
                QLabel(f"❌ Lỗi phân quyền: {str(e)}")
            )

        # =============================================================
        # 11. MỤC LỤC HỒ SƠ
        # =============================================================

        try:
            self.tab_muclichoso = MucLucHoSo()
            self.stacked_widget.addWidget(self.tab_muclichoso)
        except Exception as e:
            self.stacked_widget.addWidget(
                QLabel(f"❌ Lỗi mục lục hồ sơ: {str(e)}")
            )

        # =============================================================
        # 12. DANH MỤC HỒ SƠ
        # =============================================================

        try:
            self.tab_danhmuchoso = DanhMucHoSo()
            self.stacked_widget.addWidget(self.tab_danhmuchoso)
        except Exception as e:
            self.stacked_widget.addWidget(
                QLabel(f"❌ Lỗi danh mục hồ sơ: {str(e)}")
            )

        # =============================================================
        # 13. CÔNG VIỆC
        # =============================================================

        try:
            self.tab_congviec = QuanLyCongViec(self.user_session, CONN_STR)
            self.stacked_widget.addWidget(self.tab_congviec)
        except Exception as e:
            self.stacked_widget.addWidget(QLabel(f"❌ Lỗi công việc: {str(e)}"))

        # =============================================================
        # 14. VĂN BẢN NỘI BỘ CỦA TÔI (DÀNH CHO NGƯỜI NHẬN)
        # =============================================================
        try:
            from View.view_noibo_nhan import NoiBoNhanWidget
            from Controller.controller_noibo_nhan import ControllerNoiBoNhan
            self.tab_noibo_nhan = NoiBoNhanWidget(self.user_session, CONN_STR, ModelNoiBo())
            self.noibo_nhan_controller = ControllerNoiBoNhan(ModelNoiBo(), self.tab_noibo_nhan, self.user_session)
            self.stacked_widget.addWidget(self.tab_noibo_nhan)
        except Exception as e:
            self.stacked_widget.addWidget(QLabel(f"❌ Lỗi văn bản nội bộ của tôi: {str(e)}"))

    def change_page(self, index):
        if index > 0:
            # Map chỉ mục sidebar sang chỉ mục stacked_widget
            # Danh sách các tab theo thứ tự stacked_widget:
            # 0: Trang chủ
            # 1: Văn bản đến
            # 2: Văn bản đi
            # 3: Văn bản nội bộ (quản lý)
            # 4: Danh sách cán bộ
            # 5: Danh mục chức vụ
            # 6: Thời hạn bảo quản
            # 7: Loại công văn
            # 8: Đơn vị, bộ phận
            # 9: Xử lý công văn
            # 10: Phân quyền sử dụng
            # 11: Mục lục hồ sơ
            # 12: Danh mục hồ sơ
            # 13: Công việc
            # 14: Văn bản nội bộ của tôi
            #
            # Sidebar index (bắt đầu từ 1, vì index 0 là " ☰ "):
            # 1: Tổng quan hệ thống -> stacked 0
            # 2: Văn bản đến -> stacked 1
            # 3: Văn bản đi -> stacked 2
            # 4: Văn bản nội bộ -> stacked 3
            # 5: Văn bản nội bộ của tôi -> stacked 14
            # 6: Danh sách cán bộ -> stacked 4
            # 7: Danh mục chức vụ -> stacked 5
            # 8: Thời hạn bảo quản -> stacked 6
            # 9: Loại công văn -> stacked 7
            # 10: Đơn vị, bộ phận -> stacked 8
            # 11: Xử lý công văn -> stacked 9
            # 12: Phân quyền sử dụng -> stacked 10
            # 13: Mục lục hồ sơ -> stacked 11
            # 14: Danh mục hồ sơ -> stacked 12
            # 15: Công việc -> stacked 13
            mapping = {
                1: 0,   # Tổng quan
                2: 1,   # Văn bản đến
                3: 2,   # Văn bản đi
                4: 3,   # Văn bản nội bộ (quản lý)
                5: 14,  # Văn bản nội bộ của tôi
                6: 4,   # Danh sách cán bộ
                7: 5,   # Danh mục chức vụ
                8: 6,   # Thời hạn bảo quản
                9: 7,   # Loại công văn
                10: 8,  # Đơn vị, bộ phận
                11: 9,  # Xử lý công văn
                12: 10, # Phân quyền sử dụng
                13: 11, # Mục lục hồ sơ
                14: 12, # Danh mục hồ sơ
                15: 13, # Công việc
            }
            stacked_idx = mapping.get(index)
            if stacked_idx is not None:
                self.stacked_widget.setCurrentIndex(stacked_idx)
            if index == 1 and hasattr(self, 'home_controller'):
                self.home_controller.load_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))

    while True:
        login = LoginWindow()
        login.show()
        app.exec()

        session = UserSession()
        if not session.user_id:
            break

        window = MainApp(session)
        window.show()
        app.exec()

        if window.logout_requested:
            continue
        else:
            break

    sys.exit()