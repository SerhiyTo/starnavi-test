from typing import List

from ninja_schema import Schema

from api.posts.schemas.post_response_schema import PostResponseSchema


class PostListSchema(Schema):
    """
    Post schema with fields for the title, content, and published status.

    Attributes:
        - posts (List[Post]): A list of posts.
    """
    posts: List[PostResponseSchema]
