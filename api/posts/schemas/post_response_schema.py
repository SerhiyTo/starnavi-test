from ninja_schema import ModelSchema

from api.posts.models import Post


class PostResponseSchema(ModelSchema):
    """
    Post schema with fields for the title, content, author, created_at, updated_at, published, and tags.

    Attributes:
        - id (int): The ID of the post.
        - title (str): The title of the post.
        - content (str): The content of the post.
        - author (int): The ID of the author of the post.
        - created_at (datetime): The date and time the post was created.
        - updated_at (datetime): The date and time the post was last updated.
        - is_published (bool): Whether the post is published or not.
    """

    class Config:
        model = Post
        include = [
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
            "is_published",
        ]
