import factory.fuzzy
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from app.users.user_profile.models import UserProfile

faker = FakerFactory.create()


@register
class UserProfileFactory(factory.Factory):
    class Meta:
        model = UserProfile

    id = factory.LazyFunction(lambda: faker.random_number())
    username = factory.LazyFunction(lambda: faker.user_name())
    email = factory.LazyFunction(lambda: faker.email())
    name = factory.LazyFunction(lambda: faker.name())
    google_access_token = factory.LazyFunction(lambda: faker.sha256())
    yandex_access_token = factory.LazyFunction(lambda: faker.sha256())