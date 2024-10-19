import factory

from api.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """
    User factory for creating users with common fields.
    """

    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")
    is_staff = False
    is_superuser = False
    is_active = True
