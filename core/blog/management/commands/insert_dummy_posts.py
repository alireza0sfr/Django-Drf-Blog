from django.core.management.base import BaseCommand

from core.factories.blog import PostFactory

class Command(BaseCommand):
    help = "Inserts 5 dummy posts."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        for _ in range(5):
            PostFactory()