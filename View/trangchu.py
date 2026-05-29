from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, 
                             QAbstractItemView, QSizePolicy, QScrollArea, QDateEdit, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont, QColor

import numpy as np
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime

# ==========================================
# BIỂU ĐỒ ĐƯỜNG MODERN PREMIUM SAAS (STRAIGHT LINE)
# ==========================================
class LineChart(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(8, 5), dpi=130) 
        fig.patch.set_facecolor('#ffffff')
        fig.subplots_adjust(left=0.05, right=0.98, top=0.92, bottom=0.15)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        
        self.mpl_connect("motion_notify_event", self.on_hover)
        self.annot = None
        self.x_labels = []
        self.hover_labels = []
        self.x_num = []
        self.den_vals = []
        self.di_vals = []
        self.scatter_den = None
        self.scatter_di = None

    def update_chart(self, display_labels, hover_labels, den_values, di_values):
        self.axes.clear()
        if not display_labels:
            display_labels = [f"T{i}" for i in range(1, 13)]
            hover_labels = display_labels
            den_values = [0]*12
            di_values = [0]*12

        self.x_labels = display_labels
        self.hover_labels = hover_labels
        self.x_num = np.arange(len(display_labels))
        self.den_vals = np.array(den_values)
        self.di_vals = np.array(di_values)

        color_den = '#8A2BE2' # Tím
        color_di = '#00E5FF'  # Xanh Cyan
        
        # --- VẼ ĐƯỜNG THẲNG (STRAIGHT LINES) ---
        # 1. Tạo hiệu ứng Glow nhẹ (bóng đổ mờ dưới line)
        for n in range(1, 6):
            self.axes.plot(self.x_num, self.den_vals, color=color_den, linewidth=2 + (n*1.2), alpha=0.04, zorder=1)
            self.axes.plot(self.x_num, self.di_vals, color=color_di, linewidth=2 + (n*1.2), alpha=0.04, zorder=1)

        # 2. Vẽ đường thẳng chính (Sharp/Straight lines)
        self.axes.plot(self.x_num, self.den_vals, color=color_den, linewidth=3.5, label='Công văn đến', zorder=3)
        self.axes.plot(self.x_num, self.di_vals, color=color_di, linewidth=3.5, label='Công văn đi', zorder=3)
        
        # 3. Phủ mờ vùng dưới đường (Area Fill)
        self.axes.fill_between(self.x_num, self.den_vals, color=color_den, alpha=0.08, zorder=2)
        self.axes.fill_between(self.x_num, self.di_vals, color=color_di, alpha=0.08, zorder=2)

        # 4. Chấm điểm Dot Point rõ nét (Viền trắng)
        self.scatter_den = self.axes.scatter(self.x_num, self.den_vals, facecolors=color_den, edgecolors='white', s=90, linewidths=2.5, zorder=4)
        self.scatter_di = self.axes.scatter(self.x_num, self.di_vals, facecolors=color_di, edgecolors='white', s=90, linewidths=2.5, zorder=4)

        # 5. Cấu hình Trục và Grid (Minimal UI)
        self.axes.set_xticks(self.x_num)
        self.axes.set_xticklabels(self.x_labels, rotation=0, ha='center', fontweight='500')
        max_y = max(max(den_values, default=0), max(di_values, default=0))
        self.axes.set_ylim(0, max_y * 1.25 if max_y > 0 else 10)
        
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['left'].set_visible(False) 
        self.axes.spines['bottom'].set_visible(False)
        
        self.axes.grid(axis='y', linestyle='-', alpha=0.3, color='#E2E8F0', zorder=0)
        self.axes.tick_params(axis='x', colors='#A0AEC0', length=0, pad=15, labelsize=10)
        self.axes.tick_params(axis='y', colors='#A0AEC0', length=0, pad=5, labelsize=10)
        self.axes.margins(x=0.03, y=0)

        # 6. Chú thích (Legend)
        legend = self.axes.legend(loc='upper right', frameon=True, fontsize=10, labelcolor='#4A5568', edgecolor='#F8F9FA', facecolor='#F8F9FA')
        for line in legend.get_lines():
            line.set_linewidth(3.5)

        # 7. Khởi tạo Tooltip (Hộp thoại Hover)
        self.annot = self.axes.annotate(
            "", xy=(0,0), xytext=(0, 20), textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.6", fc="#1E1E2D", ec="none", alpha=0.9),
            fontsize=11, fontweight='bold', color="white", ha='center', zorder=10
        )
        self.annot.set_visible(False)
        self.vline = self.axes.axvline(x=0, color="#CBD5E0", linestyle="dashed", linewidth=1.5, alpha=0.8, zorder=2)
        self.vline.set_visible(False)
        self.draw()

    def on_hover(self, event):
        if not event.inaxes == self.axes:
            if self.annot and self.annot.get_visible():
                self.annot.set_visible(False)
                self.vline.set_visible(False)
                self.draw_idle()
            return

        min_dist_x = float('inf')
        closest_idx = None
        
        for idx, x in enumerate(self.x_num):
            dist_x = abs(x - event.xdata)
            if dist_x < 0.4 and dist_x < min_dist_x:
                min_dist_x = dist_x
                closest_idx = idx

        if closest_idx is not None:
            y_den = self.den_vals[closest_idx]
            y_di = self.di_vals[closest_idx]
            
            label_text = f"{self.hover_labels[closest_idx]}\n📥 Đến: {int(y_den)}   |   📤 Đi: {int(y_di)}"
            max_y = max(y_den, y_di)
            self.annot.xy = (self.x_num[closest_idx], max_y)
            self.annot.set_text(label_text)
            self.annot.set_visible(True)
            self.vline.set_xdata([self.x_num[closest_idx]])
            self.vline.set_visible(True)
            if self.scatter_den: self.scatter_den.set_sizes([180 if i == closest_idx else 90 for i in range(len(self.x_num))])
            if self.scatter_di: self.scatter_di.set_sizes([180 if i == closest_idx else 90 for i in range(len(self.x_num))])
            self.draw_idle()
        else:
            if self.annot and self.annot.get_visible():
                self.annot.set_visible(False)
                self.vline.set_visible(False)
                if self.scatter_den: self.scatter_den.set_sizes([90]*len(self.x_num))
                if self.scatter_di: self.scatter_di.set_sizes([90]*len(self.x_num))
                self.draw_idle()
                
    def __init__(self, parent=None):
        fig = Figure(figsize=(8, 5), dpi=130) 
        fig.patch.set_facecolor('#ffffff')
        fig.subplots_adjust(left=0.05, right=0.98, top=0.92, bottom=0.15)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        
        self.mpl_connect("motion_notify_event", self.on_hover)
        self.annot = None
        self.x_labels = []
        self.hover_labels = []
        self.x_num = []
        self.den_vals = []
        self.di_vals = []
        self.scatter_den = None
        self.scatter_di = None

    def update_chart(self, display_labels, hover_labels, den_values, di_values):
        self.axes.clear()
        if not display_labels:
            display_labels = [f"T{i}" for i in range(1, 13)]
            hover_labels = display_labels
            den_values = [0]*12
            di_values = [0]*12

        self.x_labels = display_labels
        self.hover_labels = hover_labels
        self.x_num = np.arange(len(display_labels))
        self.den_vals = np.array(den_values)
        self.di_vals = np.array(di_values)

        color_den = '#8A2BE2' 
        color_di = '#00E5FF'  
        
        if len(self.x_num) > 3:
            x_smooth = np.linspace(self.x_num.min(), self.x_num.max(), 300) 
            try:
                spl_den = make_interp_spline(self.x_num, self.den_vals, k=3)
                y_smooth_den = np.clip(spl_den(x_smooth), 0, None)
                spl_di = make_interp_spline(self.x_num, self.di_vals, k=3)
                y_smooth_di = np.clip(spl_di(x_smooth), 0, None)
            except:
                x_smooth, y_smooth_den, y_smooth_di = self.x_num, self.den_vals, self.di_vals
        else:
            x_smooth, y_smooth_den, y_smooth_di = self.x_num, self.den_vals, self.di_vals

        for n in range(1, 8):
            self.axes.plot(x_smooth, y_smooth_den, color=color_den, linewidth=2 + (n*1.2), alpha=0.04, zorder=1)
            self.axes.plot(x_smooth, y_smooth_di, color=color_di, linewidth=2 + (n*1.2), alpha=0.04, zorder=1)

        self.axes.plot(x_smooth, y_smooth_den, color=color_den, linewidth=3.5, label='Công văn đến', zorder=3)
        self.axes.plot(x_smooth, y_smooth_di, color=color_di, linewidth=3.5, label='Công văn đi', zorder=3)
        self.axes.fill_between(x_smooth, y_smooth_den, color=color_den, alpha=0.08, zorder=2)
        self.axes.fill_between(x_smooth, y_smooth_di, color=color_di, alpha=0.08, zorder=2)

        self.scatter_den = self.axes.scatter(self.x_num, self.den_vals, facecolors=color_den, edgecolors='white', s=90, linewidths=2.5, zorder=4)
        self.scatter_di = self.axes.scatter(self.x_num, self.di_vals, facecolors=color_di, edgecolors='white', s=90, linewidths=2.5, zorder=4)

        self.axes.set_xticks(self.x_num)
        self.axes.set_xticklabels(self.x_labels, rotation=0, ha='center', fontweight='500')
        max_y = max(max(den_values, default=0), max(di_values, default=0))
        self.axes.set_ylim(0, max_y * 1.25 if max_y > 0 else 10)
        
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['left'].set_visible(False) 
        self.axes.spines['bottom'].set_visible(False)
        
        self.axes.grid(axis='y', linestyle='-', alpha=0.3, color='#E2E8F0', zorder=0)
        self.axes.tick_params(axis='x', colors='#A0AEC0', length=0, pad=15, labelsize=10)
        self.axes.tick_params(axis='y', colors='#A0AEC0', length=0, pad=5, labelsize=10)
        self.axes.margins(x=0.03, y=0)

        legend = self.axes.legend(loc='upper right', frameon=True, fontsize=10, labelcolor='#4A5568', edgecolor='#F8F9FA', facecolor='#F8F9FA')
        for line in legend.get_lines():
            line.set_linewidth(3.5)

        self.annot = self.axes.annotate(
            "", xy=(0,0), xytext=(0, 20), textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.6", fc="#1E1E2D", ec="none", alpha=0.9),
            fontsize=11, fontweight='bold', color="white", ha='center', zorder=10
        )
        self.annot.set_visible(False)
        self.vline = self.axes.axvline(x=0, color="#CBD5E0", linestyle="dashed", linewidth=1.5, alpha=0.8, zorder=2)
        self.vline.set_visible(False)
        self.draw()

    def on_hover(self, event):
        if not event.inaxes == self.axes:
            if self.annot and self.annot.get_visible():
                self.annot.set_visible(False)
                self.vline.set_visible(False)
                self.draw_idle()
            return

        min_dist_x = float('inf')
        closest_idx = None
        
        for idx, x in enumerate(self.x_num):
            dist_x = abs(x - event.xdata)
            if dist_x < 0.4 and dist_x < min_dist_x:
                min_dist_x = dist_x
                closest_idx = idx

        if closest_idx is not None:
            y_den = self.den_vals[closest_idx]
            y_di = self.di_vals[closest_idx]
            
            label_text = f"{self.hover_labels[closest_idx]}\n📥 Đến: {int(y_den)}   |   📤 Đi: {int(y_di)}"
            max_y = max(y_den, y_di)
            self.annot.xy = (self.x_num[closest_idx], max_y)
            self.annot.set_text(label_text)
            self.annot.set_visible(True)
            self.vline.set_xdata([self.x_num[closest_idx]])
            self.vline.set_visible(True)
            if self.scatter_den: self.scatter_den.set_sizes([180 if i == closest_idx else 90 for i in range(len(self.x_num))])
            if self.scatter_di: self.scatter_di.set_sizes([180 if i == closest_idx else 90 for i in range(len(self.x_num))])
            self.draw_idle()
        else:
            if self.annot and self.annot.get_visible():
                self.annot.set_visible(False)
                self.vline.set_visible(False)
                if self.scatter_den: self.scatter_den.set_sizes([90]*len(self.x_num))
                if self.scatter_di: self.scatter_di.set_sizes([90]*len(self.x_num))
                self.draw_idle()

# ==========================================
# GIAO DIỆN CHUNG (UI COMPONENTS)
# ==========================================
def create_shadow(blur_radius=30, y_offset=8, alpha=10):
    from PyQt6.QtWidgets import QGraphicsDropShadowEffect
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur_radius)
    shadow.setColor(QColor(0, 0, 0, alpha))
    shadow.setOffset(0, y_offset)
    return shadow

CALENDAR_CSS = """
    QCalendarWidget QWidget {
        background-color: #FFFFFF;
        border-radius: 12px;
    }
    QCalendarWidget QWidget#qt_calendar_navigationbar {
        background-color: #FFFFFF;
        border-bottom: 1px solid #EDF2F7;
        padding: 6px;
        min-height: 42px;
    }
    QCalendarWidget QToolButton {
        color: #2D3748;
        font-weight: 700;
        font-size: 13px;
        border: none;
        border-radius: 6px;
        padding: 4px 8px;
    }
    QCalendarWidget QToolButton:hover {
        background-color: #F3F0FF;
        color: #8A2BE2;
    }
    QCalendarWidget QAbstractItemView:enabled {
        color: #2D3748;
        background-color: #FFFFFF;
        selection-background-color: #8A2BE2;
        selection-color: #FFFFFF;
        font-size: 12px;
        outline: none;
    }
    QCalendarWidget QAbstractItemView:disabled { color: #CBD5E0; }
"""

class ModernDatePicker(QDateEdit):
    def __init__(self, default_date):
        super().__init__()
        self.setDate(default_date)
        self.setCalendarPopup(True)
        self.setDisplayFormat("dd/MM/yyyy")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QDateEdit {
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 6px 30px 6px 12px;
                background-color: #FFFFFF;
                color: #2D3748;
                font-weight: 600;
                font-size: 13px;
                min-width: 115px;
            }
            QDateEdit:hover { border: 1px solid #8A2BE2; }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 28px;
                border: none;
                background: transparent;
            }
        """)
        cal = self.calendarWidget()
        cal.setGridVisible(False)
        cal.setStyleSheet(CALENDAR_CSS)

class ModernStatCard(QFrame):
    def __init__(self, title, color_hex, icon_char):
        super().__init__()
        self.setStyleSheet("QFrame { background-color: white; border-radius: 20px; border: none; }")
        self.setGraphicsEffect(create_shadow())
        self.setFixedHeight(120)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #718096; font-size: 14px; font-weight: 600; border: none;")
        
        bot_layout = QHBoxLayout()
        self.lbl_value = QLabel("0")
        self.lbl_value.setStyleSheet(f"color: {color_hex}; font-size: 38px; font-weight: bold; border: none;")
        
        lbl_icon = QLabel(icon_char)
        lbl_icon.setStyleSheet(f"color: {color_hex}; font-size: 28px; background-color: {color_hex}15; border-radius: 14px; padding: 12px; border: none;")
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_icon.setFixedSize(56, 56)
        
        bot_layout.addWidget(self.lbl_value)
        bot_layout.addStretch()
        bot_layout.addWidget(lbl_icon)
        
        layout.addWidget(lbl_title)
        layout.addLayout(bot_layout)

    def update_data(self, total_val):
        if hasattr(self, 'lbl_value') and self.lbl_value is not None:
            self.lbl_value.setText(str(total_val))

class ModernTable(QTableWidget):
    def __init__(self, headers):
        super().__init__(0, len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QTableWidget { background-color: white; border: none; color: #2D3748; font-size: 13px; }
            QHeaderView::section { background-color: #F8F9FA; color: #718096; font-weight: 600; padding: 15px; border: none; border-bottom: 1px solid #E2E8F0; text-align: left; }
            QTableWidget::item { padding: 15px; border-bottom: 1px solid #EDF2F7; }
            QTableWidget::item:hover { background-color: #F8F9FA; }
            QTableWidget::item:selected { background-color: #F3F0FF; color: #8A2BE2; border-radius: 8px;}
        """)

class TaskItemWidget(QFrame):
    clicked = pyqtSignal(dict)
    def __init__(self, task_data, is_new=False):
        super().__init__()
        self.task_data = task_data
        self.lbl_badge = None
        self.setStyleSheet("QFrame { background-color: #F8F9FA; border-radius: 12px; margin-bottom: 8px; } QFrame:hover { background-color: #EDF2F7; }")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        
        title_layout = QHBoxLayout()
        lbl_name = QLabel(str(task_data.get('NoiDung', 'Không có tiêu đề')))
        lbl_name.setWordWrap(True)
        lbl_name.setStyleSheet("font-weight: 600; color: #2D3748; font-size: 14px; border: none; background: transparent;")
        title_layout.addWidget(lbl_name)
        
        if is_new:
            self.lbl_badge = QLabel(" MỚI ")
            self.lbl_badge.setStyleSheet("background-color: #FF4757; color: white; border-radius: 4px; font-size: 10px; font-weight: bold; padding: 2px 6px; margin-left: 5px;")
            title_layout.addWidget(self.lbl_badge)
        title_layout.addStretch()

        ngay = task_data.get('NgayTao', '')
        ngay_str = ngay.strftime("%d/%m/%Y") if hasattr(ngay, 'strftime') else str(ngay)[:10]
        tt = task_data.get('TrangThai', 1)
        if tt == 1: status = "⚪ Mới giao"
        elif tt == 2: status = "🔵 Đang xử lý"
        elif tt == 3: status = "🟢 Đã hoàn thành"
        elif tt == 4: status = "🔴 Quá hạn"
        else: status = "⚪ Chưa rõ"

        lbl_det = QLabel(f"⏳ {ngay_str}   |   {status}")
        lbl_det.setStyleSheet("font-size: 12px; color: #A0AEC0; border: none; background: transparent; margin-top: 2px;")
        layout.addLayout(title_layout)
        layout.addWidget(lbl_det)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.lbl_badge: self.lbl_badge.hide()
            self.clicked.emit(self.task_data)

class TrangChuView(QWidget):
    yeu_cau_mo_cong_viec = pyqtSignal(int)
    yeu_cau_mo_cv_den = pyqtSignal(str) 
    yeu_cau_mo_cv_di = pyqtSignal(str)  

    def __init__(self):
        super().__init__()
        self.setFont(QFont("Segoe UI", 10))
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #F8FAFC; }") 
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F8FAFC;")
        dash_layout = QVBoxLayout(content_widget)
        dash_layout.setContentsMargins(40, 40, 40, 40)
        dash_layout.setSpacing(35)

        # 1. THỂ THỐNG KÊ (ĐÃ BỔ SUNG VĂN BẢN NỘI BỘ THÀNH 4 THẺ)
        row1 = QHBoxLayout()
        row1.setSpacing(20) # Giảm khoảng cách để 4 thẻ hiển thị đều đẹp
        self.card_den = ModernStatCard("CÔNG VĂN ĐẾN", "#8A2BE2", "📥")
        self.card_di = ModernStatCard("CÔNG VĂN ĐI", "#00E5FF", "📤")
        self.card_noibo = ModernStatCard("VĂN BẢN NỘI BỘ", "#F59E0B", "📁") 
        self.card_congviec = ModernStatCard("TỔNG CÔNG VIỆC", "#14B8A6", "📋")
        
        row1.addWidget(self.card_den)
        row1.addWidget(self.card_di)
        row1.addWidget(self.card_noibo)
        row1.addWidget(self.card_congviec)
        dash_layout.addLayout(row1)

        # 2. LINE CHART & TASKS PANEL
        row2 = QHBoxLayout()
        row2.setSpacing(30)
        
        chart_frame = QFrame()
        chart_frame.setStyleSheet("background-color: white; border-radius: 20px; border: none;")
        chart_frame.setGraphicsEffect(create_shadow())
        
        chart_layout = QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(30, 25, 30, 15) 
        chart_layout.setSpacing(15) 
        
        chart_header = QHBoxLayout()
        chart_header.setContentsMargins(0, 0, 0, 15) 
        
        lbl_chart = QLabel("Tổng quan biến động công văn")
        lbl_chart.setStyleSheet("font-size: 16px; font-weight: 800; color: #2D3748; border: none;")
        
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_layout.setSpacing(10)
        
        self.date_from = ModernDatePicker(QDate.currentDate().addMonths(-3))
        self.date_to = ModernDatePicker(QDate.currentDate())
        
        filter_layout.addWidget(QLabel("Từ:"))
        filter_layout.addWidget(self.date_from)
        filter_layout.addWidget(QLabel("Đến:"))
        filter_layout.addWidget(self.date_to)
        filter_layout.addStretch()
        
        chart_header.addWidget(lbl_chart)
        chart_header.addStretch()
        chart_header.addLayout(filter_layout)
        
        self.line_chart = LineChart()
        chart_layout.addLayout(chart_header)
        chart_layout.addWidget(self.line_chart)
        row2.addWidget(chart_frame, stretch=7) 
        
        noti_frame = QFrame()
        noti_frame.setStyleSheet("background-color: white; border-radius: 20px; border: none;")
        noti_frame.setGraphicsEffect(create_shadow())
        self.noti_layout = QVBoxLayout(noti_frame)
        self.noti_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.noti_layout.setContentsMargins(25, 25, 25, 25)
        
        lbl_noti = QLabel("Công việc mới")
        lbl_noti.setStyleSheet("font-size: 16px; font-weight: 700; color: #2D3748; border: none; padding-bottom: 15px;")
        self.noti_layout.addWidget(lbl_noti)
        
        row2.addWidget(noti_frame, stretch=3)
        dash_layout.addLayout(row2)

        # 3. TOP 5 TABLES
        row3 = QHBoxLayout()
        row3.setSpacing(30)
        
        tb_den_frame = QFrame()
        tb_den_frame.setStyleSheet("background-color: white; border-radius: 20px; border: none;")
        tb_den_frame.setGraphicsEffect(create_shadow())
        tb_den_layout = QVBoxLayout(tb_den_frame)
        tb_den_layout.setContentsMargins(25, 25, 25, 25)
        lbl_tb_den = QLabel("Công văn đến mới nhất")
        lbl_tb_den.setStyleSheet("font-size: 16px; font-weight: 700; color: #2D3748; border: none; padding-bottom: 15px;")
        self.tb_den = ModernTable(["Ký hiệu", "Ngày", "Trích yếu"])
        self.tb_den.itemDoubleClicked.connect(self._on_den_double_click)
        tb_den_layout.addWidget(lbl_tb_den)
        tb_den_layout.addWidget(self.tb_den)
        row3.addWidget(tb_den_frame)
        
        tb_di_frame = QFrame()
        tb_di_frame.setStyleSheet("background-color: white; border-radius: 20px; border: none;")
        tb_di_frame.setGraphicsEffect(create_shadow())
        tb_di_layout = QVBoxLayout(tb_di_frame)
        tb_di_layout.setContentsMargins(25, 25, 25, 25)
        lbl_tb_di = QLabel("Công văn đi mới nhất")
        lbl_tb_di.setStyleSheet("font-size: 16px; font-weight: 700; color: #2D3748; border: none; padding-bottom: 15px;")
        self.tb_di = ModernTable(["Ký hiệu", "Ngày", "Nơi nhận"])
        self.tb_di.itemDoubleClicked.connect(self._on_di_double_click)
        tb_di_layout.addWidget(lbl_tb_di)
        tb_di_layout.addWidget(self.tb_di)
        row3.addWidget(tb_di_frame)
        
        dash_layout.addLayout(row3)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

    def _on_task_clicked(self, task_data):
        self.yeu_cau_mo_cong_viec.emit(task_data.get('Id', 0))
    def _on_den_double_click(self, item):
        self.yeu_cau_mo_cv_den.emit(self.tb_den.item(item.row(), 0).text())
    def _on_di_double_click(self, item):
        self.yeu_cau_mo_cv_di.emit(self.tb_di.item(item.row(), 0).text())

    def update_task_panel(self, tasks):
        for i in reversed(range(1, self.noti_layout.count())): 
            widget = self.noti_layout.itemAt(i).widget()
            if widget: widget.setParent(None)
        if not tasks:
            lbl_empty = QLabel("Chưa có công việc nào.")
            lbl_empty.setStyleSheet("color: #A0AEC0; font-style: italic; font-size: 13px;")
            self.noti_layout.addWidget(lbl_empty)
            return
        
        for t in tasks[:5]: 
            is_new = (t.get('TrangThai', 1) == 1)
            t_widget = TaskItemWidget(t, is_new)
            t_widget.clicked.connect(self._on_task_clicked)
            self.noti_layout.addWidget(t_widget)

    def update_table_den(self, data_list):
        self.tb_den.setRowCount(len(data_list))
        for i, row in enumerate(data_list):
            self.tb_den.setItem(i, 0, QTableWidgetItem(str(row.get('so_ky_hieu', row.get('KyHieu', '')))))
            ngay = row.get('ngay_den', row.get('NgayDen', ''))
            ngay_str = ngay.strftime("%d/%m/%Y") if hasattr(ngay, 'strftime') else str(ngay)[:10]
            self.tb_den.setItem(i, 1, QTableWidgetItem(ngay_str))
            self.tb_den.setItem(i, 2, QTableWidgetItem(str(row.get('trich_yeu', row.get('TrichYeu', '')))))

    def update_table_di(self, data_list):
        self.tb_di.setRowCount(len(data_list))
        for i, row in enumerate(data_list):
            self.tb_di.setItem(i, 0, QTableWidgetItem(str(row.get('KyHieu', ''))))
            ngay = row.get('NgayKy', '')
            ngay_str = ngay.strftime("%d/%m/%Y") if hasattr(ngay, 'strftime') else str(ngay)[:10]
            self.tb_di.setItem(i, 1, QTableWidgetItem(ngay_str))
            self.tb_di.setItem(i, 2, QTableWidgetItem(str(row.get('NoiNhan', ''))))