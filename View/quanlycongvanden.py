import os, shutil
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate, pyqtSignal, Qt, QUrl
from PyQt6.QtGui import QDesktopServices

class MainWindow(QMainWindow):
    # --- CÁC SIGNAL KẾT NỐI VỚI CONTROLLER ---
    them_cv_signal = pyqtSignal(dict)
    sua_cv_signal = pyqtSignal(int, dict)
    xoa_cv_signal = pyqtSignal(int)
    tim_kiem_signal = pyqtSignal(str)
    loc_cv_signal = pyqtSignal()
    xuat_excel_signal = pyqtSignal()
    nap_dulieu_signal = pyqtSignal()
    giao_viec_signal = pyqtSignal(int) 
    nap_danh_muc_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống Quản lý Văn bản Đến & Phân công")
        self.setGeometry(80, 80, 1720, 900)

        self.ds_nhan_su = [] 
        self.ds_loai_van_ban = []
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

        header = QLabel("📋 QUẢN LÝ VĂN BẢN ĐẾN & PHÂN CÔNG")
        header.setStyleSheet("""
            font-size: 20px; font-weight: bold; padding: 12px; 
            background-color: #f0f2f5; border-radius: 6px; color: #1e3a8a;
        """)
        main_layout.addWidget(header)

        toolbar = QHBoxLayout()
        self.btn_them = QPushButton("➕ ")
        self.btn_them.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 9px 18px; border-radius: 5px;")
        
        self.btn_giao_viec = QPushButton("👤")
        self.btn_giao_viec.setStyleSheet("background-color: #fd7e14; color: white; font-weight: bold; padding: 9px 18px; border-radius: 5px;")
        
        self.btn_xoa = QPushButton("❌ ")
        self.btn_xoa.setStyleSheet("background-color: #dc3545; color: white; font-weight: bold; padding: 9px 18px; border-radius: 5px;")
        
        self.btn_refresh = QPushButton("🔄 Làm mới")
        self.btn_excel = QPushButton("📊 Xuất Excel")
        
        for btn in [self.btn_them, self.btn_giao_viec, self.btn_xoa, self.btn_refresh, self.btn_excel]:
            toolbar.addWidget(btn)

        toolbar.addStretch()
        toolbar.addWidget(QLabel("Loại VB:"))
        self.cb_loai_vb = QComboBox()
        self.cb_loai_vb.addItem("Tất cả", None)
        self.cb_loai_vb.currentIndexChanged.connect(self.loc_cv_signal.emit)
        toolbar.addWidget(self.cb_loai_vb)
        toolbar.addSpacing(15)

        # ========== THÊM COMBOBOX MỨC ĐỘ ==========
        toolbar.addWidget(QLabel("Mức độ:"))
        self.cb_muc_do = QComboBox()
        self.cb_muc_do.addItems(["Tất cả", "Thường", "Khẩn", "Hỏa tốc"])
        self.cb_muc_do.setCurrentText("Tất cả")
        self.cb_muc_do.currentIndexChanged.connect(self.loc_cv_signal.emit)
        toolbar.addWidget(self.cb_muc_do)
        # ==========================================

        self.chk_bo_qua_ngay = QCheckBox("Bỏ qua ngày")
        self.chk_bo_qua_ngay.setChecked(True)
        toolbar.addWidget(self.chk_bo_qua_ngay)
        toolbar.addSpacing(25)

        toolbar.addWidget(QLabel("Từ ngày:"))
        self.date_tu_ngay = QDateEdit(calendarPopup=True)
        self.date_tu_ngay.setDisplayFormat("dd/MM/yyyy")
        self.date_tu_ngay.setDate(QDate.currentDate().addDays(-30))
        toolbar.addWidget(self.date_tu_ngay)

        toolbar.addWidget(QLabel("đến ngày:"))
        self.date_den_ngay = QDateEdit(calendarPopup=True)
        self.date_den_ngay.setDisplayFormat("dd/MM/yyyy")
        self.date_den_ngay.setDate(QDate.currentDate())
        toolbar.addWidget(self.date_den_ngay)

        self.btn_loc = QPushButton("🔍 Lọc")
        self.btn_loc.setStyleSheet("background-color: #17a2b8; color: white; font-weight: bold; padding: 9px 18px; border-radius: 5px;")
        toolbar.addWidget(self.btn_loc)
        main_layout.addLayout(toolbar)

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

        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view.setStyleSheet("""
            QTableView { gridline-color: #d0d7e3; font-size: 13px; }
            QHeaderView::section { background-color: #e9ecef; font-weight: bold; padding: 8px; border: 1px solid #c0c4cc; }
        """)
        main_layout.addWidget(self.table_view)

        # Connect signals
        self.btn_them.clicked.connect(self.open_them_dialog)
        self.btn_giao_viec.clicked.connect(self.open_giao_viec_dialog) 
        self.btn_xoa.clicked.connect(self.confirm_delete)
        self.btn_refresh.clicked.connect(self.nap_dulieu_signal.emit)
        self.btn_excel.clicked.connect(self.xuat_excel_signal.emit)
        self.btn_search.clicked.connect(self.handle_search)
        self.search_input.returnPressed.connect(self.handle_search)
        self.btn_loc.clicked.connect(self.loc_cv_signal.emit)
        self.table_view.doubleClicked.connect(self.open_sua_dialog)
        self.table_view.clicked.connect(self.on_table_click)

    def handle_search(self):
        self.tim_kiem_signal.emit(self.search_input.text().strip())

    def set_table_model(self, model):
        self.table_view.setModel(model)
        self.table_view.setColumnHidden(0, True) 
        widths = [0, 50, 100, 100, 170, 135, 100, 340, 180, 100, 110, 120, 160] 
        for i, w in enumerate(widths):
            if i < model.columnCount():
                self.table_view.setColumnWidth(i, w)
        self.lbl_count.setText(f"Đang xem: {model.rowCount()} mục")

    def set_nhan_su_list(self, ds):
        self.ds_nhan_su = ds or []

    def set_loai_van_ban_list(self, ds):
        self.ds_loai_van_ban = ds or []
        self.cb_loai_vb.blockSignals(True)
        self.cb_loai_vb.clear()
        self.cb_loai_vb.addItem("Tất cả", None)
        for item in self.ds_loai_van_ban:
            ten = item.get('ten_loai') or item.get('ten') or item.get('TenLoai') or "Chưa rõ"
            id_val = item.get('id') or item.get('Id')
            self.cb_loai_vb.addItem(ten, id_val)
        self.cb_loai_vb.blockSignals(False)

    def show_status(self, msg: str):
        self.statusBar().showMessage(msg, 5000)

    def show_error(self, msg: str):
        QMessageBox.critical(self, "Lỗi", msg)

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

    def open_giao_viec_dialog(self):
        index = self.table_view.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một văn bản để phân công!")
            return
        row_data = self.table_view.model().get_row(index.row())
        self.giao_viec_signal.emit(row_data["id"])

    def open_them_dialog(self):
        self.nap_danh_muc_signal.emit()
        dialog = QDialog(self)
        dialog.setWindowTitle("Tiếp nhận Công văn Đến")
        dialog.setFixedWidth(680)
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        form.setSpacing(12)
        style = "padding: 6px 8px; border: 1px solid #b0b0b0; border-radius: 4px;"

        loai_vb_cb = QComboBox()
        for item in self.ds_loai_van_ban:
            ten = item.get('ten_loai') or item.get('ten') or item.get('TenLoai') or "Chưa rõ"
            id_val = item.get('id') or item.get('Id')
            loai_vb_cb.addItem(ten, id_val)

        # ========== THAY COMBOBOX TRẠNG THÁI BẰNG LABEL ==========
        trang_thai_label = QLabel("Chờ phân công")
        trang_thai_label.setStyleSheet("padding: 6px 8px; background-color: #f0f0f0; border-radius: 4px;")
        trang_thai_value = 1  # Chờ phân công
        # ========================================================

        muc_do_cb = QComboBox()
        muc_do_cb.addItems(["Thường", "Khẩn", "Hỏa tốc"])

        inputs = {
            "ngay_den": QDateEdit(calendarPopup=True, date=QDate.currentDate()),
            "tac_gia": QLineEdit(),
            "so_ky_hieu": QLineEdit(),
            "ngay_van_ban": QDateEdit(calendarPopup=True, date=QDate.currentDate()),
            "han_xu_ly": QDateEdit(calendarPopup=True, date=QDate.currentDate().addDays(7)),
            "trich_yeu": QTextEdit(),
            "nguoi_xu_ly": QComboBox(), 
            "ghi_chu": QLineEdit()
        }
        
        inputs["ngay_den"].setDisplayFormat("dd/MM/yyyy")
        inputs["ngay_van_ban"].setDisplayFormat("dd/MM/yyyy")
        inputs["han_xu_ly"].setDisplayFormat("dd/MM/yyyy")
        
        inputs["nguoi_xu_ly"].addItem("-- Chưa phân công --", None)
        for ns in self.ds_nhan_su:
            ten_nv = ns.get('ho_ten', ns.get('ten', ''))
            inputs["nguoi_xu_ly"].addItem(ten_nv, ns['id'])

        for key, w in inputs.items():
            if isinstance(w, (QLineEdit, QTextEdit)):
                w.setStyleSheet(style)
        inputs["trich_yeu"].setFixedHeight(80)

        file_layout = QHBoxLayout()
        self.them_file_edit = QLineEdit()
        self.them_file_edit.setReadOnly(True)
        self.them_file_edit.setPlaceholderText("Chưa chọn file...")
        btn_file = QPushButton("📎 Chọn file")
        btn_file.clicked.connect(lambda: self._chon_file(self.them_file_edit, 'them'))
        file_layout.addWidget(self.them_file_edit)
        file_layout.addWidget(btn_file)

        form.addRow("Ngày nhận (*):", inputs["ngay_den"])
        form.addRow("Nơi gửi / Tác giả (*):", inputs["tac_gia"])
        form.addRow("Số ký hiệu (*):", inputs["so_ky_hieu"])
        form.addRow("Ngày trên văn bản:", inputs["ngay_van_ban"])
        form.addRow("Hạn xử lý (Deadline):", inputs["han_xu_ly"])
        form.addRow("Trích yếu nội dung:", inputs["trich_yeu"])
        form.addRow("Loại văn bản:", loai_vb_cb)
        form.addRow("Trạng thái:", trang_thai_label)   # <--- dùng label
        form.addRow("Mức độ:", muc_do_cb)
        form.addRow("Đơn vị/Người chủ trì:", inputs["nguoi_xu_ly"])
        form.addRow("File đính kèm:", file_layout)
        form.addRow("Ghi chú thêm:", inputs["ghi_chu"])

        layout.addLayout(form)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            if not inputs["tac_gia"].text().strip() or not inputs["so_ky_hieu"].text().strip():
                QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập đầy đủ Nơi gửi và Số ký hiệu!")
                return

            data = {
                "ngay_den": inputs["ngay_den"].date().toString("yyyy-MM-dd"),
                "tac_gia": inputs["tac_gia"].text().strip(),
                "so_ky_hieu": inputs["so_ky_hieu"].text().strip(),
                "ngay_van_ban": inputs["ngay_van_ban"].date().toString("yyyy-MM-dd"),
                "han_xu_ly": inputs["han_xu_ly"].date().toString("yyyy-MM-dd"),
                "trich_yeu": inputs["trich_yeu"].toPlainText().strip(),
                "phan_loai_id": loai_vb_cb.currentData(),
                "trang_thai": trang_thai_value,   # 1 = Chờ phân công
                "muc_do": muc_do_cb.currentText(),
                "nguoi_xu_ly": inputs["nguoi_xu_ly"].currentData(), 
                "ghi_chu": inputs["ghi_chu"].text().strip(),
                "file_dinh_kem": self._them_file_path
            }
            self.them_cv_signal.emit(data)

    def open_sua_dialog(self):
        index = self.table_view.currentIndex()
        if not index.isValid(): return
        row_data = self.table_view.model().get_row(index.row())
        if not row_data: return

        self.nap_danh_muc_signal.emit()
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Chỉnh sửa Văn bản - ID: {row_data.get('id')}")
        dialog.setFixedWidth(680)
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        form.setSpacing(12)
        style = "padding: 6px 8px; border: 1px solid #b0b0b0; border-radius: 4px;"

        loai_vb_cb = QComboBox()
        for item in self.ds_loai_van_ban:
            ten = item.get('ten_loai') or item.get('ten') or item.get('TenLoai') or "Chưa rõ"
            id_val = item.get('id') or item.get('Id')
            loai_vb_cb.addItem(ten, id_val)
            
        phan_loai_id = row_data.get("phan_loai_id")
        if phan_loai_id is not None:
            for i in range(loai_vb_cb.count()):
                if str(loai_vb_cb.itemData(i)) == str(phan_loai_id):
                    loai_vb_cb.setCurrentIndex(i)
                    break

        trang_thai_cb = QComboBox()
        trang_thai_cb.addItems(["Mới tiếp nhận", "Chờ sếp phân công", "Đang xử lý", "Hoàn thành"])
        map_tt = {0: "Mới tiếp nhận", 1: "Chờ sếp phân công", 2: "Đang xử lý", 3: "Hoàn thành"}
        trang_thai_cb.setCurrentText(map_tt.get(row_data.get("trang_thai"), "Mới tiếp nhận"))

        muc_do_cb = QComboBox()
        muc_do_cb.addItems(["Thường", "Khẩn", "Hỏa tốc"])
        idx_muc = muc_do_cb.findText(row_data.get("muc_do", "Thường"))
        if idx_muc >= 0: muc_do_cb.setCurrentIndex(idx_muc)

        inputs = {
            "ngay_den": QDateEdit(calendarPopup=True),
            "tac_gia": QLineEdit(str(row_data.get("tac_gia", ""))),
            "so_ky_hieu": QLineEdit(str(row_data.get("so_ky_hieu", ""))),
            "ngay_van_ban": QDateEdit(calendarPopup=True),
            "han_xu_ly": QDateEdit(calendarPopup=True),
            "trich_yeu": QTextEdit(str(row_data.get("trich_yeu", ""))),
            "nguoi_xu_ly": QComboBox(),
            "ghi_chu": QLineEdit(str(row_data.get("ghi_chu", "")))
        }

        inputs["ngay_den"].setDisplayFormat("dd/MM/yyyy")
        inputs["ngay_van_ban"].setDisplayFormat("dd/MM/yyyy")
        inputs["han_xu_ly"].setDisplayFormat("dd/MM/yyyy")

        def set_date(widget, value):
            if value:
                try: widget.setDate(QDate.fromString(str(value).split()[0], "yyyy-MM-dd"))
                except: widget.setDate(QDate.currentDate())
            else: widget.setDate(QDate.currentDate())

        set_date(inputs["ngay_den"], row_data.get("ngay_den"))
        set_date(inputs["ngay_van_ban"], row_data.get("ngay_van_ban"))
        set_date(inputs["han_xu_ly"], row_data.get("han_xu_ly"))

        inputs["nguoi_xu_ly"].addItem("-- Chưa phân công --", None)
        for ns in self.ds_nhan_su:
            ten_nv = ns.get('ho_ten', ns.get('ten', ''))
            inputs["nguoi_xu_ly"].addItem(ten_nv, ns['id'])
            
        nguoi_xu_ly_cu = row_data.get("nguoi_xu_ly") 
        if nguoi_xu_ly_cu is not None:
            found = False
            for i in range(inputs["nguoi_xu_ly"].count()):
                if str(inputs["nguoi_xu_ly"].itemData(i)) == str(nguoi_xu_ly_cu):
                    inputs["nguoi_xu_ly"].setCurrentIndex(i)
                    found = True
                    break
            if not found:
                idx_text = inputs["nguoi_xu_ly"].findText(str(nguoi_xu_ly_cu))
                if idx_text >= 0:
                    inputs["nguoi_xu_ly"].setCurrentIndex(idx_text)

        for w in inputs.values():
            if isinstance(w, (QLineEdit, QTextEdit)): w.setStyleSheet(style)
        inputs["trich_yeu"].setFixedHeight(80)

        file_layout = QHBoxLayout()
        self.sua_file_edit = QLineEdit()
        self.sua_file_edit.setReadOnly(True)
        old_file = row_data.get("file_dinh_kem")
        self._sua_old_file = old_file
        self._sua_file_path = old_file
        if old_file: self.sua_file_edit.setText(os.path.basename(old_file))
        else: self.sua_file_edit.setPlaceholderText("Không có file")
        
        btn_chon = QPushButton("📎 Chọn file")
        btn_xoa_file = QPushButton("Xóa file")
        btn_chon.clicked.connect(lambda: self._chon_file(self.sua_file_edit, 'sua'))
        btn_xoa_file.clicked.connect(self._xoa_file_sua)
        file_layout.addWidget(self.sua_file_edit)
        file_layout.addWidget(btn_chon)
        file_layout.addWidget(btn_xoa_file)

        form.addRow("Ngày nhận:", inputs["ngay_den"])
        form.addRow("Nơi gửi / Tác giả:", inputs["tac_gia"])
        form.addRow("Số ký hiệu:", inputs["so_ky_hieu"])
        form.addRow("Ngày trên văn bản:", inputs["ngay_van_ban"])
        form.addRow("Hạn xử lý (Deadline):", inputs["han_xu_ly"])
        form.addRow("Trích yếu nội dung:", inputs["trich_yeu"])
        form.addRow("Loại văn bản:", loai_vb_cb)
        form.addRow("Trạng thái:", trang_thai_cb)
        form.addRow("Mức độ:", muc_do_cb)
        form.addRow("Đơn vị/Người chủ trì:", inputs["nguoi_xu_ly"])
        form.addRow("File đính kèm:", file_layout)
        form.addRow("Ghi chú thêm:", inputs["ghi_chu"])

        layout.addLayout(form)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            if self._sua_file_path != self._sua_old_file and self._sua_old_file and os.path.exists(self._sua_old_file):
                try: os.remove(self._sua_old_file)
                except: pass

            map_tt_reverse = {"Mới tiếp nhận": 0, "Chờ sếp phân công": 1, "Đang xử lý": 2, "Hoàn thành": 3}
            new_data = {
                "ngay_den": inputs["ngay_den"].date().toString("yyyy-MM-dd"),
                "tac_gia": inputs["tac_gia"].text().strip(),
                "so_ky_hieu": inputs["so_ky_hieu"].text().strip(),
                "ngay_van_ban": inputs["ngay_van_ban"].date().toString("yyyy-MM-dd"),
                "han_xu_ly": inputs["han_xu_ly"].date().toString("yyyy-MM-dd"),
                "trich_yeu": inputs["trich_yeu"].toPlainText().strip(),
                "phan_loai_id": loai_vb_cb.currentData(),
                "trang_thai": map_tt_reverse.get(trang_thai_cb.currentText(), 0),
                "muc_do": muc_do_cb.currentText(),
                "nguoi_xu_ly": inputs["nguoi_xu_ly"].currentData(),
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
        model = self.table_view.model()
        if not model: return
        file_path = model.data(index, Qt.ItemDataRole.UserRole)
        if file_path and isinstance(file_path, str) and os.path.exists(file_path):
            try: QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.abspath(file_path)))
            except Exception as e: self.show_error(f"Không thể mở file: {str(e)}")