class UserSession:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.user_id = None
            cls._instance.username = None
            cls._instance.hoten = None          # Thêm dòng này
            cls._instance.don_vi_id = None
            cls._instance.is_admin = False
            cls._instance.role = None
            cls._instance.ten_don_vi = None
        return cls._instance

    def set_user(self, user_id, username, hoten, don_vi_id, is_admin, role, ten_don_vi=""):
        self.user_id = user_id
        self.username = username
        self.hoten = hoten
        self.don_vi_id = don_vi_id
        self.is_admin = is_admin    
        self.role = role
        self.ten_don_vi = ten_don_vi

    def get_hoten(self):
        return self.hoten

    def get_don_vi_id(self):
        return self.don_vi_id

    def is_admin_user(self):
        return self.is_admin or self.role == 'GiamDoc'

    def get_role(self):
        return self.role

    def get_ten_don_vi(self):
        return self.ten_don_vi