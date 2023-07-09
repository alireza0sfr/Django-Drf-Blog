from django.db import models

from common.models import BaseModel
from enums.blog import PostStatus


class Post(BaseModel):
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    status = models.IntegerField(default=PostStatus.PUBLISHED, choices=PostStatus.choices)
    category = models.ForeignKey('Category', on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)
    image = models.ImageField()

    def __str__(self):
        return self.title
    
    def get_snippet(self):
        return f'{self.content[0: 5]}...'


class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
