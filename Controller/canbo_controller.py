from PyQt6.QtWidgets import QMessageBox
from Model.canbo_model import CanBoModel
from Model.canbo_table_model import CanBoTableModel
from View.canbo_dialog import CanBoDialog # Đảm bảo bạn đã có file này

class CanBoController:
    def __init__(self, model: CanBoModel, view):
        self.model = model
        self.view = view
        self.table_model = None
        
        # --- KẾT NỐI TÍN HIỆU (Signals) ---
        # Kết nối nút Thêm cán bộ
        self.view.them_signal.connect(self.add_canbo)
        
        # Kết nối tín hiệu Sửa (nhận vào một dictionary data)
        self.view.sua_signal.connect(self.edit_canbo_by_data)
        
        # Kết nối tín hiệu Xóa (nhận vào ID)
        self.view.xoa_signal.connect(self.delete_canbo)
        
        # Kết nối nút Làm mới
        self.view.lam_moi_signal.connect(self.load_data)
        
        # Tải dữ liệu lần đầu khi mở trang
        self.load_data()

    def load_data(self):
        """Tải dữ liệu từ Database và đổ vào TableView/TableWidget"""
        try:
            data = self.model.get_all()
            headers = ["STT", "Họ và tên", "Ngày sinh", "Giới tính", "Chức vụ", "Đơn vị", "Tên truy cập", "Email", "Thao tác"]
            
            # Sử dụng TableModel để quản lý dữ liệu
            self.table_model = CanBoTableModel(data, headers)
            self.view.set_table_model(self.table_model)
            
            # Nếu View sử dụng QTableWidget (như code View mình gửi lúc trước)
            # thì gọi hàm load trực tiếp:
            if hasattr(self.view, 'load_data_to_table'):
                self.view.load_data_to_table(data)
                
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Không thể tải dữ liệu cán bộ: {e}")

    def add_canbo(self):
        """Xử lý khi nhấn nút Thêm"""
        try:
            don_vi = self.model.get_don_vi()
            chuc_vu = self.model.get_chuc_vu()
            
            dialog = CanBoDialog(don_vi_list=don_vi, chuc_vu_list=chuc_vu)
            if dialog.exec():
                new_data = dialog.get_data()
                self.model.add(new_data)
                self.load_data()
                QMessageBox.information(None, "Thành công", "Đã thêm cán bộ mới!")
        except Exception as e:
            QMessageBox.warning(None, "Lỗi", f"Không thể thêm cán bộ: {e}")

    def edit_canbo_by_data(self, data):
        """Xử lý khi nhấn nút Sửa (📝) trên từng dòng"""
        try:
            don_vi = self.model.get_don_vi()
            chuc_vu = self.model.get_chuc_vu()

            dialog = CanBoDialog(data=data, don_vi_list=don_vi, chuc_vu_list=chuc_vu)
            if dialog.exec():
                updated_data = dialog.get_data()
                self.model.update(updated_data)
                self.load_data()
                QMessageBox.information(None, "Thành công", "Đã cập nhật thông tin cán bộ!")
        except Exception as e:
            QMessageBox.warning(None, "Lỗi", f"Không thể cập nhật: {e}")

    def delete_canbo(self, id_canbo):
        """Xử lý khi nhấn nút Xóa (🗑️)"""
        try:
            res = QMessageBox.question(
                None, "Xác nhận", 
                "Bạn có chắc chắn muốn xóa cán bộ này không?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if res == QMessageBox.StandardButton.Yes:
                self.model.delete(id_canbo)
                self.load_data()
                # Hiển thị thông báo (vì QWidget không có statusBar trực tiếp như QMainWindow)
                QMessageBox.information(None, "Thông báo", "Đã xóa cán bộ thành công")
        except Exception as e:
            QMessageBox.warning(None, "Lỗi", f"Lỗi khi xóa: {e}")