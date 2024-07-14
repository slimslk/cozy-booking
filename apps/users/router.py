from django.urls import path

from apps.users.controllers.user_controller import UserCRUDView, UserListView
from apps.users.controllers.user_detail_controller import UserDetailRetrieveCreateDeleteUpdateView

urlpatterns = [
    path('', UserCRUDView.as_view(), name='users'),
    path('all/', UserListView.as_view()),
    path('user-detail/', UserDetailRetrieveCreateDeleteUpdateView.as_view()),
]
