from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt6.QtGui import QTextDocument, QPageLayout, QPageSize
from PyQt6.QtCore import QMarginsF

class MainWindow(QMainWindow):
    # Định nghĩa các Signal để giao tiếp với Controller
    them_cv_signal = pyqtSignal(dict)
    sua_cv_signal = pyqtSignal(int, dict)
    xoa_cv_signal = pyqtSignal(int)
    tim_kiem_signal = pyqtSignal(str)
    loc_cv_signal = pyqtSignal()  # Signal để Controller gọi hàm handle_filter
    xuat_excel_signal = pyqtSignal()
    nap_dulieu_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống quản lý văn bản")
        self.setGeometry(100, 100, 1600, 800)
        self.ds_phong_ban = [] 
        self.setStyleSheet("QMainWindow { background-color: #ffffff; }")
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # --- Header ---
        header_lbl = QLabel("🪟 Danh mục văn bản đến")
        header_lbl.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            color: #333; 
            padding: 10px; 
            background-color: #f4f5f7; 
            border: 1px solid #ddd;
        """)
        main_layout.addWidget(header_lbl)

        # --- Toolbar (Chứa các nút chức năng và Lọc ngày) ---
        toolbar_layout = QHBoxLayout()
        
        self.btn_them = QPushButton("➕ Thêm")
        self.btn_them.setStyleSheet("background-color: #4CAF50; color: white; padding: 6px 15px; border-radius: 3px; font-weight: bold; border: none;")
        
        self.btn_xoa = QPushButton("❌ Xóa")
        self.btn_xoa.setStyleSheet("background-color: #f4f4f4; color: #d32f2f; padding: 6px 15px; border: 1px solid #ccc; border-radius: 3px;")
        
        self.btn_in = QPushButton("🖨️ In")
        self.btn_excel = QPushButton("📊 Excel")
        self.btn_refresh = QPushButton("🔄 Làm mới")
        
        for btn in [self.btn_them, self.btn_xoa, self.btn_in, self.btn_excel, self.btn_refresh]:
            if btn not in [self.btn_them, self.btn_xoa]:
                btn.setStyleSheet("padding: 6px 15px; border: 1px solid #ccc; border-radius: 3px; background-color: #fff;")
            toolbar_layout.addWidget(btn)
            
        toolbar_layout.addStretch()

        # Bộ lọc ngày tháng (Dùng cho hàm handle_filter trong Controller)
        toolbar_layout.addWidget(QLabel("Từ ngày:"))
        self.date_tu_ngay = QDateEdit(calendarPopup=True) # Đặt tên khớp với Controller
        self.date_tu_ngay.setDate(QDate.currentDate().addDays(-30))
        toolbar_layout.addWidget(self.date_tu_ngay)

        toolbar_layout.addWidget(QLabel("đến ngày:"))
        self.date_den_ngay = QDateEdit(calendarPopup=True) # Đặt tên khớp với Controller
        self.date_den_ngay.setDate(QDate.currentDate())
        toolbar_layout.addWidget(self.date_den_ngay)

        self.btn_loc = QPushButton("Lọc văn bản")
        self.btn_loc.setStyleSheet("background-color: #2196F3; color: white; padding: 6px 15px; border-radius: 3px; border: none;")
        toolbar_layout.addWidget(self.btn_loc)
        
        main_layout.addLayout(toolbar_layout)

        # --- Search Bar ---
        search_layout = QHBoxLayout()
        self.lbl_count = QLabel("Đang xem: 0 mục")
        search_layout.addWidget(self.lbl_count)
        
        search_layout.addStretch()
        
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập số đến, trích yếu, tác giả...")
        self.search_input.setFixedWidth(300)
        self.btn_search = QPushButton("Tìm")
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.btn_search)
        main_layout.addLayout(search_layout)

        # --- Table View ---
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.setStyleSheet("QHeaderView::section { background-color: #f0f2f5; font-weight: bold; border: 1px solid #ddd; }")
        main_layout.addWidget(self.table_view)

        # --- Kết nối Signals nội bộ ---
        self.btn_them.clicked.connect(self.open_them_dialog)
        self.btn_xoa.clicked.connect(self.confirm_delete)
        self.btn_in.clicked.connect(self.print_table)
        self.btn_excel.clicked.connect(self.xuat_excel_signal.emit)
        self.btn_refresh.clicked.connect(self.nap_dulieu_signal.emit)
        
        # Kết nối Tìm kiếm
        self.btn_search.clicked.connect(self.handle_search_click)
        self.search_input.returnPressed.connect(self.handle_search_click)
        
        # Kết nối nút Lọc (Phát signal để Controller xử lý)
        self.btn_loc.clicked.connect(self.loc_cv_signal.emit)

        # Double click để sửa
        self.table_view.doubleClicked.connect(self.open_sua_dialog)

    def handle_search_click(self):
        keyword = self.search_input.text().strip()
        self.tim_kiem_signal.emit(keyword)

    def set_table_model(self, model):
        self.table_view.setModel(model)
        # 12 cột tương ứng với headers
        widths = [40, 80, 100, 80, 150, 130, 110, 350, 180, 100, 100, 150]
        for i, w in enumerate(widths):
            self.table_view.setColumnWidth(i, w)
        # Cập nhật số lượng hiển thị trên nhãn
        self.lbl_count.setText(f"Đang xem: {model.rowCount()} mục")

    def set_phong_ban_list(self, ds):
        self.ds_phong_ban = ds

    def show_status(self, msg):
        self.statusBar().showMessage(msg, 5000)

    def show_error(self, msg):
        QMessageBox.critical(self, "Lỗi", msg)

    # --- DIALOG THÊM / SỬA (Dùng ComboBox cho đơn vị nhận) ---
    def open_them_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Thêm công văn đến mới")
        dialog.setFixedWidth(550)
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        
        style = "padding: 5px; border: 1px solid #ccc; border-radius: 3px;"
        
        cb_don_vi = QComboBox()
        cb_don_vi.addItems(self.ds_phong_ban)
        cb_don_vi.setEditable(True) 
        cb_don_vi.setStyleSheet(style)

        inputs = {
            "ngay_den": QDateEdit(calendarPopup=True, date=QDate.currentDate()),
            "so_den": QLineEdit(),
            "tac_gia": QLineEdit(),
            "so_ky_hieu": QLineEdit(),
            "ngay_van_ban": QDateEdit(calendarPopup=True, date=QDate.currentDate()),
            "trich_yeu": QTextEdit(),
            "ngay_chuyen": QDateEdit(calendarPopup=True, date=QDate.currentDate()),
            "ghi_chu": QLineEdit()
        }

        for w in inputs.values(): w.setStyleSheet(style)
        inputs["trich_yeu"].setFixedHeight(70)

        form.addRow("Ngày đến (*):", inputs["ngay_den"])
        form.addRow("Số đến:", inputs["so_den"])
        form.addRow("Tác giả/Cơ quan (*):", inputs["tac_gia"])
        form.addRow("Số ký hiệu (*):", inputs["so_ky_hieu"])
        form.addRow("Ngày ký văn bản:", inputs["ngay_van_ban"])
        form.addRow("Trích yếu nội dung:", inputs["trich_yeu"])
        form.addRow("Đơn vị nhận:", cb_don_vi)
        form.addRow("Ngày chuyển đi:", inputs["ngay_chuyen"])
        form.addRow("Ghi chú:", inputs["ghi_chu"])

        layout.addLayout(form)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            if not inputs["tac_gia"].text() or not inputs["so_ky_hieu"].text():
                self.show_error("Vui lòng nhập Tác giả và Số ký hiệu!")
                return

            data = {
                "ngay_den": inputs["ngay_den"].date().toString("yyyy-MM-dd"),
                "so_den": inputs["so_den"].text(),
                "tac_gia": inputs["tac_gia"].text(),
                "so_ky_hieu": inputs["so_ky_hieu"].text(),
                "ngay_van_ban": inputs["ngay_van_ban"].date().toString("yyyy-MM-dd"),
                "trich_yeu": inputs["trich_yeu"].toPlainText(),
                "don_vi_nhan": cb_don_vi.currentText(),
                "ngay_chuyen": inputs["ngay_chuyen"].date().toString("yyyy-MM-dd"),
                "ghi_chu": inputs["ghi_chu"].text()
            }
            self.them_cv_signal.emit(data)

    def open_sua_dialog(self):
        selected = self.table_view.currentIndex()
        if not selected.isValid(): return
        
        old_data = self.table_view.model().get_row(selected.row())
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Chỉnh sửa công văn - ID: {old_data['id']}")
        dialog.setFixedWidth(550)
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        style = "padding: 5px; border: 1px solid #ccc; border-radius: 3px;"
        
        cb_don_vi = QComboBox()
        cb_don_vi.addItems(self.ds_phong_ban)
        cb_don_vi.setEditable(True)
        cb_don_vi.setCurrentText(str(old_data.get("don_vi_nhan", "")))
        cb_don_vi.setStyleSheet(style)

        def parse_d(s): 
            return QDate.fromString(str(s).split()[0], "yyyy-MM-dd") if s else QDate.currentDate()

        inputs = {
            "ngay_den": QDateEdit(calendarPopup=True, date=parse_d(old_data.get("ngay_den"))),
            "so_den": QLineEdit(str(old_data.get("so_den", ""))),
            "tac_gia": QLineEdit(str(old_data.get("tac_gia", ""))),
            "so_ky_hieu": QLineEdit(str(old_data.get("so_ky_hieu", ""))),
            "ngay_van_ban": QDateEdit(calendarPopup=True, date=parse_d(old_data.get("ngay_van_ban"))),
            "trich_yeu": QTextEdit(str(old_data.get("trich_yeu", ""))),
            "ngay_chuyen": QDateEdit(calendarPopup=True, date=parse_d(old_data.get("ngay_chuyen"))),
            "ghi_chu": QLineEdit(str(old_data.get("ghi_chu", "")))
        }

        for w in inputs.values(): w.setStyleSheet(style)
        inputs["trich_yeu"].setFixedHeight(70)

        form.addRow("Ngày đến:", inputs["ngay_den"])
        form.addRow("Số đến:", inputs["so_den"])
        form.addRow("Tác giả/Cơ quan:", inputs["tac_gia"])
        form.addRow("Số ký hiệu:", inputs["so_ky_hieu"])
        form.addRow("Ngày ký:", inputs["ngay_van_ban"])
        form.addRow("Trích yếu:", inputs["trich_yeu"])
        form.addRow("Đơn vị nhận:", cb_don_vi)
        form.addRow("Ngày chuyển:", inputs["ngay_chuyen"])
        form.addRow("Ghi chú:", inputs["ghi_chu"])

        layout.addLayout(form)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)
        buttons.accepted.connect(dialog.accept)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = {
                "ngay_den": inputs["ngay_den"].date().toString("yyyy-MM-dd"),
                "so_den": inputs["so_den"].text(),
                "tac_gia": inputs["tac_gia"].text(),
                "so_ky_hieu": inputs["so_ky_hieu"].text(),
                "ngay_van_ban": inputs["ngay_van_ban"].date().toString("yyyy-MM-dd"),
                "trich_yeu": inputs["trich_yeu"].toPlainText(),
                "don_vi_nhan": cb_don_vi.currentText(),
                "ngay_chuyen": inputs["ngay_chuyen"].date().toString("yyyy-MM-dd"),
                "ghi_chu": inputs["ghi_chu"].text()
            }
            self.sua_cv_signal.emit(old_data["id"], new_data)

    def confirm_delete(self):
        selected = self.table_view.currentIndex()
        if not selected.isValid(): 
            self.show_status("Vui lòng chọn một dòng để xóa")
            return
        data = self.table_view.model().get_row(selected.row())
        msg = f"Bạn có chắc muốn xóa văn bản số: {data['so_ky_hieu']}?"
        if QMessageBox.question(self, "Xác nhận xóa", msg) == QMessageBox.StandardButton.Yes:
            self.xoa_cv_signal.emit(data["id"])

    # --- HÀM IN (PRINT) CHUẨN LANDSCAPE ---
    def print_table(self):
        model = self.table_view.model()
        if not model or model.rowCount() == 0:
            self.show_error("Không có dữ liệu hiển thị để in!")
            return

        html = f"""
        <html>
        <head>
            <style>
                @page {{ size: A4 landscape; margin: 10mm; }}
                body {{ font-family: 'Times New Roman'; width: 100%; }}
                .header-table {{ width: 100%; border: none; margin-bottom: 20px; }}
                .main-title {{ text-align: center; font-weight: bold; font-size: 16pt; margin: 20px 0; text-transform: uppercase; }}
                .data-table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
                .data-table th, .data-table td {{ border: 1px solid black; padding: 5px; font-size: 10pt; word-wrap: break-word; }}
                .data-table th {{ background-color: #f2f2f2; text-align: center; }}
                .text-center {{ text-align: center; }}
            </style>
        </head>
        <body>
            <table class="header-table">
                <tr>
                    <td style="text-align: center; width: 40%;">HỌC VIỆN HÀNH CHÍNH QUỐC GIA<br><b>PHÂN HIỆU TP. HỒ CHÍ MINH</b></td>
                    <td style="text-align: center; width: 60%;"><b>CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM</b><br>Độc lập - Tự do - Hạnh phúc<br>---</td>
                </tr>
            </table>
            <div class="main-title">DANH MỤC VĂN BẢN ĐẾN</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th style="width: 30px;">STT</th>
                        <th style="width: 80px;">Ngày đến</th>
                        <th style="width: 50px;">Số đến</th>
                        <th style="width: 150px;">Cơ quan ban hành</th>
                        <th style="width: 100px;">Số ký hiệu</th>
                        <th>Trích yếu nội dung</th>
                        <th style="width: 120px;">Nơi nhận</th>
                    </tr>
                </thead>
                <tbody>
        """
        for row in range(model.rowCount()):
            d = model.get_row(row)
            ngay = str(d.get('ngay_den','')).split()[0]
            html += f"""
                <tr>
                    <td class="text-center">{row + 1}</td>
                    <td class="text-center">{ngay}</td>
                    <td class="text-center">{d.get('so_den','')}</td>
                    <td>{d.get('tac_gia','')}</td>
                    <td class="text-center">{d.get('so_ky_hieu','')}</td>
                    <td>{d.get('trich_yeu','')}</td>
                    <td>{d.get('don_vi_nhan','')}</td>
                </tr>
            """
        html += "</tbody></table></body></html>"

        self.doc = QTextDocument()
        self.doc.setHtml(html)
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setPageOrientation(QPageLayout.Orientation.Landscape)
        
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(lambda p: self.doc.print(p))
        preview.exec()  

    def _handle_print(self, printer):
        self.doc.print(printer)
   

    def set_table_model(self, model):
        self.table_view.setModel(model)
        widths = [30, 60, 90, 60, 150, 150, 90, 300, 200, 90, 80, 100]
        for i, w in enumerate(widths):
            self.table_view.setColumnWidth(i, w)

    # --- HÀM MỚI ĐỂ NHẬN LIST TỪ CONTROLLER ---
    def set_phong_ban_list(self, ds):
        self.ds_phong_ban = ds

    def open_them_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Thêm công văn đến")
        dialog.setFixedWidth(500)
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        
        style = "padding: 5px; border: 1px solid #ccc; border-radius: 3px;"
        
        # Đơn vị nhận dùng ComboBox
        cb_don_vi = QComboBox()
        cb_don_vi.addItems(self.ds_phong_ban)
        cb_don_vi.setEditable(True) 
        cb_don_vi.setStyleSheet(style)

        inputs = {
            "ngay_den": QDateEdit(calendarPopup=True, date=QDate.currentDate()),
            "so_den": QLineEdit(),
            "tac_gia": QLineEdit(),
            "so_ky_hieu": QLineEdit(),
            "ngay_van_ban": QDateEdit(calendarPopup=True, date=QDate.currentDate()),
            "trich_yeu": QTextEdit(),
            "ngay_chuyen": QDateEdit(calendarPopup=True, date=QDate.currentDate()),
            "ghi_chu": QLineEdit()
        }

        for w in inputs.values(): w.setStyleSheet(style)
        inputs["trich_yeu"].setFixedHeight(80)

        form.addRow("Ngày đến (*):", inputs["ngay_den"])
        form.addRow("Số đến:", inputs["so_den"])
        form.addRow("Tác giả (*):", inputs["tac_gia"])
        form.addRow("Số ký hiệu (*):", inputs["so_ky_hieu"])
        form.addRow("Ngày văn bản:", inputs["ngay_van_ban"])
        form.addRow("Trích yếu:", inputs["trich_yeu"])
        form.addRow("Đơn vị nhận:", cb_don_vi) # <--- SỬ DỤNG COMBOBOX
        form.addRow("Ngày chuyển:", inputs["ngay_chuyen"])
        form.addRow("Ghi chú:", inputs["ghi_chu"])

        layout.addLayout(form)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            if not inputs["tac_gia"].text() or not inputs["so_ky_hieu"].text():
                self.show_error("Vui lòng nhập đầy đủ các trường (*)")
                return

            data = {
                "ngay_den": inputs["ngay_den"].date().toString("yyyy-MM-dd"),
                "so_den": inputs["so_den"].text(),
                "tac_gia": inputs["tac_gia"].text(),
                "so_ky_hieu": inputs["so_ky_hieu"].text(),
                "ngay_van_ban": inputs["ngay_van_ban"].date().toString("yyyy-MM-dd"),
                "trich_yeu": inputs["trich_yeu"].toPlainText(),
                "don_vi_nhan": cb_don_vi.currentText(), # <--- LẤY TEXT TỪ COMBOBOX
                "ngay_chuyen": inputs["ngay_chuyen"].date().toString("yyyy-MM-dd"),
                "ghi_chu": inputs["ghi_chu"].text()
            }
            self.them_cv_signal.emit(data)

    def open_sua_dialog(self):
        selected = self.table_view.currentIndex()
        if not selected.isValid(): return
        
        old_data = self.table_view.model().get_row(selected.row())
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Sửa công văn - ID: {old_data['id']}")
        dialog.setFixedWidth(500)
        layout = QVBoxLayout(dialog)
        form = QFormLayout()

        style = "padding: 5px; border: 1px solid #ccc; border-radius: 3px;"
        
        # ComboBox Đơn vị nhận cho Form sửa
        cb_don_vi = QComboBox()
        cb_don_vi.addItems(self.ds_phong_ban)
        cb_don_vi.setEditable(True)
        cb_don_vi.setCurrentText(str(old_data.get("don_vi_nhan", "")))
        cb_don_vi.setStyleSheet(style)

        def parse_d(s): return QDate.fromString(str(s).split()[0], "yyyy-MM-dd") if s else QDate.currentDate()

        inputs = {
            "ngay_den": QDateEdit(calendarPopup=True, date=parse_d(old_data.get("ngay_den"))),
            "so_den": QLineEdit(str(old_data.get("so_den", ""))),
            "tac_gia": QLineEdit(str(old_data.get("tac_gia", ""))),
            "so_ky_hieu": QLineEdit(str(old_data.get("so_ky_hieu", ""))),
            "ngay_van_ban": QDateEdit(calendarPopup=True, date=parse_d(old_data.get("ngay_van_ban"))),
            "trich_yeu": QTextEdit(str(old_data.get("trich_yeu", ""))),
            "ngay_chuyen": QDateEdit(calendarPopup=True, date=parse_d(old_data.get("ngay_chuyen"))),
            "ghi_chu": QLineEdit(str(old_data.get("ghi_chu", "")))
        }

        for w in inputs.values(): w.setStyleSheet(style)
        inputs["trich_yeu"].setFixedHeight(80)

        form.addRow("Ngày đến:", inputs["ngay_den"])
        form.addRow("Số đến:", inputs["so_den"])
        form.addRow("Tác giả:", inputs["tac_gia"])
        form.addRow("Số ký hiệu:", inputs["so_ky_hieu"])
        form.addRow("Ngày văn bản:", inputs["ngay_van_ban"])
        form.addRow("Trích yếu:", inputs["trich_yeu"])
        form.addRow("Đơn vị nhận:", cb_don_vi) # <--- SỬ DỤNG COMBOBOX
        form.addRow("Ngày chuyển:", inputs["ngay_chuyen"])
        form.addRow("Ghi chú:", inputs["ghi_chu"])

        layout.addLayout(form)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = {
                "ngay_den": inputs["ngay_den"].date().toString("yyyy-MM-dd"),
                "so_den": inputs["so_den"].text(),
                "tac_gia": inputs["tac_gia"].text(),
                "so_ky_hieu": inputs["so_ky_hieu"].text(),
                "ngay_van_ban": inputs["ngay_van_ban"].date().toString("yyyy-MM-dd"),
                "trich_yeu": inputs["trich_yeu"].toPlainText(),
                "don_vi_nhan": cb_don_vi.currentText(),
                "ngay_chuyen": inputs["ngay_chuyen"].date().toString("yyyy-MM-dd"),
                "ghi_chu": inputs["ghi_chu"].text()
            }
            self.sua_cv_signal.emit(old_data["id"], new_data)

    def confirm_delete(self):
        selected = self.table_view.currentIndex()
        if not selected.isValid(): return
        data = self.table_view.model().get_row(selected.row())
        if QMessageBox.question(self, "Xác nhận", f"Xóa CV: {data['so_ky_hieu']}?") == QMessageBox.StandardButton.Yes:
            self.xoa_cv_signal.emit(data["id"])

    def show_status(self, msg): self.statusBar().showMessage(msg, 3000)
    def show_error(self, msg): QMessageBox.critical(self, "Lỗi", msg)