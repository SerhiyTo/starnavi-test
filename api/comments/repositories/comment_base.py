from abc import ABC, abstractmethod
from typing import List

from api.comments.models import Comment


class CommentBaseRepository(ABC):
    """
    CommentBaseRepository is an abstract class that defines the methods that must be implemented by the CommentRepository class.

    The methods defined in this class are:
    - create: creates a new comment
    - get_by_id: retrieves a comment by its id
    - get_all_by_post_id: retrieves all comments related to a post
    - update: updates a comment
    - delete: deletes a comment
    """

    @abstractmethod
    async def create(self, comment: dict, post_id: int, author_id: int) -> Comment:
        raise NotImplementedError

    @abstractmethod
    async def create_reply(self, comment: dict, post_id: int, comment_id: int, author_id: int) -> Comment:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, post_id: int, comment_id: int) -> Comment:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_post_id(self, post_id: int) -> List[Comment]:
        raise NotImplementedError

    @abstractmethod
    async def get_replies_by_comment(self, post_id: int, comment_id: int) -> List[Comment]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, comment: dict, post_id: int, comment_id: int, author_id: int) -> Comment:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, post_id: int, comment_id: int, author_id: int) -> Comment:
        raise NotImplementedError
