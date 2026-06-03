import os
import shutil
from datetime import datetime, timedelta
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QDialog
from Utils.excel_export import export_to_excel
from Model.congvandi_model import CongVanDiModel
from Model.congvandi_table_model import CongVanDiTableModel
from View.quanlycongvandi import MainWindowDi
from Model.loaicongvan_model import LoaiCongVanModel
from Model.hanbaoquan_model import HanBaoQuanModel
from Model.hoso_congvandi_model import HoSoCongVanDiModel
from Model.congviec_model import CongViecModel
from View.dialog_luu_hoso import LuuHoSoDialog
import pyodbc

class CongVanDiController:
    def __init__(self, model: CongVanDiModel, view: MainWindowDi, user_session):
        self.model = model
        self.view = view
        self.user_session = user_session
        self.table_model = None

        self.current_keyword = None
        self.current_tu_ngay = None
        self.current_den_ngay = None

        self.view.them_cv_signal.connect(self.them_cong_van)
        self.view.sua_cv_signal.connect(self.sua_cong_van)
        self.view.xoa_cv_signal.connect(self.xoa_cong_van)
        self.view.tim_kiem_signal.connect(self.tim_kiem)
        self.view.loc_cv_signal.connect(self.loc_cong_van)
        self.view.nap_dulieu_signal.connect(self.nap_lai_du_lieu)
        self.view.xuat_excel_signal.connect(self.xuat_excel)
        self.view.table_view.clicked.connect(self.on_table_click)
        self.view.luu_hoso_signal.connect(self.luu_vao_hoso)
        self.view.ky_cv_signal.connect(self.ky_cong_van)

        self.nap_danh_muc()
        self.load_data()

    def get_headers(self):
        return ["ID", "Số đi", "Năm", "Ký hiệu", "Ngày ký", "Nơi nhận", "Trích yếu", "Trạng thái", "Mức độ", "File"]

    def nap_danh_muc(self):
        conn_str = self.model.conn_str

        try:
            lcv_model = LoaiCongVanModel(conn_str)
            ds_loai = lcv_model.get_all(trang_thai=2)
            loai_list = [{
                'id': item.get('Id'),
                'Id': item.get('Id'),
                'ten': item.get('TenLoai'),
                'ten_loai': item.get('TenLoai'),
                'TenLoai': item.get('TenLoai'),
                'ma_loai': item.get('MaLoai', '')
            } for item in ds_loai]
            self.view.set_loai_van_ban_list(loai_list)
        except Exception as e:
            print(f"Lỗi nạp loại văn bản: {e}")

        donvi_list = []
        try:
            with pyodbc.connect(conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, TenDonVi FROM DonViTrucThuoc ORDER BY TenDonVi")
                donvi_list = [{'id': row[0], 'ten_don_vi': row[1]} for row in cursor.fetchall()]
        except Exception as e:
            print(f"Lỗi nạp đơn vị: {e}")
        self.view.set_don_vi_list(donvi_list)

        try:
            with pyodbc.connect(conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, HoTen FROM CanBo ORDER BY HoTen")
                nhansu_list = [{'id': row[0], 'ten': row[1], 'ho_ten': row[1]} for row in cursor.fetchall()]
                self.view.set_nhan_su_list(nhansu_list)
        except Exception as e:
            print(f"Lỗi nạp nhân sự: {e}")
            self.view.set_nhan_su_list([])

        try:
            with pyodbc.connect(conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, KyHieu, TrichYeu FROM CongVanDen ORDER BY Id DESC")
                cvden_list = [{'id': row[0], 'so_ky_hieu': row[1], 'trich_yeu': row[2] or ''} for row in cursor.fetchall()]
                self.view.set_cv_den_list(cvden_list)
        except Exception as e:
            print(f"Lỗi nạp công văn đến: {e}")
            self.view.set_cv_den_list([])

    def load_data(self):
        try:
            user_id = self.user_session.user_id
            role = self.user_session.get_role()
            if user_id == 1 or role == 'Giám đốc' or role == 'Admin':
                is_admin = True
            else:
                is_admin = self.user_session.is_admin_user()
            data = self.model.get_all(
                tu_ngay=self.current_tu_ngay,
                den_ngay=self.current_den_ngay,
                keyword=self.current_keyword,
                is_admin=is_admin,
                role=role,
                ten_don_vi=self.user_session.get_ten_don_vi(),
                nguoi_tao_id=user_id
            )
            self.table_model = CongVanDiTableModel(data, self.get_headers())
            self.view.set_table_model(self.table_model)
            self.view.show_status(f"Đã tải {len(data)} công văn đi")
        except Exception as e:
            self.view.show_error(f"Lỗi tải dữ liệu: {str(e)}")

    def nap_lai_du_lieu(self):
        self.current_keyword = None
        self.current_tu_ngay = None
        self.current_den_ngay = None
        if hasattr(self.view, 'search_input'):
            self.view.search_input.clear()
        self.load_data()

    def tim_kiem(self, keyword: str):
        if not keyword.strip():
            self.current_keyword = None
        else:
            self.current_keyword = keyword.strip()
        self.load_data()

    def loc_cong_van(self, tu_ngay: str, den_ngay: str):
        self.current_tu_ngay = tu_ngay
        self.current_den_ngay = den_ngay
        self.load_data()

    def _copy_file(self, source_path):
        if not source_path or not os.path.isfile(source_path):
            return None
        dest_dir = "attachments_di"
        os.makedirs(dest_dir, exist_ok=True)
        base = os.path.basename(source_path)
        new_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{base}"
        dest_path = os.path.join(dest_dir, new_name)
        shutil.copy2(source_path, dest_path)
        return dest_path

    def them_cong_van(self, data: dict):
        try:
            data['NguoiTaoId'] = self.user_session.user_id
            # Mặc định trạng thái = 1 (Chờ ký)
            data['TrangThaiChuyen'] = 1
            file_path = data.get('FilePath')
            if file_path and os.path.isfile(file_path):
                data['FilePath'] = self._copy_file(file_path)
            self.model.add(data)
            self.load_data()
            self.view.show_status("Thêm công văn đi thành công!")
        except Exception as e:
            self.view.show_error(f"Lỗi thêm: {str(e)}")

    def sua_cong_van(self, id_cv: int, new_data: dict):
        try:
            # Không cho phép sửa trạng thái qua form
            new_data.pop('TrangThaiChuyen', None)
            file_path = new_data.get('FilePath')
            if file_path and os.path.isfile(file_path):
                new_data['FilePath'] = self._copy_file(file_path)
            self.model.update(id_cv, new_data)
            self.load_data()
            self.view.show_status("Cập nhật thành công")
        except Exception as e:
            self.view.show_error(f"Lỗi cập nhật: {str(e)}")

    def xoa_cong_van(self, id_cv: int):
        try:
            self.model.delete(id_cv)
            self.load_data()
            self.view.show_status("Đã xóa công văn!")
        except Exception as e:
            self.view.show_error(f"Lỗi xóa: {str(e)}")

    def xuat_excel(self):
        try:
            data = self.table_model._data if self.table_model else []
            if not data:
                self.view.show_error("Không có dữ liệu để xuất!")
                return
            success, msg = export_to_excel(data, sheet_name="CongVanDi")
            if success:
                self.view.show_status(msg)
            else:
                self.view.show_error(msg)
        except Exception as e:
            self.view.show_error(f"Lỗi xuất Excel: {str(e)}")

    def on_table_click(self, index):
        if not self.table_model:
            return
        file_path = self.table_model.data(index, Qt.ItemDataRole.UserRole)
        if file_path and isinstance(file_path, str) and os.path.exists(file_path):
            try:
                QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.abspath(file_path)))
            except Exception as e:
                self.view.show_error(f"Không thể mở file: {str(e)}")

    def luu_vao_hoso(self, congvan_id):
        try:
            conn_str = self.model.conn_str
            with pyodbc.connect(conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, TieuDeHoSo FROM QuanLyHoSo ORDER BY TieuDeHoSo")
                ds_hoso = [{'Id': row[0], 'TieuDeHoSo': row[1]} for row in cursor.fetchall()]
            if not ds_hoso:
                self.view.show_error("Chưa có hồ sơ nào. Vui lòng tạo hồ sơ trước (trong mục Quản lý hồ sơ).")
                return
            hbq_model = HanBaoQuanModel(conn_str)
            ds_hanbaoquan = hbq_model.get_all()
            dialog = LuuHoSoDialog(ds_hoso, ds_hanbaoquan, self.view)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                hoso_id = data['hoso_id']
                hanbaoquan_id = data['hanbaoquan_id']
                hs_cv_model = HoSoCongVanDiModel(conn_str)
                if hs_cv_model.da_luu_chua(hoso_id, congvan_id):
                    self.view.show_error("Công văn này đã được lưu vào hồ sơ đã chọn!")
                    return
                hs_cv_model.luu_cong_van_vao_hoso(hoso_id, congvan_id, hanbaoquan_id)
                # Chuyển trạng thái thành Đã phát hành (3)
                self.model.update_trang_thai(congvan_id, 3)
                self.load_data()
                self.view.show_status("Đã lưu công văn vào hồ sơ thành công!")
        except Exception as e:
            self.view.show_error(f"Lỗi lưu hồ sơ: {str(e)}")

    def ky_cong_van(self, id_cv: int):
        try:
            conn = self.model._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT NguoiKyId, TrangThaiChuyen FROM CongVanPhatHanh WHERE Id = ?", (id_cv,))
            row = cursor.fetchone()
            conn.close()
            if not row:
                self.view.show_error("Không tìm thấy công văn!")
                return
            nguoi_ky_id, trang_thai = row
            if trang_thai != 1:
                self.view.show_error("Công văn không ở trạng thái chờ ký!")
                return
            if nguoi_ky_id != self.user_session.user_id:
                self.view.show_error("Bạn không có quyền ký công văn này!")
                return
            # Cập nhật trạng thái thành Đã ký (2)
            self.model.update_trang_thai(id_cv, 2)
            self.load_data()
            self.view.show_status("Đã ký công văn thành công!")
        except Exception as e:
            self.view.show_error(f"Lỗi ký: {str(e)}")