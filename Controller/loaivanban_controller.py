from PyQt6.QtWidgets import QMessageBox
from View.loaivanban_dialog import LoaiVanBanDialog

class LoaiVanBanController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.them_signal.connect(self.handle_add)
        self.view.sua_signal.connect(self.handle_edit)
        self.view.xoa_signal.connect(self.handle_delete)
        self.view.lam_moi_signal.connect(self.refresh)
        self.view.timkiem_signal.connect(self.handle_search)
        self.refresh()

    def refresh(self):
        self.view.load_data(self.model.get_all())
        if hasattr(self.view, 'txt_search'):
            self.view.txt_search.clear()

    def handle_search(self, k):
        self.view.load_data(self.model.search(k) if k else self.model.get_all())

    def handle_add(self):
        dlg = LoaiVanBanDialog(title=f"Thêm {self.view.title_text}")
        if dlg.exec():
            self.model.add(dlg.get_data())
            self.refresh()

    def handle_edit(self, data):
        dlg = LoaiVanBanDialog(title=f"Sửa {self.view.title_text}", data=data)
        if dlg.exec():
            self.model.update(dlg.get_data())
            self.refresh()

    def handle_delete(self, id_val):
        if QMessageBox.question(None, "Xác nhận", "Bạn có chắc chắn muốn xóa mục này?") == QMessageBox.StandardButton.Yes:
            self.model.delete(id_val)
            self.refresh()