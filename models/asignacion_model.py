# models/asignacion_model.py
import pymysql
from app import get_db_connection
from datetime import datetime

class AsignacionModel:
    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS asignaciones (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        donacion_id INT NOT NULL,
                        beneficiario_id INT NOT NULL,
                        tipo_id INT NOT NULL,
                        cantidad INT,
                        monto DECIMAL(15,2),
                        fecha_asignacion DATETIME NOT NULL,
                        FOREIGN KEY (donacion_id) REFERENCES donaciones(id),
                        FOREIGN KEY (beneficiario_id) REFERENCES beneficiarios(id),
                        FOREIGN KEY (tipo_id) REFERENCES tipo_donacion(id)
                    )
                """)
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def create(donacion_id, beneficiario_id, tipo_id, cantidad, monto):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO asignaciones (donacion_id, beneficiario_id, tipo_id, cantidad, monto, fecha_asignacion)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (donacion_id, beneficiario_id, tipo_id, cantidad, monto, datetime.utcnow()))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_by_id(asignacion_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT a.*, t.nombre as tipo_nombre
                    FROM asignaciones a
                    LEFT JOIN tipo_donacion t ON a.tipo_id = t.id
                    WHERE a.id = %s
                """, (asignacion_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT a.*, t.nombre as tipo_nombre
                    FROM asignaciones a
                    LEFT JOIN tipo_donacion t ON a.tipo_id = t.id
                """)
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def delete(asignacion_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM asignaciones WHERE id = %s", (asignacion_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()