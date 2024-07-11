from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.security.controller.auth_controller import CustomTokenObtainPairView, UserLogoutView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('logout/', UserLogoutView.as_view()),
]
