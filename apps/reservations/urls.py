from django.urls import path, include

from apps.reservations.views.reservation_views import (
    ReservationListCreateView,
    ReservationUpdateRetrieveDeleteView,
)

urlpatterns = [
    path('', ReservationListCreateView.as_view()),
    # path('lessor/', ReservationListByLessorView.as_view()),
    path('<int:pk>/', ReservationUpdateRetrieveDeleteView.as_view()),
    path('<int:pk>/', include('apps.reviews.for_booking_urls')),
]
