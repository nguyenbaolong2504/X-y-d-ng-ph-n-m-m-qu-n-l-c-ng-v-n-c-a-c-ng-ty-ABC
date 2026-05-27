import os
import shutil
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pyodbc

from Model.congviec_model import CongViecModel, CongVanDenModel, CongVanDiModel

class ChiTietCongViecDialog(QDialog):
    def __init__(self, cv_id, user_info, conn_str, parent=None):
        super().__init__(parent)
        self.cv_id = cv_id
        self.user_info = user_info
        self.conn_str = conn_str
        self.cv_model = CongViecModel(conn_str)
        self.setWindowTitle("Chi tiết công việc")
        self.setMinimumSize(800, 600)
        self.resize(800, 700)

        # Main layout với scroll area để tránh bố cục bị tụt
        main_layout = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        layout = QVBoxLayout(container)
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        # Ô hiển thị phản hồi mới
        self.phanhoi_label = QLabel()
        self.phanhoi_label.setWordWrap(True)
        self.phanhoi_label.setStyleSheet("background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; padding: 8px; border-radius: 5px;")
        self.phanhoi_label.hide()
        layout.addWidget(self.phanhoi_label)

        self.btn_xem_congvan = QPushButton("📄 Xem công văn gốc")
        self.btn_xem_congvan.clicked.connect(self.xem_cong_van_goc)
        layout.addWidget(self.btn_xem_congvan)

        # File báo cáo
        self.file_frame = QGroupBox("File báo cáo kết quả")
        file_layout = QHBoxLayout()
        self.lbl_file = QLabel("Chưa có file")
        self.btn_download = QPushButton("⬇️ Tải file báo cáo")
        self.btn_download.clicked.connect(self.download_file)
        self.btn_view = QPushButton("👁️ Xem file")
        self.btn_view.clicked.connect(self.view_file)
        file_layout.addWidget(self.lbl_file)
        file_layout.addWidget(self.btn_download)
        file_layout.addWidget(self.btn_view)
        self.file_frame.setLayout(file_layout)
        layout.addWidget(self.file_frame)

        self.lich_su_label = QLabel("📜 Lịch sử xử lý:")
        self.lich_su_text = QTextEdit()
        self.lich_su_text.setReadOnly(True)
        layout.addWidget(self.lich_su_label)
        layout.addWidget(self.lich_su_text)

        # Các nút hành động
        self.btn_frame = QHBoxLayout()
        self.btn_upload = QPushButton("📎 Tải file báo cáo lên")
        self.btn_chuyen = QPushButton("➡️ Chuyển tiếp")
        self.btn_trinh = QPushButton("⬆️ Trình duyệt")
        self.btn_duyet = QPushButton("✅ Duyệt")
        self.btn_phanhoi = QPushButton("✍️ Gửi phản hồi")
        self.btn_frame.addStretch()
        for btn in [self.btn_upload, self.btn_chuyen, self.btn_trinh, self.btn_duyet, self.btn_phanhoi]:
            self.btn_frame.addWidget(btn)
        layout.addLayout(self.btn_frame)

        self.load_data()

        self.btn_upload.clicked.connect(self.upload_file)
        self.btn_chuyen.clicked.connect(self.chuyen_tiep)
        self.btn_trinh.clicked.connect(self.trinh_duyet)
        self.btn_duyet.clicked.connect(self.duyet)
        self.btn_phanhoi.clicked.connect(self.phan_hoi)

    def get_ten_nguoi(self, uid):
        if not uid:
            return "?"
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT HoTen FROM CanBo WHERE Id = ?", uid)
            row = cursor.fetchone()
            return row[0] if row else "?"
        except Exception:
            return "?"
        finally:
            conn.close()

    def _map_trang_thai(self, code):
        mapping = {1: "Chờ xử lý", 2: "Đang xử lý", 3: "Chờ duyệt", 4: "Hoàn thành", 5: "Cần sửa"}
        return mapping.get(code, "Không xác định")

    def _lay_phan_hoi_moi_nhat(self):
        ls = self.cv_model.get_lich_su(self.cv_id)
        for hanh_dong, chi_tiet, thoi_gian, nguoi in reversed(ls):
            if hanh_dong == "Phản hồi":
                return f"[{thoi_gian}] {nguoi}: {chi_tiet}"
        return ""

    def load_data(self):
        cv = self.cv_model.get_chi_tiet(self.cv_id)
        if not cv:
            return
        self.cv_data = cv
        # cv: 0 Id,1 CongVanDenId,2 DonViDuocGiaoId,3 NguoiDuocGiaoId,4 HanXuLy,5 NoiDung,
        #     6 NguoiGiaoId,7 TrangThai,8 KetQua,9 FileKetQua,10 YKienDuyet,11 NgayNop,12 NgayTao
        info = f"""
        <b>Công việc:</b> {cv[5] or ''}<br>
        <b>Người giao:</b> {self.get_ten_nguoi(cv[6])}<br>
        <b>Người nhận:</b> {self.get_ten_nguoi(cv[3])}<br>
        <b>Trạng thái:</b> {self._map_trang_thai(cv[7])}<br>
        <b>Hạn xử lý:</b> {cv[4]}<br>
        <b>Ngày tạo:</b> {cv[12]}<br>
        <b>Ngày nộp báo cáo:</b> {cv[11] if cv[11] else 'Chưa nộp'}<br>
        <b>Nội dung xử lý:</b> {cv[8] or ''}<br>
        <b>Ý kiến duyệt/phản hồi:</b> {cv[10] or ''}
        """
        self.info_label.setText(info)

        phanhoi_text = self._lay_phan_hoi_moi_nhat()
        if phanhoi_text:
            self.phanhoi_label.setText(f"💬 Phản hồi mới:\n{phanhoi_text}")
            self.phanhoi_label.show()
        else:
            self.phanhoi_label.hide()

        file_path = self.cv_model.get_file_chung(self.cv_id)
        if file_path and os.path.exists(file_path):
            self.lbl_file.setText(os.path.basename(file_path))
            self.btn_download.setEnabled(True)
            self.btn_view.setEnabled(True)
        else:
            self.lbl_file.setText("Chưa có file báo cáo")
            self.btn_download.setEnabled(False)
            self.btn_view.setEnabled(False)
            if file_path:
                self.lbl_file.setToolTip(f"Đường dẫn lưu: {file_path} (file không tồn tại)")
            else:
                self.lbl_file.setToolTip("")

        ls = self.cv_model.get_lich_su(self.cv_id)
        self.lich_su_text.clear()
        for hanh_dong, chi_tiet, thoi_gian, nguoi in ls:
            self.lich_su_text.append(f"[{thoi_gian}] {nguoi}: {hanh_dong} - {chi_tiet}")

        for btn in [self.btn_upload, self.btn_chuyen, self.btn_trinh, self.btn_duyet, self.btn_phanhoi]:
            btn.hide()

        trang_thai = cv[7]
        vai_tro = self.user_info['vai_tro']
        nguoi_nhan_id = cv[3]
        nguoi_giao_id = cv[6]
        user_id = self.user_info['id']

        # Người nhận và trạng thái 1 hoặc 2
        if nguoi_nhan_id == user_id and trang_thai in (1, 2):
            self.btn_upload.show()
            if file_path and os.path.exists(file_path):
                if vai_tro == 'Nhân viên':
                    self.btn_chuyen.show()
                elif vai_tro == 'Trưởng phòng':
                    self.btn_chuyen.show()
                    self.btn_trinh.show()
                elif vai_tro == 'Giám đốc':
                    self.btn_chuyen.show()
        # Người giao và trạng thái 3 (Chờ duyệt) – chỉ duyệt
        if vai_tro in ('Trưởng phòng', 'Giám đốc') and nguoi_giao_id == user_id and trang_thai == 3:
            self.btn_duyet.show()
        # Nút phản hồi hiện cho tất cả những người liên quan khi công việc chưa hoàn thành
        if trang_thai in (1, 2, 3) and (nguoi_nhan_id == user_id or nguoi_giao_id == user_id):
            self.btn_phanhoi.show()

    def xem_cong_van_goc(self):
        if not self.cv_data:
            return
        cv_den_id = self.cv_data[1]
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT FilePath FROM CongVanDen WHERE Id = ?", cv_den_id)
            row = cursor.fetchone()
            if row and row[0] and os.path.exists(row[0]):
                os.startfile(row[0])
                conn.close()
                return
        except Exception:
            pass
        try:
            cursor.execute("SELECT FileDinhKem FROM CongVanDen WHERE Id = ?", cv_den_id)
            row = cursor.fetchone()
            if row and row[0] and os.path.exists(row[0]):
                os.startfile(row[0])
                conn.close()
                return
        except Exception:
            pass
        conn.close()
        QMessageBox.warning(self, "Không có file", "Công văn gốc không có file đính kèm hoặc file không tồn tại.")

    def download_file(self):
        file_path = self.cv_model.get_file_chung(self.cv_id)
        if file_path and os.path.exists(file_path):
            save_path, _ = QFileDialog.getSaveFileName(self, "Lưu file báo cáo", os.path.basename(file_path))
            if save_path:
                shutil.copy2(file_path, save_path)
                QMessageBox.information(self, "Thành công", "Đã lưu file báo cáo")
        else:
            QMessageBox.warning(self, "Lỗi", "Không có file báo cáo để tải hoặc file không tồn tại.")

    def view_file(self):
        file_path = self.cv_model.get_file_chung(self.cv_id)
        if file_path and os.path.exists(file_path):
            os.startfile(file_path)
        else:
            QMessageBox.warning(self, "Lỗi", "Không thể mở file. File không tồn tại hoặc đường dẫn sai.")

    def upload_file(self):
        source, _ = QFileDialog.getOpenFileName(self, "Chọn file báo cáo kết quả", "", "All Files (*.*)")
        if source:
            base_dir = os.path.abspath("ket_qua_cong_viec")
            os.makedirs(base_dir, exist_ok=True)
            file_name = os.path.basename(source)
            safe_name = f"cv_{self.cv_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file_name}"
            safe_name = safe_name.replace(" ", "_")
            import unicodedata
            safe_name = unicodedata.normalize('NFKD', safe_name).encode('ASCII', 'ignore').decode('ASCII')
            dest = os.path.join(base_dir, safe_name)
            try:
                shutil.copy2(source, dest)
                if os.path.exists(dest):
                    self.cv_model.cap_nhat_file_ket_qua(self.cv_id, dest)
                    self.cv_model.cap_nhat_ngay_nop(self.cv_id)
                    self.cv_model.them_lich_su(self.cv_id, self.user_info['id'], "Đã tải file báo cáo", f"File: {safe_name}")
                    QMessageBox.information(self, "Thành công", f"Đã lưu file báo cáo tại:\n{dest}")
                    self.load_data()
                else:
                    QMessageBox.warning(self, "Lỗi", "Không thể lưu file. Kiểm tra quyền thư mục.")
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Lỗi khi lưu file: {str(e)}")

    def chuyen_tiep(self):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cb.Id, cb.HoTen
            FROM CanBo cb
            JOIN ChucVu cv ON cb.ChucVuId = cv.Id
            WHERE cv.TenChucVu IN ('Trưởng phòng', 'Giám đốc')
        """)
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            QMessageBox.warning(self, "Lỗi", "Không có ai để chuyển tiếp")
            return
        dlg = QDialog(self)
        dlg.setWindowTitle("Chuyển tiếp công việc")
        dlg.resize(400, 300)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Chuyển tới:"))
        cbo = QComboBox()
        for uid, ten in rows:
            cbo.addItem(ten, uid)
        layout.addWidget(cbo)
        layout.addWidget(QLabel("Ý kiến chuyển tiếp:"))
        txt_y = QTextEdit()
        txt_y.setPlaceholderText("Nhập ý kiến của bạn...")
        layout.addWidget(txt_y)
        btn = QPushButton("Gửi")
        btn.clicked.connect(dlg.accept)
        layout.addWidget(btn)
        dlg.setLayout(layout)
        if dlg.exec():
            nguoi_nhan_moi = cbo.currentData()
            y_kien = txt_y.toPlainText()
            self.cv_model.cap_nhat_nguoi_nhan(self.cv_id, nguoi_nhan_moi, 1)
            self.cv_model.them_lich_su(self.cv_id, self.user_info['id'], "Chuyển tiếp", f"Chuyển tới {cbo.currentText()}: {y_kien}")
            QMessageBox.information(self, "OK", "Đã chuyển tiếp")
            self.accept()

    def trinh_duyet(self):
        conn = pyodbc.connect(self.conn_str)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cb.Id FROM CanBo cb
            JOIN ChucVu cv ON cb.ChucVuId = cv.Id
            WHERE cv.TenChucVu = 'Giám đốc'
        """)
        gd = cursor.fetchone()
        conn.close()
        if not gd:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy Giám đốc")
            return
        y_kien, ok = QInputDialog.getMultiLineText(self, "Trình duyệt", "Ý kiến trình lên Giám đốc:")
        if not ok:
            return
        self.cv_model.cap_nhat_nguoi_nhan(self.cv_id, gd[0], 3)
        self.cv_model.them_lich_su(self.cv_id, self.user_info['id'], "Trình duyệt", y_kien)
        QMessageBox.information(self, "OK", "Đã trình lên Giám đốc")
        self.accept()

    def duyet(self):
        file_path = self.cv_model.get_file_chung(self.cv_id)
        if not file_path or not os.path.exists(file_path):
            QMessageBox.warning(self, "Thiếu file", "Chưa có file báo cáo hoặc file không tồn tại, yêu cầu người xử lý tải lên trước")
            return
        so_ky_hieu, ok1 = QInputDialog.getText(self, "Công văn đi", "Số ký hiệu:")
        if not ok1 or not so_ky_hieu.strip():
            return
        noi_nhan, ok2 = QInputDialog.getText(self, "Công văn đi", "Nơi nhận:")
        if not ok2 or not noi_nhan.strip():
            return
        y_kien_duyet, ok3 = QInputDialog.getMultiLineText(self, "Ý kiến duyệt", "Nhập ý kiến duyệt (nếu có):")
        trich_yeu = self.cv_data[5]
        os.makedirs("congvan_di", exist_ok=True)
        dest_path = os.path.join("congvan_di", os.path.basename(file_path))
        shutil.copy2(file_path, dest_path)

        # Lấy CongVanDenId thực tế (VanBanDenGocId) - đảm bảo là int
        cv_den_id = self.cv_data[1]
        try:
            cv_den_id = int(cv_den_id)
        except (ValueError, TypeError):
            # Nếu không ép được (ví dụ bị lưu chuỗi 'Nguyễn Văn IT'), truy vấn lại ID từ bảng CongVanDen
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            cursor.execute("SELECT Id FROM CongVanDen WHERE TrichYeu = ?", (trich_yeu,))
            row = cursor.fetchone()
            conn.close()
            if row:
                cv_den_id = row[0]
            else:
                QMessageBox.warning(self, "Lỗi", "Không xác định được công văn gốc để tạo công văn đi!")
                return

        # Gọi model công văn đi với VanBanDenGocId
        cv_di_model = CongVanDiModel(self.conn_str)
        cv_di_model.tao(cv_den_id, so_ky_hieu, noi_nhan, trich_yeu, dest_path)
        self.cv_model.cap_nhat_trang_thai(self.cv_id, 4, y_kien_duyet=f"Đã duyệt - {y_kien_duyet}" if y_kien_duyet else "Đã duyệt")
        self.cv_model.them_lich_su(self.cv_id, self.user_info['id'], "Duyệt", f"Đã tạo công văn đi {so_ky_hieu}. Ý kiến: {y_kien_duyet}")
        QMessageBox.information(self, "Thành công", "Đã duyệt và tạo công văn đi")
        self.accept()

    def phan_hoi(self):
        y_kien, ok = QInputDialog.getMultiLineText(self, "Phản hồi công việc", "Nhập nội dung phản hồi / ý kiến:")
        if not ok or not y_kien.strip():
            return
        self.cv_model.them_lich_su(self.cv_id, self.user_info['id'], "Phản hồi", y_kien)
        QMessageBox.information(self, "Đã phản hồi", f"Đã gửi phản hồi: {y_kien}")
        self.load_data()


class PhanCongDialog(QDialog):
    def __init__(self, cong_van_den_id, conn_str, parent=None):
        super().__init__(parent)
        self.cong_van_den_id = cong_van_den_id
        self.conn_str = conn_str
        self.setWindowTitle("Phân công công việc từ công văn đến")
        self.resize(500, 450)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📄 Công văn đến ID: " + str(cong_van_den_id)))
        layout.addWidget(QLabel("Nội dung công việc / yêu cầu chi tiết:"))
        self.txt_noi_dung = QTextEdit()
        self.txt_noi_dung.setPlaceholderText("Mô tả nhiệm vụ cần thực hiện...")
        layout.addWidget(self.txt_noi_dung)
        layout.addWidget(QLabel("Người xử lý:"))
        self.cbo_nguoi_nhan = QComboBox()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cb.Id, cb.HoTen
            FROM CanBo cb
            JOIN ChucVu cv ON cb.ChucVuId = cv.Id
            WHERE cv.TenChucVu = 'Nhân viên'
        """)
        for uid, ten in cursor.fetchall():
            self.cbo_nguoi_nhan.addItem(ten, int(uid))
        conn.close()
        layout.addWidget(self.cbo_nguoi_nhan)
        layout.addWidget(QLabel("Hạn xử lý:"))
        self.date_han = QDateEdit()
        self.date_han.setCalendarPopup(True)
        self.date_han.setDate(QDate.currentDate().addDays(7))
        layout.addWidget(self.date_han)
        btn_ok = QPushButton("Phân công")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)
        self.setLayout(layout)

    def get_data(self):
        return {
            "noi_dung": self.txt_noi_dung.toPlainText(),
            "nguoi_nhan_id": self.cbo_nguoi_nhan.currentData(),
            "han": self.date_han.date().toString("yyyy-MM-dd")
        }


class QuanLyCongViec(QWidget):
    def __init__(self, user_session, conn_str):
        super().__init__()
        self.user_id = user_session.user_id
        self.user_ten = user_session.get_hoten()
        self.vai_tro = getattr(user_session, 'role', 'Nhân viên')
        self.user_info = {
            'id': self.user_id,
            'ten': self.user_ten,
            'vai_tro': self.vai_tro
        }
        self.conn_str = conn_str
        self.cv_model = CongViecModel(conn_str)
        self.setup_ui()
        self.load_cong_viec()
        self.kiem_tra_phan_hoi_moi()

    def kiem_tra_phan_hoi_moi(self):
        phan_hoi_list = self.cv_model.get_phan_hoi_moi_cho_nguoi(self.user_id)
        if phan_hoi_list:
            msg = "📢 Bạn có phản hồi mới:\n\n"
            for row in phan_hoi_list:
                cv_id, ten_cv, hanh_dong, chi_tiet, thoi_gian, nguoi_phanhoi = row
                msg += f"• Công việc: {ten_cv}\n  Phản hồi từ {nguoi_phanhoi}: {chi_tiet}\n  (lúc {thoi_gian})\n\n"
            QMessageBox.information(self, "Thông báo phản hồi", msg)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        title = QLabel("✅ QUẢN LÝ CÔNG VIỆC")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #00b894;")
        layout.addWidget(title)
        self.toolbar = QHBoxLayout()
        self.btn_phan_cong = QPushButton("📋 Phân công từ công văn đến")
        self.btn_phan_cong.clicked.connect(self.phan_cong_tu_congvan)
        self.btn_refresh = QPushButton("🔄 Làm mới")
        self.btn_refresh.clicked.connect(self.load_cong_viec)
        self.toolbar.addWidget(self.btn_phan_cong)
        self.toolbar.addStretch()
        self.toolbar.addWidget(self.btn_refresh)
        if self.vai_tro != 'Giám đốc':
            self.btn_phan_cong.hide()
        layout.addLayout(self.toolbar)
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Nội dung công việc", "Người giao", "Người nhận", "Trạng thái", "Hạn xử lý", "Ngày tạo"])
        self.table.setColumnHidden(0, True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.xem_chi_tiet)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

    def load_cong_viec(self):
        rows = self.cv_model.get_cong_viec_cua_toi(self.user_id, self.vai_tro)
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            for j, val in enumerate(row[1:7], start=1):
                self.table.setItem(i, j, QTableWidgetItem(str(val) if val else ""))
        self.table.resizeColumnsToContents()

    def xem_chi_tiet(self):
        row = self.table.currentRow()
        if row < 0:
            return
        cv_id = int(self.table.item(row, 0).text())
        dlg = ChiTietCongViecDialog(cv_id, self.user_info, self.conn_str, self)
        if dlg.exec():
            self.load_cong_viec()

    def phan_cong_tu_congvan(self):
        model_cvden = CongVanDenModel(self.conn_str)
        ds_cvden = model_cvden.get_all()
        if not ds_cvden:
            QMessageBox.warning(self, "Không có công văn", "Chưa có công văn đến để phân công")
            return
        items = [f"{row[1]} - {row[3]}" for row in ds_cvden]
        selected, ok = QInputDialog.getItem(self, "Chọn công văn", "Công văn đến:", items, 0, False)
        if not ok:
            return
        idx = items.index(selected)
        cvden_id = ds_cvden[idx][0]
        dlg = PhanCongDialog(cvden_id, self.conn_str, self)
        if dlg.exec():
            data = dlg.get_data()
            if not data['noi_dung']:
                QMessageBox.warning(self, "Lỗi", "Nội dung công việc không được để trống")
                return
            new_id = self.cv_model.them(cvden_id, data['noi_dung'], self.user_id, data['nguoi_nhan_id'], data['han'])
            self.cv_model.them_lich_su(new_id, self.user_id, "Phân công", f"Giao cho {data['nguoi_nhan_id']}")
            QMessageBox.information(self, "Thành công", "Đã phân công công việc")
            self.load_cong_viec()