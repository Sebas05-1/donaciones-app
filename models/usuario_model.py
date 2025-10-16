# models/usuario_model.py
import pymysql
from app import get_db_connection
from datetime import datetime

class UsuarioModel:
    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS usuarios (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(80) UNIQUE NOT NULL,
                        email VARCHAR(150) UNIQUE NOT NULL,
                        telefono VARCHAR(30),
                        cedula VARCHAR(50),
                        password VARCHAR(255) NOT NULL,
                        role_id INT,
                        activo BOOLEAN NOT NULL DEFAULT TRUE,
                        creado_en DATETIME NOT NULL,
                        FOREIGN KEY (role_id) REFERENCES roles(id)
                    )
                """)
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def create_user(username, email, password, telefono, cedula, role_id=None, activo=True):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuarios (username, email, telefono, cedula, password, role_id, activo, creado_en)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (username, email, telefono, cedula, password, role_id, activo, datetime.utcnow()))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_user_by_username_or_email(identifier):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT u.*, r.nombre as role_nombre
                    FROM usuarios u
                    LEFT JOIN roles r ON u.role_id = r.id
                    WHERE u.username = %s OR u.email = %s
                """, (identifier, identifier))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT u.*, r.nombre as role_nombre
                    FROM usuarios u
                    LEFT JOIN roles r ON u.role_id = r.id
                    WHERE u.id = %s
                """, (user_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT u.*, r.nombre as role_nombre
                    FROM usuarios u
                    LEFT JOIN roles r ON u.role_id = r.id
                """)
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def update_user_role(user_id, role_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE usuarios SET role_id = %s WHERE id = %s", (role_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def deactivate_user(user_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE usuarios SET activo = FALSE WHERE id = %s", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()