from django.db import models

from apps.listings.choices.appartment_type_choices import ApartmentTypeChoice
from apps.listings.models.address import Address


class Apartment(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    address = models.ForeignKey(
        Address,
        related_name='apartment',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    price = models.DecimalField(max_digits=7, decimal_places=2)
    rooms = models.SmallIntegerField()
    apartment_type = models.CharField(
        max_length=20,
        choices=ApartmentTypeChoice.choices,
        default=ApartmentTypeChoice.APARTMENT
    )
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'apartments'

    def __str__(self):
        return f'{self.title}'
