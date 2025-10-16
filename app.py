# app.py
from flask import Flask
from flask_bcrypt import Bcrypt
from config import Config
import pymysql

bcrypt = Bcrypt()

def get_db_connection():
    """Función para obtener conexión PyMySQL."""
    return pymysql.connect(**Config.DB_CONFIG)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)

    with app.app_context():
        # Importar rutas
        from routes import bp as main_bp
        app.register_blueprint(main_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)