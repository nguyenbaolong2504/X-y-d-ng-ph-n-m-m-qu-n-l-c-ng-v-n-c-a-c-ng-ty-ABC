import sqlite3
import os

DB_NAME = "quanlyvanban.db"

def get_db_connection():
    """Tạo kết nối đến cơ sở dữ liệu SQLite."""
    conn = sqlite3.connect(DB_NAME)
    # Trả về dữ liệu dạng dictionary (dễ truy xuất bằng tên cột)
    conn.row_factory = sqlite3.Row 
    return conn