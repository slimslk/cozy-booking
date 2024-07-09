from enum import Enum


class UserChoices(Enum):
    ADMIN = 'admin'
    LESSOR = 'lessor'
    RENTER = 'renter'

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(choice.name, choice.value) for choice in cls]
