# models/role_model.py
import pymysql
from app import get_db_connection

class RoleModel:
    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS roles (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(50) UNIQUE NOT NULL,
                        descripcion VARCHAR(255)
                    )
                """)
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_all_roles(exclude_superadmin=True):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                if exclude_superadmin:
                    cursor.execute("SELECT * FROM roles WHERE nombre != 'superAdmin'")
                else:
                    cursor.execute("SELECT * FROM roles")
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_role_by_id(role_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM roles WHERE id = %s", (role_id,))
                return cursor.fetchone()
        finally:
            conn.close()