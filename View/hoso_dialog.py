from PyQt6.QtWidgets import *

class HoSoDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Thông tin Hồ sơ")

        self.resize(500,250)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.txt_ten = QLineEdit()

        self.txt_ghichu = QTextEdit()

        form.addRow("Tên hồ sơ (*):", self.txt_ten)
        form.addRow("Ghi chú:", self.txt_ghichu)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
