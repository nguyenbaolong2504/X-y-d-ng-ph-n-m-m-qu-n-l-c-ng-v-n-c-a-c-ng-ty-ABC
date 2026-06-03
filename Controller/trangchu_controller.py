from Model.congvan_model import CongVanModel
from Model.congvandi_model import CongVanDiModel
from Model.model_noibo import ModelNoiBo
from Model.congviec_model import CongViecModel
from datetime import datetime, timedelta
import calendar

FALLBACK_CONN_STR = r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=congtyadc;Trusted_Connection=yes;"

class TrangChuController:
    def __init__(self, view, user_session):
        self.view = view
        self.user_session = user_session
        
        self.model_den = CongVanModel()
        self.model_di = CongVanDiModel()
        conn_str = getattr(self.model_den, 'conn_str', FALLBACK_CONN_STR)
        self.model_noibo = ModelNoiBo()
        self.model_congviec = CongViecModel(conn_str)

        if hasattr(self.view, 'date_from') and hasattr(self.view, 'date_to'):
            self.view.date_from.dateChanged.connect(self.load_chart_data)
            self.view.date_to.dateChanged.connect(self.load_chart_data)
        
        self.view.yeu_cau_mo_cong_viec.connect(self.mark_task_as_read)
        self.load_data()

    def load_data(self):
        from PyQt6.QtWidgets import QApplication
        QApplication.processEvents()
        
        self.load_data_den()
        self.load_data_di()
        self.load_data_noibo()
        self.load_data_congviec()
        self.load_tables_and_panel()
        self.load_chart_data()

    def mark_task_as_read(self, task_id):
        try:
            conn = self.model_congviec._get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE PhanCongXuLy SET TrangThai = 2 WHERE Id = ? AND TrangThai = 1", (task_id,))
            conn.commit()
            conn.close()
            self.load_tables_and_panel()
        except: pass

    def _check_date(self, date_val, d=None, m=None, y=None):
        if not date_val: return False
        try:
            if hasattr(date_val, 'year'):
                val_y, val_m, val_d = date_val.year, date_val.month, date_val.day
            else:
                d_str = str(date_val)[:10].strip()
                if '/' in d_str:
                    parts = d_str.split('/')
                    if len(parts[0]) == 4: val_y, val_m, val_d = int(parts[0]), int(parts[1]), int(parts[2])
                    else: val_y, val_m, val_d = int(parts[2]), int(parts[1]), int(parts[0])
                elif '-' in d_str:
                    parts = d_str.split('-')
                    val_y, val_m, val_d = int(parts[0]), int(parts[1]), int(parts[2])
                else: return False
            
            if y is not None and val_y != y: return False
            if m is not None and val_m != m: return False
            if d is not None and val_d != d: return False
            return True
        except: return False

    def load_data_den(self):
        try:
            ds = self.model_den.get_all(
                is_admin=self.user_session.is_admin_user(),
                role=self.user_session.get_role(),
                ten_don_vi=self.user_session.get_ten_don_vi()
            )
            self.view.card_den.update_data(len(ds))
        except Exception as e:
            print("Lỗi đếm công văn đến:", e)

    def load_data_di(self):
        try:
            user_id = self.user_session.user_id
            role = self.user_session.get_role()
            if user_id == 1 or role == 'Giám đốc' or role == 'Admin':
                is_admin = True
            else:
                is_admin = self.user_session.is_admin_user()
            ds = self.model_di.get_all(
                is_admin=is_admin,
                role=role,
                ten_don_vi=self.user_session.get_ten_don_vi(),
                nguoi_tao_id=user_id
            )
            self.view.card_di.update_data(len(ds))
        except Exception as e:
            print("Lỗi đếm công văn đi:", e)

    def load_data_noibo(self):
        try:
            ds_noibo = self.model_noibo.get_all(
                user_id=self.user_session.user_id,
                is_admin=self.user_session.is_admin_user()
            )
            self.view.card_noibo.update_data(len(ds_noibo))
        except Exception as e:
            print("Lỗi tải Văn bản nội bộ:", e)

    def load_data_congviec(self):
        try:
            raw_cv = self.model_congviec.get_cong_viec_cua_toi(self.user_session.user_id, self.user_session.get_role())
            self.view.card_congviec.update_data(len(raw_cv))
        except Exception as e:
            print("Lỗi đếm công việc:", e)

    def load_tables_and_panel(self):
        ds_den = self.model_den.get_all(
            is_admin=self.user_session.is_admin_user(),
            role=self.user_session.get_role(),
            ten_don_vi=self.user_session.get_ten_don_vi()
        )
        user_id = self.user_session.user_id
        role = self.user_session.get_role()
        if user_id == 1 or role == 'Giám đốc' or role == 'Admin':
            is_admin = True
        else:
            is_admin = self.user_session.is_admin_user()
        ds_di = self.model_di.get_all(
            is_admin=is_admin,
            role=role,
            ten_don_vi=self.user_session.get_ten_don_vi(),
            nguoi_tao_id=user_id
        )
        try:
            self.view.update_table_den(sorted(ds_den, key=lambda x: str(x.get('NgayDen', x.get('ngay_den', ''))), reverse=True)[:5])
        except: pass
        try:
            self.view.update_table_di(sorted(ds_di, key=lambda x: str(x.get('NgayKy', '')) if x.get('NgayKy') else '', reverse=True)[:5])
        except: pass
        try:
            raw_cv = self.model_congviec.get_cong_viec_cua_toi(self.user_session.user_id, self.user_session.get_role())
            ds_cv = [r if isinstance(r, dict) else {'Id': getattr(r, 'Id', 0), 'NoiDung': getattr(r, 'NoiDung', ''), 'NgayTao': getattr(r, 'NgayTao', ''), 'TrangThai': getattr(r, 'TrangThai', 0)} for r in raw_cv]
            self.view.update_task_panel(ds_cv)
        except: pass

    def load_chart_data(self, *args):
        try:
            user_id = self.user_session.user_id
            role = self.user_session.get_role()
            if user_id == 1 or role == 'Giám đốc' or role == 'Admin':
                is_admin = True
            else:
                is_admin = self.user_session.is_admin_user()
            ds_den = self.model_den.get_all(
                is_admin=self.user_session.is_admin_user(),
                role=role,
                ten_don_vi=self.user_session.get_ten_don_vi()
            )
            ds_di = self.model_di.get_all(
                is_admin=is_admin,
                role=role,
                ten_don_vi=self.user_session.get_ten_don_vi(),
                nguoi_tao_id=user_id
            )
            
            q_from = self.view.date_from.date()
            q_to = self.view.date_to.date()
            
            d_from = datetime(q_from.year(), q_from.month(), q_from.day())
            d_to = datetime(q_to.year(), q_to.month(), q_to.day())
            
            if d_from > d_to: d_from, d_to = d_to, d_from
                
            delta_days = (d_to - d_from).days
            display_labels, hover_labels, counts_den, counts_di = [], [], [], []
            
            if delta_days <= 31:
                for i in range(delta_days + 1):
                    curr = d_from + timedelta(days=i)
                    hover_labels.append(curr.strftime("%d/%m/%Y"))
                    display_labels.append(curr.strftime("%d/%m") if delta_days <= 10 or i == 0 or i == delta_days or i % 5 == 0 else "")
                    
                    counts_den.append(sum(1 for item in ds_den if self._check_date(item.get('NgayDen', item.get('ngay_den')), d=curr.day, m=curr.month, y=curr.year)))
                    counts_di.append(sum(1 for item in ds_di if self._check_date(item.get('NgayKy'), d=curr.day, m=curr.month, y=curr.year)))
            else:
                curr_y, curr_m = d_from.year, d_from.month
                while (curr_y < d_to.year) or (curr_y == d_to.year and curr_m <= d_to.month):
                    hover_labels.append(f"Tháng {curr_m}/{curr_y}")
                    display_labels.append(f"T{curr_m}/{str(curr_y)[2:]}")
                    
                    counts_den.append(sum(1 for item in ds_den if self._check_date(item.get('NgayDen', item.get('ngay_den')), m=curr_m, y=curr_y)))
                    counts_di.append(sum(1 for item in ds_di if self._check_date(item.get('NgayKy'), m=curr_m, y=curr_y)))
                    
                    curr_m += 1
                    if curr_m > 12: curr_m = 1; curr_y += 1
                        
            self.view.line_chart.update_chart(display_labels, hover_labels, counts_den, counts_di)
        except Exception as e:
            print("Lỗi tải Line Chart:", e)