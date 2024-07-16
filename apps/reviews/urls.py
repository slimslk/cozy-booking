from django.urls import path

from apps.reviews.views.review_views import ReviewListView, ReviewDeleteView

urlpatterns = [
    path('', ReviewListView.as_view()),
    path('<int:pk>/', ReviewDeleteView.as_view()),
]