import pytest

from accounts.models import User, Profile


@pytest.fixture
def GlobalFixtures():
    user = User.objects.create_user(email='john@doe.com', password='A123456!')
    profile = Profile.objects.create(
        user=user,
        first_name='john',
        last_name='Doe'
    )
    return {
        'user': user,
        'profile': profile,
    }