from django.urls import path

from apps.listing_views.views.listing_search_views import ListingSearchView

urlpatterns = [
    path('', ListingSearchView.as_view()),
]