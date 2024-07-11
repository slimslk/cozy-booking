from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('apps.router')),
    path('', include('apps.security.router')),
    path('admin/', admin.site.urls),
]
