from abc import ABC, abstractmethod

from api.users.models import User


class UserBaseRepository(ABC):
    """
    UserBaseRepository is an abstract class that defines the methods that must be implemented by the UserRepository class.

    The methods defined here are:
    - create: creates a new user in the database.
    - get_by_email: retrieves a user from the database by email.
    """

    @abstractmethod
    async def create(self, user: dict) -> User:
        """
        Create a new user in the database.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        """
        Get a user from the database by email.
        """
        raise NotImplementedError
