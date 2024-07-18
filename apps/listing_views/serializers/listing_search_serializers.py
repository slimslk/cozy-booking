from rest_framework import serializers

from apps.listing_views.models import ListingSearch


class ListingSearchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingSearch
        fields = '__all__'


class ListingSearchListSerializer(serializers.Serializer):
    search_field = serializers.CharField(max_length=128)
    search_value = serializers.CharField(max_length=256)
    amount = serializers.IntegerField()
