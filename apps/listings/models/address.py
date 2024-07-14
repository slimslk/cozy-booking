from django.db import models

from apps.listings.choices.address_choices import LandChoice


class Address(models.Model):

    land = models.CharField(max_length=50, choices=LandChoice.choices())
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    postal_code = models.PositiveIntegerField()

    class Meta:
        db_table = 'addresses'
        unique_together = ['land', 'city', 'street', 'house_number', 'postal_code']
