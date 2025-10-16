def test_donantes_list(monkeypatch, client):
    """Verifica que /donantes carga correctamente con usuario autenticado."""
    fake_donantes = [
        {"id": 1, "nombre": "Juan Pérez", "correo": "juan@example.com", "estado": True}
    ]

    class FakeDonantePresenter:
        def get_all(self):
            return fake_donantes

    monkeypatch.setattr("routes.donante_presenter", FakeDonantePresenter())

    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["username"] = "admin"
        sess["role"] = "superAdmin"

    resp = client.get("/donantes")
    assert resp.status_code == 200
    assert b"Juan" in resp.data
