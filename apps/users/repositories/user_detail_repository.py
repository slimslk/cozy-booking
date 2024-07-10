from typing import Any

from apps.users.models import UserDetail


class UserDetailRepository:

    def create_user_detail(self, user_detail_data: Any):
        pass

    def get_user_details_by_user_id(self, user_id: int) -> UserDetail:
        user_detail: UserDetail = UserDetail.objects.filter(user_id == user_id).first()
        return user_detail
