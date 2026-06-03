from Model.phanquyen_model import PhanQuyenModel
from View.quanlyphanquyen import QuanLyPhanQuyen
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox, QMessageBox

class PhanQuyenController:
    def __init__(self, model: PhanQuyenModel, view: QuanLyPhanQuyen):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_data()
        self.load_menus()

    def connect_signals(self):
        self.view.load_users_signal.connect(self.load_data)
        self.view.load_permissions_signal.connect(self.load_permissions_by_username)
        self.view.save_permissions_signal.connect(self.save_permissions)
        self.view.add_user_signal.connect(self.open_them_dialog)
        self.view.update_user_signal.connect(self.open_sua_dialog)
        self.view.delete_user_signal.connect(self.delete_user)

    def load_data(self, keyword=""):
        users = self.model.get_all_users(keyword)
        self.view.set_users(users)

    def load_permissions_by_username(self, username):
        user = self.model.get_user_by_username(username)
        if user:
            self.view.current_user_id = user['Id']
            perms = self.model.get_user_permissions(user['Id'])
            self.view.set_permissions(perms)
        else:
            self.view.current_user_id = None
            self.view.set_permissions([])

    def save_permissions(self, user_id, menu_ids):
        try:
            self.model.save_permissions(user_id, menu_ids)
            QMessageBox.information(self.view, "Thành công", "Lưu phân quyền thành công!")
        except Exception as e:
            QMessageBox.critical(self.view, "Lỗi", f"Lưu thất bại: {str(e)}")

    def load_menus(self):
        menus = self.model.get_all_menus()
        self.view.set_menus(menus)

    # ==================== THÊM NGƯỜI DÙNG ====================
    def open_them_dialog(self, _):
        dialog = QDialog(self.view)
        dialog.setWindowTitle("Thêm người dùng")
        layout = QFormLayout(dialog)

        txt_username = QLineEdit()
        txt_password = QLineEdit()
        txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        txt_confirm = QLineEdit()
        txt_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        txt_hoten = QLineEdit()
        cb_role = QComboBox()
        for nq in self.model.get_nhomquyen_list():
            cb_role.addItem(nq['ten'], nq['id'])

        layout.addRow("Tên đăng nhập:", txt_username)
        layout.addRow("Mật khẩu:", txt_password)
        layout.addRow("Xác nhận mật khẩu:", txt_confirm)
        layout.addRow("Họ tên:", txt_hoten)
        layout.addRow("Nhóm quyền:", cb_role)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addRow(buttons)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            username = txt_username.text().strip()
            password = txt_password.text().strip()
            confirm = txt_confirm.text().strip()
            hoten = txt_hoten.text().strip()
            if not username or not password:
                QMessageBox.warning(dialog, "Lỗi", "Tên đăng nhập và mật khẩu không được để trống!")
                return
            if password != confirm:
                QMessageBox.warning(dialog, "Lỗi", "Mật khẩu xác nhận không khớp!")
                return
            data = {
                "Username": username,
                "Password": password,
                "NhomQuyenId": cb_role.currentData(),
                "HoTen": hoten
            }
            try:
                self.model.add_user(data)
                QMessageBox.information(self.view, "Thành công", "Thêm người dùng thành công!")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self.view, "Lỗi", f"Thêm thất bại: {str(e)}")

    # ==================== SỬA NGƯỜI DÙNG (CÓ SỬA VAI TRÒ) ====================
    def open_sua_dialog(self, username, _):
        user = self.model.get_user_by_username(username)
        if not user:
            QMessageBox.warning(self.view, "Lỗi", "Không tìm thấy người dùng!")
            return

        dialog = QDialog(self.view)
        dialog.setWindowTitle(f"Sửa người dùng: {username}")
        layout = QFormLayout(dialog)

        # Mật khẩu: để trống nếu không đổi
        txt_password = QLineEdit()
        txt_password.setPlaceholderText("Để trống nếu không đổi mật khẩu")
        txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        txt_confirm = QLineEdit()
        txt_confirm.setPlaceholderText("Nhập lại mật khẩu mới nếu có")
        txt_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        txt_hoten = QLineEdit(user['HoTen'])

        # Nhóm quyền (Vai trò)
        cb_role = QComboBox()
        for nq in self.model.get_nhomquyen_list():
            cb_role.addItem(nq['ten'], nq['id'])
        # Chọn đúng nhóm quyền hiện tại
        idx = cb_role.findData(user['NhomQuyenId'])
        if idx >= 0:
            cb_role.setCurrentIndex(idx)

        layout.addRow("Mật khẩu mới:", txt_password)
        layout.addRow("Xác nhận mật khẩu:", txt_confirm)
        layout.addRow("Họ tên:", txt_hoten)
        layout.addRow("Nhóm quyền (Vai trò):", cb_role)   # ← Rõ ràng là vai trò

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addRow(buttons)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_password = txt_password.text().strip()
            confirm = txt_confirm.text().strip()
            if new_password and new_password != confirm:
                QMessageBox.warning(dialog, "Lỗi", "Mật khẩu xác nhận không khớp!")
                return
            data = {
                "Password": new_password if new_password else user['Password'],
                "NhomQuyenId": cb_role.currentData(),   # ← cập nhật vai trò
                "HoTen": txt_hoten.text().strip()
            }
            try:
                self.model.update_user(user['Id'], data)
                QMessageBox.information(self.view, "Thành công", "Cập nhật người dùng thành công (bao gồm vai trò)!")
                self.load_data()
                # Tải lại quyền cho người dùng vừa sửa (nếu đang chọn)
                if self.view.current_username == username:
                    self.load_permissions_by_username(username)
            except Exception as e:
                QMessageBox.critical(self.view, "Lỗi", f"Cập nhật thất bại: {str(e)}")

    # ==================== XÓA NGƯỜI DÙNG ====================
    def delete_user(self, username):
        user = self.model.get_user_by_username(username)
        if not user:
            QMessageBox.warning(self.view, "Lỗi", "Không tìm thấy người dùng!")
            return
        try:
            self.model.delete_user(user['Id'])
            QMessageBox.information(self.view, "Thành công", f"Đã xóa người dùng '{username}'")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self.view, "Lỗi", f"Xóa thất bại: {str(e)}")