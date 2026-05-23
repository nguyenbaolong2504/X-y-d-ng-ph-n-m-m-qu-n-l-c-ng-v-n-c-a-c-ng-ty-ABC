
from Model.congvan_model import CongVanModel
from Model.congvandi_model import CongVanDiModel


class TrangChuController:

    def __init__(self, view, user_session):

        self.view = view

        self.user_session = user_session

        self.model_den = CongVanModel()

        self.model_di = CongVanDiModel()

        # ==========================================
        # SIGNAL
        # ==========================================

        self.view.yeu_cau_thong_ke.connect(
            self.load_data
        )

        # ==========================================
        # LOAD
        # ==========================================

        self.load_data()

    # =====================================================
    # LOAD DATA
    # =====================================================

    def load_data(self):

        try:

            # ======================================
            # GET DATA
            # ======================================

            ds_den = self.model_den.get_all()

            ds_di = self.model_di.get_all()

            # ======================================
            # THONG KE
            # ======================================

            so_luong_den = len(ds_den)

            so_luong_di = len(ds_di)

            so_luong_hoso = 12

            # ======================================
            # NHIEM VU MAU
            # ======================================

            ds_nhiem_vu = [

                {
                    'tieu_de':
                        'Xử lý công văn đến 577/UBND-VX',

                    'han_hoan_thanh':
                        '2026-04-20',

                    'trang_thai':
                        'Đang xử lý',

                    'lien_quan':
                        'Công văn đến'
                },

                {
                    'tieu_de':
                        'Soạn công văn trình ký',

                    'han_hoan_thanh':
                        '2026-04-22',

                    'trang_thai':
                        'Chưa xử lý',

                    'lien_quan':
                        'Công văn đi'
                },

                {
                    'tieu_de':
                        'Kiểm tra hồ sơ lưu trữ',

                    'han_hoan_thanh':
                        '2026-04-18',

                    'trang_thai':
                        'Hoàn thành',

                    'lien_quan':
                        'Hồ sơ'
                }

            ]

            so_luong_nhiem_vu = len(
                ds_nhiem_vu
            )

            # ======================================
            # UPDATE CARD
            # ======================================

            self.view.update_thong_ke(

                so_luong_den,

                so_luong_di,

                so_luong_hoso,

                so_luong_nhiem_vu

            )

            # ======================================
            # CONG VAN DEN MOI
            # ======================================

            ds_den_moi = ds_den[:5]

            self.view.update_danh_sach_den([

                {

                    'so_ky_hieu':
                        str(
                            item.get(
                                'KyHieu',
                                ''
                            )
                        ),

                    'ngay_den':
                        str(
                            item.get(
                                'NgayDen',
                                ''
                            )
                        ),

                    'trich_yeu':
                        str(
                            item.get(
                                'TrichYeu',
                                ''
                            )
                        )

                }

                for item in ds_den_moi

            ])

            # ======================================
            # CONG VAN DI MOI
            # ======================================

            ds_di_moi = ds_di[:5]

            self.view.update_danh_sach_di([

                {

                    'so_ky_hieu':
                        str(
                            item.get(
                                'KyHieu',
                                ''
                            )
                        ),

                    'ngay_van_ban':
                        str(
                            item.get(
                                'NgayKy',
                                ''
                            )
                        ),

                    'noi_nhan':
                        str(
                            item.get(
                                'NoiNhan',
                                ''
                            )
                        )

                }

                for item in ds_di_moi

            ])

            # ======================================
            # NHIEM VU
            # ======================================

            self.view.update_nhiem_vu(
                ds_nhiem_vu
            )

        except Exception as e:

            print(
                "Lỗi trang chủ:",
                e
            )