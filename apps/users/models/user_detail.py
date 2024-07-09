from django.db import models


class UserDetail(models.Model):
    first_name: str = models.CharField(max_length=30)
    last_name: str = models.CharField(max_length=60)
    phone: str = models.CharField(max_length=17, null=False, blank=False, unique=True)
    address: str = models.CharField(max_length=255)

    class Meta:
        db_table = 'users_detail'
