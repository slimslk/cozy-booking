from django.urls import path

from apps.reviews.views.review_views import ReviewCreateView, ReviewListForListing

urlpatterns = [
    path('reviews/', ReviewListForListing.as_view())
]