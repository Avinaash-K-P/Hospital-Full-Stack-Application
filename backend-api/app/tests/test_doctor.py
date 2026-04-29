def test_get_doctors(test_client):
    login = test_client.post("/auth/login", json={
        "email": "lisa@hospital.com",
        "password": "1234"
    })

    token = login.json()["access_token"]

    response = test_client.get(
        "/doctor/search?specialization=",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200