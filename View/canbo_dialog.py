from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate

class CanBoDialog(QDialog):
    def __init__(self, parent=None, data=None, don_vi_list=[], chuc_vu_list=[]):
        super().__init__(parent)
        self.setWindowTitle("Thông tin cán bộ" if not data else "Cập nhật cán bộ")
        self.setFixedWidth(450)
        self.data = data
        self.don_vi_list = don_vi_list
        self.chuc_vu_list = chuc_vu_list
        self.setup_ui()
        if data: self.fill_data()

    def setup_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(10)

        self.txt_hoten = QLineEdit()
        self.date_ngaysinh = QDateEdit(calendarPopup=True)
        self.date_ngaysinh.setDisplayFormat("yyyy-MM-dd")
        self.date_ngaysinh.setDate(QDate.currentDate())
        
        self.cmb_gioitinh = QComboBox()
        self.cmb_gioitinh.addItems(["Nữ", "Nam"]) # 0: Nữ, 1: Nam
        
        self.cmb_donvi = QComboBox()
        for dv in self.don_vi_list: 
            # dv[0] là Id, dv[1] là TenDonVi
            self.cmb_donvi.addItem(str(dv[1]), dv[0])
            
        self.cmb_chucvu = QComboBox()
        for cv in self.chuc_vu_list: 
            self.cmb_chucvu.addItem(str(cv[1]), cv[0])

        self.txt_username = QLineEdit()
        self.txt_email = QLineEdit()
        self.txt_mobile = QLineEdit()
        
        layout.addRow("Họ và tên (*):", self.txt_hoten)
        layout.addRow("Ngày sinh:", self.date_ngaysinh)
        layout.addRow("Giới tính:", self.cmb_gioitinh)
        layout.addRow("Đơn vị:", self.cmb_donvi)
        layout.addRow("Chức vụ:", self.cmb_chucvu)
        layout.addRow("Tên truy cập (*):", self.txt_username)
        layout.addRow("Email:", self.txt_email)
        layout.addRow("Số điện thoại:", self.txt_mobile)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.validate_and_accept)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)

    def fill_data(self):
        """Đổ dữ liệu cũ vào form khi sửa"""
        self.txt_hoten.setText(self.data.get('HoTen', ''))
        if self.data.get('NgaySinh'):
            self.date_ngaysinh.setDate(QDate.fromString(str(self.data['NgaySinh']), "yyyy-MM-dd"))
        self.cmb_gioitinh.setCurrentIndex(1 if self.data.get('GioiTinh') == 1 else 0)
        self.txt_username.setText(self.data.get('Username', ''))
        self.txt_email.setText(str(self.data.get('Email') or ""))
        self.txt_mobile.setText(str(self.data.get('Mobile') or ""))
        
        # Chọn đúng đơn vị/chức vụ trong combobox
        index_dv = self.cmb_donvi.findData(self.data.get('DonViId'))
        if index_dv >= 0: self.cmb_donvi.setCurrentIndex(index_dv)
        index_cv = self.cmb_chucvu.findData(self.data.get('ChucVuId'))
        if index_cv >= 0: self.cmb_chucvu.setCurrentIndex(index_cv)

    def validate_and_accept(self):
        if not self.txt_hoten.text() or not self.txt_username.text():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ Họ tên và Tên truy cập!")
            return
        self.accept()

    def get_data(self):
        return {
            "Id": self.data['Id'] if self.data else None,
            "HoTen": self.txt_hoten.text(),
            "NgaySinh": self.date_ngaysinh.date().toPyDate(),
            "GioiTinh": self.cmb_gioitinh.currentIndex(),
            "DonViId": self.cmb_donvi.currentData(),
            "ChucVuId": self.cmb_chucvu.currentData(),
            "Username": self.txt_username.text(),
            "Password": "123", # Mặc định cho người mới
            "Email": self.txt_email.text(),
            "Mobile": self.txt_mobile.text(),
            "IsAdmin": 0,
            "KiVanBan": 1
        }