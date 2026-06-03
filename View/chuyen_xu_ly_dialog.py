from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QPushButton, QTextEdit, QComboBox, QDateEdit, 
                             QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from typing import Dict, List

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

    def set_checked_ids(self, ids: List[int]):
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            item_id = item.data(Qt.ItemDataRole.UserRole)
            if item_id in ids:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)


class ChuyenXuLyDialog(QDialog):
    def __init__(self, danh_sach_can_bo, cong_viec_model, cong_van_den_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Phân công / Cập nhật xử lý công văn")
        self.setMinimumSize(800, 500)
        self.danh_sach_can_bo = danh_sach_can_bo
        self.cong_viec_model = cong_viec_model
        self.cong_van_den_id = cong_van_den_id
        self.existing_tasks = []
        self.current_chu_tri_id = None
        self.setup_ui()
        self.nap_du_lieu_can_bo()
        self.load_existing_assignments()
        self.cb_chu_tri.currentIndexChanged.connect(self.on_chu_tri_changed)

    def setup_ui(self):
        layout = QGridLayout(self)

        layout.addWidget(QLabel("Nội dung công việc"), 0, 0)
        self.txt_noi_dung = QTextEdit()
        layout.addWidget(self.txt_noi_dung, 1, 0, 1, 2)

        layout.addWidget(QLabel("Hạn xử lý (Deadline)"), 2, 0)
        self.date_han = QDateEdit(QDate.currentDate().addDays(7))
        self.date_han.setCalendarPopup(True)
        self.date_han.setDisplayFormat("dd/MM/yyyy")
        layout.addWidget(self.date_han, 3, 0)

        layout.addWidget(QLabel("Yêu cầu xử lý chi tiết"), 4, 0)
        self.txt_yeu_cau = QTextEdit()
        layout.addWidget(self.txt_yeu_cau, 5, 0, 1, 2)

        layout.addWidget(QLabel("⭐ Chủ trì giải quyết (người duyệt/ký)"), 0, 2)
        self.cb_chu_tri = QComboBox()
        layout.addWidget(self.cb_chu_tri, 1, 2, Qt.AlignmentFlag.AlignTop)

        layout.addWidget(QLabel("👥 Cán bộ tham gia xử lý (nhận task)"), 2, 2)
        self.cb_tham_gia = CheckableComboBox()
        layout.addWidget(self.cb_tham_gia, 3, 2, Qt.AlignmentFlag.AlignTop)

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

        self.cb_tham_gia.model().clear()
        for cb in self.danh_sach_can_bo:
            item = QStandardItem(cb['ho_ten'])
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
            item.setData(cb['id'], Qt.ItemDataRole.UserRole)
            self.cb_tham_gia.model().appendRow(item)

    def load_existing_assignments(self):
        if not self.cong_viec_model or not self.cong_van_den_id:
            return
        conn = self.cong_viec_model._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Id, NguoiDuocGiaoId, IsChuTri, NoiDung, HanXuLy, KetQua
            FROM PhanCongXuLy
            WHERE CongVanDenId = ?
        """, (self.cong_van_den_id,))
        rows = cursor.fetchall()
        conn.close()
        self.existing_tasks = []
        chu_tri_id = None
        tham_gia_ids = []
        first_task = None
        for row in rows:
            task_id, nguoi_id, is_chu_tri, noi_dung, han_xl, yeu_cau = row
            self.existing_tasks.append({"id": task_id, "nguoi_id": nguoi_id, "is_chu_tri": is_chu_tri})
            if is_chu_tri:
                chu_tri_id = nguoi_id
            else:
                tham_gia_ids.append(nguoi_id)
            if first_task is None:
                first_task = (noi_dung, han_xl, yeu_cau)

        self.current_chu_tri_id = chu_tri_id

        if chu_tri_id is not None:
            idx = self.cb_chu_tri.findData(chu_tri_id)
            if idx >= 0:
                self.cb_chu_tri.setCurrentIndex(idx)
        self.cb_tham_gia.set_checked_ids(tham_gia_ids)

        if first_task:
            self.txt_noi_dung.setText(first_task[0] or "")
            han_xl = first_task[1]
            if han_xl:
                if isinstance(han_xl, str):
                    self.date_han.setDate(QDate.fromString(han_xl, "yyyy-MM-dd"))
                elif hasattr(han_xl, 'year'):
                    self.date_han.setDate(QDate(han_xl.year, han_xl.month, han_xl.day))
            self.txt_yeu_cau.setText(first_task[2] or "")

    def on_chu_tri_changed(self, index):
        new_chu_tri_id = self.cb_chu_tri.currentData()
        if new_chu_tri_id is None:
            return
        checked_ids, _ = self.cb_tham_gia.get_checked_items()
        if self.current_chu_tri_id is not None and self.current_chu_tri_id in checked_ids:
            checked_ids.remove(self.current_chu_tri_id)
        if new_chu_tri_id not in checked_ids:
            checked_ids.append(new_chu_tri_id)
        self.cb_tham_gia.set_checked_ids(checked_ids)
        self.current_chu_tri_id = new_chu_tri_id

    def get_data(self) -> Dict:
        tham_gia_ids, tham_gia_names = self.cb_tham_gia.get_checked_items()
        chu_tri_id = self.cb_chu_tri.currentData()
        if chu_tri_id is not None and chu_tri_id not in tham_gia_ids:
            tham_gia_ids.append(chu_tri_id)
            self.cb_tham_gia.set_checked_ids(tham_gia_ids)
        return {
            "noi_dung": self.txt_noi_dung.toPlainText(),
            "yeu_cau_xu_ly": self.txt_yeu_cau.toPlainText(),
            "ngay_han": self.date_han.date().toString("yyyy-MM-dd"),
            "chu_tri_id": chu_tri_id,
            "chu_tri_ten": self.cb_chu_tri.currentText() if chu_tri_id else "",
            "tham_gia_ids": tham_gia_ids,
            "tham_gia_ten": tham_gia_names,
            "existing_tasks": self.existing_tasks
        }