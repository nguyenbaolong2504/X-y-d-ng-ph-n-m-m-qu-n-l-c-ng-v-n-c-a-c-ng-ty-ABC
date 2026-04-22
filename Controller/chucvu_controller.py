from PyQt6.QtWidgets import QMessageBox
from View.chucvu_dialog import ChucVuDialog

class ChucVuController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.view.them_signal.connect(self.handle_add)
        self.view.sua_signal.connect(self.handle_edit)
        self.view.xoa_signal.connect(self.handle_delete)
        
        self.refresh_table()

    def refresh_table(self):
        data = self.model.get_all()
        self.view.load_data(data)

    def handle_add(self):
        dialog = ChucVuDialog()
        if dialog.exec():
            self.model.add(dialog.get_data())
            self.refresh_table()

    def handle_edit(self, data):
        dialog = ChucVuDialog(data=data)
        if dialog.exec():
            self.model.update(dialog.get_data())
            self.refresh_table()

    def handle_delete(self, id_cv):
        confirm = QMessageBox.question(None, "Xác nhận", "Bạn có chắc muốn xóa chức vụ này?")
        if confirm == QMessageBox.StandardButton.Yes:
            self.model.delete(id_cv)
            self.refresh_table()