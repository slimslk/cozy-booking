from typing import Any

from apps.users.models import User


class UserRepository:

    def get_all_users(self) -> list[User]:
        users: list[User] | User = self.__get_users()
        if type(users) is User:
            return [users]

        return users

    def create_user(self, user_data: dict[str, Any]) -> User:
        user: User = User(**user_data)
        user.set_password(user_data.get('password'))
        user.save()
        return user

    def get_user_by_id(self, user_id: int) -> User | None:
        user: User = self.__get_users(pk=user_id)
        return user

    def update_user(self, user: User) -> User:
        user.save()
        return user

    def __get_users(self, *args, **kwargs) -> list[User] | User:
        categories = User.objects.filter(is_deleted=False, **kwargs)
        if len(categories) < 2:
            return categories.first()
        return categories.all()
