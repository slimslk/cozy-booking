class UserService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_user(self, user_data: dict):
        ...

    def get_all_users(self):
        ...
