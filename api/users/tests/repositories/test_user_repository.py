from asgiref.sync import sync_to_async
from django.test import TestCase, tag

from api.users.factories import UserFactory
from api.users.models import User
from api.users.repositories import UserRepository


@tag("repositories")
class UserRepositoryTestCase(TestCase):
    async def test_create_user_success(self):
        user_data = {
            "email": "test@gmail.com",
            "password": "password",  # nosec
        }
        user_repository = UserRepository()
        user = await user_repository.create(user=user_data)
        self.assertEqual(user.email, user_data["email"])

    async def test_create_user_unsuccessful(self):
        user_data = {
            "email": None,
            "password": "password",  # nosec
        }
        user_repository = UserRepository()
        with self.assertRaises(ValueError) as context:
            await user_repository.create(user=user_data)
        self.assertEqual(str(context.exception), "The Email must be set")

    async def test_get_user_by_email_success(self):
        user = await sync_to_async(UserFactory)(email="test@gmail.com")
        user_repository = UserRepository()
        found_user = await user_repository.get_by_email(email=user.email)
        self.assertEqual(user, found_user)

    async def test_get_user_by_email_unsuccessful(self):
        user_repository = UserRepository()
        with self.assertRaises(User.DoesNotExist) as context:
            await user_repository.get_by_email(email="")
        self.assertEqual(str(context.exception), "User matching query does not exist.")
