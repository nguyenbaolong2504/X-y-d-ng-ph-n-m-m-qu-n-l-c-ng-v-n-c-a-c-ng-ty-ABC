import pandas as pd

def export_to_excel_di(data, filename):
    if not data:
        df = pd.DataFrame(columns=["Số đi", "Năm", "Ký hiệu", "Ngày ký", "Nơi nhận", "Trích yếu", "Trạng thái"])
    else:
        df = pd.DataFrame(data)
        # Lọc và map lại status
        df['TrangThaiChuyen'] = df['TrangThaiChuyen'].apply(lambda x: "Đã chuyển" if x == 1 else "Chưa chuyển")
        
        # Chọn các cột cần xuất
        df = df[["SoPhatHanh", "Nam", "KyHieu", "NgayKy", "NoiNhan", "TrichYeu", "TrangThaiChuyen"]]
        df.columns = ["Số đi", "Năm", "Ký hiệu", "Ngày ký", "Nơi nhận", "Trích yếu", "Trạng thái"]
        
    df.to_excel(filename, index=False)