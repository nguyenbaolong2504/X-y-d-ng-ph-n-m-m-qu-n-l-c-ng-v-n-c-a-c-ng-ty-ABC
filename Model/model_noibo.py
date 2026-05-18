import pyodbc

from PyQt6.QtCore import (
    QAbstractTableModel,
    Qt,
    QModelIndex
)

from typing import List, Dict

from config import DB_CONFIG


# =========================================================
# MODEL
# =========================================================

class ModelNoiBo:

    def __init__(self):

        if 'trusted_connection' in DB_CONFIG:

            self.conn_str = (
                f"DRIVER={DB_CONFIG['driver']};"
                f"SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};"
                f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
            )

        else:

            self.conn_str = (
                f"DRIVER={DB_CONFIG['driver']};"
                f"SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};"
                f"UID={DB_CONFIG['username']};"
                f"PWD={DB_CONFIG['password']};"
            )

    # =====================================================
    # CONNECTION
    # =====================================================

    def _get_connection(self):

        return pyodbc.connect(self.conn_str)

    # =====================================================
    # GET ALL
    # =====================================================

    def get_all(self, keyword="") -> List[Dict]:

        with self._get_connection() as conn:

            cursor = conn.cursor()

            query = """

                SELECT 
                    Id,
                    KyHieu,
                    NgayBanHanh,
                    LoaiCongVanId,
                    TrichYeu,
                    DonViSoanId,
                    NguoiKyId,
                    NguoiNhan,
                    GhiChu

                FROM CongVanNoiBo

            """

            if keyword:

                query += """

                    WHERE 
                        KyHieu LIKE ?
                        OR TrichYeu LIKE ?

                """

                cursor.execute(
                    query,
                    (
                        f"%{keyword}%",
                        f"%{keyword}%"
                    )
                )

            else:

                query += " ORDER BY Id DESC "

                cursor.execute(query)

            rows = cursor.fetchall()

            return [

                dict(
                    zip(
                        [col[0] for col in cursor.description],
                        row
                    )
                )

                for row in rows

            ]

    # =====================================================
    # ADD
    # =====================================================

    def add(self, data: Dict):

        with self._get_connection() as conn:

            cursor = conn.cursor()

            sql = """

                INSERT INTO CongVanNoiBo
                (
                    KyHieu,
                    NgayBanHanh,
                    LoaiCongVanId,
                    TrichYeu,
                    DonViSoanId,
                    NguoiKyId,
                    NguoiNhan,
                    GhiChu
                )

                VALUES
                (
                    ?, ?, ?, ?, ?, ?, ?, ?
                )

            """

            cursor.execute(sql,(

                data.get("KyHieu"),

                data.get("NgayBanHanh"),

                data.get("LoaiCongVanId"),

                data.get("TrichYeu"),

                data.get("DonViSoanId"),

                data.get("NguoiKyId"),

                data.get("NguoiNhan"),

                data.get("GhiChu")

            ))

            conn.commit()

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, id, data: Dict):

        with self._get_connection() as conn:

            cursor = conn.cursor()

            sql = """

                UPDATE CongVanNoiBo

                SET
                    KyHieu=?,
                    NgayBanHanh=?,
                    LoaiCongVanId=?,
                    TrichYeu=?,
                    DonViSoanId=?,
                    NguoiKyId=?,
                    NguoiNhan=?,
                    GhiChu=?

                WHERE Id=?

            """

            cursor.execute(sql,(

                data.get("KyHieu"),

                data.get("NgayBanHanh"),

                data.get("LoaiCongVanId"),

                data.get("TrichYeu"),

                data.get("DonViSoanId"),

                data.get("NguoiKyId"),

                data.get("NguoiNhan"),

                data.get("GhiChu"),

                id

            ))

            conn.commit()

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, id):

        with self._get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""

                DELETE FROM CongVanNoiBo

                WHERE Id=?

            """,(id,))

            conn.commit()


# =========================================================
# TABLE MODEL
# =========================================================

class NoiBoTableModel(QAbstractTableModel):

    def __init__(self, data: List[Dict]):

        super().__init__()

        self._data = data

        self._headers = [

            "ID",
            "Ký hiệu",
            "Ngày ban hành",
            "Loại văn bản",
            "Trích yếu, thông báo",
            "Đơn vị soạn",
            "Người ký",
            "Đơn vị nhận",
            "Ghi chú"

        ]

        self._keys = [

            "Id",
            "KyHieu",
            "NgayBanHanh",
            "LoaiCongVanId",
            "TrichYeu",
            "DonViSoanId",
            "NguoiKyId",
            "NguoiNhan",
            "GhiChu"

        ]

    # =====================================================
    # DATA
    # =====================================================

    def data(
        self,
        index,
        role=Qt.ItemDataRole.DisplayRole
    ):

        if not index.isValid():

            return None

        if role == Qt.ItemDataRole.DisplayRole:

            row = self._data[index.row()]

            col = index.column()

            key = self._keys[col]

            value = row.get(key, "")

            return str(value) if value is not None else ""

        return None

    # =====================================================
    # ROW
    # =====================================================

    def rowCount(self,parent=QModelIndex()):

        return len(self._data)

    # =====================================================
    # COLUMN
    # =====================================================

    def columnCount(self,parent=QModelIndex()):

        return len(self._headers)

    # =====================================================
    # HEADER
    # =====================================================

    def headerData(
        self,
        section,
        orientation,
        role=Qt.ItemDataRole.DisplayRole
    ):

        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):

            return self._headers[section]

        return None