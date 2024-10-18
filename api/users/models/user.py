from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.users.models.manager import UserManager


class User(AbstractUser):
    """
    Custom User model with email as the unique identifier
    The default that's used is "User"

    Attributes:
        - first_name (str): The first name of the user.
        - last_name (str): The last name of the user.
        - email (str): The email of the user.
    """

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        """
        Save the user with a hashed password.
        """
        if self.password and not self.password.startswith("pbkdf2_"):
            self.set_password(self.password)
        super().save(*args, **kwargs)
