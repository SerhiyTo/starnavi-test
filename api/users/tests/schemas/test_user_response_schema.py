from django.test import TestCase

from api.users.factories import UserFactory
from api.users.schemas import UserResponseSchema


class UserSchemaTest(TestCase):
    def test_user_schema(self):
        user = UserFactory()
        user_schema = UserResponseSchema.from_orm(user)
        user_data = user_schema.dict()
        self.assertEqual(user_data["id"], user.id)
        self.assertEqual(user_data["first_name"], user.first_name)
        self.assertEqual(user_data["last_name"], user.last_name)
        self.assertEqual(user_data["email"], user.email)
