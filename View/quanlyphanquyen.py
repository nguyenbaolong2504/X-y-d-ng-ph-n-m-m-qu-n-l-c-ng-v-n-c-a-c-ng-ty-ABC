from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal

class QuanLyPhanQuyen(QWidget):
    load_users_signal = pyqtSignal(str)
    load_permissions_signal = pyqtSignal(str)
    save_permissions_signal = pyqtSignal(int, list)
    add_user_signal = pyqtSignal(dict)
    update_user_signal = pyqtSignal(str, dict)
    delete_user_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_username = None
        self.current_user_id = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("🔐 QUẢN LÝ PHÂN QUYỀN HỆ THỐNG")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #6c5ce7; padding: 8px 0;")
        main_layout.addWidget(title)

        # Toolbar
        toolbar = QHBoxLayout()
        self.btn_them = QPushButton("➕ Thêm người dùng")
        self.btn_sua = QPushButton("✏️ Sửa người dùng")
        self.btn_xoa = QPushButton("🗑️ Xóa người dùng")
        self.btn_refresh = QPushButton("🔄 Làm mới")
        for btn in [self.btn_them, self.btn_sua, self.btn_xoa, self.btn_refresh]:
            btn.setStyleSheet("background-color: #6c5ce7; color: white; border: none; padding: 8px 15px; border-radius: 8px; font-weight: bold;")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
        toolbar.addWidget(self.btn_them)
        toolbar.addWidget(self.btn_sua)
        toolbar.addWidget(self.btn_xoa)
        toolbar.addWidget(self.btn_refresh)
        toolbar.addStretch()
        toolbar.addWidget(QLabel("Tìm tên đăng nhập:"))
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Nhập tên đăng nhập...")
        self.txt_search.setFixedWidth(200)
        self.txt_search.setStyleSheet("padding: 8px; border: 1px solid #ddd; border-radius: 8px;")
        toolbar.addWidget(self.txt_search)
        self.btn_search = QPushButton("🔍 Tìm")
        self.btn_search.setStyleSheet("background-color: #00b894; color: white; border: none; padding: 8px 15px; border-radius: 8px;")
        toolbar.addWidget(self.btn_search)
        main_layout.addLayout(toolbar)

        # Bảng người dùng
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Tên đăng nhập", "Mật khẩu", "Vai trò", "Họ tên"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget { border: none; gridline-color: #e0e0e0; }
            QHeaderView::section { background-color: #f0f2f5; padding: 10px; font-weight: bold; border: none; }
            QTableWidget::item { padding: 8px; }
        """)
        main_layout.addWidget(self.table)

        # Khung phân quyền menu
        perm_frame = QFrame()
        perm_frame.setStyleSheet("background-color: white; border-radius: 12px; padding: 10px; margin-top: 10px;")
        perm_layout = QVBoxLayout(perm_frame)

        title_perm = QLabel("📋 Menu được phép sử dụng")
        title_perm.setStyleSheet("font-size: 18px; font-weight: bold; padding: 5px 0;")
        perm_layout.addWidget(title_perm)

        self.menu_list = QListWidget()
        self.menu_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.menu_list.setStyleSheet("""
            QListWidget { border: 1px solid #ddd; border-radius: 8px; padding: 5px; }
            QListWidget::item { padding: 8px; border-bottom: 1px solid #f0f0f0; }
        """)
        perm_layout.addWidget(self.menu_list)

        self.btn_save = QPushButton("💾 Lưu phân quyền")
        self.btn_save.setStyleSheet("background-color: #e84118; color: white; border: none; padding: 10px; border-radius: 8px; font-weight: bold;")
        perm_layout.addWidget(self.btn_save)

        main_layout.addWidget(perm_frame)

        # Kết nối
        self.btn_them.clicked.connect(self.open_them_dialog)
        self.btn_sua.clicked.connect(self.open_sua_dialog)
        self.btn_xoa.clicked.connect(self.delete_user)
        self.btn_refresh.clicked.connect(lambda: self.load_users_signal.emit(self.txt_search.text().strip()))
        self.btn_search.clicked.connect(lambda: self.load_users_signal.emit(self.txt_search.text().strip()))
        self.table.itemSelectionChanged.connect(self.on_user_selected)
        self.btn_save.clicked.connect(self.save_permission)

    def set_users(self, users):
        self.table.setRowCount(len(users))
        for i, u in enumerate(users):
            self.table.setItem(i, 0, QTableWidgetItem(u['Username']))
            self.table.setItem(i, 1, QTableWidgetItem(u['Password']))
            self.table.setItem(i, 2, QTableWidgetItem(u['VaiTro']))
            self.table.setItem(i, 3, QTableWidgetItem(u['HoTen']))
        self.table.resizeColumnsToContents()

    def set_menus(self, menus):
        self.menu_list.clear()
        for m in menus:
            item = QListWidgetItem(m['TenMenu'])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            item.setData(Qt.ItemDataRole.UserRole, m['Id'])
            self.menu_list.addItem(item)

    def set_permissions(self, menu_ids):
        for i in range(self.menu_list.count()):
            item = self.menu_list.item(i)
            menu_id = item.data(Qt.ItemDataRole.UserRole)
            item.setCheckState(Qt.CheckState.Checked if menu_id in menu_ids else Qt.CheckState.Unchecked)

    def on_user_selected(self):
        row = self.table.currentRow()
        if row < 0:
            self.current_username = None
            self.current_user_id = None
            return
        self.current_username = self.table.item(row, 0).text()
        self.load_permissions_signal.emit(self.current_username)

    def save_permission(self):
        if self.current_user_id is None:
            QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn người dùng trước khi lưu phân quyền!")
            return
        selected_ids = []
        for i in range(self.menu_list.count()):
            item = self.menu_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected_ids.append(item.data(Qt.ItemDataRole.UserRole))
        self.save_permissions_signal.emit(self.current_user_id, selected_ids)

    def open_them_dialog(self):
        self.add_user_signal.emit({})

    def open_sua_dialog(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn người dùng cần sửa!")
            return
        username = self.table.item(row, 0).text()
        self.update_user_signal.emit(username, {})

    def delete_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn người dùng cần xóa!")
            return
        username = self.table.item(row, 0).text()
        reply = QMessageBox.question(self, "Xác nhận", f"Xóa người dùng '{username}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_user_signal.emit(username)