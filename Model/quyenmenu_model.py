import pyodbc

class QuyenMenuModel:

    def __init__(self, conn_str):
        self.conn_str = conn_str

    def get_menu_by_user(self, canbo_id):

        conn = pyodbc.connect(self.conn_str)

        cursor = conn.cursor()

        cursor.execute("""
            SELECT m.MaMenu
            FROM QuyenMenu q
            JOIN MenuHeThong m
                ON q.MenuId = m.Id
            WHERE q.CanBoId = ?
            AND q.DuocXem = 1
        """,(canbo_id,))

        rows = cursor.fetchall()

        conn.close()

        return [r[0] for r in rows]