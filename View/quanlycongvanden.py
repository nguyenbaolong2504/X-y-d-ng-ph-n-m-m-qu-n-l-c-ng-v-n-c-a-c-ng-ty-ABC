import os, shutil
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate, pyqtSignal, Qt, QUrl
from PyQt6.QtGui import QDesktopServices


class MainWindow(QMainWindow):
    them_cv_signal = pyqtSignal(dict)
    sua_cv_signal = pyqtSignal(int, dict)
    xoa_cv_signal = pyqtSignal(int)
    tim_kiem_signal = pyqtSignal(str)
    loc_cv_signal = pyqtSignal()
    xuat_excel_signal = pyqtSignal()
    nap_dulieu_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống Quản lý Công văn - Công ty ABC")
        self.setGeometry(80, 80, 1720, 900)

        self.ds_phong_ban = []
        self.ds_loai_van_ban = []          # list dict: {'id':..., 'ten_loai':...}
        self._them_file_path = None
        self._sua_file_path = None
        self._sua_old_file = None

        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        # Header
        header = QLabel("📋 DANH MỤC VĂN BẢN ĐẾN")
        header.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            padding: 12px; 
            background-color: #f0f2f5; 
            border-radius: 6px;
            color: #1e3a8a;
        """)
        main_layout.addWidget(header)

        # Toolbar
        toolbar = QHBoxLayout()
        self.btn_them = QPushButton("➕ Thêm mới")
        self.btn_them.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 9px 18px; border-radius: 5px;")
        self.btn_xoa = QPushButton("❌ Xóa")
        self.btn_xoa.setStyleSheet("background-color: #dc3545; color: white; font-weight: bold; padding: 9px 18px; border-radius: 5px;")
        self.btn_refresh = QPushButton("🔄 Làm mới")
        self.btn_excel = QPushButton("📊 Xuất Excel")
        self.btn_in = QPushButton("🖨️ In")
        for btn in [self.btn_them, self.btn_xoa, self.btn_refresh, self.btn_excel, self.btn_in]:
            toolbar.addWidget(btn)

        toolbar.addStretch()

            # Trong setup_ui, thay thế phần BỘ LỌC LOẠI VĂN BẢN bằng:
        # ---- BỘ LỌC LOẠI VĂN BẢN ----
        toolbar.addWidget(QLabel("Loại VB:"))
        self.cb_loai_vb = QComboBox()
        self.cb_loai_vb.addItem("Tất cả", None)

        # THÊM CHECKBOX BỎ QUA NGÀY
        self.chk_bo_qua_ngay = QCheckBox("Bỏ qua ngày")
        self.chk_bo_qua_ngay.setChecked(True)  # mặc định bỏ qua
        toolbar.addWidget(self.chk_bo_qua_ngay)

        self.cb_loai_vb.currentIndexChanged.connect(self.loc_cv_signal.emit)
        toolbar.addWidget(self.cb_loai_vb)
        toolbar.addSpacing(25)

        # ---- BỘ LỌC NGÀY (giữ nguyên) ----
        toolbar.addWidget(QLabel("Từ ngày:"))
        self.date_tu_ngay = QDateEdit(calendarPopup=True)
        self.date_tu_ngay.setDate(QDate.currentDate().addDays(-30))
        toolbar.addWidget(self.date_tu_ngay)

        toolbar.addWidget(QLabel("đến ngày:"))
        self.date_den_ngay = QDateEdit(calendarPopup=True)
        self.date_den_ngay.setDate(QDate.currentDate())
        toolbar.addWidget(self.date_den_ngay)

        self.btn_loc = QPushButton("🔍 Lọc")
        self.btn_loc.setStyleSheet("background-color: #17a2b8; color: white; font-weight: bold; padding: 9px 18px; border-radius: 5px;")
        toolbar.addWidget(self.btn_loc)
        main_layout.addLayout(toolbar)

        # Search bar
        search_layout = QHBoxLayout()
        self.lbl_count = QLabel("Đang xem: 0 mục")
        self.lbl_count.setStyleSheet("font-weight: bold; color: #1e3a8a;")
        search_layout.addWidget(self.lbl_count)
        search_layout.addStretch()
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập số ký hiệu, trích yếu, tác giả...")
        self.search_input.setFixedWidth(420)
        self.btn_search = QPushButton("Tìm")
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.btn_search)
        main_layout.addLayout(search_layout)

        # Table
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view.setStyleSheet("""
            QTableView { gridline-color: #d0d7e3; font-size: 13px; }
            QHeaderView::section { 
                background-color: #e9ecef; 
                font-weight: bold; 
                padding: 8px; 
                border: 1px solid #c0c4cc;
            }
        """)
        main_layout.addWidget(self.table_view)

        # Signals
        self.btn_them.clicked.connect(self.open_them_dialog)
        self.btn_xoa.clicked.connect(self.confirm_delete)
        self.btn_refresh.clicked.connect(self.nap_dulieu_signal.emit)
        self.btn_excel.clicked.connect(self.xuat_excel_signal.emit)
        self.btn_in.clicked.connect(self.print_table)
        self.btn_search.clicked.connect(self.handle_search)
        self.search_input.returnPressed.connect(self.handle_search)
        self.btn_loc.clicked.connect(self.loc_cv_signal.emit)
        self.table_view.doubleClicked.connect(self.open_sua_dialog)
        self.table_view.clicked.connect(self.on_table_click)

    def handle_search(self):
        keyword = self.search_input.text().strip()
        self.tim_kiem_signal.emit(keyword)

    def set_table_model(self, model):
        self.table_view.setModel(model)
        widths = [40, 70, 100, 85, 170, 135, 100, 340, 180, 100, 110, 90, 120, 160]
        for i, w in enumerate(widths):
            if i < model.columnCount():
                self.table_view.setColumnWidth(i, w)
        self.lbl_count.setText(f"Đang xem: {model.rowCount()} mục")

    def set_phong_ban_list(self, ds):
        self.ds_phong_ban = ds or []

    def set_loai_van_ban_list(self, ds):
        """Nhận list dict: [{'id':..., 'ten_loai':...}], nạp vào combobox lọc"""
        self.ds_loai_van_ban = ds or []
        self.cb_loai_vb.blockSignals(True)
        self.cb_loai_vb.clear()
        self.cb_loai_vb.addItem("Tất cả", None)
        for item in self.ds_loai_van_ban:
            self.cb_loai_vb.addItem(item['ten_loai'], item['id'])
        self.cb_loai_vb.blockSignals(False)

    def show_status(self, msg: str):
        self.statusBar().showMessage(msg, 5000)

    def show_error(self, msg: str):
        QMessageBox.critical(self, "Lỗi", msg)

    def print_table(self):
        QMessageBox.information(self, "Thông báo", 
            "Chức năng In đang được phát triển.\nBạn có thể dùng nút **Xuất Excel** tạm thời.")

    # ================== CHỌN FILE ==================
    def _chon_file(self, line_edit: QLineEdit, mode: str):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file đính kèm", "", "All Files (*.*)")
        if file_path:
            dest_dir = "attachments"
            os.makedirs(dest_dir, exist_ok=True)
            base, ext = os.path.splitext(os.path.basename(file_path))
            new_name = f"{base}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
            dest_path = os.path.join(dest_dir, new_name)
            shutil.copy2(file_path, dest_path)
            line_edit.setText(new_name)
            if mode == 'them':
                self._them_file_path = dest_path
            else:
                self._sua_file_path = dest_path

    def _xoa_file_sua(self):
        self._sua_file_path = None
        self.sua_file_edit.clear()
        self.sua_file_edit.setPlaceholderText("Đã xóa file")

    # ================== FORM THÊM ==================
    def open_them_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Thêm Công văn Đến Mới")
        dialog.setFixedWidth(680)
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        form.setSpacing(12)
        style = "padding: 6px 8px; border: 1px solid #b0b0b0; border-radius: 4px;"

        # Combo Loại văn bản
        loai_vb_cb = QComboBox()
        for item in self.ds_loai_van_ban:
            loai_vb_cb.addItem(item['ten_loai'], item['id'])

        # Trạng thái
        trang_thai_cb = QComboBox()
        trang_thai_cb.addItems(["Mới", "Đang xử lý", "Hoàn thành"])

        inputs = {
            "ngay_den": QDateEdit(calendarPopup=True, date=QDate.currentDate()),
            "so_den": QLineEdit(),
            "tac_gia": QLineEdit(),
            "so_ky_hieu": QLineEdit(),
            "ngay_van_ban": QDateEdit(calendarPopup=True, date=QDate.currentDate()),
            "trich_yeu": QTextEdit(),
            "don_vi_nhan": QComboBox(),
            "ngay_chuyen": QDateEdit(calendarPopup=True, date=QDate.currentDate()),
            "ghi_chu": QLineEdit()
        }
        inputs["don_vi_nhan"].addItems(self.ds_phong_ban)
        inputs["don_vi_nhan"].setEditable(True)

        for w in inputs.values():
            if isinstance(w, (QLineEdit, QTextEdit)):
                w.setStyleSheet(style)
        inputs["trich_yeu"].setFixedHeight(80)

        # File
        file_layout = QHBoxLayout()
        self.them_file_edit = QLineEdit()
        self.them_file_edit.setReadOnly(True)
        self.them_file_edit.setPlaceholderText("Chưa chọn file...")
        btn_file = QPushButton("📎 Chọn file")
        btn_file.clicked.connect(lambda: self._chon_file(self.them_file_edit, 'them'))
        file_layout.addWidget(self.them_file_edit)
        file_layout.addWidget(btn_file)

        form.addRow("Ngày đến (*):", inputs["ngay_den"])
        form.addRow("Số đến:", inputs["so_den"])
        form.addRow("Tác giả / Cơ quan (*):", inputs["tac_gia"])
        form.addRow("Số ký hiệu (*):", inputs["so_ky_hieu"])
        form.addRow("Ngày văn bản:", inputs["ngay_van_ban"])
        form.addRow("Trích yếu nội dung:", inputs["trich_yeu"])
        form.addRow("Loại văn bản:", loai_vb_cb)
        form.addRow("Trạng thái:", trang_thai_cb)
        form.addRow("Đơn vị nhận:", inputs["don_vi_nhan"])
        form.addRow("Ngày chuyển:", inputs["ngay_chuyen"])
        form.addRow("File đính kèm:", file_layout)
        form.addRow("Ghi chú:", inputs["ghi_chu"])

        layout.addLayout(form)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            if not inputs["tac_gia"].text().strip() or not inputs["so_ky_hieu"].text().strip():
                QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập đầy đủ Tác giả và Số ký hiệu!")
                return

            map_tt = {"Mới": 0, "Đang xử lý": 1, "Hoàn thành": 2}
            data = {
                "ngay_den": inputs["ngay_den"].date().toString("yyyy-MM-dd"),
                "so_den": inputs["so_den"].text().strip(),
                "tac_gia": inputs["tac_gia"].text().strip(),
                "so_ky_hieu": inputs["so_ky_hieu"].text().strip(),
                "ngay_van_ban": inputs["ngay_van_ban"].date().toString("yyyy-MM-dd"),
                "trich_yeu": inputs["trich_yeu"].toPlainText().strip(),
                "phan_loai_id": loai_vb_cb.currentData(),
                "trang_thai": map_tt.get(trang_thai_cb.currentText(), 0),
                "don_vi_nhan": inputs["don_vi_nhan"].currentText().strip(),
                "ngay_chuyen": inputs["ngay_chuyen"].date().toString("yyyy-MM-dd"),
                "ghi_chu": inputs["ghi_chu"].text().strip(),
                "file_dinh_kem": self._them_file_path
            }
            self.them_cv_signal.emit(data)

    # ================== FORM SỬA ==================
    def open_sua_dialog(self):
        index = self.table_view.currentIndex()
        if not index.isValid():
            return
        row_data = self.table_view.model().get_row(index.row())
        if not row_data:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Chỉnh sửa Công văn - ID: {row_data.get('id')}")
        dialog.setFixedWidth(680)
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        form.setSpacing(12)
        style = "padding: 6px 8px; border: 1px solid #b0b0b0; border-radius: 4px;"

        # Loại văn bản
        loai_vb_cb = QComboBox()
        for item in self.ds_loai_van_ban:
            loai_vb_cb.addItem(item['ten_loai'], item['id'])
        current_id = row_data.get("phan_loai_id")
        idx = loai_vb_cb.findData(current_id)
        if idx >= 0:
            loai_vb_cb.setCurrentIndex(idx)

        # Trạng thái
        trang_thai_cb = QComboBox()
        trang_thai_cb.addItems(["Mới", "Đang xử lý", "Hoàn thành"])
        map_tt = {0: "Mới", 1: "Đang xử lý", 2: "Hoàn thành"}
        trang_thai_cb.setCurrentText(map_tt.get(row_data.get("trang_thai"), "Mới"))

        inputs = {
            "ngay_den": QDateEdit(calendarPopup=True),
            "so_den": QLineEdit(str(row_data.get("so_den", ""))),
            "tac_gia": QLineEdit(str(row_data.get("tac_gia", ""))),
            "so_ky_hieu": QLineEdit(str(row_data.get("so_ky_hieu", ""))),
            "ngay_van_ban": QDateEdit(calendarPopup=True),
            "trich_yeu": QTextEdit(str(row_data.get("trich_yeu", ""))),
            "don_vi_nhan": QComboBox(),
            "ngay_chuyen": QDateEdit(calendarPopup=True),
            "ghi_chu": QLineEdit(str(row_data.get("ghi_chu", "")))
        }

        def set_date(widget, value):
            if value:
                try:
                    widget.setDate(QDate.fromString(str(value).split()[0], "yyyy-MM-dd"))
                except:
                    widget.setDate(QDate.currentDate())
            else:
                widget.setDate(QDate.currentDate())

        set_date(inputs["ngay_den"], row_data.get("ngay_den"))
        set_date(inputs["ngay_van_ban"], row_data.get("ngay_van_ban"))
        set_date(inputs["ngay_chuyen"], row_data.get("ngay_chuyen"))

        inputs["don_vi_nhan"].addItems(self.ds_phong_ban)
        inputs["don_vi_nhan"].setEditable(True)
        inputs["don_vi_nhan"].setCurrentText(str(row_data.get("don_vi_nhan", "")))

        for w in inputs.values():
            if isinstance(w, (QLineEdit, QTextEdit)):
                w.setStyleSheet(style)
        inputs["trich_yeu"].setFixedHeight(80)

        # File
        file_layout = QHBoxLayout()
        self.sua_file_edit = QLineEdit()
        self.sua_file_edit.setReadOnly(True)
        old_file = row_data.get("file_dinh_kem")
        self._sua_old_file = old_file
        self._sua_file_path = old_file
        if old_file:
            self.sua_file_edit.setText(os.path.basename(old_file))
        else:
            self.sua_file_edit.setPlaceholderText("Không có file")
        btn_chon = QPushButton("📎 Chọn file")
        btn_xoa_file = QPushButton("Xóa file")
        btn_chon.clicked.connect(lambda: self._chon_file(self.sua_file_edit, 'sua'))
        btn_xoa_file.clicked.connect(self._xoa_file_sua)
        file_layout.addWidget(self.sua_file_edit)
        file_layout.addWidget(btn_chon)
        file_layout.addWidget(btn_xoa_file)

        form.addRow("Ngày đến:", inputs["ngay_den"])
        form.addRow("Số đến:", inputs["so_den"])
        form.addRow("Tác giả / Cơ quan:", inputs["tac_gia"])
        form.addRow("Số ký hiệu:", inputs["so_ky_hieu"])
        form.addRow("Ngày văn bản:", inputs["ngay_van_ban"])
        form.addRow("Trích yếu:", inputs["trich_yeu"])
        form.addRow("Loại văn bản:", loai_vb_cb)
        form.addRow("Trạng thái:", trang_thai_cb)
        form.addRow("Đơn vị nhận:", inputs["don_vi_nhan"])
        form.addRow("Ngày chuyển:", inputs["ngay_chuyen"])
        form.addRow("File đính kèm:", file_layout)
        form.addRow("Ghi chú:", inputs["ghi_chu"])

        layout.addLayout(form)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            if self._sua_file_path != self._sua_old_file and self._sua_old_file and os.path.exists(self._sua_old_file):
                try:
                    os.remove(self._sua_old_file)
                except:
                    pass

            map_tt_reverse = {"Mới": 0, "Đang xử lý": 1, "Hoàn thành": 2}
            new_data = {
                "ngay_den": inputs["ngay_den"].date().toString("yyyy-MM-dd"),
                "so_den": inputs["so_den"].text().strip(),
                "tac_gia": inputs["tac_gia"].text().strip(),
                "so_ky_hieu": inputs["so_ky_hieu"].text().strip(),
                "ngay_van_ban": inputs["ngay_van_ban"].date().toString("yyyy-MM-dd"),
                "trich_yeu": inputs["trich_yeu"].toPlainText().strip(),
                "phan_loai_id": loai_vb_cb.currentData(),
                "trang_thai": map_tt_reverse.get(trang_thai_cb.currentText(), 0),
                "don_vi_nhan": inputs["don_vi_nhan"].currentText().strip(),
                "ngay_chuyen": inputs["ngay_chuyen"].date().toString("yyyy-MM-dd"),
                "ghi_chu": inputs["ghi_chu"].text().strip(),
                "file_dinh_kem": self._sua_file_path
            }
            self.sua_cv_signal.emit(row_data["id"], new_data)

    def confirm_delete(self):
        index = self.table_view.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một công văn để xóa!")
            return
        row_data = self.table_view.model().get_row(index.row())
        msg = f"Bạn có chắc chắn muốn xóa công văn:\nSố ký hiệu: {row_data.get('so_ky_hieu', '')} ?"
        if QMessageBox.question(self, "Xác nhận xóa", msg) == QMessageBox.StandardButton.Yes:
            self.xoa_cv_signal.emit(row_data["id"])

    def on_table_click(self, index):
        if index.column() != 12:   # cột File
            return
        model = self.table_view.model()
        if not model:
            return
        file_path = model.data(index, Qt.ItemDataRole.UserRole)
        if file_path and os.path.exists(file_path):
            try:
                QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.abspath(file_path)))
            except Exception as e:
                self.show_error(f"Không thể mở file: {str(e)}")
        else:
            QMessageBox.warning(self, "Thông báo", "Không tìm thấy file đính kèm!")