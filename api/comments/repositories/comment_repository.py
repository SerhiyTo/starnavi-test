from typing import List

from asgiref.sync import sync_to_async

from api.comments.models import Comment
from api.comments.repositories import CommentBaseRepository
from api.services import UserService


class CommentRepository(CommentBaseRepository):
    """
    CommentRepository is a class that implements the methods defined in the CommentBaseRepository abstract class.

    The methods implemented in this class are:
    - create: creates a new comment
    - get_by_id: retrieves a comment by its id
    - get_all_by_post_id: retrieves all comments related to a post
    - update: updates a comment
    - delete: deletes a comment
    """

    async def create(self, comment: dict, post_id: int, author_id: int) -> Comment:
        """
        Creates a new comment.

        :param comment: dict with the comment data
        :param post_id: id of the post related to the comment
        :param author_id: id of the author of the comment
        :return: created object
        """
        return await Comment.objects.acreate(author_id=author_id, post_id=post_id, **comment)

    async def create_reply(self, comment: dict, post_id: int, comment_id: int, author_id: int) -> Comment:
        """
        Creates a new reply to a comment.

        :param comment: dict with the comment data
        :param post_id: id of the post related to the comment
        :param comment_id: id of the comment to reply to
        :param author_id: id of the author of the comment
        :return:
        """
        return await Comment.objects.acreate(author_id=author_id, post_id=post_id, parent_id=comment_id, **comment)

    async def get_by_id(self, post_id: int, comment_id: int) -> Comment:
        """
        Retrieves a comment by its id.

        :param post_id: id of the post
        :param comment_id: id of the comment
        :return: comment object
        """
        return await Comment.objects.aget(pk=comment_id, post_id=post_id)

    async def get_all_by_post_id(self, post_id: int) -> List[Comment]:
        """
        Retrieves all comments related to a post.

        :param post_id: id of the post
        :return: list of comments
        """
        return await sync_to_async(Comment.available.filter(post_id=post_id).all)()

    async def get_replies_by_comment(self, post_id: int, comment_id: int) -> List[Comment]:
        """
        Retrieves all replies to a comment.

        :param post_id: id of the post
        :param comment_id: id of the comment
        :return: list of comments
        """
        return await sync_to_async(Comment.available.filter(post_id=post_id, parent_id=comment_id).all)()

    async def update(self, comment: dict, post_id: int, comment_id: int, author_id: int) -> Comment:
        """
        Updates a comment.

        :param comment: dict with the updated comment data
        :param post_id: id of the post related to the comment
        :param comment_id: id of the comment
        :param author_id: id of the author of the comment
        :return: updated object
        """
        user_service = UserService()
        comment_to_update = await self.get_by_id(post_id=post_id, comment_id=comment_id)

        await user_service.check_author_permission(
            obj_author_id=comment_to_update.author_id,
            author_id=author_id,
        )

        await Comment.objects.filter(pk=comment_id).aupdate(**comment)
        return await self.get_by_id(post_id=post_id, comment_id=comment_id)

    async def delete(self, post_id: int, comment_id: int, author_id: int) -> Comment:
        """
        Deletes a comment.

        :param post_id: id of the post related to the comment
        :param comment_id: id of the comment
        :param author_id: id of the author of the comment
        :return: deleted object
        """
        user_service = UserService()
        comment_to_delete = await self.get_by_id(post_id=post_id, comment_id=comment_id)

        await user_service.check_author_permission(
            obj_author_id=comment_to_delete.author_id,
            author_id=author_id,
        )

        return await comment_to_delete.adelete()
