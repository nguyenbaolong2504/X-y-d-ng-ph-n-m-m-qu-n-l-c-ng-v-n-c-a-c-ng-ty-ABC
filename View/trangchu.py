from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QIcon, QAction

class TrangChuView(QWidget):
    yeu_cau_thong_ke = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Đặt font chung cho toàn bộ View
        self.setFont(QFont("Segoe UI", 10))
        self.setup_ui()

    def setup_ui(self):
        # Bố cục chính theo chiều dọc (Main Layout)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Khu vực nội dung chính (Xám nhạt) ---
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #f1f2f6;") # Màu nền xám nhạt
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 15, 20, 20)
        content_layout.setSpacing(15)

        # =========================================================================
        # 1. Hàng Card Thống Kê (Statistics Row)
        # =========================================================================
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        # Khởi tạo các Card với màu sắc và icon
        self.card_den = self._create_colorful_card("📥", "CÔNG VĂN ĐẾN CT ABC (2026)", "5", "#ff6b6b")
        self.card_di = self._create_colorful_card("📤", "CÔNG VĂN ĐI CT ABC (2026)", "5", "#a55eea")
        self.card_ho_so = self._create_colorful_card("📁", "DANH MỤC HỒ SƠ ABC", "0", "#f0932b")
        self.card_nhiem_vu = self._create_colorful_card("📊", "NHIỆM VỤ - THÔNG BÁO", "3", "#00cec9")

        cards_layout.addWidget(self.card_den)
        cards_layout.addWidget(self.card_di)
        cards_layout.addWidget(self.card_ho_so)
        cards_layout.addWidget(self.card_nhiem_vu)
        content_layout.addLayout(cards_layout)

        # =========================================================================
        # 2. Khu vực chia tách (Split Area)
        # =========================================================================
        split_layout = QHBoxLayout()
        split_layout.setSpacing(15)

        # --- Khu vực TRÁI: Hai khung danh sách Công văn ---
        list_v_layout = QVBoxLayout()
        list_v_layout.setSpacing(15)

        # Khung Công văn Đến
        self.frame_den = self._create_list_frame("📋 Công văn đến mới nhất CT ABC", "Cập nhật: 08/04/2026")
        self.table_den = self.frame_den.findChild(QTableWidget)
        list_v_layout.addWidget(self.frame_den)

        # Khung Công văn Đi
        self.frame_di = self._create_list_frame("📤 Công văn đi mới nhất CT ABC", "Cập nhật: 19/04/2026")
        self.table_di = self.frame_di.findChild(QTableWidget)
        list_v_layout.addWidget(self.frame_di)

        split_layout.addLayout(list_v_layout, stretch=3)

        # --- Khu vực PHẢI: Các ô thông tin nhiệm vụ/sự kiện ---
        right_info_layout = QVBoxLayout()
        right_info_layout.setSpacing(10)
        right_info_layout.setContentsMargins(0, 0, 0, 0)
        
        # Ô Sự kiện
        self.box_events = self._create_info_box("Sự kiện diễn ra (0 sự kiện)", "#27ae60")
        lbl_event_content = QLabel("Hôm nay không có sự kiện nào được lịch hẹn.")
        lbl_event_content.setStyleSheet("color: #7f8c8d; padding: 5px; border: none;")
        self.box_events.layout().addWidget(lbl_event_content)
        right_info_layout.addWidget(self.box_events)

        # Ô Sinh nhật
        self.box_birthdays = self._create_info_box("Thông báo sinh nhật (0 cán bộ)", "#2ecc71")
        lbl_bday_content = QLabel("Hôm nay không có ai sinh nhật.")
        lbl_bday_content.setStyleSheet("color: #7f8c8d; padding: 5px; border: none;")
        self.box_birthdays.layout().addWidget(lbl_bday_content)
        right_info_layout.addWidget(self.box_birthdays)

        # Ô Nhiệm vụ mới
        self.box_new_tasks = self._create_info_box("Nhiệm vụ mới (0 công việc)", "#e67e22")
        right_info_layout.addWidget(self.box_new_tasks)

        right_info_layout.addStretch()
        split_layout.addLayout(right_info_layout, stretch=1)

        content_layout.addLayout(split_layout, stretch=1)

        # =========================================================================
        # 3. Bảng Nhiệm vụ cần xử lý dưới cùng
        # =========================================================================
        task_header = QFrame()
        task_header.setFixedHeight(30)
        task_header.setStyleSheet("background-color: #0c2461; border-top-left-radius: 8px; border-top-right-radius: 8px;")
        h_layout_task = QHBoxLayout(task_header)
        h_layout_task.setContentsMargins(10, 0, 10, 0)
        lbl_task_title = QLabel("✅ Danh sách nhiệm vụ trong năm 2026 cần xử lý")
        lbl_task_title.setStyleSheet("color: white; font-weight: bold; border: none;")
        btn_more_task = QPushButton("Xem thêm »")
        btn_more_task.setStyleSheet("color: #a4b0be; background: none; border: none; font-size: 11px;")
        h_layout_task.addWidget(lbl_task_title)
        h_layout_task.addStretch()
        h_layout_task.addWidget(btn_more_task)
        
        content_layout.addWidget(task_header)

        self.table_task = QTableWidget()
        self.table_task.setColumnCount(4)
        self.table_task.setHorizontalHeaderLabels(["Công việc", "Hạn xử lý", "Trạng thái", "Liên quan"])
        self.table_task.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #dcdde1;
                border-top: none;
                gridline-color: white;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            QTableWidget::item { padding: 5px; border-bottom: 1px solid #f1f2f6; }
            QHeaderView::section { background-color: #f8f9fa; font-weight: bold; border: 1px solid #f1f2f6; }
        """)
        self.table_task.horizontalHeader().setStretchLastSection(True)
        self.table_task.verticalHeader().setVisible(False)
        self.table_task.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_task.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        content_layout.addWidget(self.table_task)

        # Nút làm mới dữ liệu
        footer_layout = QHBoxLayout()
        btn_refresh = QPushButton("🔄 Cập nhật thống kê hệ thống ABC")
        btn_refresh.setFixedSize(220, 35)
        btn_refresh.setStyleSheet("""
            background-color: #1e3799; 
            color: white; 
            border-radius: 5px; 
            font-weight: bold; 
            font-size: 13px;
        """)
        btn_refresh.clicked.connect(self.yeu_cau_thong_ke.emit)
        footer_layout.addWidget(btn_refresh, alignment=Qt.AlignmentFlag.AlignRight)
        content_layout.addLayout(footer_layout)

        main_layout.addWidget(content_widget)

    # --- Helper: Tạo Card màu sắc thống kê ---
    def _create_colorful_card(self, icon_char, title, value, color):
        card = QFrame()
        card.setFixedHeight(120)
        card.setStyleSheet(f"""
            background-color: {color};
            border-radius: 12px;
            color: white;
        """)
        grid_layout = QGridLayout(card)
        grid_layout.setContentsMargins(15, 10, 15, 10)
        grid_layout.setSpacing(0)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 13px; font-weight: normal; color: rgba(255,255,255,0.8); border: none;")
        
        lbl_value = QLabel(value)
        lbl_value.setStyleSheet("font-size: 40px; font-weight: bold; border: none;")
        lbl_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_icon = QLabel(icon_char)
        lbl_icon.setStyleSheet("font-size: 50px; color: rgba(255,255,255,0.4); border: none;")
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        grid_layout.addWidget(lbl_title, 0, 0, 1, 1)
        grid_layout.addWidget(lbl_value, 1, 0, 1, 1)
        grid_layout.addWidget(lbl_icon, 0, 1, 2, 1)

        card.value_label = lbl_value
        return card

    # --- Helper: Tạo Khung danh sách công văn ---
    def _create_list_frame(self, title, update_time_str):
        frame = QFrame()
        frame.setStyleSheet("background-color: white; border: 1px solid #dcdde1; border-radius: 8px;")
        v_layout = QVBoxLayout(frame)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)

        header_widget = QWidget()
        header_widget.setFixedHeight(35)
        header_widget.setStyleSheet("background-color: #1e90ff; border-top-left-radius: 8px; border-top-right-radius: 8px; border: none;")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 0, 10, 0)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: white; font-weight: bold; font-size: 13px; border: none;")
        lbl_update = QLabel(update_time_str)
        lbl_update.setStyleSheet("color: rgba(255,255,255,0.7); font-size: 11px; border: none;")
        
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        header_layout.addWidget(lbl_update)
        v_layout.addWidget(header_widget)

        table = QTableWidget()
        table.setColumnCount(3)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setStyleSheet("QTableWidget { border: none; background-color: white; gridline-color: white; }")
        table.horizontalHeader().setStretchLastSection(True)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        v_layout.addWidget(table, stretch=1)

        footer_widget = QWidget()
        footer_widget.setFixedHeight(25)
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(10, 0, 10, 0)
        btn_more = QPushButton("Xem thêm »")
        btn_more.setStyleSheet("color: #1e90ff; background: none; border: none; font-size: 11px; text-align: left;")
        footer_layout.addWidget(btn_more)
        v_layout.addWidget(footer_widget)

        return frame

    # --- Helper: Tạo ô thông tin nhỏ bên phải ---
    def _create_info_box(self, title, color):
        box = QFrame()
        box.setStyleSheet("background-color: white; border: 1px solid #dcdde1; border-radius: 8px;")
        v_layout = QVBoxLayout(box)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)

        header = QLabel(f"  🟢 {title}")
        header.setFixedHeight(30)
        header.setStyleSheet(f"background-color: {color}; color: white; font-weight: bold; border-top-left-radius: 8px; border-top-right-radius: 8px; border: none;")
        v_layout.addWidget(header)
        return box

    # --- Cập nhật dữ liệu cho Card ---
    def update_thong_ke(self, den, di, ho_so, nhiem_vu):
        self.card_den.value_label.setText(str(den))
        self.card_di.value_label.setText(str(di))
        self.card_ho_so.value_label.setText(str(ho_so))
        self.card_nhiem_vu.value_label.setText(str(nhiem_vu))

    # --- Cập nhật danh sách CV Đến ---
    def update_danh_sach_den(self, danh_sach):
        self.table_den.setRowCount(len(danh_sach))
        for i, item in enumerate(danh_sach):
            self.table_den.setItem(i, 0, QTableWidgetItem(f"SỐ KÝ HIỆU: {item.get('so_ky_hieu', '')}"))
            ngay_den = item.get('ngay_den', '')
            ngay_den_str = ngay_den.strftime("%d/%m/%Y") if hasattr(ngay_den, 'strftime') else str(ngay_den)
            self.table_den.setItem(i, 1, QTableWidgetItem(ngay_den_str))
            trich_yeu = str(item.get('trich_yeu', ''))
            if len(trich_yeu) > 50: trich_yeu = trich_yeu[:50] + '...'
            item_trich_yeu = QTableWidgetItem(trich_yeu)
            item_trich_yeu.setForeground(Qt.GlobalColor.blue)
            self.table_den.setItem(i, 2, item_trich_yeu)
        self.table_den.resizeColumnsToContents()

    # --- Cập nhật danh sách CV Đi ---
    def update_danh_sach_di(self, danh_sach):
        self.table_di.setRowCount(len(danh_sach))
        for i, item in enumerate(danh_sach):
            self.table_di.setItem(i, 0, QTableWidgetItem(f"SỐ KÝ HIỆU: {item.get('so_ky_hieu', '')}"))
            ngay_vb = item.get('ngay_van_ban', '')
            ngay_vb_str = ngay_vb.strftime("%d/%m/%Y") if hasattr(ngay_vb, 'strftime') else str(ngay_vb)
            self.table_di.setItem(i, 1, QTableWidgetItem(ngay_vb_str))
            noi_nhan = str(item.get('noi_nhan', ''))
            if len(noi_nhan) > 40: noi_nhan = noi_nhan[:40] + '...'
            item_noi_nhan = QTableWidgetItem(noi_nhan)
            item_noi_nhan.setForeground(Qt.GlobalColor.darkBlue)
            self.table_di.setItem(i, 2, item_noi_nhan)
        self.table_di.resizeColumnsToContents()

    # --- Cập nhật danh sách Nhiệm vụ ---
    def update_nhiem_vu(self, danh_sach):
        self.table_task.setRowCount(len(danh_sach))
        for i, nv in enumerate(danh_sach):
            self.table_task.setItem(i, 0, QTableWidgetItem(str(nv.get('tieu_de', ''))))
            han = nv.get('han_hoan_thanh', '')
            han_str = han.strftime("%d/%m/%Y") if hasattr(han, 'strftime') else str(han)
            self.table_task.setItem(i, 1, QTableWidgetItem(han_str))
            trang_thai = str(nv.get('trang_thai', ''))
            item_status = QTableWidgetItem(trang_thai)
            if "Đang xử lý" in trang_thai: item_status.setForeground(Qt.GlobalColor.darkYellow)
            elif "Chưa xử lý" in trang_thai: item_status.setForeground(Qt.GlobalColor.darkRed)
            elif "Đã hoàn thành" in trang_thai: item_status.setForeground(Qt.GlobalColor.darkGreen)
            self.table_task.setItem(i, 2, item_status)
            self.table_task.setItem(i, 3, QTableWidgetItem(str(nv.get('lien_quan', ''))))
        self.table_task.resizeColumnsToContents()