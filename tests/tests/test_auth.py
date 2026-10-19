import requests
import pytest

AUTH_URL = "https://restful-booker.herokuapp.com/auth"


def test_create_token_with_valid_credentials():
    payload = {
        "username": "admin",
        "password": "password123",
    }

    response = requests.post(
        AUTH_URL,
        json=payload,
        timeout=10,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]

    data = response.json()

    assert isinstance(data, dict)
    assert data["token"]
    assert isinstance(data["token"], str)
    assert data["token"] != ''


@pytest.mark.parametrize(
    "username, password",
    [
        ("wrong_user", "password123"),
        ("admin", "wrong_password"),
    ])
def test_create_token_with_invalid_credentials(username, password):
    payload = {
        "username": username,
        "password": password,
    }

    response = requests.post(
        AUTH_URL,
        json=payload,
        timeout=10,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]

    data = response.json()

    assert isinstance(data, dict)
    assert "token" not in data
    assert data["reason"] == "Bad credentials"
