from rest_framework.generics import ListAPIView

from apps.listing_views.serializers.listing_search_serializers import ListingSearchListSerializer
from apps.listing_views.services.listing_search_services import ListingSearchService
from apps.security.permissions.user_permission import IsAdmin


class ListingSearchView(ListAPIView):
    listing_search_service = ListingSearchService()
    serializer_class = ListingSearchListSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return self.listing_search_service.get_popular_listing_searches()
