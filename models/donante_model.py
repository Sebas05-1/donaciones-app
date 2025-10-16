# models/donante_model.py
import pymysql
from app import get_db_connection

class DonanteModel:
    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS donantes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(150) NOT NULL,
                        correo VARCHAR(150),
                        telefono VARCHAR(50),
                        direccion VARCHAR(255),
                        cedula VARCHAR(80),
                        estado BOOLEAN NOT NULL DEFAULT TRUE
                    )
                """)
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def create(nombre, correo, telefono, direccion, cedula):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO donantes (nombre, correo, telefono, direccion, cedula, estado)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nombre, correo, telefono, direccion, cedula, True))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_by_id(donante_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM donantes WHERE id = %s", (donante_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_all(only_active=False):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                if only_active:
                    cursor.execute("SELECT * FROM donantes WHERE estado = TRUE")
                else:
                    cursor.execute("SELECT * FROM donantes")
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def update(donante_id, nombre, correo, telefono, direccion, cedula):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE donantes
                    SET nombre = %s, correo = %s, telefono = %s, direccion = %s, cedula = %s
                    WHERE id = %s
                """, (nombre, correo, telefono, direccion, cedula, donante_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def toggle_estado(donante_id, estado):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE donantes SET estado = %s WHERE id = %s", (estado, donante_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()