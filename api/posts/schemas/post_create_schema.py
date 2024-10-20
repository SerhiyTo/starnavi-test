from ninja_schema import ModelSchema

from api.posts.models import Post


class PostCreateSchema(ModelSchema):
    """
    Post schema with fields for the title, content, and published status.

    Attributes:
        - title (str): The title of the post.
        - content (str): The content of the post.
        - is_published (bool): Whether the post is published or not.
    """

    class Config:
        model = Post
        include = [
            "title",
            "content",
            "is_published",
        ]
