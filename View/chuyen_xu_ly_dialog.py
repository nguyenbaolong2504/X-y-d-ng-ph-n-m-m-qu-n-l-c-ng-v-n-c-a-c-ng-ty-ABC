from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QPushButton, QTextEdit, QComboBox, QDateEdit, 
                             QMessageBox)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from typing import Dict

class CheckableComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.view().pressed.connect(self.handle_item_pressed)
        self.setModel(QStandardItemModel(self))

    def handle_item_pressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.CheckState.Checked:
            item.setCheckState(Qt.CheckState.Unchecked)
        else:
            item.setCheckState(Qt.CheckState.Checked)

    def get_checked_items(self):
        checked_ids = []
        checked_names = []
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            if item.checkState() == Qt.CheckState.Checked:
                checked_ids.append(item.data(Qt.ItemDataRole.UserRole))
                checked_names.append(item.text())
        return checked_ids, checked_names

class ChuyenXuLyDialog(QDialog):
    def __init__(self, danh_sach_can_bo, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chuyển xử lý văn bản đến")
        self.setMinimumSize(800, 400)
        self.danh_sach_can_bo = danh_sach_can_bo
        
        self.setup_ui()
        self.nap_du_lieu_can_bo()

    def setup_ui(self):
        layout = QGridLayout(self)

        # -- Cột trái --
        layout.addWidget(QLabel("Nội dung công việc"), 0, 0)
        self.txt_noi_dung = QTextEdit()
        layout.addWidget(self.txt_noi_dung, 1, 0, 1, 2)

        layout.addWidget(QLabel("Ngày tạo"), 2, 0)
        self.date_tao = QDateEdit(QDate.currentDate())
        self.date_tao.setCalendarPopup(True)
        self.date_tao.setDisplayFormat("dd/MM/yyyy")
        layout.addWidget(self.date_tao, 3, 0)

        layout.addWidget(QLabel("Ngày xử lý"), 2, 1)
        self.date_xu_ly = QDateEdit(QDate.currentDate().addDays(7))
        self.date_xu_ly.setCalendarPopup(True)
        self.date_xu_ly.setDisplayFormat("dd/MM/yyyy")
        layout.addWidget(self.date_xu_ly, 3, 1)

        layout.addWidget(QLabel("Yêu cầu xử lý"), 4, 0)
        self.txt_yeu_cau = QTextEdit()
        layout.addWidget(self.txt_yeu_cau, 5, 0, 1, 2)

        # -- Cột phải --
        layout.addWidget(QLabel("Chủ trì giải quyết công việc (người có thẩm quyền)"), 0, 2)
        self.cb_chu_tri = QComboBox()
        layout.addWidget(self.cb_chu_tri, 1, 2, Qt.AlignmentFlag.AlignTop)

        layout.addWidget(QLabel("Danh sách cán bộ tham gia giải quyết công việc"), 2, 2)
        self.cb_tham_gia = CheckableComboBox()
        layout.addWidget(self.cb_tham_gia, 3, 2, Qt.AlignmentFlag.AlignTop)

        # -- Nút bấm --
        btn_layout = QHBoxLayout()
        self.btn_luu = QPushButton("💾 Lưu công việc")
        self.btn_luu.setStyleSheet("background-color: #2196F3; color: white; padding: 5px 15px;")
        self.btn_huy = QPushButton("✖ Hủy bỏ")
        self.btn_huy.setStyleSheet("background-color: #f44336; color: white; padding: 5px 15px;")
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_luu)
        btn_layout.addWidget(self.btn_huy)

        layout.addLayout(btn_layout, 6, 0, 1, 3)

        self.btn_luu.clicked.connect(self.accept)
        self.btn_huy.clicked.connect(self.reject)

    def nap_du_lieu_can_bo(self):
        self.cb_chu_tri.clear()
        self.cb_chu_tri.addItem("--- Chọn cán bộ chủ trì ---", None)
        for cb in self.danh_sach_can_bo:
            cb_id = int(cb['id']) if cb['id'] is not None else None
            self.cb_chu_tri.addItem(cb['ho_ten'], cb_id)
            print(f"[DEBUG] Thêm combobox: {cb['ho_ten']} - ID: {cb_id}")

        self.cb_tham_gia.model().clear()
        for cb in self.danh_sach_can_bo:
            item = QStandardItem(cb['ho_ten'])
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
            item.setData(cb['id'], Qt.ItemDataRole.UserRole)
            self.cb_tham_gia.model().appendRow(item)

    def get_data(self) -> Dict:
        tham_gia_ids, tham_gia_names = self.cb_tham_gia.get_checked_items()
        chu_tri_id = self.cb_chu_tri.currentData()
        print(f"[DEBUG] get_data: chu_tri_id = {chu_tri_id}, loại = {type(chu_tri_id)}")
        return {
            "noi_dung": self.txt_noi_dung.toPlainText(),
            "yeu_cau_xu_ly": self.txt_yeu_cau.toPlainText(),
            "ngay_tao": self.date_tao.date().toString("yyyy-MM-dd"),
            "ngay_xu_ly": self.date_xu_ly.date().toString("yyyy-MM-dd"),
            "chu_tri_id": chu_tri_id,
            "chu_tri_ten": self.cb_chu_tri.currentText() if chu_tri_id else "",
            "tham_gia_ids": tham_gia_ids,
            "tham_gia_ten": tham_gia_names
        }