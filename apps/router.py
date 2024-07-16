from django.urls import path, include

from apps.listings.controller.listing_controller import ApartmentListByUserIdView

urlpatterns = [
    path('users/', include('apps.users.router')),
    path('listings/', include('apps.listings.router')),
    path('bookings/', include('apps.reservations.urls')),
    path('users/listings/', ApartmentListByUserIdView.as_view()),  # TODO: Refactor this?
    path('reviews/', include('apps.reviews.urls')),
]
