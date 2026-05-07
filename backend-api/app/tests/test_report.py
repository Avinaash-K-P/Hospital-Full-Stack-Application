from app.tests.conftest import client

def get_token():

    response = client.post(
        "/auth/login",
        json={
            "email": "jim@hospital.com",
            "password": "1234"
        }
    )

    return response.json()["data"]["access_token"]

def test_upload_pdf_report():

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    files = {
        "file": (
            "test_report.pdf",
            b"Dummy PDF content",
            "application/pdf"
        )
    }

    response = client.post(
        "/reports/upload/1",
        headers=headers,
        files=files
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

def test_invalid_file_type():

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    files = {
        "file": (
            "virus.exe",
            b"fake exe content",
            "application/octet-stream"
        )
    }

    response = client.post(
        "/reports/upload/1",
        headers=headers,
        files=files
    )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False    