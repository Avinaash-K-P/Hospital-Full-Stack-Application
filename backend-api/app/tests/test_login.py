from app.tests.conftest import client

def test_login_success():

    response = client.post(
        "/auth/login",
        json={
            "email": "jim@hospital.com",
            "password": "1234"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "access_token" in data["data"]

def test_login_failure():

    response = client.post(
        "/auth/login",
        json={
            "email": "j@hospital.com",
            "password": "0000"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "access_token" in data["data"]