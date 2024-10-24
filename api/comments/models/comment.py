from django.db import models
from django.utils.translation import gettext_lazy as _

from api.comments.models.manager import AvailableCommentsManager
from api.services.profanity_service import ProfanityFilter


class Comment(models.Model):
    """
    Comment model class that represents a comment in the database.

    Attributes:
        - text(str): The text of the comment.
        - created_at(datetime): The date and time the comment was created.
        - updated_at(datetime): The date and time the comment was last updated.
        - author(User): The user that created the comment.
        - post(Post): The post that the comment belongs to.
        - parent(Comment): The comment that this comment is an answer to.
        - is_blocked(bool): A boolean that indicates if the comment is blocked.
    """

    text = models.CharField(_("text"), max_length=255)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    is_blocked = models.BooleanField(_("is blocked"), default=False)

    objects = models.Manager()
    available = AvailableCommentsManager()

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-created_at"]

    def __str__(self):
        return self.text

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        """
        Save the comment.

        Args:
            - args: Additional positional arguments.
            - force_insert(bool): A boolean that indicates if the save is a forced insert.
            - force_update(bool): A boolean that indicates if the save is a forced update.
            - using(str): The database alias to use for saving.
            - update_fields(list): A list of fields to update.
        """

        profanity_filter = ProfanityFilter()

        if profanity_filter.is_profane(self.text):
            self.is_blocked = True

        super().save(*args, force_insert, force_update, using, update_fields)
