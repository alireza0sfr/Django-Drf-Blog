from django.db import models


class CommentStatus(models.IntegerChoices):
    PUBLISHED = 1, 'Published'
    HIDDEN = 2, 'Hidden'
    DELETED = 3, 'Deleted'
