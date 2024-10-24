from asgiref.sync import sync_to_async

from api.posts.models import Post
from api.posts.repositories.post_base import PostBaseRepository
from api.services import UserService


class PostRepository(PostBaseRepository):
    """
    Post repository class to handle database operations.

    The methods defined here are:
    - create: Create a new post.
    - update: Update an existing post.
    - get_all_published: Get all published posts.
    - get_by_id: Get a post by ID.
    """

    async def create(self, post: dict, author_id: int) -> Post:
        """
        Create a new post in the database.

        :param post: post data.
        :param author_id: user ID.
        :return: created post.
        """

        if not post.get("title"):
            raise ValueError("The Title must be set")

        if not post.get("content"):
            raise ValueError("The Content must be set")

        return await Post.objects.acreate(author_id=author_id, **post)

    async def get_all_published(self) -> list[Post]:
        """
        Get all published posts from the database.

        :return: list of published posts.
        """
        return await sync_to_async(Post.published.all)()

    async def get_by_id(self, post_id: int) -> Post:
        """
        Get a post from the database by ID.

        :param post_id: post ID.
        :return: post with the given ID.
        """
        return await Post.objects.aget(pk=post_id)

    async def update(self, post_id: int, post: dict, author_id: int) -> Post:
        """
        Update an existing post in the database.

        :param post_id: post ID.
        :param post: updated post data.
        :param author_id: user ID.
        :return: updated post.
        """

        if not post.get("title"):
            raise ValueError("The Title must be set")

        if not post.get("content"):
            raise ValueError("The Content must be set")

        user_service = UserService()
        post_to_update = await self.get_by_id(post_id)

        await user_service.check_author_permission(post_to_update.author_id, author_id)
        await Post.objects.filter(pk=post_id).aupdate(**post)

        return await self.get_by_id(post_id)

    async def delete(self, post_id: int, author_id: int) -> Post:
        """
        Delete a post from the database.

        :param post_id: post ID.
        :param author_id: user ID.
        :return: deleted post.
        """
        user_service = UserService()
        post_to_delete = await self.get_by_id(post_id)

        await user_service.check_author_permission(
            obj_author_id=post_to_delete.author_id,
            author_id=author_id,
        )

        return await post_to_delete.adelete()
