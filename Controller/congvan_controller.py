from Model.congvan_model import CongVanModel
from Model.congvan_table_model import CongVanTableModel
from View.quanlycongvanden import MainWindow
from View.chuyen_xu_ly_dialog import ChuyenXuLyDialog
from Utils.excel_export import export_to_excel
from Model.loaicongvan_model import LoaiCongVanModel
from PyQt6.QtWidgets import QDialog
from Model.congviec_model import CongViecModel
from datetime import datetime, timedelta

class CongVanController:
    def __init__(self, model: CongVanModel, view: MainWindow, user_session):
        self.model = model
        self.view = view
        self.user_session = user_session
        self.table_model = None

        self.view.them_cv_signal.connect(self.them_cong_van)
        self.view.sua_cv_signal.connect(self.sua_cong_van)
        self.view.xoa_cv_signal.connect(self.xoa_cong_van)
        self.view.tim_kiem_signal.connect(self.tim_kiem)
        self.view.nap_dulieu_signal.connect(self.load_data)
        self.view.loc_cv_signal.connect(self.handle_filter)
        self.view.xuat_excel_signal.connect(self.xuat_excel)
        self.view.giao_viec_signal.connect(self.giao_viec_cv)

        self.nap_danh_muc()
        self.load_data()

    def get_headers(self):
        return [
            "☑", "Tác vụ", "Ngày nhận", "Số đến", "Nơi gửi",
            "Số KH", "Ngày VB", "Trích yếu", "Người xử lý",
            "Trạng thái", "Loại VB", "Mức độ", "File đính kèm", "Ghi chú"
        ]

    def nap_danh_muc(self):
        try:
            ds_can_bo = self.model.get_danh_sach_can_bo()
            if hasattr(self.view, 'set_nhan_su_list') and ds_can_bo:
                danh_sach_ns = [{'id': cb.get('id'), 'Id': cb.get('id'), 'ten': cb.get('ho_ten'), 'ho_ten': cb.get('ho_ten')} for cb in ds_can_bo]
                self.view.set_nhan_su_list(danh_sach_ns)
        except Exception as e:
            self._handle_error(f"Lỗi nạp danh sách cán bộ: {str(e)}")

        try:
            conn_str = getattr(self.model, 'connection_string', None) or getattr(self.model, 'conn_str', None)
            if conn_str:
                loai_cv_model = LoaiCongVanModel(connection_string=conn_str)
                ds_loai_cv = loai_cv_model.get_all(trang_thai=1)
                if hasattr(self.view, 'set_loai_van_ban_list') and ds_loai_cv:
                    danh_sach_loai = [{
                        'id': x.get('Id'), 
                        'Id': x.get('Id'), 
                        'ten': x.get('TenLoai'), 
                        'ten_loai': x.get('TenLoai'), 
                        'TenLoai': x.get('TenLoai')
                    } for x in ds_loai_cv]
                    self.view.set_loai_van_ban_list(danh_sach_loai)
            else:
                if hasattr(self.model, 'get_loai_van_ban'):
                    ds_loai_cv = self.model.get_loai_van_ban()
                    if hasattr(self.view, 'set_loai_van_ban_list') and ds_loai_cv:
                        danh_sach_loai = [{
                            'id': x.get('id'), 
                            'Id': x.get('id'), 
                            'ten': x.get('ten_loai'), 
                            'ten_loai': x.get('ten_loai'), 
                            'TenLoai': x.get('ten_loai')
                        } for x in ds_loai_cv]
                        self.view.set_loai_van_ban_list(danh_sach_loai)
        except Exception as e:
            self._handle_error(f"Lỗi nạp danh mục loại văn bản: {str(e)}")

    def load_data(self):
        try:
            data = self.model.get_all(
                is_admin=self.user_session.is_admin_user(),
                role=self.user_session.get_role(),
                ten_don_vi=self.user_session.get_ten_don_vi()
            )
            self._update_table_view(data)
            if hasattr(self.view, 'cb_loai_vb'):
                self.view.cb_loai_vb.setCurrentIndex(0)
            self.view.show_status(f"Đã tải {len(data)} công văn")
        except Exception as e:
            self._handle_error(f"Lỗi tải dữ liệu: {str(e)}")

    def handle_filter(self):
        try:
            tu = self.view.date_tu_ngay.date().toString("yyyy-MM-dd")
            den = self.view.date_den_ngay.date().toString("yyyy-MM-dd")
            loai_id = self.view.cb_loai_vb.currentData()
            if self.view.chk_bo_qua_ngay.isChecked():
                tu = None
                den = None
            data = self.model.filter_by_criteria(
                tu, den, loai_id,
                is_admin=self.user_session.is_admin_user(),
                role=self.user_session.get_role(),
                ten_don_vi=self.user_session.get_ten_don_vi()
            )
            self._update_table_view(data)
            self.view.show_status(f"Lọc được {len(data)} mục")
        except Exception as e:
            self._handle_error(f"Lỗi lọc dữ liệu: {str(e)}")

    def tim_kiem(self, keyword: str):
        try:
            keyword = keyword.strip()
            if not keyword:
                self.load_data()
                return
            data = self.model.search_by_author_or_number(
                keyword,
                is_admin=self.user_session.is_admin_user(),
                role=self.user_session.get_role(),
                ten_don_vi=self.user_session.get_ten_don_vi()
            )
            self._update_table_view(data)
            self.view.show_status(f"Tìm thấy {len(data)} kết quả cho '{keyword}'")
        except Exception as e:
            self._handle_error(f"Lỗi tìm kiếm: {str(e)}")

    def xuat_excel(self):
        try:
            data = None
            if self.table_model:
                data = self.table_model.get_data() if hasattr(self.table_model, 'get_data') else getattr(self.table_model, '_data', None)
            if not data:
                data = self.model.get_all()
            if not data:
                self.view.show_error("Không có dữ liệu để xuất Excel!")
                return
            success, msg = export_to_excel(data, sheet_name="CongVanDen")
            if success:
                self.view.show_status(msg)
            else:
                self.view.show_error(msg)
        except Exception as e:
            self._handle_error(f"Lỗi xuất Excel: {str(e)}")

    def them_cong_van(self, data: dict):
        try:
            new_id = self.model.add(data)
            self.load_data()
            self.view.show_status(f"Tiếp nhận thành công công văn ID {new_id}")
        except Exception as e:
            self._handle_error(f"Lỗi tiếp nhận: {str(e)}")

    def sua_cong_van(self, id_cv: int, new_data: dict):
        try:
            self.model.update(id_cv, new_data)
            self.load_data()
            self.view.show_status(f"Cập nhật ID {id_cv} thành công")
        except Exception as e:
            self._handle_error(f"Lỗi cập nhật: {str(e)}")

    def xoa_cong_van(self, id_cv: int):
        try:
            self.model.delete(id_cv)
            self.load_data()
            self.view.show_status(f"Đã xóa công văn ID {id_cv}")
        except Exception as e:
            self._handle_error(f"Lỗi xóa công văn: {str(e)}")

    def giao_viec_cv(self, id_cv: int):
        try:
            cv_info = self.model.get_by_id(id_cv)
            if not cv_info:
                self.view.show_error("Không tìm thấy công văn!")
                return

            ds_can_bo = self.model.get_danh_sach_can_bo()
            if not ds_can_bo:
                self.view.show_error("Không thể lấy danh sách cán bộ!")
                return

            dialog = ChuyenXuLyDialog(ds_can_bo, self.view)
            dialog.setWindowTitle("Phân công xử lý công văn thành công việc")
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                nguoi_nhan_id = data.get('chu_tri_id')
                print(f"[DEBUG] Người nhận ID: {nguoi_nhan_id}, loại: {type(nguoi_nhan_id)}")
                if not nguoi_nhan_id:
                    self.view.show_error("Chưa chọn người xử lý!")
                    return

                # Ép kiểu về int để tránh lỗi
                try:
                    nguoi_nhan_id = int(nguoi_nhan_id)
                except (TypeError, ValueError):
                    self.view.show_error("ID người xử lý không hợp lệ!")
                    return

                conn_str = self.model.get_connection_string()
                cv_model = CongViecModel(conn_str)
                noi_dung_task = data.get('noi_dung', '').strip()
                if not noi_dung_task:
                    noi_dung_task = f"Xử lý công văn: {cv_info.get('KyHieu', '')} - {cv_info.get('TrichYeu', '')}"
                han_xl = data.get('ngay_xu_ly')
                if not han_xl:
                    han_xl = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

                new_task_id = cv_model.them(
                    id_cv_den=id_cv,
                    noi_dung=noi_dung_task,
                    nguoi_giao=self.user_session.user_id,
                    nguoi_nhan=nguoi_nhan_id,
                    han_xu_ly=han_xl
                )
                print(f"[DEBUG] Đã tạo công việc ID: {new_task_id} cho người {nguoi_nhan_id}")
                cv_model.them_lich_su(new_task_id, self.user_session.user_id, "Phân công",
                                      f"Giao cho {data.get('chu_tri_ten', '')} xử lý công văn {cv_info.get('KyHieu', '')}")
                self.view.show_status(f"Đã tạo công việc và giao cho {data.get('chu_tri_ten', '')}")
                self.model.update_trang_thai(id_cv, 2)
        except Exception as e:
            self.view.show_error(f"Lỗi phân công: {str(e)}")

    def _update_table_view(self, data: list):
        self.table_model = CongVanTableModel(data, self.get_headers())
        self.view.set_table_model(self.table_model)

    def _handle_error(self, error_msg: str):
        print(error_msg)
        if hasattr(self.view, 'show_error'):
            self.view.show_error(error_msg)