from Model.congvan_model import CongVanModel
from Model.congvan_table_model import CongVanTableModel
from View.quanlycongvanden import MainWindow
from Utils.excel_export import export_to_excel

class CongVanController:
    def __init__(self, model: CongVanModel, view: MainWindow):
        self.model = model
        self.view = view
        self.table_model = None
        
        # --- Kết nối các tín hiệu (Signals) ---
        self.view.them_cv_signal.connect(self.them_cong_van)
        self.view.sua_cv_signal.connect(self.sua_cong_van)
        self.view.xoa_cv_signal.connect(self.xoa_cong_van)
        self.view.tim_kiem_signal.connect(self.tim_kiem)
        self.view.nap_dulieu_signal.connect(self.load_data)
        
        # Tín hiệu Lọc và Xuất Excel (Đảm bảo bên View đã định nghĩa các signal này)
        if hasattr(self.view, 'loc_cv_signal'):
            self.view.loc_cv_signal.connect(self.handle_filter)
        if hasattr(self.view, 'xuat_excel_signal'):
            self.view.xuat_excel_signal.connect(self.xuat_excel)

        # --- Khởi tạo dữ liệu ban đầu ---
        self.nap_danh_mục_phong_ban()
        self.load_data() # Mặc định hiện tất cả danh sách khi mở app

    def get_headers(self):
        """Danh sách tiêu đề cột chuẩn để đồng nhất mọi nơi"""
        return ["☑", "Tác vụ", "Ngày đến", "Số đến", "Tác giả", 
                "Số, ký hiệu văn bản", "Ngày văn bản", "Tên loại và trích yếu", 
                "Đơn vị hoặc người nhận", "Ngày chuyển", "Trạng thái", "Ghi chú"]

    def nap_danh_mục_phong_ban(self):
        """Đổ dữ liệu phòng ban vào các ComboBox trên View"""
        try:
            ds = self.model.get_phong_ban()
            self.view.set_phong_ban_list(ds)
        except Exception as e:
            print(f"Lỗi nạp danh mục đơn vị: {e}")

    def load_data(self):
        """Hàm 'Hiện tất cả' - Dùng khi mở app hoặc khi nhấn Làm mới/Refresh"""
        try:
            data = self.model.get_all()
            self.table_model = CongVanTableModel(data, self.get_headers())
            self.view.set_table_model(self.table_model)
            
            # Cập nhật trạng thái hiển thị
            count = len(data)
            self.view.show_status(f"Đã tải toàn bộ {count} công văn")
            if hasattr(self.view, 'lbl_count'): # Nếu có label hiển thị số lượng
                self.view.lbl_count.setText(f"Tổng số: {count}")
        except Exception as e:
            self.view.show_error(f"Lỗi nạp dữ liệu: {str(e)}")

    def handle_filter(self):
        """Chỉ hiện danh sách thu nhỏ khi nhấn nút Lọc"""
        try:
            # Lấy ngày từ View
            tu_ngay = self.view.date_tu_ngay.date().toString("yyyy-MM-dd")
            den_ngay = self.view.date_den_ngay.date().toString("yyyy-MM-dd")
            
            data = self.model.filter_by_ngay_den(tu_ngay, den_ngay)
            
            self.table_model = CongVanTableModel(data, self.get_headers())
            self.view.set_table_model(self.table_model)
            
            self.view.show_status(f"Tìm thấy {len(data)} mục từ {tu_ngay} đến {den_ngay}")
        except Exception as e:
            self.view.show_error(f"Lỗi lọc dữ liệu: {str(e)}")

    def tim_kiem(self, keyword):
        """Tìm kiếm linh hoạt: có keyword thì hiện kết quả, trống thì hiện tất cả"""
        try:
            if not keyword.strip():
                self.load_data() # Nếu để trống ô tìm kiếm, tự động hiện lại tất cả
                return

            data = self.model.search_by_author_or_number(keyword)
            self.table_model = CongVanTableModel(data, self.get_headers())
            self.view.set_table_model(self.table_model)
            
            self.view.show_status(f"Tìm thấy {len(data)} kết quả cho '{keyword}'")
        except Exception as e:
            self.view.show_error(f"Lỗi tìm kiếm: {str(e)}")

    def xuat_excel(self):
        """Xuất dữ liệu đang hiển thị trên bảng (đã lọc hoặc tất cả)"""
        try:
            # Lấy dữ liệu đang có trong TableModel (dữ liệu hiện tại người dùng đang thấy)
            if self.table_model and hasattr(self.table_model, '_data'):
                data = self.table_model._data
            else:
                data = self.model.get_all()

            if not data:
                self.view.show_error("Không có dữ liệu để xuất!")
                return

            success, message = export_to_excel(data)
            if success:
                self.view.show_status(f"Xuất Excel thành công: {message}")
            else:
                if "Hủy bỏ" not in message:
                    self.view.show_error(message)
        except Exception as e:
            self.view.show_error(f"Lỗi khi xuất file: {str(e)}")

    # --- Các hàm CRUD (Thêm, Sửa, Xóa) luôn làm mới bảng sau khi thực hiện ---
    def them_cong_van(self, data):
        try:
            new_id = self.model.add(data)
            self.load_data() # Hiện lại tất cả sau khi thêm
            self.view.show_status(f"Thêm thành công ID {new_id}")
        except Exception as e:
            self.view.show_error(f"Lỗi khi thêm: {str(e)}")

    def sua_cong_van(self, id_cv, new_data):
        try:
            self.model.update(id_cv, new_data)
            self.load_data() # Làm mới danh sách
            self.view.show_status(f"Đã cập nhật công văn ID {id_cv}")
        except Exception as e:
            self.view.show_error(f"Lỗi khi sửa: {str(e)}")

    def xoa_cong_van(self, id_cv):
        try:
            self.model.delete(id_cv)
            self.load_data() # Làm mới danh sách
            self.view.show_status(f"Đã xóa công văn ID {id_cv}")
        except Exception as e:
            self.view.show_error(f"Lỗi khi xóa: {str(e)}")