from rest_framework import serializers

from apps.listings.choices.address_choices import LandChoice
from apps.listings.models import Address


class BaseAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        abstract = True
        fields = '__all__'

class AddressSerializer(serializers.Serializer):
    land = serializers.ChoiceField(choices=LandChoice.choices())
    city = serializers.CharField(max_length=50)
    street = serializers.CharField(max_length=100)
    house_number = serializers.CharField(max_length=10)
    postal_code = serializers.IntegerField(min_value=10000, max_value=99999)


class RequestAddressDTO(BaseAddressSerializer):
    class Meta(BaseAddressSerializer.Meta):
        fields = '__all__'


class ResponseAddressDTO(BaseAddressSerializer):
    class Meta(BaseAddressSerializer.Meta):
        fields = [
            'id',
            'land',
            'city',
            'street',
            'house_number',
            'postal_code'
        ]
