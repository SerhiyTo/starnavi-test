from typing import List

from asgiref.sync import sync_to_async
from django.http import HttpRequest
from ninja_extra import api_controller, route, status
from ninja_extra import permissions
from ninja_extra.exceptions import APIException
from ninja_jwt.authentication import AsyncJWTAuth

from api.posts.models import Post
from api.posts.repositories.post_repository import PostRepository
from api.posts.schemas import PostCreateSchema, PostResponseSchema
from api.services import UserService


@api_controller("/posts", tags=["posts"], auth=AsyncJWTAuth(), permissions=[permissions.IsAuthenticatedOrReadOnly])
class PostController:
    """
    Controller for user functionality.

    Attributes:
        - create_post (method): Create a new post.
        - get_all_published_posts (method): Get all published posts.
        - get_post (method): Get a post by ID.
        - update_post (method): Update an existing post.
        - delete_post (method): Delete a post.
    """

    @route.post("/", response={status.HTTP_201_CREATED: PostResponseSchema})
    async def create_post(self, request: HttpRequest, post_data: PostCreateSchema) -> PostResponseSchema:
        """
        Create a new post.

        :param request: http request object
        :param post_data: post data
        :return: created post
        """
        try:
            post_repository = PostRepository()
            user_service = UserService()
            user_id = await user_service.get_user_id(request)
            created_post = await post_repository.create(post=post_data.dict(), author_id=user_id)
            return PostResponseSchema.from_orm(created_post)
        except Exception as err:
            raise APIException(detail=str(err))

    @route.get("/", response={status.HTTP_200_OK: List[PostResponseSchema]}, auth=None)
    async def get_all_published_posts(self) -> List[PostResponseSchema]:
        """
        Get all published posts.

        :return: published posts
        """
        try:
            post_repository = PostRepository()
            posts = await post_repository.get_all_published()
            posts_schema = await sync_to_async(lambda: [PostResponseSchema.from_orm(post) for post in posts])()
            return posts_schema
        except Exception as err:
            raise APIException(detail=str(err))

    @route.get("/{post_id}", response={status.HTTP_200_OK: PostResponseSchema}, auth=None)
    async def get_post(self, post_id: int) -> PostResponseSchema:
        """
        Get a post by ID.

        :param post_id: post ID
        :return: post
        """
        try:
            post_repository = PostRepository()
            post = await post_repository.get_by_id(post_id=post_id)
            return PostResponseSchema.from_orm(post)

        except Post.DoesNotExist:
            exception = APIException("Post not found")
            exception.status_code = status.HTTP_404_NOT_FOUND
            raise exception

        except Exception as err:
            raise APIException(detail=str(err))

    @route.put("/{post_id}", response={status.HTTP_200_OK: PostResponseSchema})
    async def update_post(self, request: HttpRequest, post_id: int, post_data: PostCreateSchema) -> PostResponseSchema:
        """
        Update an existing post.

        :param request: http request object
        :param post_id: post ID
        :param post_data: post data
        :return: updated post
        """
        try:
            post_repository = PostRepository()
            user_service = UserService()
            user_id = await user_service.get_user_id(request)
            updated_post = await post_repository.update(post_id=post_id, post=post_data.dict(), author_id=user_id)
            return PostResponseSchema.from_orm(updated_post)

        except Post.DoesNotExist:
            exception = APIException("Post not found")
            exception.status_code = status.HTTP_404_NOT_FOUND
            raise exception

        except Exception as err:
            raise APIException(detail=str(err))

    @route.delete("/{post_id}", response={status.HTTP_204_NO_CONTENT: None})
    async def delete_post(self, request: HttpRequest, post_id: int):
        """
        Delete a post.

        :param request: http request object
        :param post_id: post ID
        :return: deleted post
        """
        try:
            post_repository = PostRepository()
            user_service = UserService()
            user_id = await user_service.get_user_id(request)
            await post_repository.delete(post_id=post_id, author_id=user_id)

        except Post.DoesNotExist:
            exception = APIException("Post not found")
            exception.status_code = status.HTTP_404_NOT_FOUND
            raise exception

        except Exception as err:
            raise APIException(detail=str(err))
