from django.test import TestCase

from api.users.schemas import AuthSchema


class AuthSchemaTest(TestCase):
    def test_auth_schema(self):
        schema = AuthSchema(
            email="test@gmail.com",
            password="123456",  # nosec
        )
        self.assertEqual(schema.email, "test@gmail.com")
        self.assertEqual(schema.password, "123456")
