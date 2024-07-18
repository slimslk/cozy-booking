from typing import Any

from apps.listings.constants.filter_and_order_constants import (
    DEFAULT_PAGE_SIZE,
    ORDER_PARAMETER,
    PAGE,
    PAGE_SIZE,
)
from apps.listings.filters.listing_filters import ListingFilter
from apps.listings.models.apartment import Apartment


class ListingRepository:

    LISTING_FILTER = ListingFilter()

    def get_all_apartments(self, **kwargs) -> list[Apartment]:
        apartments = self.__get_apartments(is_active=True, **kwargs)
        if type(apartments) is Apartment:
            return [apartments]

        return apartments

    def get_apartment_by_id(self, apartment_id) -> Apartment:
        return self.__get_apartments(pk=apartment_id)

    def get_all_apartment_by_user_id(self, user_id: int) -> list[Apartment]:
        apartments = self.__get_apartments(user_id=user_id)
        if type(apartments) is Apartment:
            return [apartments]

        return apartments

    def creat_apartment(self, apartment_data: dict[str, Any]) -> Apartment:
        apartment: Apartment = Apartment(**apartment_data)
        apartment.save()
        return apartment

    def delete_apartment_by_id(self, apartment_id: int):
        Apartment.objects.filter(pk=apartment_id).delete()

    def update_apartment_by_id(self, apartment: Apartment) -> Apartment:
        apartment.save()
        return apartment

    def __get_apartments(self, *args, **kwargs) -> list[Apartment] | Apartment:
        order: str | list[dict[str, str]] = ''
        if ORDER_PARAMETER in kwargs.keys():
            order = kwargs.pop(ORDER_PARAMETER)
        page_size = int(kwargs.pop(PAGE_SIZE, DEFAULT_PAGE_SIZE))
        page = (int(kwargs.pop(PAGE, 1)) - 1) * page_size

        instance = Apartment.objects
        instance = self.LISTING_FILTER.add_filters_to_query(instance, **kwargs)

        instance = self.LISTING_FILTER.add_sorting_to_query(instance, order=order)
        instance = self.LISTING_FILTER.add_pagination_to_query(instance, page_size=page_size, page=page)

        if len(instance) < 2:
            return instance[0] if instance else None
        return instance
