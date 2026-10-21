import pytest
import requests
import test_auth


@pytest.fixture
def auth_token():
    payload = {
        "username": "admin",
        "password": "password123",
    }

    response = requests.post(
        test_auth.AUTH_URL,
        json=payload,
        timeout=10,
    )

    assert response.status_code == 200

    data = response.json()

    assert "token" in data
    assert isinstance(data["token"], str)
    assert data["token"]

    return data["token"]
