from rest_framework import serializers

from apps.listing_views.models.listing_views import ListingView


class ListingViewsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ListingView
        fields = '__all__'
