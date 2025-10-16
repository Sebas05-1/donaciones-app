# tests/test_dashboard.py

def test_dashboard_requires_login(client):
    response = client.get('/dashboard')
    assert response.status_code == 302
    assert '/login' in response.location


def test_dashboard_with_session(client):
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['role'] = 'administrador'
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'dashboard' in response.data.lower()
