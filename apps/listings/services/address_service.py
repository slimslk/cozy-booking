from typing import Any

from django.db import transaction

from rest_framework import serializers

from apps.listings.dto.address_dto import ResponseAddressDTO, RequestAddressDTO, AddressSerializer
from apps.listings.errors.listings_errors import ListingDataValidationError
from apps.listings.models import Apartment, Address
from apps.listings.repositories.address_repository import AddressRepository
from apps.listings.services.listing_service import ListingService
from apps.utils import content_utils
from apps.utils.content_utils import check_and_update_entity_with_new_data_helper


class AddressService:

    def __init__(
            self,
            listing_service: ListingService = ListingService(),
            address_repository: AddressRepository = AddressRepository()
    ):
        self.__listing_service = listing_service
        self.__address_repository = address_repository

    def get_address(self, apartment_id: int) -> ResponseAddressDTO:
        address: Address = self.__listing_service.get_apartments_by_id(apartment_id).data.get('address')
        content_utils.check_content_helper(address)
        return ResponseAddressDTO(address)

    def create_address(self, address_data: dict[str, Any],  apartment_id: int) -> ResponseAddressDTO:
        apartment: Apartment = self.__listing_service.get_apartment_as_model(apartment_id=apartment_id)
        serializer = AddressSerializer(data=address_data)

        try:
            if serializer.is_valid(raise_exception=True):
                with transaction.atomic():
                    address: Address = self.get_or_create_address(serializer.validated_data)
                    updated_apartment_data = {'address': address.id}
                    self.__listing_service.update_apartment(apartment=apartment, updated_data=updated_apartment_data)
                return ResponseAddressDTO(address)

        except serializers.ValidationError as err:
            raise ListingDataValidationError(err.args[0])

    def update_address(self, apartment_id: int, address_data: dict[str, Any]) -> ResponseAddressDTO:
        address: Address = self.__listing_service.get_apartments_by_id(apartment_id).data.get('address')
        content_utils.check_content_helper(address)
        serializer = RequestAddressDTO(instance=address, data=address_data, partial=True)

        try:
            if serializer.is_valid(raise_exception=True):
                address = self.__check_and_update_address(
                    address=address,
                    updated_data=serializer.validated_data
                )

                address = self.__address_repository.update_address(address)
                return ResponseAddressDTO(address)

        except serializers.ValidationError as err:
            raise ListingDataValidationError(err=err.args[0])

    def delete_address(self, apartment_id: int):
        address: Address = self.__listing_service.get_apartments_by_id(apartment_id).data.get('address')
        content_utils.check_content_helper(address)
        self.__address_repository.delete_address_by_id(address.id)

    def get_or_create_address(self, address_data: dict[str, Any]) -> Address:
        address: Address = self.__address_repository.get_address(**address_data)
        if not address:
            address: Address = self.__address_repository.create_address(address_data)

        return address

    def __check_and_update_address(self, address: Address, updated_data: dict[str, Any]) -> Address:
        address = check_and_update_entity_with_new_data_helper(
            entity=address,
            updated_data=updated_data
        )
        return address
