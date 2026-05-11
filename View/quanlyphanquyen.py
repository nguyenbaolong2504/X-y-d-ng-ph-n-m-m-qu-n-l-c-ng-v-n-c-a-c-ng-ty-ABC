from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt


class QuanLyPhanQuyen(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setStyleSheet("""
            QWidget{
                background:#f5f6fa;
                font-family:Segoe UI;
            }

            QLabel{
                color:#2d3436;
            }

            QFrame{
                background:white;
                border-radius:15px;
                border:1px solid #dfe6e9;
            }

            QListWidget{
                background:white;
                border:none;
                font-size:15px;
                padding:10px;
            }

            QListWidget::item{
                padding:12px;
            }

            QListWidget::item:selected{
                background:#6c5ce7;
                color:white;
                border-radius:8px;
            }
        """)

        main_layout = QHBoxLayout(self)

        # =====================================================
        # MENU LEFT
        # =====================================================

        left_frame = QFrame()

        left_frame.setFixedWidth(300)

        left_layout = QVBoxLayout(left_frame)

        title_menu = QLabel("QUẢN TRỊ HỆ THỐNG")

        title_menu.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            color:#6c5ce7;
            padding:15px;
        """)

        left_layout.addWidget(title_menu)

        self.menu = QListWidget()

        self.menu.addItems([
            "👤 Quản lý người dùng",
            "🏢 Quản lý phòng ban",
            "🔐 Quản lý quyền hạn",
            "📁 Quản lý template",
            "⚙️ Cấu hình workflow",
            "📋 Audit log"
        ])

        left_layout.addWidget(self.menu)

        # =====================================================
        # CONTENT RIGHT
        # =====================================================

        right_frame = QFrame()

        right_layout = QVBoxLayout(right_frame)

        title = QLabel(
            "9. Quản trị Hệ thống (Admin)"
        )

        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            padding:10px;
        """)

        right_layout.addWidget(title)

        # =====================================================
        # CHỨC NĂNG
        # =====================================================

        chucnang_title = QLabel(
            "Chức năng chính:"
        )

        chucnang_title.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            padding-top:10px;
        """)

        right_layout.addWidget(chucnang_title)

        features = [
            "• Quản lý người dùng, phòng ban",
            "• Quản lý quyền hạn",
            "• Quản lý template, danh mục",
            "• Cấu hình workflow",
            "• Audit log"
        ]

        for feature in features:

            label = QLabel(feature)

            label.setStyleSheet("""
                font-size:18px;
                padding:8px;
            """)

            right_layout.addWidget(label)

        # =====================================================
        # ACTOR
        # =====================================================

        actor_title = QLabel("Actor & Quyền:")

        actor_title.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            padding-top:20px;
        """)

        right_layout.addWidget(actor_title)

        actors = [
            ("Admin","Toàn quyền"),
            ("Giám đốc","Xem và phê duyệt"),
            ("Văn thư","Quản lý công văn"),
            ("Nhân viên","Xem dữ liệu được cấp")
        ]

        for role,desc in actors:

            card = QFrame()

            card.setStyleSheet("""
                background:#ffffff;
                border:1px solid #dfe6e9;
                border-radius:12px;
            """)

            card_layout = QHBoxLayout(card)

            role_label = QLabel(role)

            role_label.setStyleSheet("""
                font-size:18px;
                font-weight:bold;
                color:#6c5ce7;
            """)

            desc_label = QLabel(desc)

            desc_label.setStyleSheet("""
                font-size:16px;
                color:#636e72;
            """)

            card_layout.addWidget(role_label)

            card_layout.addStretch()

            card_layout.addWidget(desc_label)

            right_layout.addWidget(card)

        right_layout.addStretch()

        # =====================================================
        # ADD
        # =====================================================

        main_layout.addWidget(left_frame)

        main_layout.addWidget(right_frame)