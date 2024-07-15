from django.urls import path

from apps.reservations.views.reservation_views import (
    ReservationListCreateView,
    ReservationUpdateRetrieveDeleteView
)

urlpatterns = [
    path('', ReservationListCreateView.as_view()),
    path('<int:pk>/', ReservationUpdateRetrieveDeleteView.as_view())
]
