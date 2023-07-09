from factory.django import DjangoModelFactory
from factory import SubFactory
from factory.faker import Faker

from tests.base import BaseFactory

class UserFactory(DjangoModelFactory, BaseFactory):
  
  email = Faker('email')
  password = 'a@123456'
  is_verified = True

  class Meta:
      model = 'accounts.User'

class ProfileFactory(DjangoModelFactory, BaseFactory):
    user = SubFactory(UserFactory)
    first_name = Faker('first_name')
    last_name = Faker('last_name')

    class Meta:
        model = 'accounts.Profile'