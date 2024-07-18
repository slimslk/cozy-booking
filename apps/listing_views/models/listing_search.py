from django.db import models


class ListingSearch(models.Model):
    search_field = models.CharField(max_length=128)
    search_value = models.CharField(max_length=256)

    class Meta:
        db_table = 'listing_searches'
