from django.urls import path, include

from apps.listings.controller.listing_controller import ApartmentListByUserIdView

app_name = 'API/V1'

urlpatterns = [
    path('users/', include('apps.users.urls'), name='API/V1'),
    path('listings/', include('apps.listings.urls')),
    path('bookings/', include('apps.reservations.urls')),
    path('users/listings/', ApartmentListByUserIdView.as_view()),  # TODO: Refactor this?
    path('reviews/', include('apps.reviews.urls')),
    path('searches/', include('apps.listing_views.urls')),
]
