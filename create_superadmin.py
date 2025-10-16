# create_superadmin.py
import pymysql
from getpass import getpass
from bcrypt import hashpw, gensalt

DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASS = '123456'
DB_NAME = 'proyecto_mvp'

# Cambia estos datos
SUPER_USERNAME = 'superadmin'
SUPER_EMAIL = 'superadmin@fundacion.local'
# SUPER_PASSWORD = 123456789
# ingresa la contraseña cuando ejecutes
pw = getpass("Nueva contraseña para superadmin: ")
pw_hash = hashpw(pw.encode('utf-8'), gensalt()).decode('utf-8')

conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, db=DB_NAME, charset='utf8mb4')
try:
    with conn.cursor() as cur:
        # Obtener id del role superAdmin
        cur.execute("SELECT id FROM roles WHERE nombre='superAdmin' LIMIT 1;")
        row = cur.fetchone()
        if row is None:
            raise RuntimeError("No existe el role 'superAdmin'. Asegúrate de haber insertado los roles.")
        role_id = row[0]
        # Insertar usuario superadmin
        cur.execute("""
            INSERT INTO usuarios (username, email, telefono, cedula, password, role_id, activo)
            VALUES (%s, %s, %s, %s, %s, %s, 1);
        """, (SUPER_USERNAME, SUPER_EMAIL, '', '', pw_hash, role_id))
        conn.commit()
        print("superAdmin creado correctamente.")
finally:
    conn.close()
