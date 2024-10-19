from asgiref.sync import sync_to_async
from django.test import TestCase
from ninja_extra.testing import TestAsyncClient

from api.users.api import AuthController
from api.users.factories import UserFactory


class TestAuthController(TestCase):
    async def test_login_success(self):
        await sync_to_async(UserFactory)(
            email="test@gmail.com",
            password="password",  # nosec
        )
        client = TestAsyncClient(AuthController)
        response = await client.post(
            path="/login",
            json={
                "email": "test@gmail.com",
                "password": "password",  # nosec
            },
        )
        self.assertEqual(response.status_code, 200)

    async def test_login_unsuccessful(self):
        client = TestAsyncClient(AuthController)
        response = await client.post(
            path="/login",
            json={
                "email": "test@gmail.com",
                "password": "password",  # nosec
            },
        )
        self.assertEqual(response.status_code, 404)
