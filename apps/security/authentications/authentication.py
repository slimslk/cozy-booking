from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import Token

from apps.security.models.token_blacklist import Blacklist
from apps.users.models import User


class CustomJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token: Token) -> AuthUser:
        return User()

    def get_validated_token(self, raw_token: bytes) -> Token:
        decoded_raw_token = raw_token.decode()
        blacklisted_token = Blacklist.objects.filter(Q(refresh_token=decoded_raw_token) | Q(access_token=decoded_raw_token)).all()
        if blacklisted_token:
            raise InvalidToken('Token is blacklisted')
        return super().get_validated_token(raw_token)
