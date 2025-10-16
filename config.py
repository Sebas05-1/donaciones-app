# config.py
import os
import pymysql

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '95556e16175f65f09fcea65a5ca9fe534b7a4fc88025df86')
    # Configuración para PyMySQL
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'db': 'proyecto_vpdos',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor  # Resultados como dicts
    }