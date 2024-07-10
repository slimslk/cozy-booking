from apps.users.dto.user_dto import RequestUserDTO, ResponseUserDTO
from apps.users.errors.common_errors import NoContentFoundError
from apps.users.models import User
from apps.users.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository: UserRepository = user_repository

    def create_user(self, user_data: dict) -> ResponseUserDTO:
        serializer: RequestUserDTO = RequestUserDTO(data=user_data)
        if serializer.is_valid(raise_exception=True):
            user_data: dict = serializer.validated_data
            user_data.pop('re_password')
            user = self.__user_repository.create_user(user_data)
            return ResponseUserDTO(user)

    def get_all_users(self) -> list[dict]:
        users: list[User] = self.__user_repository.get_all_users()
        self.__check_content(users)
        response_users = [ResponseUserDTO(user).data for user in users]
        return response_users

    def get_user_by_id(self, user_id: int) -> ResponseUserDTO:
        user: User = self.__user_repository.get_user_by_id(user_id)
        self.__check_content(user)
        response_user = ResponseUserDTO(user)
        return response_user

    def update_user_by_id(self, user_id: int, updated_data: dict) -> ResponseUserDTO:
        ...

    def soft_delete_user_by_id(self, user_id: int):
        updated_data = {'deleted_at': True}
        self.update_user_by_id(user_id, updated_data)


    def __check_content(self, content):
        if not content:
            raise NoContentFoundError()

