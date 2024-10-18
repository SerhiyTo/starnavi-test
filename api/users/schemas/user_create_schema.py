from ninja_schema import ModelSchema

from api.users.models import User


class UserCreateSchema(ModelSchema):
    """
    Schema for creating a new user.

    The fields defined here are:
    - first_name: the first name of the user.
    - last_name: the last name of the user.
    - email: the email address of the user.
    - password: the password of the user.
    """

    class Config:
        model = User
        include = [
            "first_name",
            "last_name",
            "email",
            "password",
        ]
