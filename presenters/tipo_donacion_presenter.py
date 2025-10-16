import pymysql
from app import get_db_connection

class TipoDonacionModel:
    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tipo_donacion (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(50) UNIQUE NOT NULL,
                        descripcion VARCHAR(255)
                    )
                """)
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM tipo_donacion")
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_by_id(tipo_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM tipo_donacion WHERE id = %s", (tipo_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_by_name(nombre):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM tipo_donacion WHERE nombre = %s", (nombre,))
                return cursor.fetchone()
        finally:
            conn.close()