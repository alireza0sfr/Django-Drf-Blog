from django.db import models

from common.models import BaseModel
from enums.comment import CommentStatus

class Comment(BaseModel):
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    status = models.IntegerField(default=CommentStatus.PUBLISHED, choices=CommentStatus.choices)
    
    def __str__(self):
      return self.content