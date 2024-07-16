from typing import Any

from django.db.models import Q

from apps.listings.constants.filter_and_order_constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
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
        order: str = kwargs.pop('order', '-created_at')
        location: str | None = kwargs.pop('location', '')
        search = kwargs.pop('search', '')
        page_size = int(kwargs.pop('page_size', DEFAULT_PAGE_SIZE))
        page = (int(kwargs.pop('page', 1)) - 1) * page_size

        if page_size > MAX_PAGE_SIZE:
            page_size = MAX_PAGE_SIZE
        if page < 0:
            raise PageParameterError()

        location_query = Q(address__city__icontains=location) | Q(address__land__icontains=location)
        title_and_description_query = Q(title__icontains=search) | Q(description__icontains=search)

        if location:
            apartments = Apartment.objects.filter(
                title_and_description_query,
                location_query,
                **kwargs
            ).order_by(order)[page:page_size + page]
        else:
            apartments = Apartment.objects.filter(
                title_and_description_query,
                **kwargs
            ).order_by(order)[page:page_size + page]

        if len(apartments) < 2:
            return apartments.first()
        return apartments.all()
