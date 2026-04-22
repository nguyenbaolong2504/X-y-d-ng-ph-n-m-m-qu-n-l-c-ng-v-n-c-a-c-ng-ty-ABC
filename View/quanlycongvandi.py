from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QTextDocument, QPageLayout
from PyQt6.QtPrintSupport import QPrinter, QPrintPreviewDialog

class MainWindowDi(QMainWindow):
    # --- Định nghĩa các tín hiệu kết nối với Controller ---
    them_cv_signal = pyqtSignal(dict)
    sua_cv_signal = pyqtSignal(int, dict)
    xoa_cv_signal = pyqtSignal(int)
    tim_kiem_signal = pyqtSignal(str)
    loc_cv_signal = pyqtSignal(QDate, QDate)
    xuat_excel_signal = pyqtSignal()
    nap_dulieu_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống Quản lý Công văn Phát hành")
        self.setGeometry(100, 100, 1500, 850)
        
        # Style UI chuẩn chuyên nghiệp
        self.setStyleSheet("""
            QMainWindow { background-color: #ffffff; }
            QPushButton { padding: 6px 15px; border: 1px solid #ccc; border-radius: 4px; background-color: #fff; font-size: 13px; }
            QPushButton:hover { background-color: #f8f9fa; border-color: #bbb; }
            QLineEdit, QComboBox, QDateEdit, QTextEdit { border: 1px solid #ccc; padding: 6px; border-radius: 4px; }
            QHeaderView::section { background-color: #f0f2f5; font-weight: bold; border: 1px solid #ddd; padding: 8px; }
            QTableView { border: 1px solid #ddd; gridline-color: #eee; selection-background-color: #e3f2fd; selection-color: black; }
        """)
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(12)

        # --- 1. Header ---
        header_container = QWidget()
        header_container.setStyleSheet("background-color: #f4f5f7; border: 1px solid #ddd; border-radius: 4px;")
        header_h_layout = QHBoxLayout(header_container)
        header_lbl = QLabel("📒 DANH MỤC CÔNG VĂN PHÁT HÀNH (ĐI)")
        header_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; border: none;")
        header_h_layout.addWidget(header_lbl)
        main_layout.addWidget(header_container)

        # --- 2. Toolbar (Nút bấm & Bộ lọc ngày) ---
        toolbar_container = QHBoxLayout()
        
        self.btn_them = QPushButton("➕ Thêm mới")
        self.btn_them.setStyleSheet("background-color: #4CAF50; color: white; border: none; font-weight: bold;")
        self.btn_xoa = QPushButton("❌ Xóa")
        self.btn_in = QPushButton("🖨️ In ấn")
        self.btn_excel = QPushButton("📊 Xuất Excel")
        self.btn_refresh = QPushButton("🔄 Làm mới")

        for btn in [self.btn_them, self.btn_xoa, self.btn_in, self.btn_excel, self.btn_refresh]:
            toolbar_container.addWidget(btn)
        
        toolbar_container.addStretch()

        toolbar_container.addWidget(QLabel("Từ ngày:"))
        self.date_tu = QDateEdit(calendarPopup=True, date=QDate.currentDate().addMonths(-1))
        self.date_tu.setFixedWidth(115)
        toolbar_container.addWidget(self.date_tu)

        toolbar_container.addWidget(QLabel("đến ngày:"))
        self.date_den = QDateEdit(calendarPopup=True, date=QDate.currentDate())
        self.date_den.setFixedWidth(115)
        toolbar_container.addWidget(self.date_den)

        self.btn_loc = QPushButton("Lọc dữ liệu")
        self.btn_loc.setStyleSheet("background-color: #2196F3; color: white; border: none; font-weight: bold;")
        toolbar_container.addWidget(self.btn_loc)
        
        main_layout.addLayout(toolbar_container)

        # --- 3. Search & Count Bar ---
        search_row_layout = QHBoxLayout()
        self.lbl_count = QLabel("Đang xem: 0 mục")
        self.lbl_count.setStyleSheet("font-weight: bold; color: #666;")
        search_row_layout.addWidget(self.lbl_count)
        search_row_layout.addStretch()
        
        search_row_layout.addWidget(QLabel("Tìm nhanh:"))
        search_group = QHBoxLayout()
        search_group.setSpacing(0) 
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập số đi, ký hiệu, nơi nhận...")
        self.search_input.setFixedWidth(320)
        self.search_input.setStyleSheet("border-top-right-radius: 0px; border-bottom-right-radius: 0px;")
        
        self.btn_search = QPushButton("Tìm")
        self.btn_search.setFixedWidth(60)
        self.btn_search.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0; border-left: none;
                border-top-left-radius: 0px; border-bottom-left-radius: 0px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #e0e0e0; }
        """)
        
        search_group.addWidget(self.search_input)
        search_group.addWidget(self.btn_search)
        search_row_layout.addLayout(search_group)
        main_layout.addLayout(search_row_layout)

        # --- 4. Table View ---
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.verticalHeader().setVisible(False)
        main_layout.addWidget(self.table_view)

        # --- Kết nối Signals ---
        self.btn_them.clicked.connect(self.open_them_dialog)
        self.btn_xoa.clicked.connect(self.confirm_delete)
        self.btn_in.clicked.connect(self.print_table)
        self.btn_excel.clicked.connect(self.xuat_excel_signal.emit)
        self.btn_refresh.clicked.connect(self.nap_dulieu_signal.emit)
        self.btn_loc.clicked.connect(lambda: self.loc_cv_signal.emit(self.date_tu.date(), self.date_den.date()))
        self.btn_search.clicked.connect(lambda: self.tim_kiem_signal.emit(self.search_input.text()))
        self.search_input.returnPressed.connect(lambda: self.tim_kiem_signal.emit(self.search_input.text()))
        self.table_view.doubleClicked.connect(self.open_sua_dialog)

    # --- Các hàm xử lý giao diện ---
    def show_status(self, message):
        """Sửa lỗi AttributeError: 'MainWindowDi' object has no attribute 'show_status'"""
        if self.statusBar():
            self.statusBar().showMessage(message, 3000)

    def set_table_model(self, model):
        self.table_view.setModel(model)
        self.table_view.setColumnHidden(0, True) 
        self.table_view.setColumnWidth(1, 80)   # Số đi
        self.table_view.setColumnWidth(2, 70)   # Năm
        self.table_view.setColumnWidth(3, 150)  # Ký hiệu
        self.table_view.setColumnWidth(4, 110)  # Ngày ký
        self.table_view.setColumnWidth(5, 250)  # Nơi nhận
        self.table_view.setColumnWidth(6, 450)  # Trích yếu
        self.table_view.setColumnWidth(7, 120)  # Trạng thái
        self.lbl_count.setText(f"Đang xem: {model.rowCount()} mục")

    def _to_qdate(self, value):
        if isinstance(value, str) and value:
            return QDate.fromString(value.split(' ')[0], "yyyy-MM-dd")
        return QDate.currentDate()

    # --- HÀM TẠO DIALOG NHẬP LIỆU PHONG CÁCH Ô LƯỚI (GRID) ---
    def create_input_dialog(self, title, row_data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setFixedWidth(950)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 15)
        layout.setSpacing(15)

        # Header
        header = QLabel(f"  {title}")
        header.setStyleSheet("background-color: #005a9e; color: white; font-weight: bold; padding: 12px; font-size: 14px;")
        layout.addWidget(header)

        form_widget = QWidget()
        grid = QGridLayout(form_widget)
        grid.setSpacing(10)

        # Hàng 1: Hồ sơ công việc
        grid.addWidget(QLabel("Hồ sơ công việc:"), 0, 0)
        in_hoso = QLineEdit(row_data.get("GhiChu", "") if row_data else "")
        grid.addWidget(in_hoso, 0, 1, 1, 7)

        # Hàng 2: Năm | Số | Ký hiệu | Ngày văn bản
        grid.addWidget(QLabel("Năm:"), 1, 0)
        in_nam = QLineEdit(str(row_data.get("Nam", QDate.currentDate().year())) if row_data else str(QDate.currentDate().year()))
        grid.addWidget(in_nam, 1, 1)

        grid.addWidget(QLabel("Số:"), 1, 2)
        in_so = QLineEdit(str(row_data.get("SoPhatHanh", "")) if row_data else "")
        grid.addWidget(in_so, 1, 3)

        grid.addWidget(QLabel("Ký hiệu:"), 1, 4)
        in_kh = QLineEdit(row_data.get("KyHieu", "") if row_data else "")
        grid.addWidget(in_kh, 1, 5)

        grid.addWidget(QLabel("Ngày ký:"), 1, 6)
        in_ngay = QDateEdit(calendarPopup=True)
        in_ngay.setDate(self._to_qdate(row_data.get("NgayKy")) if row_data else QDate.currentDate())
        grid.addWidget(in_ngay, 1, 7)

        # Hàng 3: Loại văn bản | Đơn vị soạn | Người ký
        grid.addWidget(QLabel("Loại văn bản:"), 2, 0)
        in_loai = QComboBox()
        in_loai.addItems(["Công văn", "Quyết định", "Thông báo", "Tờ trình"])
        grid.addWidget(in_loai, 2, 1)

        grid.addWidget(QLabel("Đơn vị soạn:"), 2, 2)
        in_donvi = QComboBox()
        in_donvi.addItems(["Phòng Hành chính", "Phòng Kế toán", "Ban Giám đốc"])
        grid.addWidget(in_donvi, 2, 3)

        grid.addWidget(QLabel("Người ký:"), 2, 4)
        in_nguoiky = QComboBox()
        in_nguoiky.addItems(["Nguyễn Văn A", "Trần Thị B", "Lê Văn C"])
        grid.addWidget(in_nguoiky, 2, 5, 1, 3)

        # Hàng 4: Trích yếu
        grid.addWidget(QLabel("Trích yếu:"), 3, 0)
        in_trichyeu = QTextEdit(row_data.get("TrichYeu", "") if row_data else "")
        in_trichyeu.setFixedHeight(80)
        grid.addWidget(in_trichyeu, 3, 1, 1, 7)

        # --- HÀNG 5 MỚI: FILE ĐÍNH KÈM ---
        grid.addWidget(QLabel("File đính kèm:"), 4, 0)
        in_file_path = QLineEdit(row_data.get("FilePath", "") if row_data else "")
        in_file_path.setReadOnly(True) # Không cho gõ, bắt buộc chọn file
        in_file_path.setPlaceholderText("Chọn file văn bản (PDF, Word,...)")
        grid.addWidget(in_file_path, 4, 1, 1, 6)
        
        btn_browse = QPushButton("📁 Chọn File")
        btn_browse.setFixedWidth(100)
        btn_browse.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        grid.addWidget(btn_browse, 4, 7)

        # Hàm xử lý khi bấm nút chọn file
        def browse_file():
            fname, _ = QFileDialog.getOpenFileName(dialog, "Chọn file đính kèm", "", "All Files (*);;PDF Files (*.pdf);;Word Files (*.docx)")
            if fname:
                in_file_path.setText(fname)
        
        btn_browse.clicked.connect(browse_file)
        # --------------------------------

        # Hàng 6: Nơi nhận
        grid.addWidget(QLabel("Nơi nhận:"), 5, 0)
        in_noinhan = QTextEdit(row_data.get("NoiNhan", "") if row_data else "")
        in_noinhan.setFixedHeight(60)
        grid.addWidget(in_noinhan, 5, 1, 1, 7)

        layout.addWidget(form_widget)

        # Nút Footer
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        btn_save = QPushButton("💾 Lưu dữ liệu")
        btn_save.setStyleSheet("background-color: #0078d4; color: white; font-weight: bold; min-width: 120px; padding: 8px;")
        btn_close = QPushButton("❌ Đóng")
        btn_close.setStyleSheet("background-color: #d83b01; color: white; font-weight: bold; min-width: 100px; padding: 8px;")
        
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_close)
        layout.addLayout(button_layout)

        btn_save.clicked.connect(dialog.accept)
        btn_close.clicked.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            return {
                "SoPhatHanh": int(in_so.text() or 0),
                "Nam": int(in_nam.text() or 2026),
                "KyHieu": in_kh.text(),
                "NgayKy": in_ngay.date().toString("yyyy-MM-dd"),
                "NoiNhan": in_noinhan.toPlainText(),
                "TrichYeu": in_trichyeu.toPlainText(),
                "GhiChu": in_hoso.text(),
                "FilePath": in_file_path.text(), # Trả về đường dẫn file
                "TrangThaiChuyen": 1
            }
        return None

    def open_them_dialog(self):
        data = self.create_input_dialog("THÊM MỚI THÔNG TIN VĂN BẢN ĐI")
        if data:
            self.them_cv_signal.emit(data)

    def open_sua_dialog(self):
        idx = self.table_view.currentIndex()
        if not idx.isValid(): return
        row_data = self.table_view.model().get_row(idx.row())
        data = self.create_input_dialog(f"CẬP NHẬT VĂN BẢN: {row_data['KyHieu']}", row_data)
        if data:
            self.sua_cv_signal.emit(row_data["Id"], data)

    def confirm_delete(self):
        idx = self.table_view.currentIndex()
        if not idx.isValid():
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn dòng cần xóa")
            return
        data = self.table_view.model().get_row(idx.row())
        if QMessageBox.question(self, "Xác nhận", f"Xóa công văn '{data['KyHieu']}'?") == QMessageBox.StandardButton.Yes:
            self.xoa_cv_signal.emit(data["Id"])

    def print_table(self):
        model = self.table_view.model()
        if not model or model.rowCount() == 0: return
        html = "<html><head><style>table { width: 100%; border-collapse: collapse; } th, td { border: 1px solid black; padding: 8px; text-align: center; font-size: 10pt; } th { background-color: #f2f2f2; }</style></head><body>"
        html += "<h2 style='text-align: center;'>DANH MỤC CÔNG VĂN PHÁT HÀNH</h2><table><tr><th>STT</th><th>Số đi</th><th>Ký hiệu</th><th>Ngày ký</th><th>Nơi nhận</th><th>Trích yếu</th><th>Trạng thái</th></tr>"
        for i in range(model.rowCount()):
            d = model.get_row(i)
            tt = "Đã chuyển" if d.get('TrangThaiChuyen') == 1 else "Chưa chuyển"
            html += f"<tr><td>{i+1}</td><td>{d.get('SoPhatHanh','')}</td><td>{d.get('KyHieu','')}</td><td>{d.get('NgayKy','')}</td><td>{d.get('NoiNhan','')}</td><td>{d.get('TrichYeu','')}</td><td>{tt}</td></tr>"
        html += "</table></body></html>"
        self.doc = QTextDocument()
        self.doc.setHtml(html)
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setPageOrientation(QPageLayout.Orientation.Landscape)
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(lambda p: self.doc.print(p))
        preview.exec()

    def show_error(self, msg):
        QMessageBox.critical(self, "Lỗi", msg)