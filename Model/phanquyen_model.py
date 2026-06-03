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

    def _get_connection(self):
        return pyodbc.connect(self.conn_str)

    # ---------- Quản lý người dùng ----------
    def get_all_users(self, keyword=""):
        sql = """
            SELECT Id, Username, Password,
                   CASE 
                       WHEN IsAdmin = 1 THEN N'Admin'
                       WHEN NhomQuyenId = 1 THEN N'Giám đốc'
                       WHEN NhomQuyenId = 2 THEN N'Trưởng phòng'
                       ELSE N'Nhân viên'
                   END AS VaiTro,
                   HoTen
            FROM CanBo
            WHERE Username IS NOT NULL
        """
        params = []
        if keyword:
            sql += " AND Username LIKE ?"
            params.append(f"%{keyword}%")
        sql += " ORDER BY Id"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    def get_user_by_id(self, user_id):
        sql = "SELECT Id, Username, Password, NhomQuyenId, HoTen FROM CanBo WHERE Id = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None

    def get_user_by_username(self, username):
        sql = "SELECT Id, Username, Password, NhomQuyenId, HoTen FROM CanBo WHERE Username = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, row))
            return None

    def add_user(self, data):
        # Khi thêm mới, mặc định IsAdmin = 0
        sql = """
            INSERT INTO CanBo (Username, Password, NhomQuyenId, HoTen, IsAdmin)
            VALUES (?, ?, ?, ?, 0)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (
                data['Username'],
                data['Password'],
                data['NhomQuyenId'],
                data['HoTen']
            ))
            conn.commit()
            return cursor.execute("SELECT @@IDENTITY").fetchval()

    def update_user(self, user_id, data):
        # Khi cập nhật, set IsAdmin = 0 để hiển thị đúng theo NhomQuyenId
        sql = """
            UPDATE CanBo
            SET Password = ?, NhomQuyenId = ?, HoTen = ?, IsAdmin = 0
            WHERE Id = ?
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (
                data['Password'],
                data['NhomQuyenId'],
                data['HoTen'],
                user_id
            ))
            conn.commit()

    def delete_user(self, user_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM QuyenMenu WHERE CanBoId = ?", (user_id,))
            cursor.execute("DELETE FROM CanBo WHERE Id = ?", (user_id,))
            conn.commit()

    # ---------- Quản lý menu ----------
    def get_all_menus(self):
        sql = "SELECT Id, TenMenu FROM MenuHeThong ORDER BY Id"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    def get_user_permissions(self, user_id):
        sql = "SELECT MenuId FROM QuyenMenu WHERE CanBoId = ? AND DuocXem = 1"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (user_id,))
            return [row[0] for row in cursor.fetchall()]

    def save_permissions(self, user_id, menu_ids):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM QuyenMenu WHERE CanBoId = ?", (user_id,))
            for menu_id in menu_ids:
                cursor.execute(
                    "INSERT INTO QuyenMenu (CanBoId, MenuId, DuocXem) VALUES (?, ?, 1)",
                    (user_id, menu_id)
                )
            conn.commit()

    def get_nhomquyen_list(self):
        return [
            {"id": 1, "ten": "Giám đốc"},
            {"id": 2, "ten": "Trưởng phòng"},
            {"id": 3, "ten": "Nhân viên"}
        ]