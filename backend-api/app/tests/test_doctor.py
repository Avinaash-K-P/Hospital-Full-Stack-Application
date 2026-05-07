from app.tests.conftest import client

def get_token():

    response = client.post(
        "/auth/login",
        json={
            "email": "jim@hospital.com",
            "password": "1234"
        }
    )

    token = response.json()["data"]["access_token"]

    return token

def test_get_doctors():

    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get("/doctor/search",headers=headers)

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True