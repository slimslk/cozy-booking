from rest_framework.serializers import ModelSerializer, ReadOnlyField

from apps.listings.dto.address_dto import ResponseAddressDTO, RequestAddressDTO
from apps.listings.models.apartment import Apartment


class BaseApartmentSerializer(ModelSerializer):

    class Meta:
        model = Apartment
        abstract = True
        fields = '__all__'


class RequestApartmentDTO(BaseApartmentSerializer):

    # address = RequestAddressDTO(write_only=True, required=False)

    class Meta(BaseApartmentSerializer.Meta):
        fields = '__all__'


class ResponseApartmentDTO(BaseApartmentSerializer):

    address = ResponseAddressDTO(read_only=True, required=False)
    rating = ReadOnlyField()
    views = ReadOnlyField()

    class Meta(BaseApartmentSerializer.Meta):
        fields = '__all__'
        # fields = [
        #     'id',
        #     'title',
        #     'description',
        #     'address',
        # ]
