from ninja_schema import ModelSchema

from api.comments.models import Comment


class CommentResponseSchema(ModelSchema):
    """
    Comment response schema class that represents a comment response in the API.

    Attributes:
        - id(int): The ID of the comment.
        - text(str): The text of the comment.
        - created_at(datetime): The date and time the comment was created.
        - updated_at(datetime): The date and time the comment was last updated.
        - is_blocked(bool): A boolean that indicates if the comment is blocked.
    """

    class Config:
        model = Comment
        include = [
            "id",
            "text",
            "created_at",
            "updated_at",
            "is_blocked",
        ]
