from ninja_extra import api_controller, route, status
from ninja_extra.exceptions import APIException

from api.users.repositories import UserRepository
from api.users.schemas import UserCreateSchema, UserResponseSchema


@api_controller("/users", tags=["users"])
class UserController:
    """
    Controller for user functionality.

    Attributes:
        - register (method): Register a new user.
    """

    @route.post("/register", response={status.HTTP_201_CREATED: UserResponseSchema})
    async def register(self, user_data: UserCreateSchema) -> UserResponseSchema:
        """
        Register a new user.

        :param user_data: data to create a new user.
        :return: created user.
        """
        try:
            user_repository = UserRepository()
            created_user = await user_repository.create(user_data.dict())
            return UserResponseSchema.from_orm(created_user)
        except Exception as err:
            raise APIException(detail=str(err))
