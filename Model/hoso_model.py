import sqlite3

class HoSoModel:

    def connect(self):
        return sqlite3.connect("quanlyvanban.db")

    def get_muc_luc(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM muc_luc_ho_so
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    def insert_muc_luc(self, ma, ten, ngay):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO muc_luc_ho_so(
            ma_hoso,
            ten_hoso,
            ngay_tao
        )
        VALUES(?,?,?)
        """,(ma,ten,ngay))

        conn.commit()
        conn.close()

    def get_danh_muc(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM danh_muc_ho_so
        """)

        data = cursor.fetchall()

        conn.close()

        return data