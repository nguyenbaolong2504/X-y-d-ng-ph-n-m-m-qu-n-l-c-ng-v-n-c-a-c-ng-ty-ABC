from Model.congvandi_model import CongVanDiModel
from Model.congvandi_table_model import CongVanDiTableModel
from View.quanlycongvandi import MainWindowDi


class CongVanDiController:
    def __init__(self, model: CongVanDiModel, view: MainWindowDi, user_session):
        self.model = model
        self.view = view
        self.user_session = user_session
        self.table_model = None

        self.view.them_cv_signal.connect(self.them_cong_van)
        self.view.sua_cv_signal.connect(self.sua_cong_van)
        self.view.xoa_cv_signal.connect(self.xoa_cong_van)
        self.view.tim_kiem_signal.connect(self.tim_kiem)
        self.view.loc_cv_signal.connect(self.loc_cong_van)
        self.view.nap_dulieu_signal.connect(self.load_data)
        self.view.xuat_excel_signal.connect(self.xuat_excel)

        self.load_data()

    def get_headers(self):
        return ["ID", "Số đi", "Năm", "Ký hiệu", "Ngày ký", "Nơi nhận", "Trích yếu", "Trạng thái"]

    def load_data(self):
        try:
            data = self.model.get_all(
                is_admin=self.user_session.is_admin_user(),
                role=self.user_session.get_role(),
                ten_don_vi=self.user_session.get_ten_don_vi()
            )
            self.table_model = CongVanDiTableModel(data, self.get_headers())
            self.view.set_table_model(self.table_model)
            self.view.show_status(f"Đã tải {len(data)} công văn đi")
        except Exception as e:
            self.view.show_error(f"Lỗi tải dữ liệu: {str(e)}")

    def them_cong_van(self, data: dict):
        try:
            self.model.add(data)
            self.load_data()
            self.view.show_status("Thêm công văn đi thành công!")
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
            self.view.show_status(f"Đã xóa công văn đi ID {id_cv}")
        except Exception as e:
            self.view.show_error(f"Lỗi xóa: {str(e)}")

    def tim_kiem(self, keyword: str):
        # Tạm thời gọi load_data, bạn có thể implement search riêng nếu cần
        self.load_data()

    def loc_cong_van(self, tu, den):
        # Tạm thời gọi load_data, bạn có thể implement filter riêng
        self.load_data()

    def xuat_excel(self):
        try:
            data = self.table_model._data if self.table_model else self.model.get_all()
            if not data:
                self.view.show_error("Không có dữ liệu!")
                return
            # Giả sử bạn có hàm export_to_excel cho công văn đi
            from Utils.excel_export import export_to_excel
            success, msg = export_to_excel(data, sheet_name="CongVanDi")
            if success:
                self.view.show_status(msg)
            else:
                self.view.show_error(msg)
        except Exception as e:
            self.view.show_error(f"Lỗi xuất Excel: {str(e)}")