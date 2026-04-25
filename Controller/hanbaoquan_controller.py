from PyQt6.QtWidgets import QMessageBox
from View.hanbaoquan_dialog import HanBaoQuanDialog

class HanBaoQuanController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.view.them_signal.connect(self.handle_add)
        self.view.sua_signal.connect(self.handle_edit)
        self.view.xoa_signal.connect(self.handle_delete)
        
        # --- KẾT NỐI SỰ KIỆN MỚI ---
        self.view.lam_moi_signal.connect(self.refresh_table)
        self.view.timkiem_signal.connect(self.handle_search)
        
        self.refresh_table()

    def refresh_table(self):
        data = self.model.get_all()
        self.view.load_data(data)
        if hasattr(self.view, 'txt_search'):
            self.view.txt_search.clear()

    def handle_search(self, keyword):
        if not keyword or keyword.strip() == "":
            self.refresh_table()
        else:
            data = self.model.search(keyword.strip())
            self.view.load_data(data)

    def handle_add(self):
        dialog = HanBaoQuanDialog()
        if dialog.exec():
            self.model.add(dialog.get_data())
            self.refresh_table()

    def handle_edit(self, data):
        dialog = HanBaoQuanDialog(data=data)
        if dialog.exec():
            self.model.update(dialog.get_data())
            self.refresh_table()

    def handle_delete(self, id_hbq):
        confirm = QMessageBox.question(None, "Xác nhận", "Bạn có chắc muốn xóa thời hạn bảo quản này?")
        if confirm == QMessageBox.StandardButton.Yes:
            self.model.delete(id_hbq)
            self.refresh_table()