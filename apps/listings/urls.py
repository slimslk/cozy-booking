from django.urls import path, include

from apps.listings.controller.address_controller import ApartmentCRUDView
from apps.listings.controller.listing_controller import (
    ApartmentListCreateView,
    ApartmentRetrieveUpdateDelete,
)
from apps.listings.controller.reservetion_controller import ReservationController

app_name = 'Listings'

urlpatterns = [
    path('', ApartmentListCreateView.as_view(), name='Somethings'),
    path('bookings/', ReservationController.as_view()),
    path('<int:apartment_id>/', ApartmentRetrieveUpdateDelete.as_view()),
    path('<int:apartment_id>/address/', ApartmentCRUDView.as_view()),
    path('<int:pk>/', include('apps.reviews.for_listing_urls')),
]
