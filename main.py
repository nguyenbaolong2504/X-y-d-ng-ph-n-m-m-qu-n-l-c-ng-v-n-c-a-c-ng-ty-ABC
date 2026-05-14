import sys
import os
import pyodbc

# =====================================================================
# THỦ THUẬT MONKEY PATCHING
# =====================================================================

_original_pyodbc_connect = pyodbc.connect

def _intercept_connect(*args, **kwargs):

    my_local_conn_str = ( 
        "DRIVER={SQL Server};" 
        "SERVER=.\\SQLEXPRESS;" 
        "DATABASE=congtyadc;" 
        "Trusted_Connection=yes;" 
        )

    return _original_pyodbc_connect(my_local_conn_str)

pyodbc.connect = _intercept_connect

# =====================================================================

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QStackedWidget,
    QListWidgetItem,
    QFrame,
    QMessageBox, 
    QPushButton
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

sys.path.insert(0, os.getcwd())

# =====================================================================
# CHUỖI KẾT NỐI
# =====================================================================

CONN_STR = r""" 
DRIVER={SQL Server}; 
SERVER=.\SQLEXPRESS; 
DATABASE=congtyadc; 
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

# =====================================================================
# IMPORT HỆ THỐNG
# =====================================================================

TrangChuView, TRANGCHU_OK = safe_import(
    "View.trangchu",
    "TrangChuView"
)

TrangChuController, _ = safe_import(
    "Controller.trangchu_controller",
    "TrangChuController"
)

from Model.congvan_model import CongVanModel
from View.quanlycongvanden import MainWindow as MainWindowDen
from Controller.congvan_controller import CongVanController

from Model.congvandi_model import CongVanDiModel
from View.quanlycongvandi import MainWindowDi
from Controller.congvandi_controller import CongVanDiController

# =====================================================================
# MODULE MỚI
# =====================================================================

from View.login import LoginWindow
from View.quanlyphanquyen import QuanLyPhanQuyen
from View.muclichoso import MucLucHoSo
from View.danhmuchoso import DanhMucHoSo
from View.quanlycongviec import QuanLyCongViec

# =====================================================================

ModelNoiBo, NOIBO_OK = safe_import(
    "Model.model_noibo",
    "ModelNoiBo"
)

MainWindowNoiBo, _ = safe_import(
    "View.view_noibo",
    "MainWindowNoiBo"
)


# --- IMPORT MODULE ĐƠN VỊ ---
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

LoaiVanBanModel, LVB_OK = safe_import(
    "Model.loaivanban_model",
    "LoaiVanBanModel"
)

LoaiVanBanWindow, _ = safe_import(
    "View.quanlyloaivanban",
    "LoaiVanBanWindow"
)

LoaiVanBanController, _ = safe_import(
    "Controller.loaivanban_controller",
    "LoaiVanBanController"
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


class MainApp(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Hệ Thống Quản Lý Văn Bản - Công Ty ABC"
        )

        self.setGeometry(100, 100, 1500, 850)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
        """)

        self.setup_ui()

    # =================================================================

    def setup_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        main_layout.setContentsMargins(0,0,0,0)

        main_layout.setSpacing(0)

        # =============================================================
        # HEADER
        # =============================================================

        header = QFrame()

        header.setFixedHeight(65)

        header.setStyleSheet("""
            background-color: #0c2461;
            border: none;
        """)

        header_layout = QHBoxLayout(header)

        header_layout.setContentsMargins(15,0,20,0)

        lbl_logo = QLabel("📑")

        lbl_logo.setStyleSheet("""
            font-size: 32px;
            color: white;
            background: white;
            padding: 5px;
            border-radius: 5px;
        """)

        lbl_title_main = QLabel(
            "HỆ THỐNG QUẢN LÝ CÔNG VĂN ABC"
        )

        lbl_title_main.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 18px;
        """)

        lbl_title_sub = QLabel(
            "Hệ thống quản lý văn bản, cán bộ chuyên nghiệp"
        )

        lbl_title_sub.setStyleSheet("""
            color: #dcdde1;
            font-size: 12px;
        """)

        title_layout = QVBoxLayout()

        title_layout.addWidget(lbl_title_main)
        title_layout.addWidget(lbl_title_sub)

        lbl_admin = QLabel("Administrator 🧑‍💼")

        lbl_admin.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 14px;
        """)

        header_layout.addWidget(lbl_logo)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(lbl_admin)

        main_layout.addWidget(header)

        # =============================================================
        # BODY
        # =============================================================

        body_widget = QWidget()

        body_layout = QHBoxLayout(body_widget)

        body_layout.setContentsMargins(0,0,0,0)

        body_layout.setSpacing(0)

        # =============================================================
        # SIDEBAR
        # =============================================================

        self.sidebar = QListWidget()

        self.sidebar.setFixedWidth(240)

        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #f4f5f7;
                border-right: 1px solid #dcdde1;
                outline: none;
            }

            QListWidget::item {
                height: 50px;
                padding-left: 10px;
                border-bottom: 1px solid #e1e2e6;
                color: #2f3640;
                font-size: 14px;
            }

            QListWidget::item:selected {
                background-color: #ffffff;
                color: #0c2461;
                font-weight: bold;
                border-left: 4px solid #e67e22;
            }
        """)

        hamburger_item = QListWidgetItem(" ☰ ")

        hamburger_item.setFlags(Qt.ItemFlag.NoItemFlags)

        self.sidebar.addItem(hamburger_item)

        # =============================================================
        # MENU
        # =============================================================

        menu_items = [

            "🏠 Tổng quan hệ thống",

            "📥 Văn bản đến",
            "📤 Văn bản đi",
            "📄 Văn bản nội bộ",

            "👥 Danh sách cán bộ",
            "📂 Danh mục chức vụ",
            "⏳ Thời hạn bảo quản",
            "🏷️ Loại văn bản",
            "🏢 Đơn vị, bộ phận",
            "⚙️ Xử lý công văn",

            "🔐 Phân quyền sử dụng",
            "🗂️ Mục lục hồ sơ",
            "📁 Danh mục hồ sơ",
            "✅ Công việc"
        ]

        for text in menu_items:
            self.sidebar.addItem(QListWidgetItem(text))

        # =============================================================
        # STACKED WIDGET
        # =============================================================

        self.stacked_widget = QStackedWidget()

        self.setup_pages()

        self.sidebar.currentRowChanged.connect(
            self.change_page
        )

        self.sidebar.setCurrentRow(1)

        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.stacked_widget)

        main_layout.addWidget(body_widget)

    # =================================================================

    def setup_pages(self):

        # =============================================================
        # 0. TRANG CHỦ
        # =============================================================

        if TRANGCHU_OK:

            self.tab_home = TrangChuView()

            self.home_controller = TrangChuController(
                self.tab_home
            )

            self.stacked_widget.addWidget(self.tab_home)

        else:

            self.stacked_widget.addWidget(
                QLabel("Trang chủ chưa sẵn sàng")
            )

        # =============================================================
        # 1. CÔNG VĂN ĐẾN
        # =============================================================

        self.tab_den = MainWindowDen()

        self.stacked_widget.addWidget(self.tab_den)

        # =============================================================
        # 2. CÔNG VĂN ĐI
        # =============================================================

        self.tab_di = MainWindowDi()

        self.stacked_widget.addWidget(self.tab_di)

        # =============================================================
        # 3. NỘI BỘ
        # =============================================================

        if NOIBO_OK:

            self.tab_noibo = MainWindowNoiBo()

            self.stacked_widget.addWidget(self.tab_noibo)

        else:

            self.stacked_widget.addWidget(
                QLabel("Nội bộ chưa sẵn sàng")
            )

        # =============================================================
        # 4. CÁN BỘ
        # =============================================================

        if CANBO_OK:

            try:

                self.tab_canbo = CanBoWindow()

                model = CanBoModel()

                model.conn_str = CONN_STR

                self.canbo_controller = CanBoController(
                    model,
                    self.tab_canbo
                )

                self.stacked_widget.addWidget(
                    self.tab_canbo
                )

            except Exception as e:

                self.stacked_widget.addWidget(
                    QLabel(f"❌ Lỗi cán bộ: {str(e)}")
                )

        else:

            self.stacked_widget.addWidget(
                QLabel("Module cán bộ chưa sẵn sàng")
            )

        # =============================================================
        # 5. CHỨC VỤ
        # =============================================================

        if CHUCVU_OK:

            try:

                self.tab_chucvu = ChucVuWindow()

                cv_model = ChucVuModel(CONN_STR)

                self.chucvu_controller = ChucVuController(
                    cv_model,
                    self.tab_chucvu
                )

                self.stacked_widget.addWidget(
                    self.tab_chucvu
                )

            except Exception as e:

                self.stacked_widget.addWidget(
                    QLabel(f"❌ Lỗi chức vụ: {str(e)}")
                )

        else:

            self.stacked_widget.addWidget(
                QLabel("Module chức vụ chưa sẵn sàng")
            )

        # =============================================================
        # 6. THỜI HẠN BẢO QUẢN
        # =============================================================

        if HBQ_OK:

            try:

                self.tab_hbq = HanBaoQuanWindow()

                hbq_model = HanBaoQuanModel(CONN_STR)

                self.hbq_controller = HanBaoQuanController(
                    hbq_model,
                    self.tab_hbq
                )

                self.stacked_widget.addWidget(
                    self.tab_hbq
                )

            except Exception as e:

                self.stacked_widget.addWidget(
                    QLabel(f"❌ Lỗi HBQ: {str(e)}")
                )

        else:

            self.stacked_widget.addWidget(
                QLabel("Module HBQ chưa sẵn sàng")
            )

        # =============================================================
        # 7. LOẠI VĂN BẢN
        # =============================================================

        if LVB_OK:

            try:

                self.tab_lvb = LoaiVanBanWindow()

                self.ctrl_lvb_den = LoaiVanBanController(
                    LoaiVanBanModel(
                        CONN_STR,
                        "PhanLoaiCongVanDen"
                    ),
                    self.tab_lvb.view_den
                )

                self.ctrl_lvb_di = LoaiVanBanController(
                    LoaiVanBanModel(
                        CONN_STR,
                        "PhanLoaiCongVanPhatHanh"
                    ),
                    self.tab_lvb.view_di
                )

        # 8. Danh mục Đơn vị, bộ phận
                self.stacked_widget.addWidget(
                    self.tab_lvb
                )

            except Exception as e:

                self.stacked_widget.addWidget(
                    QLabel(f"❌ Lỗi loại văn bản: {str(e)}")
                )

        # =============================================================
        # 8. ĐƠN VỊ
        # =============================================================

        if DV_OK:
            try:
                self.tab_dv = DonViWindow()

                dv_model = DonViModel(CONN_STR)

                self.dv_controller = DonViController(
                    dv_model,
                    self.tab_dv
                )

                self.stacked_widget.addWidget(
                    self.tab_dv
                )

            except Exception as e:

                self.stacked_widget.addWidget(
                    QLabel(f"❌ Lỗi đơn vị: {str(e)}")
                )

        else:

            self.stacked_widget.addWidget(
                QLabel("Module đơn vị chưa sẵn sàng")
            )

        # --- THÊM MỚI: 9. Xử lý công văn ---
        if XULY_OK:
            try:
                self.tab_xuly = QuanLyXuLyCongVanView()
                # Khởi tạo kết nối db để truyền vào Model theo đúng code hôm qua
                db_conn = pyodbc.connect(CONN_STR)
                xl_model = XuLyCongVanModel(db_conn)
                self.xuly_controller = CongVanControllerCustom(self.tab_xuly, xl_model)
                self.stacked_widget.addWidget(self.tab_xuly)
            except Exception as e:
                self.stacked_widget.addWidget(QLabel(f"❌ Lỗi module Xử lý công văn: {str(e)}"))
        else:
            self.stacked_widget.addWidget(QLabel("Module Xử lý công văn chưa sẵn sàng"))

        # =============================================================
        # 9. PHÂN QUYỀN
        # =============================================================

        try:

            self.tab_phanquyen = QuanLyPhanQuyen()

            self.stacked_widget.addWidget(
                self.tab_phanquyen
            )

        except Exception as e:

            self.stacked_widget.addWidget(
                QLabel(f"❌ Lỗi phân quyền: {str(e)}")
            )

        # =============================================================
        # 10. MỤC LỤC HỒ SƠ
        # =============================================================

        try:

            self.tab_muclichoso = MucLucHoSo()

            self.stacked_widget.addWidget(
                self.tab_muclichoso
            )

        except Exception as e:

            self.stacked_widget.addWidget(
                QLabel(f"❌ Lỗi mục lục hồ sơ: {str(e)}")
            )

        # =============================================================
        # 11. DANH MỤC HỒ SƠ
        # =============================================================

        try:

            self.tab_danhmuchoso = DanhMucHoSo()

            self.stacked_widget.addWidget(
                self.tab_danhmuchoso
            )

        except Exception as e:

            self.stacked_widget.addWidget(
                QLabel(f"❌ Lỗi danh mục hồ sơ: {str(e)}")
            )

        # =============================================================
        # 12. CÔNG VIỆC
        # =============================================================

        try:

            self.tab_congviec = QuanLyCongViec()

            self.stacked_widget.addWidget(
                self.tab_congviec
            )

        except Exception as e:

            self.stacked_widget.addWidget(
                QLabel(f"❌ Lỗi công việc: {str(e)}")
            )

        # =============================================================
        # CONTROLLER
        # =============================================================

        try:

            self.den_controller = CongVanController(
                CongVanModel(),
                self.tab_den
            )

            self.di_controller = CongVanDiController(
                CongVanDiModel(),
                self.tab_di
            )

            if NOIBO_OK:

                self.noibo_controller = ControllerNoiBo(
                    ModelNoiBo(),
                    self.tab_noibo
                )

            if hasattr(self.tab_den, 'btn_refresh'):

                self.tab_den.btn_refresh.clicked.connect(
                    self.tab_den.nap_dulieu_signal.emit
                )

            if hasattr(self.tab_den, 'btn_in'):

                self.tab_den.btn_in.clicked.connect(
                    self.tab_den.print_table
                )

        except Exception as e:

            print(f"Lưu ý controller: {e}")

    # =================================================================

    def change_page(self, index):

        if index > 0:

            self.stacked_widget.setCurrentIndex(index - 1)


# =====================================================================
# RUN APP
# =====================================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setFont(QFont("Segoe UI", 10))

    # =============================================================
    # LOGIN
    # =============================================================

    login = LoginWindow()

    login.show()

    app.exec()

    # =============================================================
    # CHƯA LOGIN
    # =============================================================

    if not hasattr(login, "vaitro"):

        sys.exit()

    vaitro = login.vaitro

    # =============================================================
    # MAIN WINDOW
    # =============================================================

    window = MainApp()

    # =============================================================
    # ADMIN
    # =============================================================

    if vaitro == "Admin": 
        pass


    # =============================================================
    # GIÁM ĐỐC
    # =============================================================

    elif vaitro == "GiamDoc":

        window.setWindowTitle(
            "HỆ THỐNG QUẢN LÝ VĂN BẢN - GIÁM ĐỐC"
        )

        try:
            window.sidebar.item(10).setHidden(True)
        except:
            pass

    # =============================================================
    # TRƯỞNG PHÒNG
    # =============================================================

    elif vaitro == "TruongPhong":

        window.setWindowTitle(
            "HỆ THỐNG QUẢN LÝ VĂN BẢN - TRƯỞNG PHÒNG"
        )

        try:
            window.sidebar.item(10).setHidden(True)
        except:
            pass

        try:
            window.sidebar.item(5).setHidden(True)
        except:
            pass

        try:
            window.sidebar.item(6).setHidden(True)
        except:
            pass

        try:
            window.sidebar.item(7).setHidden(True)
        except:
            pass

        try:
            window.sidebar.item(8).setHidden(True)
        except:
            pass

    # =============================================================
    # NHÂN VIÊN
    # =============================================================

    elif vaitro == "NhanVien":

        window.setWindowTitle(
            "HỆ THỐNG QUẢN LÝ VĂN BẢN - NHÂN VIÊN"
        )

        try:
            window.sidebar.item(4).setHidden(True)
        except:
            pass

        try:
            window.sidebar.item(5).setHidden(True)
        except:
            pass

        try:
            window.sidebar.item(6).setHidden(True)
        except:
            pass

        try:
            window.sidebar.item(7).setHidden(True)
        except:
            pass

        try:
            window.sidebar.item(8).setHidden(True)
        except:
            pass

        try:
            window.sidebar.item(10).setHidden(True)
        except:
            pass

    # =============================================================
    # SHOW
    # =============================================================

    window.show()

    sys.exit(app.exec())