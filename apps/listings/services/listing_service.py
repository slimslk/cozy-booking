from typing import Any

from rest_framework import serializers

from apps.constants.error_messages import NOT_A_NUMBER, NOT_IN_APARTMENT_CHOICES
from apps.listings.choices.appartment_type_choices import ApartmentTypeChoice
from apps.listings.constants.filter_and_order_constants import (
    FILTER_LIST_AND_PAGINATION,
    ORDER_LIST,
    PRICE_MIN,
    PRICE_MAX,
    CREATED_AT_DESC_RANK,
    ORDER_PARAMETER,
    ROOMS,
    APARTMENT_TYPE,
    PAGE,
    PAGE_SIZE, VALUE_AS_NUMBER_LIST
)
from apps.listings.dto.apartment_dto import ResponseApartmentDTO, RequestApartmentDTO
from apps.listings.errors.listings_errors import ListingDataValidationError
from apps.listings.models import Apartment
from apps.listings.repositories.listing_repository import ListingRepository
from apps.security.errors.security_error import PermissionDeniedError
from apps.users.choices.user_choices import UserChoices
from apps.users.models import User
from apps.utils import content_utils
from apps.utils.content_utils import check_and_update_entity_with_new_data_helper


class ListingService:

    def __init__(self, listing_repository: ListingRepository = ListingRepository()):
        self.__listing_repository = listing_repository

    def get_all_apartments(self, *args, **kwargs) -> list[dict]:
        filters: dict[str, Any] = {}
        order: str = ""
        if kwargs:
            filters = self.__get_filter(kwargs)
            order = self.__get_order(kwargs)
        if not filters:
            filters = self.__get_popular_filters_request()
        if not order:
            order = self.__get_popular_orders_request()

        apartments: list[Apartment] = self.get_apartment_as_model(filters=filters, order=order)
        apartments_response = [ResponseApartmentDTO(apartment).data for apartment in apartments]
        return apartments_response

    def get_all_apartments_by_user_id(self, user_id: int) -> list[dict]:
        apartments: list[Apartment] = self.get_apartment_as_model(user_id=user_id)
        content_utils.check_content_helper(apartments)
        apartments_response = [ResponseApartmentDTO(apartment).data for apartment in apartments]
        return apartments_response

    def create_apartment(self, apartment_data: dict[str, Any], user_id: int):
        apartment_data['user_id'] = user_id
        serializer: RequestApartmentDTO = RequestApartmentDTO(data=apartment_data)
        if serializer.is_valid(raise_exception=True):
            apartment_data: dict = serializer.validated_data
            apartment = self.__listing_repository.creat_apartment(apartment_data)
            return ResponseApartmentDTO(apartment)

    def get_apartments_by_id(self, apartment_id: int) -> ResponseApartmentDTO:
        apartment = self.get_apartment_as_model(apartment_id=apartment_id)
        content_utils.check_content_helper(apartment)
        apartment_response = ResponseApartmentDTO(apartment)
        return apartment_response

    def delete_apartments_by_id(self, user: User, apartment_id: int):
        apartment: Apartment = self.get_apartment_as_model(apartment_id=apartment_id)
        content_utils.check_content_helper(apartment)
        self.__check_has_user_permissions(apartment=apartment, user=user)
        self.__listing_repository.delete_apartment_by_id(apartment_id)

    def update_apartment_by_id(self,
                               apartment_id: int,
                               user: User,
                               updated_data: dict[str, Any]) -> ResponseApartmentDTO:
        apartment: Apartment = self.get_apartment_as_model(apartment_id=apartment_id)
        content_utils.check_content_helper(apartment)
        self.__check_has_user_permissions(apartment=apartment, user=user)

        apartment = self.update_apartment(apartment=apartment, updated_data=updated_data)
        return ResponseApartmentDTO(apartment)

    # +++++++++++++++++++++++++++++++++++++++++++++++++
    def get_apartment_as_model(self, **kwargs) -> Apartment | list[Apartment]:
        apartment_id = kwargs.get('apartment_id')
        user_id = kwargs.get('user_id')
        filters = kwargs.get('filters')
        order = kwargs.get('order')
        if user_id:
            apartment = self.__listing_repository.get_all_apartment_by_user_id(user_id)
        elif apartment_id:
            apartment = self.__listing_repository.get_apartment_by_id(apartment_id)
        else:
            apartment = self.__listing_repository.get_all_apartments(**filters, order=order)
        content_utils.check_content_helper(apartment)
        return apartment

    def update_apartment(self, apartment: Apartment, updated_data: dict[str, Any]) -> Apartment:
        serializer = RequestApartmentDTO(instance=apartment, data=updated_data, partial=True)

        try:
            if serializer.is_valid(raise_exception=True):
                apartment = self.__check_and_update_apartment(
                    apartment=apartment,
                    updated_data=serializer.validated_data
                )

                apartment = self.__listing_repository.update_apartment_by_id(apartment)
                return apartment

        except serializers.ValidationError as err:
            raise ListingDataValidationError(err=err.args[0])

    def __check_has_user_permissions(self, user: User, apartment: Apartment):
        if apartment.user_id != user.id and user.role != UserChoices.ADMIN.name:
            raise PermissionDeniedError()

    def __check_and_update_apartment(self, apartment: Apartment, updated_data: dict[str, Any]) -> Apartment:
        apartment = check_and_update_entity_with_new_data_helper(
            entity=apartment,
            updated_data=updated_data
        )
        return apartment

    def __get_popular_filters_request(self) -> dict[str: Any]:
        return {}

    def __get_popular_orders_request(self) -> dict[str: Any]:
        return CREATED_AT_DESC_RANK[1]

    def __get_filter(self, request_parameters: dict[str, Any]) -> dict[str, Any]:
        listing_filter: dict[str, Any] = {}
        for key, value in request_parameters.items():
            if key in FILTER_LIST_AND_PAGINATION:
                if key in VALUE_AS_NUMBER_LIST:
                    self.__check_is_number(value[0])
                    listing_filter[key] = value[0]
                elif key == APARTMENT_TYPE:
                    self.__check_is_in_apartment_choices(value[0])
                    listing_filter[key] = value[0]
                else:
                    listing_filter[key] = value[0]
        return listing_filter

    def __get_order(self, request_parameters: dict[str, Any]) -> str:
        for key, value in request_parameters.items():
            if key == ORDER_PARAMETER:
                for order in ORDER_LIST:
                    if order[0] == value[0]:
                        return order[1]

    def __check_is_number(self, number: str):
        if not number.replace('.', '', 1).isdigit():
            raise ListingDataValidationError(
                err={"error": NOT_A_NUMBER}
            )

    def __check_is_in_apartment_choices(self, apartment_type: str):
        apartment_choices = [attr[0] for attr in ApartmentTypeChoice.choices()]
        if apartment_type.upper() not in apartment_choices:
            raise ListingDataValidationError(
                err={'err': NOT_IN_APARTMENT_CHOICES}
            )
