from asgiref.sync import sync_to_async
from django.test import TestCase, tag

from api.posts.models import Post
from api.posts.repositories.post_repository import PostRepository
from api.users.factories import UserFactory


@tag("repositories")
class PostFactory(TestCase):
    """
    Test case for the PostRepository class.
    """

    async def test_create_post_success(self):
        """
        Test that a post can be created successfully.
        """
        post_data = {
            "title": "Test Post",
            "content": "This is a test post.",
        }
        user = await sync_to_async(UserFactory)()
        post_repository = await sync_to_async(PostRepository)()
        post = await post_repository.create(post=post_data, author_id=user.pk)
        self.assertEqual(post.title, post_data["title"])
        self.assertEqual(post.content, post_data["content"])
        self.assertEqual(post.author_id, user.pk)

    async def test_create_post_unsuccessful(self):
        """
        Test that a post cannot be created without a title.
        """
        post_data = {
            "title": None,
            "content": None,
        }
        user = await sync_to_async(UserFactory)()
        post_repository = PostRepository()
        with self.assertRaises(ValueError) as context:
            await post_repository.create(post=post_data, author_id=user.pk)
        self.assertEqual(str(context.exception), "The Title must be set")

    async def test_get_post_by_id_success(self):
        """
        Test that a post can be retrieved by ID.
        """
        user = await sync_to_async(UserFactory)()
        post_data = {
            "title": "Test Post",
            "content": "This is a test post.",
        }
        post_repository = PostRepository()
        post = await post_repository.create(post=post_data, author_id=user.pk)
        found_post = await post_repository.get_by_id(post.pk)
        self.assertEqual(post, found_post)

    async def test_get_post_by_id_unsuccessful(self):
        """
        Test that a post cannot be retrieved by an empty ID.
        """
        post_repository = PostRepository()
        with self.assertRaises(Post.DoesNotExist) as context:
            await post_repository.get_by_id(post_id=None)
        self.assertEqual(str(context.exception), "Post matching query does not exist.")

    async def test_update_post_success(self):
        """
        Test that a post can be updated successfully.
        """
        user = await sync_to_async(UserFactory)()
        post_data = {
            "title": "Test Post",
            "content": "This is a test post.",
        }
        post_repository = PostRepository()
        post = await post_repository.create(post=post_data, author_id=user.pk)
        updated_post_data = {
            "title": "Updated Post",
            "content": "This is an updated post.",
        }
        updated_post = await post_repository.update(post_id=post.pk, post=updated_post_data, author_id=user.pk)
        self.assertEqual(updated_post.title, updated_post_data["title"])
        self.assertEqual(updated_post.content, updated_post_data["content"])

    async def test_update_post_unsuccessful(self):
        """
        Test that a post cannot be updated without a title.
        """
        user = await sync_to_async(UserFactory)()
        post_data = {
            "title": "Test Post",
            "content": "This is a test post.",
        }
        post_repository = PostRepository()
        post = await post_repository.create(post=post_data, author_id=user.pk)
        updated_post_data = {
            "title": None,
            "content": None,
        }
        with self.assertRaises(ValueError) as context:
            await post_repository.update(post_id=post.pk, post=updated_post_data, author_id=user.pk)
        self.assertEqual(str(context.exception), "The Title must be set")

    async def test_delete_post_success(self):
        """
        Test that a post can be deleted successfully.
        """
        user = await sync_to_async(UserFactory)()
        post_data = {
            "title": "Test Post",
            "content": "This is a test post.",
        }
        post_repository = PostRepository()
        post = await post_repository.create(post=post_data, author_id=user.pk)
        deleted_post = await post_repository.delete(post_id=post.pk, author_id=user.pk)
        self.assertEqual(deleted_post[0], 1)

    async def test_delete_post_unsuccessful(self):
        """
        Test that a post cannot be deleted without an ID.
        """
        user = await sync_to_async(UserFactory)()
        post_data = {
            "title": "Test Post",
            "content": "This is a test post.",
        }
        post_repository = PostRepository()
        post = await post_repository.create(post=post_data, author_id=user.pk)
        with self.assertRaises(Post.DoesNotExist) as context:
            await post_repository.delete(post_id=None, author_id=user.pk)
        self.assertEqual(str(context.exception), "Post matching query does not exist.")
