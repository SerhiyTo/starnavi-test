from asgiref.sync import sync_to_async
from django.test import TestCase, tag
from ninja_extra.testing import TestAsyncClient
from ninja_jwt.tokens import AccessToken

from api.posts.api import PostController
from api.posts.factories import PostFactory
from api.users.factories import UserFactory


@tag("api")
class PostControllerTest(TestCase):
    async def test_create_post_success(self):
        user = await sync_to_async(UserFactory)(
            email="test@gmail.com",
            password="password",
        )
        token = await sync_to_async(AccessToken.for_user)(user=user)
        client = TestAsyncClient(PostController)
        response = await client.post(
            path="/",
            json={
                "title": "Test Title",
                "content": "Test Content",
                "is_published": True,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Test Title")
        self.assertEqual(response.json()["content"], "Test Content")
        self.assertTrue("id" in response.json())

    async def test_create_post_unauthorized(self):
        client = TestAsyncClient(PostController)
        response = await client.post(
            path="/",
            json={
                "title": "Test Title",
                "content": "Test Content",
                "is_published": True,
            },
        )
        self.assertEqual(response.status_code, 401)

    async def test_create_post_unsuccessful(self):
        user = await sync_to_async(UserFactory)()
        token = await sync_to_async(AccessToken.for_user)(user=user)
        client = TestAsyncClient(PostController)
        response = await client.post(
            path="/",
            json={
                "title": None,
                "content": None,
                "is_published": True,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 422)

    async def test_get_all_published_posts_success(self):
        user = await sync_to_async(UserFactory)()
        await sync_to_async(PostFactory.create_batch)(3, author=user)
        client = TestAsyncClient(PostController)
        response = await client.get(path="/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    async def test_get_post_success(self):
        post = await sync_to_async(PostFactory)()
        client = TestAsyncClient(PostController)
        response = await client.get(path=f"/{post.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], post.id)
        self.assertEqual(response.json()["title"], post.title)
        self.assertEqual(response.json()["content"], post.content)

    async def test_get_post_not_found(self):
        client = TestAsyncClient(PostController)
        response = await client.get(path="/1")
        self.assertEqual(response.status_code, 404)

    async def test_update_post_success(self):
        user = await sync_to_async(UserFactory)()
        post = await sync_to_async(PostFactory)(author=user)
        token = await sync_to_async(AccessToken.for_user)(user=user)
        client = TestAsyncClient(PostController)
        response = await client.put(
            path=f"/{post.id}",
            json={
                "title": "Updated Title",
                "content": "Updated Content",
                "is_published": True,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated Title")
        self.assertEqual(response.json()["content"], "Updated Content")

    async def test_update_post_unauthorized(self):
        post = await sync_to_async(PostFactory)()
        client = TestAsyncClient(PostController)
        response = await client.put(
            path=f"/{post.id}",
            json={
                "title": "Updated Title",
                "content": "Updated Content",
                "is_published": True,
            },
        )
        self.assertEqual(response.status_code, 401)

    async def test_update_post_unsuccessful(self):
        user = await sync_to_async(UserFactory)()
        post = await sync_to_async(PostFactory)(author=user)
        token = await sync_to_async(AccessToken.for_user)(user=user)
        client = TestAsyncClient(PostController)
        response = await client.put(
            path=f"/{post.id}",
            json={
                "title": None,
                "content": None,
                "is_published": True,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 422)

    async def test_delete_post_success(self):
        user = await sync_to_async(UserFactory)()
        post = await sync_to_async(PostFactory)(author=user)
        token = await sync_to_async(AccessToken.for_user)(user=user)
        client = TestAsyncClient(PostController)
        response = await client.delete(
            path=f"/{post.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 204)

    async def test_delete_post_unauthorized(self):
        post = await sync_to_async(PostFactory)()
        client = TestAsyncClient(PostController)
        response = await client.delete(path=f"/{post.id}")
        self.assertEqual(response.status_code, 401)

    async def test_delete_post_not_found(self):
        user = await sync_to_async(UserFactory)()
        token = await sync_to_async(AccessToken.for_user)(user=user)
        client = TestAsyncClient(PostController)
        response = await client.delete(
            path="/1",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 404)
