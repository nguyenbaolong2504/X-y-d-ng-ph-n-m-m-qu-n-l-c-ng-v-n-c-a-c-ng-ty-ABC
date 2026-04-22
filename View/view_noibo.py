from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate, pyqtSignal, Qt

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
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # Header
        header_lbl = QLabel("🗂️ Danh mục văn bản, thông tin nội bộ")
        header_lbl.setStyleSheet("background-color: #f4f5f7; border: 1px solid #ddd; padding: 10px; font-size: 15px; font-weight: bold; color: #333;")
        main_layout.addWidget(header_lbl)

        # Toolbar
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

        # Tìm kiếm
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm theo số ký hiệu, trích yếu...")
        self.search_input.setFixedWidth(300)
        toolbar_layout.addWidget(self.search_input)
        
        main_layout.addLayout(toolbar_layout)

        # Table
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view.verticalHeader().setVisible(False)
        main_layout.addWidget(self.table_view)

        # Connect signals
        self.btn_them.clicked.connect(self.open_them_dialog)
        self.btn_xoa.clicked.connect(self.confirm_delete)
        self.btn_refresh.clicked.connect(self.nap_dulieu_signal.emit)
        self.btn_excel.clicked.connect(self.xuat_excel_signal.emit)
        self.table_view.doubleClicked.connect(self.open_sua_dialog)
        self.search_input.returnPressed.connect(lambda: self.tim_kiem_signal.emit(self.search_input.text()))
        self.search_input.textChanged.connect(lambda text: self.tim_kiem_signal.emit(text) if len(text)==0 else None)

    def set_table_model(self, model):
        self.table_view.setModel(model)
        self.table_view.setColumnHidden(0, True) # Ẩn cột ID
        self.table_view.setColumnWidth(1, 120) # Số ký hiệu
        self.table_view.setColumnWidth(2, 120) # Ngày ban hành
        self.table_view.setColumnWidth(3, 150) # Loại văn bản
        self.table_view.setColumnWidth(4, 300) # Trích yếu
        self.table_view.setColumnWidth(5, 150) # Đơn vị ban hành
        self.table_view.setColumnWidth(6, 120) # Người ký
        self.table_view.setColumnWidth(7, 200) # Đơn vị nhận
        self.table_view.setColumnWidth(8, 150) # Ghi chú

    def _get_form_inputs(self, data=None):
        if data is None: data = {}
        
        inputs = {
            "so_ky_hieu": QLineEdit(str(data.get("so_ky_hieu", ""))),
            "ngay_ban_hanh": QDateEdit(calendarPopup=True),
            "loai_van_ban": QComboBox(),
            "trich_yeu": QTextEdit(str(data.get("trich_yeu", ""))),
            "don_vi_ban_hanh": QLineEdit(str(data.get("don_vi_ban_hanh", ""))),
            "nguoi_ky": QLineEdit(str(data.get("nguoi_ky", ""))),
            "don_vi_nhan": QLineEdit(str(data.get("don_vi_nhan", ""))),
            "ghi_chu": QLineEdit(str(data.get("ghi_chu", "")))
        }
        
        # Set Ngày
        if data.get("ngay_ban_hanh"):
            inputs["ngay_ban_hanh"].setDate(QDate.fromString(data["ngay_ban_hanh"], "yyyy-MM-dd"))
        else:
            inputs["ngay_ban_hanh"].setDate(QDate.currentDate())

        # Set ComboBox Loại văn bản
        inputs["loai_van_ban"].addItems(["Thông báo", "Quyết định", "Chỉ thị", "Báo cáo", "Kế hoạch", "Khác"])
        if data.get("loai_van_ban"):
            inputs["loai_van_ban"].setCurrentText(data["loai_van_ban"])

        return inputs

    def _extract_form_data(self, inputs):
        return {
            "so_ky_hieu": inputs["so_ky_hieu"].text(),
            "ngay_ban_hanh": inputs["ngay_ban_hanh"].date().toString("yyyy-MM-dd"),
            "loai_van_ban": inputs["loai_van_ban"].currentText(),
            "trich_yeu": inputs["trich_yeu"].toPlainText(),
            "don_vi_ban_hanh": inputs["don_vi_ban_hanh"].text(),
            "nguoi_ky": inputs["nguoi_ky"].text(),
            "don_vi_nhan": inputs["don_vi_nhan"].text(),
            "ghi_chu": inputs["ghi_chu"].text()
        }

    def open_them_dialog(self):
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
        layout.addRow("Đơn vị/Người nhận:", inputs["don_vi_nhan"])
        layout.addRow("Ghi chú:", inputs["ghi_chu"])

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
        layout.addRow("Đơn vị/Người nhận:", inputs["don_vi_nhan"])
        layout.addRow("Ghi chú:", inputs["ghi_chu"])

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addRow(buttons)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = self._extract_form_data(inputs)
            self.sua_cv_signal.emit(data["id"], new_data)

    def confirm_delete(self):
        selected = self.table_view.currentIndex()
        if not selected.isValid():
            self.show_error("Vui lòng chọn dòng cần xóa!")
            return
        data = self.table_view.model().get_row(selected.row())
        reply = QMessageBox.question(self, "Xác nhận", f"Bạn có chắc muốn xóa văn bản: '{data.get('so_ky_hieu', '')}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.xoa_cv_signal.emit(data["id"])

    def show_status(self, msg):
        self.statusBar().showMessage(msg, 3000)

    def show_error(self, msg):
        QMessageBox.critical(self, "Lỗi", msg)