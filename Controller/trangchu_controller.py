# controller/trangchu_controller.py
from Model.congvan_model import CongVanModel
from Model.congvandi_model import CongVanDiModel

# === Giả sử bạn đã có các model này (nếu chưa thì tạo tương tự) ===
# from Model.hoso_model import HoSoModel
# from Model.nhiemvu_model import NhiemVuModel

class TrangChuController:
    def __init__(self, view):
        self.view = view
        self.model_den = CongVanModel()
        self.model_di = CongVanDiModel()

        # TODO: Khởi tạo model hồ sơ và nhiệm vụ nếu có
        # self.model_hoso = HoSoModel()
        # self.model_nhiemvu = NhiemVuModel()

        self.view.yeu_cau_thong_ke.connect(self.load_data)
        self.load_data()

    def load_data(self):
        # 1. Lấy dữ liệu thật từ database
        ds_den = self.model_den.get_all()           # list công văn đến
        ds_di = self.model_di.get_all()             # list công văn đi

        # 2. Số lượng thực tế
        so_luong_den = len(ds_den)                  # ví dụ: nếu có 5 công văn đến → hiển thị 5
        so_luong_di = len(ds_di)

        # 3. Lấy số lượng hồ sơ (nếu có model)
        try:
            # so_luong_hoso = len(self.model_hoso.get_all())
            so_luong_hoso = 0   # tạm thời, bạn thay bằng dòng trên khi có model
        except:
            so_luong_hoso = 0

        # 4. Lấy danh sách nhiệm vụ thật (nếu có model)
        try:
            # ds_nhiem_vu = self.model_nhiemvu.get_all()
            ds_nhiem_vu = []    # tạm thời, thay bằng dòng trên khi có model
        except:
            ds_nhiem_vu = []

        # Nếu chưa có dữ liệu nhiệm vụ trong DB, bạn có thể dùng mẫu (hoặc để trống)
        if not ds_nhiem_vu:
            # Bạn có thể lấy từ một bảng `tasks` thật hoặc giữ mock tạm
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

        so_luong_nhiem_vu = len(ds_nhiem_vu)   # số lượng nhiệm vụ (hiển thị lên card)

        # 5. Cập nhật 4 card thống kê
        self.view.update_thong_ke(
            so_luong_den,
            so_luong_di,
            so_luong_hoso,
            so_luong_nhiem_vu
        )

        # 6. Cập nhật danh sách 5 công văn đến mới nhất
        ds_den_moi = sorted(ds_den, key=lambda x: x.get('ngay_den', ''), reverse=True)[:5]
        self.view.update_danh_sach_den([{
            'so_ky_hieu': item.get('so_ky_hieu', ''),
            'ngay_den': item.get('ngay_den', ''),
            'trich_yeu': item.get('trich_yeu', '')
        } for item in ds_den_moi])

        # 7. Cập nhật danh sách 5 công văn đi mới nhất
        ds_di_moi = sorted(ds_di, key=lambda x: x.get('ngay_van_ban', ''), reverse=True)[:5]
        self.view.update_danh_sach_di([{
            'so_ky_hieu': item.get('so_ky_hieu', ''),
            'ngay_van_ban': item.get('ngay_van_ban', ''),
            'noi_nhan': item.get('noi_nhan', '')
        } for item in ds_di_moi])

        # 8. Cập nhật bảng nhiệm vụ phía dưới (toàn bộ, không chỉ 5)
        self.view.update_nhiem_vu(ds_nhiem_vu)