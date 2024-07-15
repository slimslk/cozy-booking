from django.db import models

from apps.listings.models import Apartment
from apps.reservations.choices.status_choices import StatusChoices
from apps.users.models import User


class Reservation(models.Model):
    user = models.ForeignKey(User, related_name='booking', on_delete=models.CASCADE)
    listing = models.ForeignKey(Apartment, related_name='booking', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=64, choices=StatusChoices.choices(), default=StatusChoices.PENDING)

    class Meta:
        db_table = 'reservations'
