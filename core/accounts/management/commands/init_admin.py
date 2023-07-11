from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).count() == 0:
            User.objects.create_superuser(
                email='a@a.com', password='!@#QWE123qwe')
            print('Admin user created!')

        else:
            print('Admin accounts can only be initialized if no Accounts exist')
