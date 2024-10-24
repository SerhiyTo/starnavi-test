from django.test import TestCase, tag

from api.posts.factories import PostFactory
from api.posts.models import Post
from api.users.factories import UserFactory


@tag("models")
class PostModelManagerTestCase(TestCase):
    """
    Test case for the Post model manager.
    """

    def test_post_manager(self):
        """
        Test the Post model manager.
        """
        user = UserFactory()
        PostFactory(
            title="Published Post",
            content="This is a published post.",
            is_published=True,
            is_blocked=False,
            author=user,
        )
        PostFactory(
            is_published=False,
            author=user,
        )
        PostFactory(
            is_blocked=True,
            author=user,
        )
        published_posts = Post.published.all()
        self.assertEqual(published_posts.count(), 1)
        self.assertEqual(published_posts.first().title, "Published Post")
        self.assertEqual(published_posts.first().content, "This is a published post.")
        self.assertTrue(published_posts.first().is_published)
        self.assertFalse(published_posts.first().is_blocked)
        self.assertIsNotNone(published_posts.first().created_at)
        self.assertIsNotNone(published_posts.first().updated_at)
        self.assertIsNotNone(published_posts.first().author)
