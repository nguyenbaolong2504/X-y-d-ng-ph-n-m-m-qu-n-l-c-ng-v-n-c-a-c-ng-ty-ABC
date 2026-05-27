import os
import shutil
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate, pyqtSignal, Qt

class ChonNguoiNhanDialog(QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.setWindowTitle("Chọn người nhận")
        self.resize(600, 500)
        self.setModal(True)
        self.selected_ids = set()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout()
        group_btn_layout = QHBoxLayout()
        self.btn_toan_cong_ty = QPushButton("📢 Toàn công ty")
        self.btn_truong_phong = QPushButton("👔 Tất cả trưởng phòng")
        group_btn_layout.addWidget(self.btn_toan_cong_ty)
        group_btn_layout.addWidget(self.btn_truong_phong)
        layout.addLayout(group_btn_layout)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Phòng ban / Nhân viên")
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        layout.addWidget(self.tree)

        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("OK")
        self.btn_cancel = QPushButton("Hủy")
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.btn_toan_cong_ty.clicked.connect(self.chon_toan_cong_ty)
        self.btn_truong_phong.clicked.connect(self.chon_truong_phong)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def load_data(self):
        donvi_list = self.model.get_donvi_list()
        self.tree.clear()
        for dv in donvi_list:
            dv_item = QTreeWidgetItem([dv['ten']])
            dv_item.setData(0, Qt.ItemDataRole.UserRole, {"type": "donvi", "id": dv['id']})
            self.tree.addTopLevelItem(dv_item)
            # Thêm mục "Chọn tất cả nhân viên phòng này"
            select_all_item = QTreeWidgetItem([f"    📌 Chọn tất cả nhân viên phòng {dv['ten']}"])
            select_all_item.setData(0, Qt.ItemDataRole.UserRole, {"type": "select_all_donvi", "id": dv['id']})
            dv_item.addChild(select_all_item)
            # Thêm từng nhân viên
            nv_list = self.model.get_canbo_by_donvi(dv['id'])
            for nv in nv_list:
                nv_item = QTreeWidgetItem([f"        {nv['ten']}"])
                nv_item.setData(0, Qt.ItemDataRole.UserRole, {"type": "canbo", "id": nv['id'], "ten": nv['ten']})
                dv_item.addChild(nv_item)
        self.tree.expandAll()

    def chon_toan_cong_ty(self):
        all_cb = self.model.get_all_canbo()
        self.selected_ids = {cb['id'] for cb in all_cb}
        for i in range(self.tree.topLevelItemCount()):
            dv_item = self.tree.topLevelItem(i)
            for j in range(dv_item.childCount()):
                item = dv_item.child(j)
                user_data = item.data(0, Qt.ItemDataRole.UserRole)
                if user_data and user_data.get("type") == "canbo":
                    item.setSelected(True)
                else:
                    item.setSelected(False)
        QMessageBox.information(self, "Thông báo", f"Đã chọn {len(self.selected_ids)} người (toàn công ty)")

    def chon_truong_phong(self):
        tp_list = self.model.get_all_truongphong()
        self.selected_ids = {tp['id'] for tp in tp_list}
        for i in range(self.tree.topLevelItemCount()):
            dv_item = self.tree.topLevelItem(i)
            for j in range(dv_item.childCount()):
                item = dv_item.child(j)
                user_data = item.data(0, Qt.ItemDataRole.UserRole)
                if user_data and user_data.get("type") == "canbo":
                    if user_data['id'] in self.selected_ids:
                        item.setSelected(True)
                    else:
                        item.setSelected(False)
                else:
                    item.setSelected(False)
        QMessageBox.information(self, "Thông báo", f"Đã chọn {len(self.selected_ids)} trưởng phòng")

    def get_selected_nguoi_nhan(self):
        self.selected_ids = set()
        selected_names = []
        for i in range(self.tree.topLevelItemCount()):
            dv_item = self.tree.topLevelItem(i)
            for j in range(dv_item.childCount()):
                item = dv_item.child(j)
                if item.isSelected():
                    user_data = item.data(0, Qt.ItemDataRole.UserRole)
                    if user_data:
                        if user_data.get("type") == "canbo":
                            self.selected_ids.add(user_data["id"])
                            selected_names.append(user_data["ten"])
                        elif user_data.get("type") == "select_all_donvi":
                            donvi_id = user_data["id"]
                            nv_list = self.model.get_canbo_by_donvi(donvi_id)
                            for nv in nv_list:
                                self.selected_ids.add(nv["id"])
                                selected_names.append(nv["ten"])
        return list(self.selected_ids), ", ".join(selected_names) if selected_names else ""


class MainWindowNoiBo(QMainWindow):
    them_cv_signal = pyqtSignal(dict)
    sua_cv_signal = pyqtSignal(int, dict)
    xoa_cv_signal = pyqtSignal(int)
    tim_kiem_signal = pyqtSignal(str)
    nap_dulieu_signal = pyqtSignal()
    xuat_excel_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý Văn bản nội bộ")
        self.setGeometry(100, 100, 1400, 750)
        self.setStyleSheet("""
            QMainWindow { background-color: #ffffff; }
            QPushButton { padding: 6px 12px; border: 1px solid #ccc; border-radius: 3px; background-color: #f8f9fa; }
            QPushButton:hover { background-color: #e2e6ea; }
            QLineEdit, QComboBox, QDateEdit, QTextEdit { border: 1px solid #ccc; padding: 5px; border-radius: 3px; }
            QHeaderView::section { background-color: #f0f2f5; border: 1px solid #ddd; padding: 6px; font-weight: bold; }
            QTableView { border: 1px solid #ddd; gridline-color: #eee; }
        """)
        self.loai_list = []
        self.donvi_list = []
        self.canbo_list = []
        self.model = None
        self.current_file_path = None
        self.selected_nguoi_nhan_ids = []
        self.selected_nguoi_nhan_text = ""
        self.setup_ui()

    def set_model(self, model):
        self.model = model

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        header_lbl = QLabel("🗂️ Danh mục văn bản, thông tin nội bộ")
        header_lbl.setStyleSheet("background-color: #f4f5f7; border: 1px solid #ddd; padding: 10px; font-size: 15px; font-weight: bold; color: #333;")
        main_layout.addWidget(header_lbl)

        toolbar_layout = QHBoxLayout()
        self.btn_them = QPushButton("➕ Thêm")
        self.btn_them.setStyleSheet("background-color: #4CAF50; color: white; border: none; font-weight: bold;")
        self.btn_xoa = QPushButton("❌ Xóa")
        self.btn_in = QPushButton("🖨️ In")
        self.btn_excel = QPushButton("📊 Excel")
        self.btn_refresh = QPushButton("🔄 Làm mới")
        for btn in [self.btn_them, self.btn_xoa, self.btn_in, self.btn_excel, self.btn_refresh]:
            toolbar_layout.addWidget(btn)
        toolbar_layout.addStretch()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm theo số ký hiệu, trích yếu...")
        self.search_input.setFixedWidth(300)
        toolbar_layout.addWidget(self.search_input)
        main_layout.addLayout(toolbar_layout)

        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.verticalHeader().setVisible(False)
        main_layout.addWidget(self.table_view)

        self.btn_them.clicked.connect(self.open_them_dialog)
        self.btn_xoa.clicked.connect(self.confirm_delete)
        self.btn_refresh.clicked.connect(self.nap_dulieu_signal.emit)
        self.btn_excel.clicked.connect(self.xuat_excel_signal.emit)
        self.table_view.doubleClicked.connect(self.open_sua_dialog)
        self.search_input.returnPressed.connect(lambda: self.tim_kiem_signal.emit(self.search_input.text()))
        self.search_input.textChanged.connect(lambda text: self.tim_kiem_signal.emit(text) if len(text)==0 else None)

    def set_danh_muc(self, loai_list, donvi_list, canbo_list):
        self.loai_list = loai_list
        self.donvi_list = donvi_list
        self.canbo_list = canbo_list

    def set_table_model(self, model):
        self.table_view.setModel(model)
        self.table_view.setColumnHidden(0, True)
        self.table_view.setColumnWidth(1, 120)
        self.table_view.setColumnWidth(2, 120)
        self.table_view.setColumnWidth(3, 150)
        self.table_view.setColumnWidth(4, 300)
        self.table_view.setColumnWidth(5, 150)
        self.table_view.setColumnWidth(6, 120)
        self.table_view.setColumnWidth(7, 150)
        self.table_view.setColumnWidth(8, 200)

    def _get_form_inputs(self, data=None):
        if data is None:
            data = {}
        
        cb_loai = QComboBox()
        for item in self.loai_list:
            cb_loai.addItem(item['ten'], item['id'])
        if data.get("LoaiVanBan"):
            idx = cb_loai.findText(data["LoaiVanBan"])
            if idx >= 0:
                cb_loai.setCurrentIndex(idx)

        cb_donvi = QComboBox()
        for item in self.donvi_list:
            cb_donvi.addItem(item['ten'], item['id'])
        if data.get("DonViSoan"):
            idx = cb_donvi.findText(data["DonViSoan"])
            if idx >= 0:
                cb_donvi.setCurrentIndex(idx)

        cb_nguoiky = QComboBox()
        for item in self.canbo_list:
            cb_nguoiky.addItem(item['ten'], item['id'])
        if data.get("NguoiKy"):
            idx = cb_nguoiky.findText(data["NguoiKy"])
            if idx >= 0:
                cb_nguoiky.setCurrentIndex(idx)

        inputs = {
            "so_ky_hieu": QLineEdit(str(data.get("KyHieu", ""))),
            "ngay_ban_hanh": QDateEdit(calendarPopup=True),
            "loai_van_ban": cb_loai,
            "trich_yeu": QTextEdit(str(data.get("TrichYeu", ""))),
            "don_vi_ban_hanh": cb_donvi,
            "nguoi_ky": cb_nguoiky,
            "ghi_chu": QLineEdit(str(data.get("GhiChu", ""))),
            "file_dinh_kem": QLineEdit(),
            "btn_chon_file": QPushButton("Chọn file"),
            "btn_chon_nguoi_nhan": QPushButton("Chọn người nhận"),
            "lbl_nguoi_nhan": QLabel("Chưa chọn người nhận")
        }
        inputs["file_dinh_kem"].setReadOnly(True)
        if data.get("FileDinhKem"):
            inputs["file_dinh_kem"].setText(os.path.basename(data["FileDinhKem"]))
            self.current_file_path = data["FileDinhKem"]
        else:
            self.current_file_path = None

        if data.get("Id") and self.model:
            nguoi_nhan_list = self.model.get_nguoi_nhan_list(data["Id"])
            self.selected_nguoi_nhan_ids = [n['id'] for n in nguoi_nhan_list]
            self.selected_nguoi_nhan_text = ", ".join([n['ten'] for n in nguoi_nhan_list])
            inputs["lbl_nguoi_nhan"].setText(self.selected_nguoi_nhan_text if self.selected_nguoi_nhan_text else "Chưa chọn người nhận")
        else:
            self.selected_nguoi_nhan_ids = []
            self.selected_nguoi_nhan_text = ""

        inputs["btn_chon_file"].clicked.connect(lambda: self.chon_file(inputs["file_dinh_kem"]))
        inputs["btn_chon_nguoi_nhan"].clicked.connect(lambda: self.chon_nguoi_nhan(inputs["lbl_nguoi_nhan"]))
        return inputs

    def chon_file(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file đính kèm", "", "All Files (*.*)")
        if file_path:
            dest_dir = "uploads/noibo"
            os.makedirs(dest_dir, exist_ok=True)
            base, ext = os.path.splitext(os.path.basename(file_path))
            new_name = f"{base}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
            dest_path = os.path.join(dest_dir, new_name)
            # Copy file với hiển thị tiến trình nếu cần, nhưng tạm thời dùng copy2
            import shutil
            shutil.copy2(file_path, dest_path)
            line_edit.setText(new_name)
            self.current_file_path = dest_path
            # Thêm dòng này để giao diện không bị đơ
            from PyQt6.QtWidgets import QApplication
            QApplication.processEvents()

    def chon_nguoi_nhan(self, label):
        if not self.model:
            QMessageBox.warning(self, "Lỗi", "Chưa kết nối dữ liệu!")
            return
        dlg = ChonNguoiNhanDialog(self.model, self)
        if dlg.exec():
            ids, text = dlg.get_selected_nguoi_nhan()
            self.selected_nguoi_nhan_ids = ids
            self.selected_nguoi_nhan_text = text
            label.setText(text if text else "Chưa chọn người nhận")

    def _extract_form_data(self, inputs):
        return {
            "KyHieu": inputs["so_ky_hieu"].text(),
            "NgayBanHanh": inputs["ngay_ban_hanh"].date().toString("yyyy-MM-dd"),
            "LoaiVanBan": inputs["loai_van_ban"].currentText(),
            "TrichYeu": inputs["trich_yeu"].toPlainText(),
            "DonViSoan": inputs["don_vi_ban_hanh"].currentText(),
            "NguoiKy": inputs["nguoi_ky"].currentText(),
            "GhiChu": inputs["ghi_chu"].text(),
            "FileDinhKem": getattr(self, 'current_file_path', None),
            "NguoiNhanList": self.selected_nguoi_nhan_ids,
            "NguoiNhanText": self.selected_nguoi_nhan_text
        }

    def open_them_dialog(self):
        if not self.model:
            QMessageBox.warning(self, "Lỗi", "Chưa kết nối dữ liệu!")
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("Thêm Văn bản nội bộ")
        layout = QFormLayout(dialog)
        inputs = self._get_form_inputs()
        layout.addRow("Số, ký hiệu:", inputs["so_ky_hieu"])
        layout.addRow("Ngày ban hành:", inputs["ngay_ban_hanh"])
        layout.addRow("Loại văn bản:", inputs["loai_van_ban"])
        layout.addRow("Trích yếu:", inputs["trich_yeu"])
        layout.addRow("Đơn vị ban hành:", inputs["don_vi_ban_hanh"])
        layout.addRow("Người ký:", inputs["nguoi_ky"])
        layout.addRow("Ghi chú:", inputs["ghi_chu"])
        file_widget = QWidget()
        file_layout = QHBoxLayout(file_widget)
        file_layout.setContentsMargins(0,0,0,0)
        file_layout.addWidget(inputs["file_dinh_kem"])
        file_layout.addWidget(inputs["btn_chon_file"])
        layout.addRow("File đính kèm:", file_widget)
        layout.addRow("Người nhận:", inputs["btn_chon_nguoi_nhan"])
        layout.addRow("", inputs["lbl_nguoi_nhan"])
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addRow(buttons)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = self._extract_form_data(inputs)
            self.them_cv_signal.emit(data)

    def open_sua_dialog(self):
        selected = self.table_view.currentIndex()
        if not selected.isValid():
            self.show_error("Vui lòng chọn văn bản cần sửa!")
            return
        data = self.table_view.model().get_row(selected.row())
        if not self.model:
            self.show_error("Chưa kết nối dữ liệu!")
            return
        nguoi_nhan = self.model.get_nguoi_nhan_list(data["Id"])
        self.selected_nguoi_nhan_ids = [n["id"] for n in nguoi_nhan]
        self.selected_nguoi_nhan_text = ", ".join([n["ten"] for n in nguoi_nhan])
        dialog = QDialog(self)
        dialog.setWindowTitle("Sửa Văn bản nội bộ")
        layout = QFormLayout(dialog)
        inputs = self._get_form_inputs(data)
        layout.addRow("Số, ký hiệu:", inputs["so_ky_hieu"])
        layout.addRow("Ngày ban hành:", inputs["ngay_ban_hanh"])
        layout.addRow("Loại văn bản:", inputs["loai_van_ban"])
        layout.addRow("Trích yếu:", inputs["trich_yeu"])
        layout.addRow("Đơn vị ban hành:", inputs["don_vi_ban_hanh"])
        layout.addRow("Người ký:", inputs["nguoi_ky"])
        layout.addRow("Ghi chú:", inputs["ghi_chu"])
        file_widget = QWidget()
        file_layout = QHBoxLayout(file_widget)
        file_layout.setContentsMargins(0,0,0,0)
        file_layout.addWidget(inputs["file_dinh_kem"])
        file_layout.addWidget(inputs["btn_chon_file"])
        layout.addRow("File đính kèm:", file_widget)
        layout.addRow("Người nhận:", inputs["btn_chon_nguoi_nhan"])
        layout.addRow("", inputs["lbl_nguoi_nhan"])
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addRow(buttons)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = self._extract_form_data(inputs)
            self.sua_cv_signal.emit(data["Id"], new_data)

    def confirm_delete(self):
        selected = self.table_view.currentIndex()
        if not selected.isValid():
            self.show_error("Vui lòng chọn dòng cần xóa!")
            return
        data = self.table_view.model().get_row(selected.row())
        reply = QMessageBox.question(self, "Xác nhận", f"Bạn có chắc muốn xóa văn bản: '{data.get('KyHieu', '')}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.xoa_cv_signal.emit(data["Id"])

    def show_status(self, msg):
        self.statusBar().showMessage(msg, 3000)

    def show_error(self, msg):
        QMessageBox.critical(self, "Lỗi", msg)