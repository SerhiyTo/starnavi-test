from ninja_schema import Schema


class AuthSchema(Schema):
    """
    User schema for serialization and deserialization of user data.

    The fields defined here are:
    - email: the user's email address.
    - password: the user's password.
    """

    email: str
    password: str
