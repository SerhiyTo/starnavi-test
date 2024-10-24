from ninja_schema import Schema


class CommentDailyBreakdownSchema(Schema):
    """
    Comment daily breakdown schema.

    Attributes:
        - date (str): The date.
        - total_comments (int): The total number of comments.
        - blocked_comments (int): The number of blocked comments.
    """

    date: str
    total_comments: int
    blocked_comments: int
