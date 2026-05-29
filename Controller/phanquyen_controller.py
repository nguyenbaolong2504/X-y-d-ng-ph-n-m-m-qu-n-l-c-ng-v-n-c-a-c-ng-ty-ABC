from Model.phanquyen_model import PhanQuyenModel

class PhanQuyenController:

    def __init__(self):

        self.model = PhanQuyenModel()

    # =============================
    # USER
    # =============================

    def get_all(self):

        return self.model.get_all()

    def insert(self, username, password, role):

        self.model.insert(
            username,
            password,
            role
        )

    # =============================
    # MENU PERMISSION
    # =============================

    def get_permissions(self, username):

        return self.model.get_permissions(
            username
        )

    def save_permissions(
        self,
        username,
        menus
    ):

        self.model.save_permissions(
            username,
            menus
        )