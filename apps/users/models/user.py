from django.contrib.auth.models import UserManager, AnonymousUser
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from apps.users.choices.user_choices import RoleChoices
from apps.users.models.user_detail import UserDetail


class User(AbstractBaseUser):
    email: str = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted: bool = models.BooleanField(default=False)
    role: str = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        choices=RoleChoices.choices(),
        default=RoleChoices.RENTER,
    )
    user_detail: UserDetail = models.OneToOneField(
        UserDetail,
        null=True,
        related_name='user',
        on_delete=models.CASCADE,
        )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['is_deleted', 'role']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email


class CustomAnonymousUser(AnonymousUser):
    role = RoleChoices.RENTER.name
    is_deleted = False
    email = ""
    user_detail = None
