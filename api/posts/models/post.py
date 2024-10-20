from django.db import models
from django.utils.translation import gettext_lazy as _

from api.posts.models.manager import PostManager


class Post(models.Model):
    """
    Post model with a title, content, created_at, updated_at, published, author, and tags.

    Attributes:
        - title (str): The title of the post.
        - content (str): The content of the post.
        - created_at (datetime): The date and time the post was created.
        - updated_at (datetime): The date and time the post was last updated.
        - is published (bool): Whether the post is published or not.
        - author (User): The author of the post.
        - is_blocked (bool): Whether the post is blocked or not.

        - publishes (PostManager): The custom manager for the Post model.
    """

    title = models.CharField(_("title"), max_length=255)
    content = models.TextField(_("content"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    author = models.ForeignKey("users.User", related_name="posts", on_delete=models.CASCADE)
    is_published = models.BooleanField(_("is published"), default=False)
    is_blocked = models.BooleanField(_("is blocked"), default=False)

    objects = models.Manager()
    published = PostManager()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
