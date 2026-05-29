from Utils.excel_export import export_to_excel
from Model.congvandi_model import CongVanDiModel
from Model.congvandi_table_model import CongVanDiTableModel
from View.quanlycongvandi import MainWindowDi
from Model.loaicongvan_model import LoaiCongVanModel 
import pyodbc
import os
import shutil
from datetime import datetime
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices

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

        self.nap_danh_muc()
        self.load_data()

    def get_headers(self):
        return ["ID", "Số đi", "Năm", "Ký hiệu", "Ngày ký", "Nơi nhận", "Trích yếu", "Trạng thái", "Mức độ", "File"]

    def nap_danh_muc(self):
        conn_str = self.model.conn_str

        # 1. Loại văn bản đi từ Database
        try:
            lcv_model = LoaiCongVanModel(conn_str)
            ds_loai = lcv_model.get_all(trang_thai=2) # Lấy loại Đi (2) và Dùng chung (3)
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

        # 2. Đơn vị - dùng bảng DonViTrucThuoc (Đã sửa lỗi chính tả chữ 'c')
        donvi_list = []
        try:
            with pyodbc.connect(conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, TenDonVi FROM DonViTrucThuoc ORDER BY TenDonVi")
                donvi_list = [{'id': row[0], 'ten_don_vi': row[1]} for row in cursor.fetchall()]
        except Exception as e:
            print(f"Lỗi nạp đơn vị: {e}")
        self.view.set_don_vi_list(donvi_list)

        # 3. Nhân sự
        try:
            with pyodbc.connect(conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Id, HoTen FROM CanBo ORDER BY HoTen")
                nhansu_list = [{'id': row[0], 'ten': row[1], 'ho_ten': row[1]} for row in cursor.fetchall()]
                self.view.set_nhan_su_list(nhansu_list)
        except Exception as e:
            print(f"Lỗi nạp nhân sự: {e}")
            self.view.set_nhan_su_list([])

    def load_data(self):
        try:
            data = self.model.get_all(
                tu_ngay=self.current_tu_ngay,
                den_ngay=self.current_den_ngay,
                keyword=self.current_keyword,
                is_admin=self.user_session.is_admin_user(),
                role=self.user_session.get_role(),
                ten_don_vi=self.user_session.get_ten_don_vi()
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

    def them_cong_van(self, data: dict):
        try:
            file_path = data.get('FilePath')
            if file_path and os.path.isfile(file_path):
                dest_dir = "attachments"
                os.makedirs(dest_dir, exist_ok=True)
                base, ext = os.path.splitext(os.path.basename(file_path))
                new_name = f"{base}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
                dest_path = os.path.join(dest_dir, new_name)
                shutil.copy2(file_path, dest_path)
                data['FilePath'] = dest_path
            else:
                data['FilePath'] = None
            self.model.add(data)
            self.load_data()
            self.view.show_status("Thêm công văn đi thành công!")
        except Exception as e:
            self.view.show_error(f"Lỗi thêm: {str(e)}")

    def sua_cong_van(self, id_cv: int, new_data: dict):
        try:
            file_path = new_data.get('FilePath')
            if file_path and os.path.isfile(file_path):
                dest_dir = "attachments"
                os.makedirs(dest_dir, exist_ok=True)
                base, ext = os.path.splitext(os.path.basename(file_path))
                new_name = f"{base}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
                dest_path = os.path.join(dest_dir, new_name)
                shutil.copy2(file_path, dest_path)
                new_data['FilePath'] = dest_path
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