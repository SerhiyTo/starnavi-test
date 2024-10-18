from asgiref.sync import sync_to_async

from api.users.models import User
from api.users.repositories.user_base import UserBaseRepository


class UserRepository(UserBaseRepository):
    """
    User repository class to handle database operations.

    The methods defined here are:
    - create: Create a new user.
    - get_by_email: Get a user by email.
    """

    async def create(self, user: dict) -> User:
        """
        Create a new user in the database.

        :param user: user data.
        :return: created user.
        """
        return await sync_to_async(User.objects.create_user)(**user)

    async def get_by_email(self, email: str) -> User:
        """
        Get a user from the database by email.

        :param email: user email.
        :return: user with the given email.
        """
        return await User.objects.aget(email=email)
