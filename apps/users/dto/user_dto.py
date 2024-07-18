from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError

from apps.users.choices.user_choices import RoleChoices
from apps.users.dto.user_detail_dto import ResponseUserDetailDTO
from apps.users.errors.user_errors import MismatchedPasswords, IncorrectPasswordError, AdminRoleValidationError
from apps.users.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        abstract = True
        fields = '__all__'


class RequestUserDTO(BaseUserSerializer):
    re_password = serializers.CharField(max_length=128, write_only=True)
    class Meta(BaseUserSerializer.Meta):
        fields = [
            'email',
            'is_deleted',
            'role',
            'password',
            're_password',
        ]

    def validate(self, attrs):
        password = attrs.get('password')
        re_password = attrs.get('re_password')
        role = attrs.get('role')

        if not self.partial:
            self.__validate_password(attrs)
        else:
            if password and re_password:
                self.__validate_password(attrs)

        if password and re_password:
            if password != re_password:
                raise MismatchedPasswords

            try:
                validate_password(password)
            except ValidationError as err:
                raise IncorrectPasswordError(err.messages)
        if role == RoleChoices.ADMIN.name:
            raise AdminRoleValidationError()

        return attrs

    def __validate_password(self, attrs: dict[str, str]):
        password = attrs.get('password')
        re_password = attrs.get('re_password')

        if password != re_password:
            raise MismatchedPasswords
        try:
            validate_password(password)
        except ValidationError as err:
            raise IncorrectPasswordError(err.messages)


class ResponseUserDTO(BaseUserSerializer):
    user_detail = ResponseUserDetailDTO(required=False, read_only=True)
    class Meta(BaseUserSerializer.Meta):
        fields = [
            'id',
            'email',
            'role',
            'user_detail'
        ]
