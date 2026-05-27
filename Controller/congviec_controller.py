from Model.congviec_model import CongViecModel

class CongViecController:
    def __init__(self, conn_str):
        self.model = CongViecModel(conn_str)

    def get_all(self, user_id, vai_tro):
        return self.model.get_cong_viec_cua_toi(user_id, vai_tro)

    def insert(self, id_cv_den, noi_dung, nguoi_giao, nguoi_nhan, han):
        return self.model.them(id_cv_den, noi_dung, nguoi_giao, nguoi_nhan, han)