from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QComboBox, QDialogButtonBox

class LuuHoSoDialog(QDialog):
    def __init__(self, ds_hoso, ds_hanbaoquan, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lưu công văn vào hồ sơ")
        self.setFixedWidth(450)
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.cbo_hoso = QComboBox()
        for hs in ds_hoso:
            self.cbo_hoso.addItem(hs['TieuDeHoSo'], hs['Id'])
        form.addRow("Tên hồ sơ:", self.cbo_hoso)

        self.cbo_hanbaoquan = QComboBox()
        self.cbo_hanbaoquan.addItem("-- Không chọn --", None)
        for hbq in ds_hanbaoquan:
            self.cbo_hanbaoquan.addItem(hbq['TenHanBaoQuan'], hbq['Id'])
        form.addRow("Thời hạn bảo quản:", self.cbo_hanbaoquan)

        layout.addLayout(form)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        return {
            'hoso_id': self.cbo_hoso.currentData(),
            'hanbaoquan_id': self.cbo_hanbaoquan.currentData()
        }