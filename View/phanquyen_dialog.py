from PyQt6.QtWidgets import *

class PhanQuyenDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Thông tin Phân quyền")

        self.resize(500,250)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.txt_ten = QLineEdit()

        self.txt_chucnang = QTextEdit()

        form.addRow("Tên quyền (*):", self.txt_ten)
        form.addRow("Chức năng:", self.txt_chucnang)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)