from asgiref.sync import sync_to_async
from django.test import TestCase, tag
from ninja_extra.exceptions import APIException

from api.users.factories import UserFactory
from api.users.repositories import UserRepository
from api.users.services.auth_service import AuthService


@tag("services")
class AuthServiceTestCase(TestCase):
    async def test_authenticate_user_with_email_success(self):
        user = await sync_to_async(UserFactory)(
            email="test@gmail.com",
            password="password",  # nosec
        )
        auth_service = AuthService(UserRepository)
        authenticated_user = await auth_service.authenticate_user(
            email="test@gmail.com",
            password="password",  # nosec
        )
        self.assertEqual(authenticated_user, user)

    async def test_authenticate_user_user_not_found(self):
        auth_service = AuthService(UserRepository)
        with self.assertRaises(APIException) as context:
            await auth_service.authenticate_user(
                email="test@gmail.com",
                password="password",  # nosec
            )
        self.assertEqual(str(context.exception), "User not found")

    async def test_authenticate_user_invalid_credentials(self):
        await sync_to_async(UserFactory)(
            email="test@gmail.com",
            password="password",  # nosec
        )
        auth_service = AuthService(UserRepository)
        with self.assertRaises(APIException) as context:
            await auth_service.authenticate_user(
                email="test@gmail.com",
                password="wrong_password",  # nosec
            )
        self.assertEqual(str(context.exception), "Invalid credentials")
