from Model.hoso_model import HoSoModel

class HoSoController:

    def __init__(self):

        self.model = HoSoModel()

    def get_muc_luc(self):

        return self.model.get_muc_luc()

    def insert_muc_luc(self, ma, ten, ngay):

        self.model.insert_muc_luc(
            ma,
            ten,
            ngay
        )

    def get_danh_muc(self):

        return self.model.get_danh_muc()