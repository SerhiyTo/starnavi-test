from django.test import TestCase

from api.users.schemas import TokenSchema


class TokenTest(TestCase):
    def test_token_success_validated(self):
        schema = TokenSchema(token="token")  # nosec
        self.assertEqual(schema.token, "token")
