import sqlite3

class PhanQuyenModel:

    def connect(self):
        return sqlite3.connect("quanlyvanban.db")

    def get_all(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM users
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    def insert(self, username, password, role):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users(username,password,role)
        VALUES(?,?,?)
        """,(username,password,role))

        conn.commit()
        conn.close()