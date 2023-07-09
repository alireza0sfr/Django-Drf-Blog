from django.db import models


class PostStatus(models.IntegerChoices):
    DONE = 1, 'Done'
    PUBLISHED = 2, 'Published'
    ARCHIVED = 3, 'Archived'
    DELETED = 4, 'Deleted'
