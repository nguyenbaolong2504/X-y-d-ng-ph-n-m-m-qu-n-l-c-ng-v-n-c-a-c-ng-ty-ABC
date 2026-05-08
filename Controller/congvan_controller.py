from Model.congvan_model import CongVanModel
from Model.congvan_table_model import CongVanTableModel
from View.quanlycongvanden import MainWindow
from Utils.excel_export import export_to_excel


class CongVanController:
    def __init__(self, model: CongVanModel, view: MainWindow):
        self.model = model
        self.view = view
        self.table_model = None

        self.view.them_cv_signal.connect(self.them_cong_van)
        self.view.sua_cv_signal.connect(self.sua_cong_van)
        self.view.xoa_cv_signal.connect(self.xoa_cong_van)
        self.view.tim_kiem_signal.connect(self.tim_kiem)
        self.view.nap_dulieu_signal.connect(self.load_data)
        self.view.loc_cv_signal.connect(self.handle_filter)
        self.view.xuat_excel_signal.connect(self.xuat_excel)

        self.nap_danh_muc()
        self.load_data()

    def get_headers(self):
        return [
            "☑", "Tác vụ", "Ngày đến", "Số đến", "Tác giả / Cơ quan",
            "Số ký hiệu", "Ngày VB", "Trích yếu", "Đơn vị nhận",
            "Ngày chuyển", "Trạng thái", "Loại văn bản", "File", "Ghi chú"
        ]

    def nap_danh_muc(self):
        try:
            ds_pb = self.model.get_phong_ban()
            self.view.set_phong_ban_list(ds_pb)
        except Exception as e:
            print(f"Lỗi nạp phòng ban: {e}")
        try:
            ds_loai = self.model.get_loai_van_ban()
            self.view.set_loai_van_ban_list(ds_loai)
        except Exception as e:
            print(f"Lỗi nạp loại văn bản: {e}")

    def load_data(self):
        try:
            data = self.model.get_all()
            self.table_model = CongVanTableModel(data, self.get_headers())
            self.view.set_table_model(self.table_model)
            # Reset combobox lọc loại về "Tất cả"
            self.view.cb_loai_vb.setCurrentIndex(0)
            self.view.show_status(f"Đã tải {len(data)} công văn")
        except Exception as e:
            self.view.show_error(f"Lỗi tải dữ liệu: {str(e)}")

    def handle_filter(self):
        try:
            tu = self.view.date_tu_ngay.date().toString("yyyy-MM-dd")
            den = self.view.date_den_ngay.date().toString("yyyy-MM-dd")
            loai_id = self.view.cb_loai_vb.currentData()   # None nếu là "Tất cả"

            # Nếu checkbox "Bỏ qua ngày" được chọn, truyền None cho ngày
            if self.view.chk_bo_qua_ngay.isChecked():
                tu = None
                den = None

            data = self.model.filter_by_criteria(tu, den, loai_id)
            self.table_model = CongVanTableModel(data, self.get_headers())
            self.view.set_table_model(self.table_model)
            self.view.show_status(f"Lọc được {len(data)} mục")
        except Exception as e:
            self.view.show_error(f"Lỗi lọc: {str(e)}")

    def tim_kiem(self, keyword: str):
        try:
            if not keyword.strip():
                self.load_data()
                return
            data = self.model.search_by_author_or_number(keyword)
            self.table_model = CongVanTableModel(data, self.get_headers())
            self.view.set_table_model(self.table_model)
            self.view.show_status(f"Tìm thấy {len(data)} kết quả")
        except Exception as e:
            self.view.show_error(f"Lỗi tìm kiếm: {str(e)}")

    def xuat_excel(self):
        try:
            data = self.table_model._data if self.table_model else self.model.get_all()
            if not data:
                self.view.show_error("Không có dữ liệu!")
                return
            success, msg = export_to_excel(data)
            if success:
                self.view.show_status(msg)
            else:
                self.view.show_error(msg)
        except Exception as e:
            self.view.show_error(f"Lỗi xuất Excel: {str(e)}")

    def them_cong_van(self, data: dict):
        try:
            new_id = self.model.add(data)
            self.load_data()
            self.view.show_status(f"Thêm thành công ID {new_id}")
        except Exception as e:
            self.view.show_error(f"Lỗi thêm: {str(e)}")

    def sua_cong_van(self, id_cv: int, new_data: dict):
        try:
            self.model.update(id_cv, new_data)
            self.load_data()
            self.view.show_status(f"Cập nhật ID {id_cv} thành công")
        except Exception as e:
            self.view.show_error(f"Lỗi cập nhật: {str(e)}")

    def xoa_cong_van(self, id_cv: int):
        try:
            self.model.delete(id_cv)
            self.load_data()
            self.view.show_status(f"Đã xóa công văn ID {id_cv}")
        except Exception as e:
            self.view.show_error(f"Lỗi xóa: {str(e)}")