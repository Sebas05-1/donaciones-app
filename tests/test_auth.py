import pytest

def test_register_get(client):
    """Verifica que la página de registro carga correctamente."""
    resp = client.get("/register")
    assert resp.status_code == 200
    assert b"Registrado" not in resp.data  # No hay mensaje todavía

def test_login_get(client):
    """Verifica que el formulario de login carga correctamente."""
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"Inicia" in resp.data or b"Login" in resp.data

def test_login_post(monkeypatch, client):
    """Simula un login exitoso."""
    class FakeAuth:
        def validate_login(self, user, password):
            return True, {"id": 1, "username": "admin", "role_nombre": "superAdmin"}

    monkeypatch.setattr("routes.auth_presenter", FakeAuth())

    resp = client.post("/login", data={"identifier": "admin", "password": "123"}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"dashboard" in resp.data.lower() or b"Inicio" in resp.data
