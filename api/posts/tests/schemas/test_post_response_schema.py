from django.test import TestCase, tag

from api.posts.factories import PostFactory
from api.posts.schemas import PostResponseSchema


@tag("schemas")
class PostResponseSchemaTest(TestCase):
    """
    Test the PostResponseSchema schema.
    """

    def test_post_response_schema(self):
        """
        Test the PostResponseSchema schema.
        """
        post = PostFactory()
        post_response_schema = PostResponseSchema.from_orm(post)
        post_data = post_response_schema.dict()
        self.assertEqual(post_data["id"], post.id)
        self.assertEqual(post_data["title"], post.title)
        self.assertEqual(post_data["content"], post.content)
        self.assertEqual(post_data["created_at"], post.created_at)
        self.assertEqual(post_data["updated_at"], post.updated_at)
        self.assertEqual(post_data["is_published"], post.is_published)
