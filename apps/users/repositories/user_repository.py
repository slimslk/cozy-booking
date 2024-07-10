from typing import Any

from apps.users.models import User


class UserRepository:

    def get_all_users(self) -> list[User]:
        users: list[User] = self.__get_users()
        return User.objects.all()

    def create_user(self, user_data: Any) -> User:
        user: User = User(**user_data)
        user.set_password(user_data.get('password'))
        user.save()
        return user

    def get_user_by_id(self, user_id: int) -> User | None:
        user: User = self.__get_users(pk=user_id)
        return user

    def __get_users(self, *args, **kwargs) -> list[User] | User:
        categories = User.objects.filter(**kwargs)
        if len(categories) < 2:
            return categories.first()
        return categories
