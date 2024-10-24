from ninja_schema import ModelSchema

from api.comments.models import Comment


class CommentCreateSchema(ModelSchema):
    """
    Schema for creating a new comment.

    Attributes:
        - text(str): The text of the comment.
    """

    class Config:
        model = Comment
        include = [
            "text",
        ]
