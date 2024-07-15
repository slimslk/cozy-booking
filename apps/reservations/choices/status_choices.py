from enum import Enum


class StatusChoices(Enum):
    CONFIRMED = 'Confirmed'
    REJECTED = 'Rejected'
    PENDING = 'Pending'
    CHECKED_IN = 'Checked in'

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]

    def __str__(self):
        return self.name
