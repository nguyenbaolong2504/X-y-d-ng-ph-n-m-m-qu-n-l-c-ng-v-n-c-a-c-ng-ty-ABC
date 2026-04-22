import pandas as pd
from PyQt6.QtWidgets import QFileDialog

def export_to_excel(data, default_filename="Danh_sach_cong_van.xlsx"):
    if not data:
        return False, "Không có dữ liệu để xuất"
    
    try:
        # Chuyển đổi list dict sang DataFrame
        df = pd.DataFrame(data)
        
        # Mapping lại tên cột cho thân thiện với Excel
        column_mapping = {
            'id': 'ID',
            'ngay_den': 'Ngày đến',
            'so_den': 'Số đến',
            'tac_gia': 'Nơi phát hành',
            'so_ky_hieu': 'Số ký hiệu',
            'ngay_van_ban': 'Ngày văn bản',
            'trich_yeu': 'Trích yếu',
            'don_vi_nhan': 'Đơn vị nhận',
            'ngay_chuyen': 'Ngày chuyển',
            'trang_thai': 'Trạng thái',
            'ghi_chu': 'Ghi chú'
        }
        df = df.rename(columns=column_mapping)

        # Mở hộp thoại lưu file
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Lưu file Excel", default_filename, "Excel Files (*.xlsx)"
        )
        
        if file_path:
            df.to_excel(file_path, index=False)
            return True, file_path
        return False, "Hủy bỏ xuất file"
    except Exception as e:
        return False, str(e)