from django.db import models
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    """
    Comment model class that represents a comment in the database.

    Attributes:
        - text(str): The text of the comment.
        - created_at(datetime): The date and time the comment was created.
        - updated_at(datetime): The date and time the comment was last updated.
        - user(User): The user that created the comment.
        - post(Post): The post that the comment belongs to.
        - answer_to(Comment): The comment that this comment is an answer to.
        - is_blocked(bool): A boolean that indicates if the comment is blocked.
    """

    text = models.CharField(_("text"), max_length=255)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
    answer_to = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    is_blocked = models.BooleanField(_("is blocked"), default=False)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-created_at"]

    def __str__(self):
        return self.text
