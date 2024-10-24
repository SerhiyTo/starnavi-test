from django.test import TestCase, tag

from api.posts.factories import PostFactory


@tag("models")
class PostModelTestCase(TestCase):
    """
    Test case for the Post model.
    """

    def test_post_model(self):
        """
        Test the Post model.
        """
        post = PostFactory(
            title="Test Post",
            content="This is a test post.",
        )
        self.assertEqual(str(post), "Test Post")
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "This is a test post.")
        self.assertTrue(post.is_published)
        self.assertFalse(post.is_blocked)
        self.assertIsNotNone(post.created_at)
        self.assertIsNotNone(post.updated_at)
        self.assertIsNotNone(post.author)
