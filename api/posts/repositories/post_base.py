from abc import ABC, abstractmethod

from api.posts.models import Post


class PostBaseRepository(ABC):
    """
    PostBaseRepository is an abstract class that defines the methods that must be implemented by the PostRepository class.

    The methods defined here are:
    - create: creates a new post in the database.
    - update: updates an existing post in the database.
    - get_all_published: retrieves all published posts from the database.
    - get_by_id: retrieves a post from the database by ID.
    """

    @abstractmethod
    async def create(self, post: dict, author_id: int) -> Post:
        raise NotImplementedError

    @abstractmethod
    async def get_all_published(self) -> list[Post]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, post_id: int) -> Post:
        raise NotImplementedError

    @abstractmethod
    async def update(self, post_id: int, post: dict, author_id: int) -> Post:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, post_id: int, author_id: int) -> Post:
        raise NotImplementedError
