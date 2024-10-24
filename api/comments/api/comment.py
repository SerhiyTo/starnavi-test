from typing import List

from asgiref.sync import sync_to_async
from django.http import HttpRequest
from ninja_extra import api_controller, route, status
from ninja_extra import permissions
from ninja_jwt.authentication import AsyncJWTAuth

from api.comments.repositories import CommentRepository
from api.comments.schemas import (
    CommentCreateSchema,
    CommentResponseSchema,
)
from api.services import UserService


@api_controller(
    "/posts/{post_id}/comments",
    tags=["comments"],
    auth=AsyncJWTAuth(),
    permissions=[permissions.IsAuthenticatedOrReadOnly],
)
class CommentController:
    """
    Controller for user functionality.

    Attributes:
        - create_comment (method): Create a new comment.
        - get_comments_by_post (method): Get all comments by post.
        - get_comment (method): Get a comment by ID.
        - update_comment (method): Update an existing comment.
        - delete_comment (method): Delete a comment.
    """

    @route.post("/", response={status.HTTP_201_CREATED: CommentResponseSchema})
    async def create_comment(
        self,
        request: HttpRequest,
        post_id: int,
        comment_data: CommentCreateSchema,
    ) -> CommentResponseSchema:
        """
        Create a new comment.

        :param request: http request object
        :param post_id: post id
        :param comment_data: comment data
        :return: created comment
        """
        comment_repository = CommentRepository()
        user_service = UserService()
        user_id = await user_service.get_user_id(request)
        comment = await comment_repository.create(
            comment=comment_data.dict(),
            post_id=post_id,
            author_id=user_id,
        )
        return CommentResponseSchema.from_orm(comment)

    @route.get("/", response={status.HTTP_200_OK: List[CommentResponseSchema]}, auth=None)
    async def get_comments_by_post(self, post_id: int) -> List[CommentResponseSchema]:
        """
        Get all comments by post.

        :param post_id: post id
        :return: comments
        """
        comment_repository = CommentRepository()
        comments = await comment_repository.get_all_by_post_id(post_id)
        comments_schema = await sync_to_async(
            lambda: [CommentResponseSchema.from_orm(comment) for comment in comments]
        )()
        return comments_schema

    @route.get(
        "/{comment_id}", response={status.HTTP_200_OK: CommentResponseSchema}, auth=None
    )
    async def get_comment(self, post_id: int, comment_id: int) -> CommentResponseSchema:
        """
        Get a comment by ID.

        :param post_id: post id
        :param comment_id: comment id
        :return: comment
        """
        comment_repository = CommentRepository()
        comment = await comment_repository.get_by_id(post_id, comment_id)
        return CommentResponseSchema.from_orm(comment)

    @route.put("/{comment_id}", response={status.HTTP_200_OK: CommentResponseSchema})
    async def update_comment(
        self,
        request: HttpRequest,
        post_id: int,
        comment_id: int,
        comment_data: CommentCreateSchema,
    ) -> CommentResponseSchema:
        """
        Update an existing comment.

        :param request: http request object
        :param post_id: post id
        :param comment_id: comment id
        :param comment_data: comment data
        :return: updated comment
        """
        comment_repository = CommentRepository()
        user_service = UserService()
        user_id = await user_service.get_user_id(request)
        comment = await comment_repository.update(
            comment=comment_data.dict(),
            post_id=post_id,
            comment_id=comment_id,
            author_id=user_id,
        )
        return CommentResponseSchema.from_orm(comment)

    @route.delete("/{comment_id}", response={status.HTTP_204_NO_CONTENT: None})
    async def delete_comment(
        self,
        request: HttpRequest,
        post_id: int,
        comment_id: int,
    ) -> None:
        """
        Delete a comment.

        :param request: http request object
        :param post_id: post id
        :param comment_id: comment id
        :return: deleted comment
        """
        comment_repository = CommentRepository()
        user_service = UserService()
        user_id = await user_service.get_user_id(request)
        await comment_repository.delete(
            post_id=post_id,
            comment_id=comment_id,
            author_id=user_id,
        )

    @route.post(
        "/{comment_id}/replies",
        response={status.HTTP_201_CREATED: CommentResponseSchema},
    )
    async def create_reply(
        self,
        request: HttpRequest,
        post_id: int,
        comment_id: int,
        comment_data: CommentCreateSchema,
    ) -> CommentResponseSchema:
        """
        Create a reply to a comment.

        :param request: http request object
        :param post_id: post id
        :param comment_id: comment id
        :param comment_data: comment data
        :return: created reply comment
        """
        comment_repository = CommentRepository()
        user_service = UserService()
        user_id = await user_service.get_user_id(request)
        comment = await comment_repository.create_reply(
            comment=comment_data.dict(),
            post_id=post_id,
            comment_id=comment_id,
            author_id=user_id,
        )
        return CommentResponseSchema.from_orm(comment)

    @route.get(
        "/{comment_id}/replies",
        response={status.HTTP_200_OK: List[CommentResponseSchema]},
        auth=None,
    )
    async def get_replies_by_comment(
        self,
        post_id: int,
        comment_id: int,
    ) -> List[CommentResponseSchema]:
        """
        Get all replies to a comment.

        :param post_id: post id
        :param comment_id: comment id
        :return: replies to the comment
        """
        comment_repository = CommentRepository()
        comments = await comment_repository.get_replies_by_comment(post_id, comment_id)
        comments_schema = await sync_to_async(
            lambda: [CommentResponseSchema.from_orm(comment) for comment in comments]
        )()
        return comments_schema
