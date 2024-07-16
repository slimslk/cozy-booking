from rest_framework import serializers

from apps.listing_views.serializers.listing_views_serializers import ListingViewsCreateSerializer


class ListingViewsService:

    def add_view(self, **kwargs):
        serializer = ListingViewsCreateSerializer(data=kwargs)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.create(serializer.validated_data)
        except serializers.ValidationError as err:
            raise serializers.ValidationError(err.args[0])
