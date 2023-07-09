from random import choice

from factory.django import DjangoModelFactory
from factory import SubFactory
from factory.faker import Faker


from factories.accounts import ProfileFactory
from enums.blog import PostStatus
from tests.base import BaseFactory


class CategoryFactory(DjangoModelFactory, BaseFactory):
    name = Faker('name')

    class Meta:
        model = 'blog.Category'


class PostFactory(DjangoModelFactory, BaseFactory):
        
    author = SubFactory(ProfileFactory)
    title = Faker('text')
    content = Faker('sentence')
    status = choice(PostStatus.choices)[0]
    category = SubFactory(CategoryFactory)
    image = Faker('image')

    class Meta:
        model = 'blog.Post'