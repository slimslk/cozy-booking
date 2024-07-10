import re

from rest_framework import serializers

from apps.users.errors.user_detail_errors import UserDetailBadRequest
from apps.users.models import UserDetail


class BaseUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        abstract = True
        fields = '__all__'


class RequestUserDetailDTO(BaseUserDetailSerializer):

    class Meta(BaseUserDetailSerializer.Meta):
        fields = [
            'first_name',
            'last_name',
            'phone',
            'address',
        ]

    def validate(self, attrs):
        #TODO: add phone and address validators
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        self.__validate_name('first_name', first_name)
        self.__validate_name('last_name', last_name)
        return attrs

    def __validate_name(self, name_type: str, name: str):
        if not re.match('^[A-Za-z]+$', name):
            message: str = f'The {name_type} must be alphabet characters.'
            raise UserDetailBadRequest({name_type: message}, message)


class ResponseUserDetailDTO(BaseUserDetailSerializer):

    class Meta(BaseUserDetailSerializer.Meta):
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone',
            'address',
        ]
