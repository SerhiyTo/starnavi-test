from ninja_extra import api_controller, route, status
from ninja_jwt.controller import TokenObtainPairController
from ninja_jwt.tokens import AccessToken

from api.users.repositories import UserRepository
from api.users.schemas import AuthSchema, TokenSchema
from api.users.services.auth_service import AuthService


@api_controller("/auth", tags=["auth"])
class AuthController(TokenObtainPairController):
    """
    Controller for authentication functionality.

    Attributes:
        - login (method): Obtain a new token.
    """

    @route.post("/login", response={status.HTTP_200_OK: TokenSchema})
    async def login(self, user_data: AuthSchema) -> TokenSchema:
        """
        Obtain a new token.

        :param user_data: data to authenticate a user.
        :return: token.
        """
        auth_service = AuthService(UserRepository)
        user = await auth_service.authenticate_user(
            email=user_data.email,
            password=user_data.password,
        )
        token = AccessToken.for_user(user)
        return TokenSchema(token=str(token))
