
import pyodbc
from typing import List, Dict
from config import DB_CONFIG


class CongVanDiModel:

    def __init__(self):

        self.conn_str = (
            f"DRIVER={DB_CONFIG['driver']};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"Trusted_Connection=yes;"
        )

    # =====================================================
    # CONNECTION
    # =====================================================

    def _get_connection(self):

        return pyodbc.connect(self.conn_str)

    # =====================================================
    # GET ALL
    # =====================================================

    def get_all(self) -> List[Dict]:

        with self._get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""

                SELECT 
                    Id,
                    SoPhatHanh,
                    Nam,
                    KyHieu,
                    NgayKy,
                    NoiNhan,
                    TrichYeu,
                    TrangThaiChuyen,
                    GhiChu,
                    FilePath

                FROM CongVanPhatHanh

                ORDER BY Id DESC

            """)

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

                INSERT INTO CongVanPhatHanh 
                (
                    SoPhatHanh,
                    Nam,
                    KyHieu,
                    NgayKy,
                    DonViSoanId,
                    TrichYeu,
                    NoiNhan,
                    NguoiKyId,
                    NguoiSoanId,
                    NguoiDuyetId,
                    IsKhan,
                    IsMat,
                    TrangThaiChuyen,
                    CoDinhKem,
                    NguoiTaoId,
                    NgayChuyen,
                    GhiChu,
                    FilePath
                )

                VALUES 
                (
                    ?, ?, ?, ?,
                    1,
                    ?, ?,
                    1,
                    1,
                    1,
                    0,
                    0,
                    0,
                    0,
                    1,
                    GETDATE(),
                    ?,
                    ?
                )


            """

            cursor.execute(sql, (

                data.get('SoPhatHanh'),

                data.get('Nam'),

                data.get('KyHieu'),

                data.get('NgayKy'),

                data.get('TrichYeu'),

                data.get('NoiNhan'),

                data.get('GhiChu'),

                data.get('FilePath')

            ))

            conn.commit()

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, id: int, data: Dict):

        with self._get_connection() as conn:

            cursor = conn.cursor()

            sql = """

                UPDATE CongVanPhatHanh

                SET
                    SoPhatHanh=?,
                    Nam=?,
                    KyHieu=?,
                    NgayKy=?,
                    TrichYeu=?,
                    NoiNhan=?,
                    TrangThaiChuyen=?,
                    GhiChu=?,
                    FilePath=?

                WHERE Id=?

            """

            cursor.execute(sql, (

                data.get('SoPhatHanh'),

                data.get('Nam'),

                data.get('KyHieu'),

                data.get('NgayKy'),

                data.get('TrichYeu'),

                data.get('NoiNhan'),

                data.get('TrangThaiChuyen', 0),

                data.get('GhiChu'),

                data.get('FilePath'),

                id

            ))

            conn.commit()

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, id: int):

        with self._get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""

                DELETE FROM CongVanPhatHanh

                WHERE Id=?

            """,(id,))

            conn.commit()

    # =====================================================
    # EXPORT
    # =====================================================

    def get_data_for_export(
        self,
        start_date=None,
        end_date=None
    ) -> List[Dict]:

        return self.get_all()