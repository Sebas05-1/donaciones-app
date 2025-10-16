# models/beneficiario_model.py
import pymysql
from app import get_db_connection
from datetime import datetime

class BeneficiarioModel:
    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS beneficiarios (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(200) NOT NULL,
                        nit VARCHAR(80),
                        telefono VARCHAR(50),
                        correo VARCHAR(150),
                        direccion VARCHAR(255),
                        observaciones TEXT,
                        activo BOOLEAN NOT NULL DEFAULT TRUE,
                        creado_en DATETIME NOT NULL
                    )
                """)
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def create(nombre, nit, telefono, correo, direccion, observaciones):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO beneficiarios (nombre, nit, telefono, correo, direccion, observaciones, activo, creado_en)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (nombre, nit, telefono, correo, direccion, observaciones, True, datetime.utcnow()))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_by_id(beneficiario_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM beneficiarios WHERE id = %s", (beneficiario_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_all(only_active=False):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                if only_active:
                    cursor.execute("SELECT * FROM beneficiarios WHERE activo = TRUE")
                else:
                    cursor.execute("SELECT * FROM beneficiarios")
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def update(beneficiario_id, nombre, nit, telefono, correo, direccion, observaciones):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE beneficiarios
                    SET nombre = %s, nit = %s, telefono = %s, correo = %s, direccion = %s, observaciones = %s
                    WHERE id = %s
                """, (nombre, nit, telefono, correo, direccion, observaciones, beneficiario_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def toggle_activo(beneficiario_id, activo):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE beneficiarios SET activo = %s WHERE id = %s", (activo, beneficiario_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()