from copy import deepcopy

original = {
    "firstname": "Anastasia",
    "bookingdates": {
        "checkin": "2026-11-01",
    }
}

second = original
second["firstname"] = "Maria"
second["bookingdates"]["checkin"] = "2027-01-01"
print(original)
print(second)

original_2 = {
    "firstname": "Anastasia",
    "bookingdates": {
        "checkin": "2026-11-01",
    }
}

second_2 = original_2.copy()
second_2["firstname"] = "Maria"
second_2["bookingdates"]["checkin"] = "2027-01-01"
print(original_2)
print(second_2)

original_3 = {
    "firstname": "Anastasia",
    "bookingdates": {
        "checkin": "2026-11-01",
    }
}

second_3 = deepcopy(original_3)
second_3["firstname"] = "Maria"
second_3["bookingdates"]["checkin"] = "2027-01-01"
print(original_3)
print(second_3)
