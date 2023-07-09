from rest_framework.serializers import ModelSerializer, ReadOnlyField

from blog.models import Post, Category
from accounts.models import Profile


class PostModelSerializer(ModelSerializer):
    snippet = ReadOnlyField(source='get_snippet')

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'snippet', 'status', 'category', 'image', 'created_date']
        read_only_fields = ['author']

    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user__id=self.context.get('request').user.id)
        return super().create(validated_data)


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_date']
