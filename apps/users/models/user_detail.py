from django.db import models


class UserDetail(models.Model):
    first_name: str = models.CharField(max_length=30, null=True, blank=True)
    last_name: str = models.CharField(max_length=60, null=True, blank=True)
    phone: str = models.CharField(max_length=17, null=True, blank=True, unique=True)
    address: str = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'users_detail'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
