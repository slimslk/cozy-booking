from rest_framework import serializers

from apps.users.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        abstract = True
        fields = '__all__'


class RequestUserDTO(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            'email',
            'password',
            're_password',
        ]


class ResponseUserDTO(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            'id',
            'email',
        ]