from app.tests.conftest import client

def get_token():

    response = client.post(
        "/auth/login",
        json={
            "email": "hari@example.com",
            "password": "hari@123"
        }
    )

    token = response.json()["data"]["access_token"]

    return token

def test_create_appointment():

    token = get_token()

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/appointment/",
        headers= headers,
        json={
            "doctor_id": 2,
            "patient_id": 3,
            "appointment_date": "2026-06-28T15:30:00",
            "status": "pending"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

def test_double_booking():

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "doctor_id": 2,
        "patient_id": 2,
        "appointment_date": "2026-05-01T12:00:00",
        "status": "pending"
    }
    first_response = client.post(
        "/appointment/",
        headers=headers,
        json=payload
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/appointment/",
        headers=headers,
        json=payload
    )

    assert second_response.status_code == 400

    data = second_response.json()

    assert data["success"] is False

def test_unauthorized_booking():

    response = client.post(
        "/appointment/",
        json={
            "doctor_id": 1,
            "patient_id": 2,
            "appointment_date": "2026-06-06T10:30:00",
            "status": "pending"
        }
    )

    assert response.status_code == 403