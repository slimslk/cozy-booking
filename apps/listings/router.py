from django.urls import path

from apps.listings.controller.address_controller import ApartmentCRUDView
from apps.listings.controller.listing_controller import (
    ApartmentListCreateView,
    ApartmentRetrieveUpdateDelete,
)
from apps.listings.controller.reservetion_controller import ReservationController

urlpatterns = [
    path('', ApartmentListCreateView.as_view()),
    path('reservations/', ReservationController.as_view()),
    path('<int:apartment_id>/', ApartmentRetrieveUpdateDelete.as_view()),
    path('<int:apartment_id>/address/', ApartmentCRUDView.as_view()),
]
