def test_login(test_client):
    response = test_client.post("/auth/login", json={
        "email": "lisa@hospital.com",
        "password": "1234"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()