from django.contrib.auth.models import UserManager
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from apps.users.choices.user_choices import UserChoices
from apps.users.models.user_detail import UserDetail


class User(AbstractBaseUser):
    email: str = models.EmailField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    is_deleted: bool = models.BooleanField(default=False, null=False)
    role: str = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        choices=UserChoices.choices(),
        default=UserChoices.RENTER,
    )
    user_detail: UserDetail = models.ForeignKey(UserDetail, related_name='user', on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ['email', 'is_deleted', 'role']

    class Meta:
        db_table = 'users'
