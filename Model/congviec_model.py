import sqlite3

class CongViecModel:

    def connect(self):
        return sqlite3.connect("quanlyvanban.db")

    def get_all(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM cong_viec
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    def insert(self, ten, nguoi, han, trangthai):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO cong_viec(
            ten_cong_viec,
            nguoi_nhan,
            han_xu_ly,
            trang_thai
        )
        VALUES(?,?,?,?)
        """,(ten,nguoi,han,trangthai))

        conn.commit()
        conn.close()