def test_create_appointment(test_client):
    login = test_client.post("/auth/login", json={
        "email": "lisa@hospital.com",
        "password": "1234"
    })

    token = login.json()["access_token"]

    response = test_client.post(
        "/appointment/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "doctor_id": 1,
            "patient_id": 1,
            "appointment_date": "2026-04-28T10:00:00",
            "status": "Scheduled"
        }
    )

    assert response.status_code == 200