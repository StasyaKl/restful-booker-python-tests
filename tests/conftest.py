import pytest
import requests
import test_auth
import test_booking


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


@pytest.fixture
def created_booking(auth_token):
    response_post = requests.post(
        test_booking.BOOKING_URL,
        json=test_booking.post_payload,
        timeout=10,
    )

    assert response_post.status_code == 200

    data = response_post.json()

    assert "bookingid" in data

    booking_id = data["bookingid"]

    assert isinstance(booking_id, int)
    assert booking_id > 0

    yield {
        "booking_id": booking_id,
        "payload": test_booking.post_payload,
    }

    response_delete = requests.delete(
        f"{test_booking.BOOKING_URL}/{booking_id}",
        headers={"Cookie": f"token={auth_token}"},
        timeout=10,
    )

    assert response_delete.status_code == 201