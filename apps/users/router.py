from django.urls import path

from apps.users.controllers.user_controller import UserListCreateView, UserRetrieveDeleteUpdate
from apps.users.controllers.user_detail_controller import UserDetailRetrieveCreateDeleteUpdateView

urlpatterns = [
    path('', UserListCreateView.as_view()),
    # path('<int:user_id>/', UserRetrieveDeleteUpdate.as_view()),
    path('user-detail/', UserDetailRetrieveCreateDeleteUpdateView.as_view()),
]
