from asgiref.sync import sync_to_async
from ninja_extra import status
from ninja_extra.exceptions import APIException

from api.users.models import User


class AuthService:
    """
    AuthService class to handle user authentication.

    The methods defined here are:
    - authenticate_user: Authenticate a user by email or phone number and password.
    """

    def __init__(self, repository: "UserBaseRepository" = None):
        self.repository = repository()

    async def authenticate_user(self, email: str, password: str) -> User:
        """
        Authenticate a user by email and password.

        :param email: user email.
        :param password: user password.
        :return: user object.
        """
        try:
            user = await self.repository.get_by_email(email)
        except User.DoesNotExist:
            exception = APIException(detail="User not found")
            exception.status_code = status.HTTP_404_NOT_FOUND
            raise exception

        if not await sync_to_async(user.check_password)(password):
            exception = APIException(detail="Invalid credentials")
            exception.status_code = status.HTTP_404_NOT_FOUND
            raise exception

        return user
