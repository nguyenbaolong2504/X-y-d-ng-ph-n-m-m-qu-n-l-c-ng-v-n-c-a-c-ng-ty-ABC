import pyodbc
from config import DB_CONFIG

class PhanQuyenModel:

    def __init__(self):

        self.conn_str = (
            f"DRIVER={DB_CONFIG['driver']};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            "Trusted_Connection=yes;"
        )

    def connect(self):

        return pyodbc.connect(
            self.conn_str
        )

    # ==================================
    # USER
    # ==================================

    def get_all(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                Username,
                Password,
                NhomQuyenId,
                HoTen
            FROM CanBo
            ORDER BY Username
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    def insert(
        self,
        username,
        password,
        role
    ):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO CanBo
            (
                Username,
                Password,
                NhomQuyenId
            )
            VALUES
            (
                ?, ?, ?
            )
            """,
            (
                username,
                password,
                role
            )
        )

        conn.commit()

        conn.close()

    # ==================================
    # MENU PERMISSION
    # ==================================

    def get_permissions(
        self,
        username
    ):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT MenuName
            FROM QuyenMenu
            WHERE UserName=?
            AND DuocXem=1
            """,
            (username,)
        )

        rows = cursor.fetchall()

        conn.close()

        return [
            row[0]
            for row in rows
        ]

    def save_permissions(
        self,
        username,
        menus
    ):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM QuyenMenu
            WHERE UserName=?
            """,
            (username,)
        )

        for menu in menus:

            cursor.execute(
                """
                INSERT INTO QuyenMenu
                (
                    UserName,
                    MenuName,
                    DuocXem
                )
                VALUES
                (
                    ?, ?, 1
                )
                """,
                (
                    username,
                    menu
                )
            )

        conn.commit()

        conn.close()