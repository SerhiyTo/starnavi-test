from ninja_schema import ModelSchema

from api.users.models import User


class UserResponseSchema(ModelSchema):
    """
    User schema for serialization and deserialization of user data.

    The fields defined here are:
    - id: the user's unique identifier.
    - first_name: the user's first name.
    - last_name: the user's last name.
    - email: the user's email address.
    """

    class Config:
        model = User
        include = [
            "id",
            "first_name",
            "last_name",
            "email",
        ]
