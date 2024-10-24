from django.test import TestCase

from api.users.factories import UserFactory
from api.users.schemas import UserCreateSchema


class UserCreateSchemaTest(TestCase):
    """
    Test the UserCreateSchema schema class.
    """

    def test_user_create_schema(self):
        """
        Test the UserCreateSchema schema class.
        """
        user = UserFactory()
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
        }
        user_create_schema = UserCreateSchema(**user_data)
        self.assertEqual(user_create_schema.first_name, user.first_name)
        self.assertEqual(user_create_schema.last_name, user.last_name)
        self.assertEqual(user_create_schema.email, user.email)
        self.assertEqual(user_create_schema.password, user.password)
