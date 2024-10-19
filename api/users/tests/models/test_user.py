from django.test import TestCase, tag

from api.users.factories import UserFactory


@tag("models")
class UserTestCase(TestCase):
    def test_create_user_successful(self):
        user = UserFactory(
            first_name="First Name",
            last_name="Last Name",
            email="test@gmail.com",
        )
        self.assertEqual(user.first_name, "First Name")
        self.assertEqual(user.last_name, "Last Name")
        self.assertEqual(user.email, "test@gmail.com")
        self.assertEqual(user.__str__(), "First Name Last Name")

    def test_update_password_user_successful(self):
        user = UserFactory()
        user.password = "new_password"  # nosec
        user.save()
        self.assertTrue(user.check_password("new_password"))
