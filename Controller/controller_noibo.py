from Model.model_noibo import ModelNoiBo, NoiBoTableModel
from PyQt6.QtWidgets import QMessageBox

class ControllerNoiBo:
    def __init__(self, model: ModelNoiBo, view, user_session):
        self.model = model
        self.view = view
        self.user_session = user_session
        self.view.set_model(model)
        self.connect_signals()
        self.load_danh_muc()
        self.load_data()

    def load_danh_muc(self):
        loai = self.model.get_loai_list()
        donvi = self.model.get_donvi_list()
        canbo = self.model.get_canbo_list()
        self.view.set_danh_muc(loai, donvi, canbo)

    def connect_signals(self):
        self.view.them_cv_signal.connect(self.handle_them)
        self.view.sua_cv_signal.connect(self.handle_sua)
        self.view.xoa_cv_signal.connect(self.handle_xoa)
        self.view.tim_kiem_signal.connect(self.handle_tim_kiem)
        self.view.nap_dulieu_signal.connect(self.load_data)
        self.view.xuat_excel_signal.connect(self.handle_xuat_excel)

    def load_data(self, keyword=""):
        try:
            data = self.model.get_all(
                keyword=keyword,
                user_id=self.user_session.user_id,
                is_admin=self.user_session.is_admin_user()
            )
            self.table_model = NoiBoTableModel(data)
            self.view.set_table_model(self.table_model)
            self.view.show_status(f"Đã tải {len(data)} văn bản nội bộ.")
        except Exception as e:
            self.view.show_error(f"Lỗi tải dữ liệu: {str(e)}")

    def handle_them(self, data):
        try:
            nguoi_tao_id = self.user_session.user_id  # dùng ID thực tế
            self.model.add(data, nguoi_tao_id)
            self.load_data()
            self.view.show_status("Thêm thành công!")
        except Exception as e:
            self.view.show_error(f"Lỗi khi thêm: {str(e)}")

    def handle_sua(self, id_cv, data):
        try:
            self.model.update(id_cv, data)
            self.load_data()
            self.view.show_status("Cập nhật thành công!")
        except Exception as e:
            self.view.show_error(f"Lỗi khi sửa: {str(e)}")

    def handle_xoa(self, id_cv):
        try:
            self.model.delete(id_cv)
            self.load_data()
            self.view.show_status("Xóa thành công!")
        except Exception as e:
            self.view.show_error(f"Lỗi khi xóa: {str(e)}")

    def handle_tim_kiem(self, keyword):
        self.load_data(keyword)

    def handle_xuat_excel(self):
        QMessageBox.information(self.view, "Xuất dữ liệu", "Chức năng xuất Excel đang được xử lý.")