from rest_framework.serializers import ModelSerializer

from comment.models import Comment


class CommentModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_date']