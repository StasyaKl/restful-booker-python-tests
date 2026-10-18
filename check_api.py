import requests


response = requests.get(
    "https://restful-booker.herokuapp.com/booking"
)

print(response.status_code)
print(response.headers.get("Content-Type"))
print(response.text)