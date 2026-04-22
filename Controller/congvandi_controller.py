from Model.congvandi_model import CongVanDiModel
from Model.congvandi_table_model import CongVanDiTableModel
from View.quanlycongvandi import MainWindowDi
import pandas as pd
import os # Thêm để xử lý đường dẫn file
from PyQt6.QtWidgets import QFileDialog

class CongVanDiController:
    def __init__(self, model: CongVanDiModel, view: MainWindowDi):
        self.model = model
        self.view = view
        
        # Tải dữ liệu lần đầu khi khởi chạy
        self.load_data()

        # --- KẾT NỐI SIGNALS TỪ VIEW ---
        self.view.them_cv_signal.connect(self.them_cong_van)
        self.view.sua_cv_signal.connect(self.sua_cong_van)
        self.view.xoa_cv_signal.connect(self.xoa_cong_van)
        self.view.tim_kiem_signal.connect(self.tim_kiem)
        self.view.loc_cv_signal.connect(self.loc_du_lieu)
        self.view.xuat_excel_signal.connect(self.xuat_excel)
        self.view.nap_dulieu_signal.connect(self.load_data)

    def update_view_table(self, data):
        """Hàm dùng chung để cập nhật bảng hiển thị"""
        # Thêm cột File vào Header nếu bạn muốn hiển thị trên bảng
        headers = ["ID", "Số đi", "Năm", "Ký hiệu", "Ngày ký", "Nơi nhận", "Trích yếu", "Trạng thái", "File"]
        self.table_model = CongVanDiTableModel(data, headers)
        self.view.set_table_model(self.table_model)

    def load_data(self):
        try:
            data = self.model.get_all()
            # Cập nhật Header có thêm cột File
            headers = ["ID", "Số đi", "Năm", "Ký hiệu", "Ngày ký", "Nơi nhận", "Trích yếu", "Trạng thái", "Hồ sơ", "File"]
            from Model.congvandi_table_model import CongVanDiTableModel
            self.table_model = CongVanDiTableModel(data, headers)
            self.view.set_table_model(self.table_model)
            self.view.show_status(f"Đã tải {len(data)} công văn") # Sẽ không còn lỗi nhờ bước 2
        except Exception as e:
            self.view.show_error(f"Lỗi: {str(e)}")

    def them_cong_van(self, data):
        if data:
            try:
                self.model.add(data)
                self.load_data()
                self.view.show_status("Thêm công văn thành công!")
            except Exception as e:
                self.view.show_error(f"Lỗi thêm dữ liệu: {str(e)}")

    def sua_cong_van(self, id_cv, new_data):
        try:
            self.model.update(id_cv, new_data)
            self.load_data()
            self.view.show_status("Cập nhật thành công")
        except Exception as e:
            self.view.show_error(f"Lỗi sửa: {str(e)}")

    def xoa_cong_van(self, id_cv):
        try:
            self.model.delete(id_cv)
            self.load_data()
            self.view.show_status("Đã xóa công văn")
        except Exception as e:
            self.view.show_error(f"Lỗi xóa: {str(e)}")

    def tim_kiem(self, keyword):
        try:
            if not keyword.strip():
                self.load_data()
            else:
                data = self.model.search(keyword)
                self.update_view_table(data)
                self.view.show_status(f"Tìm thấy {len(data)} kết quả")
        except Exception as e:
            self.view.show_error(f"Lỗi tìm kiếm: {str(e)}")

    def loc_du_lieu(self, qdate_tu, qdate_den):
        try:
            str_tu = qdate_tu.toString("yyyy-MM-dd")
            str_den = qdate_den.toString("yyyy-MM-dd")
            data = self.model.filter_by_date(str_tu, str_den)
            self.update_view_table(data)
            self.view.show_status(f"Tìm thấy {len(data)} công văn")
        except Exception as e:
            self.view.show_error(f"Lỗi lọc dữ liệu: {str(e)}")

    def xuat_excel(self):
        """Xử lý xuất dữ liệu ra file Excel"""
        try:
            data = self.model.get_all() 
            if not data:
                self.view.show_error("Không có dữ liệu để xuất!")
                return

            file_path, _ = QFileDialog.getSaveFileName(
                self.view, "Lưu file Excel", "Danh_muc_cong_van_di.xlsx", "Excel Files (*.xlsx)"
            )

            if file_path:
                df = pd.DataFrame(data)
                # Đổi tên cột cho tiếng Việt chuyên nghiệp
                mapping = {
                    "SoPhatHanh": "Số đi", 
                    "Nam": "Năm", 
                    "KyHieu": "Ký hiệu",
                    "NgayKy": "Ngày ký", 
                    "NoiNhan": "Nơi nhận", 
                    "TrichYeu": "Trích yếu nội dung", 
                    "TrangThaiChuyen": "Trạng thái",
                    "GhiChu": "Hồ sơ công việc",
                    "FilePath": "Đường dẫn File"
                }
                df = df.rename(columns=mapping)
                
                # Chỉ lấy những cột có trong mapping để xuất
                available_cols = [v for k, v in mapping.items() if v in df.columns]
                df[available_cols].to_excel(file_path, index=False)
                
                self.view.show_status(f"Xuất file thành công!")
        except Exception as e:
            self.view.show_error(f"Lỗi xuất file Excel: {str(e)}")