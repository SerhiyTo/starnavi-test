from django.db import models


class PostManager(models.Manager):
    """
    Custom manager for the Post model that only returns published posts.

    Attributes:
        - get_queryset (method): Get the queryset of published posts.
    """

    def get_queryset(self):
        """
        Get the queryset of published posts.

        :return: queryset of published posts.
        """
        return super().get_queryset().filter(published=True)
