from PyQt6.QtWidgets import QMessageBox, QDialog 
from View.quanlyxulycongvan import XuLyCongVanDialog

class CongVanController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        
        # Kết nối sự kiện cơ bản
        self.view.btn_refresh.clicked.connect(self.load_data)
        self.view.btn_add.clicked.connect(self.show_add_dialog)
        self.view.btn_search.clicked.connect(self.search_data)

        # Nạp dữ liệu lần đầu
        self.load_data()

    def load_data(self):
        # Xóa dữ liệu cũ trên bảng
        self.view.table.setRowCount(0)
        
        # Lấy dữ liệu từ Model
        try:
            data_list = self.model.get_all_xuly()
            self.view.table.setRowCount(len(data_list))
            
            for row_idx, data in enumerate(data_list):
                btn_edit, btn_delete = self.view.add_row_to_table(row_idx, data)
                
                # Gán sự kiện click cho từng nút trên từng hàng
                btn_delete.clicked.connect(lambda checked, d=data: self.handle_delete(d['Id']))
                btn_edit.clicked.connect(lambda checked, d=data: self.handle_edit(d))
                
        except Exception as e:
            QMessageBox.critical(self.view, "Lỗi Database", f"Không thể tải dữ liệu: {str(e)}")

    def search_data(self):
        # Tính năng tìm kiếm cơ bản (Lọc text trên bảng)
        keyword = self.view.txt_search.text().lower()
        for row in range(self.view.table.rowCount()):
            match = False
            for col in range(self.view.table.columnCount() - 1): # Bỏ qua cột thao tác
                item = self.view.table.item(row, col)
                if item and keyword in item.text().lower():
                    match = True
                    break
            self.view.table.setRowHidden(row, not match)

    def handle_delete(self, record_id):
        reply = QMessageBox.question(
            self.view, 'Xác nhận xóa', 
            'Bạn có chắc chắn muốn xóa dữ liệu xử lý công văn này?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = self.model.delete_xuly(record_id)
            if success:
                QMessageBox.information(self.view, "Thành công", "Đã xóa bản ghi thành công!")
                self.load_data() 
            else:
                QMessageBox.warning(self.view, "Thất bại", "Không thể xóa. Vui lòng kiểm tra lại.")

    def show_add_dialog(self):
        try:
            # 1. Lấy dữ liệu danh mục từ các bảng liên quan để người dùng chọn (không phải nhập ID)
            lists = {
                'canbo': self.model.get_list_canbo(),    # Lấy từ bảng CanBo
                'donvi': self.model.get_list_donvi(),    # Lấy từ bảng DonViTrucThuoc
                'congvan': self.model.get_list_congvan() # Lấy từ bảng CongVanDen
            }

            # 2. Khởi tạo Dialog và truyền danh sách vào
            dialog = XuLyCongVanDialog(self.view, lists=lists)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_data = dialog.get_values() # Dùng get_values() khớp với View mới
                if new_data:
                    self.model.add_xuly(new_data)
                    QMessageBox.information(self.view, "Thành công", "Đã phân công xử lý công văn!")
                    self.load_data()
                    
        except Exception as e:
            QMessageBox.critical(self.view, "Lỗi hệ thống", f"Không thể mở form thêm: {str(e)}")

    def handle_edit(self, data):
        # Mở dialog với dữ liệu cũ (data truyền vào từ nút bấm trên hàng)
        dialog = XuLyCongVanDialog(self.view, data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_data()
            updated_data['Id'] = data['Id'] # Giữ nguyên ID để Update
            try:
                self.model.update_xuly(updated_data)
                QMessageBox.information(self.view, "Thành công", "Đã cập nhật dữ liệu!")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self.view, "Lỗi", f"Không thể cập nhật: {str(e)}")