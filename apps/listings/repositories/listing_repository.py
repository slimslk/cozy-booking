from typing import Any

from django.db.models import Q, Count

from apps.listings.constants.filter_and_order_constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE, FOREIGN_ORDER_LIST, \
    VIEWS_DESC_RANK, ORDER_PARAMETER, PAGE, PAGE_SIZE, LOCATION, SEARCH
from apps.listings.errors.listings_errors import PageParameterError
from apps.listings.models.apartment import Apartment


class ListingRepository:

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
        order: str = kwargs.pop(ORDER_PARAMETER, VIEWS_DESC_RANK[1])
        page_size = int(kwargs.pop(PAGE_SIZE, DEFAULT_PAGE_SIZE))
        page = (int(kwargs.pop(PAGE, 1)) - 1) * page_size

        instance = Apartment.objects
        instance = self.__add_filters_to_query(instance,  **kwargs)
        instance = self.__add_sorting_to_query(instance, order=order)
        instance = self.__add_pagination_to_query(instance, page_size=page_size, page=page)

        if len(instance) < 2:
            return instance.first()
        return instance.all()

    def __add_filters_to_query(self, instance, *args, **kwargs):
        location = kwargs.pop(LOCATION, '')
        search = kwargs.pop(SEARCH, '')

        location_query = Q(address__city__icontains=location) | Q(address__land__icontains=location)
        title_and_description_query = Q(title__icontains=search) | Q(description__icontains=search)

        if location:
            apartments = instance.filter(
                title_and_description_query,
                location_query,
                **kwargs
            )
        else:
            apartments = instance.filter(
                title_and_description_query,
                **kwargs
            )
        return apartments

    def __add_sorting_to_query(self, instance, *args, **kwargs):
        order: str = kwargs.pop('order', VIEWS_DESC_RANK[1])

        if order in FOREIGN_ORDER_LIST:
            if order.startswith('-'):
                count_column = '-count'
            else:
                count_column = 'count'
            return instance.annotate(
                count=Count(order.replace('-', ''))
            ).order_by(count_column)

        apartments = instance.order_by(order)
        return apartments

    def __add_pagination_to_query(self, instance, *args, **kwargs):
        page_size = kwargs.pop(PAGE_SIZE, DEFAULT_PAGE_SIZE)
        page = kwargs.pop(PAGE, 1)

        if page_size > MAX_PAGE_SIZE:
            page_size = MAX_PAGE_SIZE
        if page < 0:
            raise PageParameterError()

        return instance[page:page_size + page]
