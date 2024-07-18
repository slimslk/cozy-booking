from django.db import models

from apps.listings.models import Apartment
from apps.users.models import User


class ListingView(models.Model):
    user = models.ForeignKey(User, related_name='listing_views', on_delete=models.CASCADE, null=True, blank=True)
    listing = models.ForeignKey(Apartment, related_name='listing_views', on_delete=models.CASCADE)

    class Meta:
        db_table = 'views'
