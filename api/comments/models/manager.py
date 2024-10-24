from django.db import models


class AvailableCommentsManager(models.Manager):
    """
    Manager for the Comment model that returns only comments that are not blocked.

    Attributes:
        - get_queryset (method): Returns the queryset of the manager.
    """

    def get_queryset(self):
        """
        Returns the queryset of the manager.

        :return: queryset of the manager.
        """
        return super().get_queryset().filter(is_blocked=False)
