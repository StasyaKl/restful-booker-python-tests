import requests

BASE_URL = "https://restful-booker.herokuapp.com"
BOOKING_URL = f"{BASE_URL}/booking"


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


def test_get_nonexistent_booking():
    response = requests.get(f"{BOOKING_URL}/999999999", timeout=10)

    assert response.status_code == 404
    assert response.text.strip() == "Not Found"
