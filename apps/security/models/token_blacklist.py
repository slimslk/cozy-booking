from django.db import models


class Blacklist(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()

    class Meta:
        db_table = 'blacklist'
