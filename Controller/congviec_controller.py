from Model.congviec_model import CongViecModel

class CongViecController:

    def __init__(self):

        self.model = CongViecModel()

    def get_all(self):

        return self.model.get_all()

    def insert(self, ten, nguoi, han, trangthai):

        self.model.insert(
            ten,
            nguoi,
            han,
            trangthai
        )