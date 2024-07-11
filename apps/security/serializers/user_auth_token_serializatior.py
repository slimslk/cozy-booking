from typing import Dict, Any

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.security.errors.security_error import UserNotFoundError
from apps.users.models import User


class UserObtainPairTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        user: User = self.user

        if user.is_deleted:
            raise UserNotFoundError()

        return data
