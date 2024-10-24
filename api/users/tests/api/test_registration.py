from asgiref.sync import sync_to_async
from django.test import TestCase, tag
from ninja_extra.testing import TestAsyncClient

from api.users.api import UserController
from api.users.factories import UserFactory


@tag("api")
class UserControllerTestCase(TestCase):
    async def test_register(self):
        client = TestAsyncClient(UserController)
        response = await client.post(
            path="/register",
            json={
                "email": "test@gmail.com",
                "password": "password",  # nosec
                "first_name": "first_name",
                "last_name": "last_name",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["email"], "test@gmail.com")
        self.assertEqual(response.json()["first_name"], "first_name")
        self.assertEqual(response.json()["last_name"], "last_name")
        self.assertTrue("id" in response.json())

    async def test_register_unsuccessful(self):
        user = await sync_to_async(UserFactory)()
        client = TestAsyncClient(UserController)
        response = await client.post(
            path="/register",
            json={
                "email": user.email,
                "password": user.password,  # nosec
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        )
        self.assertEqual(response.status_code, 500)
