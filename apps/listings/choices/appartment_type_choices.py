from enum import Enum


class ApartmentTypeChoice(Enum):
    HOTEL = "Hotel"
    HOUSE = "House"
    APARTMENT = "Apartment"
    FLAT = "Flat"
    HOSTEL = "Hostel"
    GUEST_HOUSE = "Guest house"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]

    def __str__(self):
        return self.name
