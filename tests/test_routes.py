def test_index_redirects_to_login(client):
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]

def test_dashboard_requires_login(client):
    resp = client.get("/dashboard", follow_redirects=True)
    assert b"Por favor inicia" in resp.data

def test_dashboard_logged_in(monkeypatch, client):
    """Simula usuario autenticado en sesión."""
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["username"] = "admin"
        sess["role"] = "superAdmin"

    resp = client.get("/dashboard")
    assert resp.status_code == 200
    assert b"dashboard" in resp.data.lower() or b"panel" in resp.data
