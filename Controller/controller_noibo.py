from Model.model_noibo import ModelNoiBo, NoiBoTableModel
from PyQt6.QtWidgets import QMessageBox

class ControllerNoiBo:
    def __init__(self, model: ModelNoiBo, view):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_data()
        
    def connect_signals(self):
        # Kết nối các tín hiệu từ giao diện người dùng
        self.view.them_cv_signal.connect(self.handle_them)
        self.view.sua_cv_signal.connect(self.handle_sua)
        self.view.xoa_cv_signal.connect(self.handle_xoa)
        self.view.tim_kiem_signal.connect(self.handle_tim_kiem)
        self.view.nap_dulieu_signal.connect(self.load_data)
        self.view.xuat_excel_signal.connect(self.handle_xuat_excel)

    def load_data(self, keyword=""):
        try:
            # Lấy dữ liệu thực từ SQL Server qua Model
            data = self.model.get_all(keyword)
            # Khởi tạo lại Model hiển thị bảng
            self.table_model = NoiBoTableModel(data)
            # Cập nhật model vào View (TableView)
            self.view.set_table_model(self.table_model)
            self.view.show_status(f"Hệ thống: Đã tải {len(data)} văn bản nội bộ.")
        except Exception as e:
            print(f"Lỗi Load Data: {e}") # Debug log
            self.view.show_error(f"Lỗi tải dữ liệu: {str(e)}")

    def handle_them(self, data):
        try:
            self.model.add(data)
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

    def run(self):
        self.view.show()