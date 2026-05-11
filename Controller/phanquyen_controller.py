from Model.phanquyen_model import PhanQuyenModel

class PhanQuyenController:

    def __init__(self):

        self.model = PhanQuyenModel()

    def get_all(self):

        return self.model.get_all()

    def insert(self, username, password, role):

        self.model.insert(
            username,
            password,
            role
        )