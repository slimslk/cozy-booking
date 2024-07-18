from django.db.models import Count
from rest_framework import serializers

from apps.listing_views.models import ListingSearch
from apps.listing_views.serializers.listing_search_serializers import ListingSearchCreateSerializer


class ListingSearchService:

    def add_listing_search(self, *args, **kwargs):

        for search_field, search_value in kwargs.items():
            search_data = {
                'search_field': search_field,
                'search_value': search_value,
            }
            serializer = ListingSearchCreateSerializer(data=search_data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.create(serializer.validated_data)
            except serializers.ValidationError as err:
                raise serializers.ValidationError(err.args[0])

    def get_popular_listing_searches(self):
        popular_searches = (ListingSearch.objects.values('search_field', 'search_value')
                            .annotate(amount=Count('search_field'))
                            .order_by('-amount')
                            .values('amount', 'search_field', 'search_value'))
        return popular_searches
