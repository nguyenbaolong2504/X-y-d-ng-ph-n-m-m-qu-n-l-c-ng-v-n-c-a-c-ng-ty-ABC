class UserSession:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance.user_id = None
            cls._instance.username = None
            cls._instance.hoten = None
            cls._instance.don_vi_id = None
            cls._instance.is_admin = False
            cls._instance.role = None
            cls._instance.ten_don_vi = None

            # menu được phép xem
            cls._instance.menus = []

        return cls._instance

    # ==========================================
    # SET USER
    # ==========================================

    def set_user(
        self,
        user_id,
        username,
        hoten,
        don_vi_id,
        is_admin,
        role,
        ten_don_vi=""
    ):

        self.user_id = user_id
        self.username = username
        self.hoten = hoten
        self.don_vi_id = don_vi_id
        self.is_admin = is_admin
        self.role = role
        self.ten_don_vi = ten_don_vi

    # ==========================================
    # MENU
    # ==========================================

    def set_menus(self, menus):

        self.menus = menus

    def get_menus(self):

        return self.menus

    # ==========================================
    # GETTER
    # ==========================================

    def get_hoten(self):

        return self.hoten

    def get_don_vi_id(self):

        return self.don_vi_id

    def get_role(self):

        return self.role

    def get_ten_don_vi(self):

        return self.ten_don_vi

    # ==========================================
    # ADMIN
    # ==========================================

    def is_admin_user(self):

        return self.is_admin

    # ==========================================
    # LOGOUT
    # ==========================================

    def clear(self):

        self.user_id = None
        self.username = None
        self.hoten = None
        self.don_vi_id = None
        self.is_admin = False
        self.role = None
        self.ten_don_vi = None
        self.menus = []