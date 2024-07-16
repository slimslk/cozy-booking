from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.listings.models import Apartment
from apps.users.models import User


class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    listing = models.ForeignKey(Apartment,  related_name='reviews', on_delete=models.CASCADE)
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reservation_id = models.IntegerField()

    class Meta:
        db_table = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'listing', 'reservation_id'],
                name='unique user_listing_reservation'
            )
        ]
