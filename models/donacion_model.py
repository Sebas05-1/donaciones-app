# models/donacion_model.py
import pymysql
from app import get_db_connection
from datetime import datetime

class DonacionModel:
    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS donaciones (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(150) NOT NULL,
                        tipo_id INT NOT NULL,
                        donante_id INT,
                        monto DECIMAL(15,2),
                        cantidad INT,
                        descripcion TEXT,
                        estado BOOLEAN NOT NULL DEFAULT TRUE,
                        creado_en DATETIME NOT NULL,
                        FOREIGN KEY (tipo_id) REFERENCES tipo_donacion(id),
                        FOREIGN KEY (donante_id) REFERENCES donantes(id)
                    )
                """)
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def create(nombre, tipo_id, donante_id, monto, cantidad, descripcion):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO donaciones (nombre, tipo_id, donante_id, monto, cantidad, descripcion, estado, creado_en)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (nombre, tipo_id, donante_id, monto, cantidad, descripcion, True, datetime.utcnow()))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_by_id(donacion_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT d.*, t.nombre as tipo_nombre
                    FROM donaciones d
                    LEFT JOIN tipo_donacion t ON d.tipo_id = t.id
                    WHERE d.id = %s
                """, (donacion_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_all(only_active=False):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                if only_active:
                    cursor.execute("""
                        SELECT d.*, t.nombre as tipo_nombre
                        FROM donaciones d
                        LEFT JOIN tipo_donacion t ON d.tipo_id = t.id
                        WHERE d.estado = TRUE
                    """)
                else:
                    cursor.execute("""
                        SELECT d.*, t.nombre as tipo_nombre
                        FROM donaciones d
                        LEFT JOIN tipo_donacion t ON d.tipo_id = t.id
                    """)
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def update(donacion_id, nombre, tipo_id, donante_id, monto, cantidad, descripcion):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE donaciones
                    SET nombre = %s, tipo_id = %s, donante_id = %s, monto = %s, cantidad = %s, descripcion = %s
                    WHERE id = %s
                """, (nombre, tipo_id, donante_id, monto, cantidad, descripcion, donacion_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def deactivate(donacion_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE donaciones SET estado = FALSE WHERE id = %s", (donacion_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def inventario_material():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT d.id, d.nombre, t.nombre as tipo_nombre, d.cantidad, d.descripcion, d.creado_en
                    FROM donaciones d
                    JOIN tipo_donacion t ON d.tipo_id = t.id
                    WHERE d.cantidad IS NOT NULL AND d.estado = TRUE
                """)
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def inventario_economico():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT d.id, d.nombre, t.nombre as tipo_nombre, d.monto, d.descripcion, d.creado_en
                    FROM donaciones d
                    JOIN tipo_donacion t ON d.tipo_id = t.id
                    WHERE d.monto IS NOT NULL AND d.estado = TRUE
                """)
                return cursor.fetchall()
        finally:
            conn.close()