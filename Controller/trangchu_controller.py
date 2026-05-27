<<<<<<< HEAD
from Model.congvan_model import CongVanModel
from Model.congvandi_model import CongVanDiModel

class TrangChuController:
    def __init__(self, view, user_session):
        self.view = view
        self.user_session = user_session
=======

from Model.congvan_model import CongVanModel
from Model.congvandi_model import CongVanDiModel


class TrangChuController:

    def __init__(self, view, user_session):

        self.view = view

        self.user_session = user_session

>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
        self.model_den = CongVanModel()

        self.model_di = CongVanDiModel()

<<<<<<< HEAD
        # Kết nối nút "Cập nhật thống kê"
        self.view.yeu_cau_thong_ke.connect(self.load_data)
        self.load_data()

    def load_data(self):
        # Lấy dữ liệu có lọc theo quyền của người dùng
        ds_den = self.model_den.get_all(
            is_admin=self.user_session.is_admin_user(),
            role=self.user_session.get_role(),
            ten_don_vi=self.user_session.get_ten_don_vi()
        )
        ds_di = self.model_di.get_all(
            is_admin=self.user_session.is_admin_user(),
            role=self.user_session.get_role(),
            ten_don_vi=self.user_session.get_ten_don_vi()
        )

        # Số lượng thực tế
        so_luong_den = len(ds_den)
        so_luong_di = len(ds_di)
        so_luong_hoso = 0   # Bạn có thể thay bằng model hồ sơ sau
        ds_nhiem_vu = []    # Bạn có thể thay bằng model nhiệm vụ sau

        # Dữ liệu nhiệm vụ mẫu (tạm thời)
        if not ds_nhiem_vu:
            ds_nhiem_vu = [
                {'tieu_de': 'Xử lý công văn đến 577/UBND-VX (về dịch bệnh)',
                 'han_hoan_thanh': '2026-04-20',
                 'trang_thai': 'Đang xử lý',
                 'lien_quan': 'Công văn đến #1'},
                {'tieu_de': 'Soạn thảo công văn đi trình Sở Y Tế ký',
                 'han_hoan_thanh': '2026-04-22',
                 'trang_thai': 'Chưa xử lý',
                 'lien_quan': 'Công văn đi #3'},
                {'tieu_de': 'Phê duyệt hồ sơ lưu trữ ABC',
                 'han_hoan_thanh': '2026-04-18',
                 'trang_thai': 'Đã hoàn thành',
                 'lien_quan': 'Hồ sơ ABC #1'},
            ]
        so_luong_nhiem_vu = len(ds_nhiem_vu)

        # Cập nhật 4 card thống kê
        self.view.update_thong_ke(so_luong_den, so_luong_di, so_luong_hoso, so_luong_nhiem_vu)

        # Cập nhật danh sách 5 công văn đến mới nhất
        ds_den_moi = sorted(ds_den, key=lambda x: x.get('ngay_den', ''), reverse=True)[:5]
        self.view.update_danh_sach_den([{
            'so_ky_hieu': item.get('so_ky_hieu', ''),
            'ngay_den': item.get('ngay_den', ''),
            'trich_yeu': item.get('trich_yeu', '')
        } for item in ds_den_moi])

        # Cập nhật danh sách 5 công văn đi mới nhất
        ds_di_moi = sorted(ds_di, key=lambda x: x.get('ngay_van_ban', ''), reverse=True)[:5]
        self.view.update_danh_sach_di([{
            'so_ky_hieu': item.get('so_ky_hieu', ''),
            'ngay_van_ban': item.get('ngay_van_ban', ''),
            'noi_nhan': item.get('noi_nhan', '')
        } for item in ds_di_moi])

        # Cập nhật bảng nhiệm vụ
        self.view.update_nhiem_vu(ds_nhiem_vu)
=======
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
>>>>>>> 6eb3327898e9fb03bcea83aed79aabac5164e987
