from PyQt6.QtWidgets import QMessageBox
from View.loaicongvan_dialog import LoaiCongVanDialog

class LoaiCongVanController:
    def __init__(self, model, view_den, view_di):
        self.model = model
        self.view_den = view_den
        self.view_di = view_di

        self.view_den.them_signal.connect(lambda: self.handle_add(1))
        self.view_den.sua_signal.connect(self.handle_edit)
        self.view_den.xoa_signal.connect(self.handle_delete)
        self.view_den.lam_moi_signal.connect(self.refresh)
        self.view_den.timkiem_signal.connect(lambda k: self.handle_search(1, k))

        self.view_di.them_signal.connect(lambda: self.handle_add(2))
        self.view_di.sua_signal.connect(self.handle_edit)
        self.view_di.xoa_signal.connect(self.handle_delete)
        self.view_di.lam_moi_signal.connect(self.refresh)
        self.view_di.timkiem_signal.connect(lambda k: self.handle_search(2, k))

        self.refresh()

    def refresh(self):
        all_data = self.model.get_all()
        
        data_den = [d for d in all_data if d['TrangThai'] in (1, 3)]
        self.view_den.load_data(data_den)
        if hasattr(self.view_den, 'txt_search'):
            self.view_den.txt_search.clear()

        data_di = [d for d in all_data if d['TrangThai'] in (2, 3)]
        self.view_di.load_data(data_di)
        if hasattr(self.view_di, 'txt_search'):
            self.view_di.txt_search.clear()

    def handle_search(self, loai, k):
        search_data = self.model.search(k) if k else self.model.get_all()
        if loai == 1:
            data_den = [d for d in search_data if d['TrangThai'] in (1, 3)]
            self.view_den.load_data(data_den)
        else:
            data_di = [d for d in search_data if d['TrangThai'] in (2, 3)]
            self.view_di.load_data(data_di)

    def handle_add(self, default_trangthai):
        dlg = LoaiCongVanDialog(title="Thêm Loại công văn", default_trangthai=default_trangthai)
        if dlg.exec():
            self.model.add(dlg.get_data())
            self.refresh()

    def handle_edit(self, data):
        dlg = LoaiCongVanDialog(title="Sửa Loại công văn", data=data)
        if dlg.exec():
            self.model.update(dlg.get_data())
            self.refresh()

    def handle_delete(self, id_val):
        if QMessageBox.question(None, "Xác nhận", "Bạn có chắc chắn muốn xóa mục này?") == QMessageBox.StandardButton.Yes:
            self.model.delete(id_val)
            self.refresh()