from typing import Any

from apps.users.models import UserDetail


class UserDetailRepository:

    def create_user_detail(self, user_detail_data: Any):
        user_detail: UserDetail = UserDetail(**user_detail_data)
        user_detail.save()
        return user_detail

    def get_user_details_by_user_id(self, user_id: int) -> UserDetail:
        user_detail: UserDetail = UserDetail.objects.filter(user__id=user_id).first()
        return user_detail

    def update_user_detail(self, user_detail: UserDetail) -> UserDetail:
        user_detail.save()
        return user_detail
