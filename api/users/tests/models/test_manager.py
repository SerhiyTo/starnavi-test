from django.test import TestCase, tag

from api.users.models import User


@tag("models")
class UserManagerTestCase(TestCase):
    def test_create_user_successful(self):
        user = User.objects.create_user(
            email="test@gmail.com",
            password="password",  # nosec
        )
        self.assertEqual(user.email, "test@gmail.com")
        self.assertTrue(user.check_password("password"))

    def test_create_user_unsuccessful(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(
                email=None,
                password="password",  # nosec
            )
        self.assertEqual(str(context.exception), "The Email must be set")


@tag("models")
class SuperUserManager(TestCase):
    def test_create_superuser_successful(self):
        user = User.objects.create_superuser(
            email="test@gmail.com",
            password="password",  # nosec
            is_superuser=True,
            is_staff=True,
        )
        self.assertEqual(user.email, "test@gmail.com")
        self.assertTrue(user.check_password("password"))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_superuser_fail_is_staff(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(
                email="test@gmail.com",
                password="password",  # nosec
                is_staff=False,
            )
        self.assertEqual(str(context.exception), "Superuser must have is_staff=True.")

    def test_create_superuser_fail_is_superuser(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(
                email="test@gmail.com",
                password="password",  # nosec
                is_superuser=False,
            )
        self.assertEqual(str(context.exception), "Superuser must have is_superuser=True.")
