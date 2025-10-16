import pytest
from app import create_app

@pytest.fixture
def app(monkeypatch):
    """Crea una app Flask configurada para pruebas con DB mockeada."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test_secret"
    })

    # Mock de conexión a base de datos
    def fake_get_db_connection():
        class FakeConn:
            def cursor(self):
                return self
            def execute(self, *args, **kwargs):
                pass
            def fetchall(self):
                return []
            def fetchone(self):
                return None
            def commit(self):
                pass
            def close(self):
                pass
        return FakeConn()

    from app import get_db_connection
    monkeypatch.setattr("app.get_db_connection", fake_get_db_connection)

    yield app

@pytest.fixture
def client(app):
    """Cliente de pruebas para simular peticiones HTTP."""
    return app.test_client()
