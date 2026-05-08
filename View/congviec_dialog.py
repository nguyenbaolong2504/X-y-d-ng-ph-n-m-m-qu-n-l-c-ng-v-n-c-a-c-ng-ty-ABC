from PyQt6.QtWidgets import *

class CongViecDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Thông tin Công việc")

        self.resize(500,300)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.txt_ten = QLineEdit()

        self.txt_nguoi = QLineEdit()

        self.txt_yeucau = QTextEdit()

        form.addRow("Tên workflow (*):", self.txt_ten)
        form.addRow("Người theo dõi:", self.txt_nguoi)
        form.addRow("Yêu cầu xử lý:", self.txt_yeucau)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)