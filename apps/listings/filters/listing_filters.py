from typing import Any

from django.db.models import Q, Count, Manager

from apps.listings.constants.filter_and_order_constants import LOCATION, SEARCH, POPULAR, FOREIGN_ORDER_LIST, PAGE_SIZE, \
    DEFAULT_PAGE_SIZE, PAGE, MAX_PAGE_SIZE
from apps.listings.errors.listings_errors import PageParameterError
from apps.listings.models import Apartment


class ListingFilter:

    def add_filters_to_query(self, instance, *args, **kwargs):
        location = kwargs.pop(LOCATION, '')
        search = kwargs.pop(SEARCH, '')
        popular = kwargs.pop(POPULAR, [])

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

        if popular:
            apartments = self.get_popular_search_apartments(apartments, popular)

        return apartments

    def add_sorting_to_query(self, instance, order):

        if order:
            if order in FOREIGN_ORDER_LIST:
                if order.startswith('-'):
                    count_column = '-count'
                else:
                    count_column = 'count'
                return instance.annotate(
                    count=Count(order.replace('-', ''))
                ).order_by(count_column)
            return instance.order_by(order)

        return instance

    def get_popular_search_apartments(self, instance: Any, filters: list):
        query_sets = []
        init_filter = filters.pop(0)
        init_queryset = self.create_queryset(instance, init_filter)
        for popular_filter in filters:
            new_instance = Apartment.objects
            query_set = self.create_queryset(new_instance, popular_filter)
            query_sets.append(query_set)
        query_sets.append(Apartment.objects.all())
        return init_queryset.union(*query_sets)

    def create_queryset(self, instance, popular_filter):
        if LOCATION in popular_filter.keys():
            location = popular_filter.get(LOCATION)
            return instance.filter(
                (Q(address__city__icontains=popular_filter.get(LOCATION))
                 | Q(address__land__icontains=location))
            )
        if SEARCH in popular_filter.keys():
            search = popular_filter.get(SEARCH)
            return instance.filter(Q(title__icontains=search) | Q(description__icontains=search))
        return instance.filter(**popular_filter)

    def add_sorting_by_popular(self, instance, *args, **kwargs):
        pass

    def add_pagination_to_query(self, instance, *args, **kwargs):
        page_size = kwargs.pop(PAGE_SIZE, DEFAULT_PAGE_SIZE)
        page = kwargs.pop(PAGE, 1)

        if page_size > MAX_PAGE_SIZE:
            page_size = MAX_PAGE_SIZE
        if page < 0:
            raise PageParameterError()

        return instance[page:page_size + page]