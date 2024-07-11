from django.urls import path

from apps.users.controllers.user_controller import UserListView, UserRetrieveSoftDeleteUpdate, UserCreateView
from apps.users.controllers.user_detail_controller import UserDetailRetrieveCreateDeleteUpdateView

urlpatterns = [
    path('', UserListView.as_view()),
    path('singup/', UserCreateView.as_view()),
    path('user/', UserRetrieveSoftDeleteUpdate.as_view()),
    path('user-detail/', UserDetailRetrieveCreateDeleteUpdateView.as_view()),
]
