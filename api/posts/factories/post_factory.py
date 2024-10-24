import factory

from api.posts.models import Post


class PostFactory(factory.django.DjangoModelFactory):
    """
    User factory for creating users with common fields.
    """

    class Meta:
        model = Post

    title = factory.Faker("sentence", nb_words=4)
    content = factory.Faker("text")
    author = factory.SubFactory("api.users.factories.UserFactory")
    is_published = True
    is_blocked = False
