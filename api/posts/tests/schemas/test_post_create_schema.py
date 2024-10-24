from django.test import TestCase, tag

from api.posts.factories import PostFactory
from api.posts.schemas import PostCreateSchema


@tag("schemas")
class PostCreateSchemaTest(TestCase):
    """
    Test the PostCreateSchema schema class.
    """

    def test_post_create_schema(self):
        """
        Test the PostCreateSchema schema class.
        """
        post = PostFactory()
        post_data = {
            "title": post.title,
            "content": post.content,
        }
        post_create_schema = PostCreateSchema(**post_data)
        self.assertEqual(post_create_schema.title, post.title)
        self.assertEqual(post_create_schema.content, post.content)
