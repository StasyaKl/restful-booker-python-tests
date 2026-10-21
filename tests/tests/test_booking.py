import requests
import pytest

BASE_URL = "https://restful-booker.herokuapp.com"
BOOKING_URL = f"{BASE_URL}/booking"

post_payload = {
    "firstname": "Anastasia",
    "lastname": "Tester",
    "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-11-01",
        "checkout": "2026-11-10",
    },
    "additionalneeds": "Breakfast",
}


def test_get_all_bookings():
    response = requests.get(BOOKING_URL, timeout=10)

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]

    data = response.json()

    assert isinstance(data, list)
    assert data

    first_booking = data[0]

    assert isinstance(first_booking, dict)
    assert "bookingid" in first_booking
    assert isinstance(first_booking["bookingid"], int)
    assert first_booking["bookingid"] > 0


def test_get_booking_by_id():
    response = requests.get(BOOKING_URL, timeout=10)
    assert response.status_code == 200

    data = response.json()
    assert data

    booking_id = data[0]["bookingid"]

    booking_url = f"{BOOKING_URL}/{booking_id}"
    booking_response = requests.get(booking_url, timeout=10)
    assert booking_response.status_code == 200
    assert "application/json" in booking_response.headers["Content-Type"]

    booking = booking_response.json()
    assert isinstance(booking, dict)

    required_fields = [
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates",
    ]

    for field in required_fields:
        assert field in booking

    assert isinstance(booking["firstname"], str)
    assert isinstance(booking["lastname"], str)
    assert isinstance(booking["totalprice"], int)
    assert isinstance(booking["depositpaid"], bool)
    assert isinstance(booking["bookingdates"], dict)

    assert "checkin" in booking["bookingdates"]
    assert "checkout" in booking["bookingdates"]
    assert isinstance(booking["bookingdates"]["checkin"], str)
    assert isinstance(booking["bookingdates"]["checkout"], str)


@pytest.mark.parametrize("booking_id", [0, -1, 999999999, "abc"])
def test_get_booking_with_invalid_id(booking_id):
    response = requests.get(f"{BOOKING_URL}/{booking_id}", timeout=10)

    assert response.status_code == 404
    assert response.text.strip() == "Not Found"


def test_create_booking():
    response = requests.post(
        BOOKING_URL,
        json=post_payload,
        timeout=10,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]

    response_data = response.json()
    assert isinstance(response_data, dict)
    assert "bookingid" in response_data
    assert response_data["bookingid"] > 0
    assert isinstance(response_data["bookingid"], int)
    assert "booking" in response_data
    assert isinstance(response_data["booking"], dict)
    assert response_data["booking"] == post_payload

    response_get = requests.get(f"{BOOKING_URL}/{response_data["bookingid"]}", timeout=10)
    assert response_get.status_code == 200
    data_get = response_get.json()
    assert post_payload == data_get


def test_update_booking(auth_token, created_booking):
    updated_payload = {
        "firstname": "Anna",
        "lastname": "Automation",
        "totalprice": 250,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2026-12-01",
            "checkout": "2026-12-15",
        },
        "additionalneeds": "Late checkout",
    }

    response_put = requests.put(
        f"{BOOKING_URL}/{created_booking["booking_id"]}",
        headers={"Cookie": f"token={auth_token}"},
        json=updated_payload,
        timeout=10,
    )

    assert response_put.status_code == 200
    assert "application/json" in response_put.headers["Content-Type"]

    data_put = response_put.json()
    assert isinstance(data_put, dict)
    assert data_put == updated_payload

    response_get = requests.get(f"{BOOKING_URL}/{created_booking["booking_id"]}", timeout=10)
    assert response_get.status_code == 200

    data_get = response_get.json()
    assert data_get == updated_payload
