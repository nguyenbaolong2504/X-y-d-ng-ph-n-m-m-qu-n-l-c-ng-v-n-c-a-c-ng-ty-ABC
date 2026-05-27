import os, shutil, re
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate, pyqtSignal, Qt, QUrl
from PyQt6.QtGui import QFont, QTextDocument, QPageLayout, QDesktopServices
from PyQt6.QtPrintSupport import QPrinter, QPrintPreviewDialog

class MainWindowDi(QMainWindow):
    them_cv_signal = pyqtSignal(dict)
    sua_cv_signal = pyqtSignal(int, dict)
    xoa_cv_signal = pyqtSignal(int)
    tim_kiem_signal = pyqtSignal(str)
    loc_cv_signal = pyqtSignal(str, str) 
    xuat_excel_signal = pyqtSignal()
    nap_dulieu_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống Quản lý Công văn Phát hành (Đi)")
        self.setGeometry(100, 100, 1500, 850)
        self.setStyleSheet("""
            QMainWindow { background-color: #f8f9fa; }
            QPushButton { padding: 8px 15px; border-radius: 5px; font-weight: bold; font-size: 13px; }
            QLineEdit, QComboBox, QDateEdit, QTextEdit { border: 1px solid #ced4da; padding: 6px; border-radius: 4px; }
            QHeaderView::section { background-color: #e9ecef; font-weight: bold; border: 1px solid #dee2e6; padding: 8px; }
            QTableView { border: 1px solid #dee2e6; gridline-color: #e9ecef; selection-background-color: #cce5ff; selection-color: black; }
        """)
        self.ds_loai_van_ban = []   # mỗi item có 'id','ten_loai','ma_loai'
        self.ds_don_vi = []
        self.ds_nhan_su = []
        self.ds_cv_den = []
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)
        
        header_lbl = QLabel("📤 QUẢN LÝ CÔNG VĂN PHÁT HÀNH (ĐI)")
        header_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e3a8a; padding: 10px; background-color: #fff; border-radius: 6px; border: 1px solid #ddd;")
        main_layout.addWidget(header_lbl)
        
        toolbar = QHBoxLayout()
        self.btn_them = QPushButton("➕ Thêm mới")
        self.btn_them.setStyleSheet("background-color: #28a745; color: white; border: none;")
        self.btn_xoa = QPushButton("❌ Xóa")
        self.btn_xoa.setStyleSheet("background-color: #dc3545; color: white; border: none;")
        self.btn_in = QPushButton("🖨️ In ấn")
        self.btn_in.setStyleSheet("background-color: #6c757d; color: white; border: none;")
        self.btn_excel = QPushButton("📊 Xuất Excel")
        self.btn_excel.setStyleSheet("background-color: #17a2b8; color: white; border: none;")
        self.btn_refresh = QPushButton("🔄 Làm mới")       
        for btn in [self.btn_them, self.btn_xoa, self.btn_in, self.btn_excel, self.btn_refresh]:
            toolbar.addWidget(btn)       
        toolbar.addStretch()        
        
        toolbar.addWidget(QLabel("Từ ngày:"))
        self.date_tu = QDateEdit(calendarPopup=True, date=QDate.currentDate().addMonths(-1))
        self.date_tu.setDisplayFormat("dd/MM/yyyy")
        toolbar.addWidget(self.date_tu)     
        
        toolbar.addWidget(QLabel("đến ngày:"))
        self.date_den = QDateEdit(calendarPopup=True, date=QDate.currentDate())
        self.date_den.setDisplayFormat("dd/MM/yyyy")
        toolbar.addWidget(self.date_den)     
        
        self.btn_loc = QPushButton("🔍 Lọc")
        self.btn_loc.setStyleSheet("background-color: #007bff; color: white; border: none;")
        toolbar.addWidget(self.btn_loc)
        main_layout.addLayout(toolbar)
        
        search_layout = QHBoxLayout()
        self.lbl_count = QLabel("Đang xem: 0 mục")
        self.lbl_count.setStyleSheet("font-weight: bold; color: #495057;")
        search_layout.addWidget(self.lbl_count)
        search_layout.addStretch()      
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập số đi, ký hiệu, nơi nhận...")
        self.search_input.setFixedWidth(350)
        self.btn_search = QPushButton("Tìm kiếm")
        self.btn_search.setStyleSheet("background-color: #e2e6ea; border: 1px solid #ced4da; color: #333;")
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.btn_search)
        main_layout.addLayout(search_layout)
        
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)    
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        main_layout.addWidget(self.table_view)
        
        # Kết nối Signal
        self.btn_them.clicked.connect(self.open_them_dialog)
        self.btn_xoa.clicked.connect(self.confirm_delete)
        self.btn_in.clicked.connect(self.print_table)
        self.btn_excel.clicked.connect(self.xuat_excel_signal.emit)
        self.btn_refresh.clicked.connect(self.nap_dulieu_signal.emit)
        self.btn_loc.clicked.connect(lambda: self.loc_cv_signal.emit(
            self.date_tu.date().toString("yyyy-MM-dd"), 
            self.date_den.date().toString("yyyy-MM-dd")
        ))
        self.btn_search.clicked.connect(lambda: self.tim_kiem_signal.emit(self.search_input.text().strip()))
        self.search_input.returnPressed.connect(lambda: self.tim_kiem_signal.emit(self.search_input.text().strip()))
        self.table_view.doubleClicked.connect(self.open_sua_dialog)

    def show_status(self, message):
        self.statusBar().showMessage(message, 4000)

    def show_error(self, msg):
        QMessageBox.critical(self, "Lỗi", msg)

    def set_table_model(self, model):
        self.table_view.setModel(model)
        self.table_view.setColumnHidden(0, True)
        widths = [0, 80, 70, 120, 110, 200, 350, 120, 100, 120]  # 10 cột
        for i, w in enumerate(widths):
            if i < model.columnCount():
                self.table_view.setColumnWidth(i, w)
        self.lbl_count.setText(f"Đang xem: {model.rowCount()} mục")

    def set_loai_van_ban_list(self, ds):
        self.ds_loai_van_ban = ds or []
        
    def set_don_vi_list(self, ds):
        self.ds_don_vi = ds or []
        
    def set_nhan_su_list(self, ds):
        self.ds_nhan_su = ds or []

    def set_cv_den_list(self, ds):
        self.ds_cv_den = ds or []

    def _to_qdate(self, value):
        if isinstance(value, str) and value:
            try: return QDate.fromString(value.split(' ')[0], "yyyy-MM-dd")
            except: pass
        return QDate.currentDate()

    def _chon_file(self, line_edit: QLineEdit):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file đính kèm", "", "All Files (*.*)")
        if file_path:
            line_edit.setText(file_path)

    def create_input_dialog(self, title, row_data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setFixedWidth(700)
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        form.setSpacing(12)

        in_nam = QLineEdit(str(row_data.get("Nam", QDate.currentDate().year())) if row_data else str(QDate.currentDate().year()))
        in_kh = QLineEdit(row_data.get("KyHieu", "") if row_data else "")
        in_ngay = QDateEdit(calendarPopup=True)
        in_ngay.setDisplayFormat("dd/MM/yyyy")
        in_ngay.setDate(self._to_qdate(row_data.get("NgayKy")) if row_data else QDate.currentDate())
        
        in_loai = QComboBox()
        for item in self.ds_loai_van_ban:
            in_loai.addItem(item['ten_loai'], item['id'])
        if row_data and row_data.get('PhanLoaiId'):
            idx = in_loai.findData(row_data.get('PhanLoaiId'))
            if idx >= 0: in_loai.setCurrentIndex(idx)

        def auto_detect_loai(kh_text):
            if not kh_text:
                return
            m = re.match(r"^\d+/([A-Za-z]+)-", kh_text.strip())
            if m:
                ma = m.group(1).upper()
                for i, item in enumerate(self.ds_loai_van_ban):
                    if item.get('ma_loai', '').upper() == ma:
                        in_loai.setCurrentIndex(i)
                        break
        in_kh.textChanged.connect(auto_detect_loai)

        # Đơn vị soạn (comboBox)
        in_donvi = QComboBox()
        in_donvi.addItem("-- Chọn Đơn vị --", None)
        for dv in self.ds_don_vi:
            in_donvi.addItem(dv['ten_don_vi'], dv['id'])
        if row_data and row_data.get("DonViSoanId"):
            idx = in_donvi.findData(row_data.get("DonViSoanId"))
            if idx >= 0: in_donvi.setCurrentIndex(idx)

        # Người ký
        in_nguoiky = QComboBox()
        in_nguoiky.addItem("-- Chọn Người ký --", None)
        for ns in self.ds_nhan_su:
            in_nguoiky.addItem(ns['ten'], ns['id'])
        if row_data and row_data.get("NguoiKyId"):
            idx = in_nguoiky.findData(row_data.get("NguoiKyId"))
            if idx >= 0: in_nguoiky.setCurrentIndex(idx)

        muc_do_cb = QComboBox()
        muc_do_cb.addItems(["Thường", "Khẩn", "Hỏa tốc"])
        if row_data and row_data.get('MucDo'): muc_do_cb.setCurrentText(row_data.get('MucDo'))

        trang_thai_cb = QComboBox()
        trang_thai_cb.addItems(["Dự thảo", "Chờ duyệt", "Đã ký", "Đã phát hành"])
        if row_data and 'TrangThai' in row_data:
            trang_thai_cb.setCurrentText(row_data.get('TrangThai'))

        in_vb_den_goc = QComboBox()
        in_vb_den_goc.addItem("-- Không --", None)
        for cv in self.ds_cv_den:
            in_vb_den_goc.addItem(f"{cv['so_ky_hieu']} - {cv['trich_yeu'][:30]}...", cv['id'])
        if row_data and row_data.get("VanBanDenGocId"):
            idx = in_vb_den_goc.findData(row_data.get("VanBanDenGocId"))
            if idx >= 0: in_vb_den_goc.setCurrentIndex(idx)

        in_trichyeu = QTextEdit(row_data.get("TrichYeu", "") if row_data else "")
        in_trichyeu.setFixedHeight(60)
        in_noinhan = QTextEdit(row_data.get("NoiNhan", "") if row_data else "")
        in_noinhan.setFixedHeight(50)
        in_hoso = QLineEdit(row_data.get("GhiChu", "") if row_data else "")

        file_layout = QHBoxLayout()
        in_file_path = QLineEdit()
        in_file_path.setReadOnly(True)
        if row_data and row_data.get("FilePath"):
            in_file_path.setText(os.path.basename(row_data["FilePath"]))
            in_file_path.setToolTip(row_data["FilePath"])
        else:
            in_file_path.setPlaceholderText("Chưa chọn file")
        btn_browse = QPushButton("📎 Chọn")
        btn_browse.clicked.connect(lambda: self._chon_file(in_file_path))
        file_layout.addWidget(in_file_path)
        file_layout.addWidget(btn_browse)

        # Layout
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Năm:"))
        row1.addWidget(in_nam)
        row1.addWidget(QLabel("Ký hiệu:"))
        row1.addWidget(in_kh)
        row1.addWidget(QLabel("Ngày ký:"))
        row1.addWidget(in_ngay)
        form.addRow(row1)
        form.addRow("Loại văn bản:", in_loai)
        form.addRow("Trả lời VB đến:", in_vb_den_goc)
        form.addRow("Đơn vị soạn:", in_donvi)
        form.addRow("Người ký:", in_nguoiky)
        form.addRow("Mức độ:", muc_do_cb)
        form.addRow("Trạng thái:", trang_thai_cb)
        form.addRow("Trích yếu:", in_trichyeu)
        form.addRow("Nơi nhận:", in_noinhan)
        form.addRow("File đính kèm:", file_layout)
        form.addRow("Hồ sơ / Ghi chú:", in_hoso)
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            kh = in_kh.text().strip()
            loai_id = in_loai.currentData()
            
            # Kiểm tra không khớp mã loại
            m = re.match(r"^\d+/([A-Za-z]+)-", kh)
            if m and loai_id:
                ma = m.group(1).upper()
                loai_chon = next((item for item in self.ds_loai_van_ban if item['id'] == loai_id), None)
                if loai_chon and loai_chon.get('ma_loai', '').upper() != ma:
                    msg = (f"Ký hiệu chứa mã loại '{ma}' nhưng loại văn bản được chọn là "
                           f"'{loai_chon['ten_loai']}' (mã '{loai_chon.get('ma_loai', '?')}').\n"
                           "Bạn có muốn lưu với loại hiện tại không?")
                    reply = QMessageBox.question(dialog, "Cảnh báo không khớp", msg,
                                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if reply == QMessageBox.StandardButton.No:
                        return None

            # Lấy dữ liệu, đảm bảo ID là số hoặc None
            phan_loai_id = loai_id
            don_vi_id = in_donvi.currentData()
            nguoi_ky_id = in_nguoiky.currentData()
            vb_den_goc_id = in_vb_den_goc.currentData()
            file_path = in_file_path.text().strip()
            if not file_path and row_data:
                file_path = row_data.get("FilePath")
            elif file_path and os.path.isabs(file_path):
                pass
            elif file_path and row_data:
                file_path = row_data.get("FilePath")

            return {
                "Nam": int(in_nam.text() or QDate.currentDate().year()),
                "KyHieu": kh,
                "NgayKy": in_ngay.date().toString("yyyy-MM-dd"),
                "PhanLoaiId": phan_loai_id,
                "DonViSoanId": don_vi_id,
                "NguoiKyId": nguoi_ky_id,
                "VanBanDenGocId": vb_den_goc_id,
                "MucDo": muc_do_cb.currentText(),
                "TrangThaiChuyen": 1,   # 1: đã phát hành (tạm)
                "TrichYeu": in_trichyeu.toPlainText().strip(),
                "NoiNhan": in_noinhan.toPlainText().strip(),
                "FilePath": file_path if file_path else None,
                "GhiChu": in_hoso.text().strip(),
                "NguoiTaoId": 1  # tạm, sau lấy từ session
            }
        return None

    def open_them_dialog(self):
        data = self.create_input_dialog("THÊM MỚI VĂN BẢN ĐI")
        if data:
            self.them_cv_signal.emit(data)

    def open_sua_dialog(self):
        idx = self.table_view.currentIndex()
        if not idx.isValid(): return
        row_data = self.table_view.model().get_row(idx.row())
        data = self.create_input_dialog(f"CẬP NHẬT: {row_data.get('KyHieu','')}", row_data)
        if data:
            self.sua_cv_signal.emit(row_data["Id"], data)

    def confirm_delete(self):
        idx = self.table_view.currentIndex()
        if not idx.isValid():
            self.show_error("Vui lòng chọn dòng cần xóa!")
            return
        data = self.table_view.model().get_row(idx.row())
        if QMessageBox.question(self, "Xác nhận", f"Xóa công văn '{data.get('KyHieu','')}'?") == QMessageBox.StandardButton.Yes:
            self.xoa_cv_signal.emit(data["Id"])

    def print_table(self):
        model = self.table_view.model()
        if not model or model.rowCount() == 0: return
        html = "<html><head><style>table { width: 100%; border-collapse: collapse; } th, td { border: 1px solid black; padding: 8px; text-align: center; } th { background-color: #f2f2f2; }</style></head><body>"
        html += "<h2 style='text-align: center;'>DANH MỤC CÔNG VĂN PHÁT HÀNH</h2><table><tr><th>STT</th><th>Số đi</th><th>Ký hiệu</th><th>Ngày ký</th><th>Nơi nhận</th><th>Trích yếu</th><th>Mức độ</th></tr>"
        for i in range(model.rowCount()):
            d = model.get_row(i)
            html += f"<tr><td>{i+1}</td><td>{d.get('SoPhatHanh','')}</td><td>{d.get('KyHieu','')}</td><td>{d.get('NgayKy','')}</td><td>{d.get('NoiNhan','')}</td><td>{d.get('TrichYeu','')}</td><td>{d.get('MucDo','Thường')}</td></tr>"
        html += "</table></body></html>"
        self.doc = QTextDocument()
        self.doc.setHtml(html)
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setPageOrientation(QPageLayout.Orientation.Landscape)
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(lambda p: self.doc.print(p))
        preview.exec()