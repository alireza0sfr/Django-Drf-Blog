from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from serializers.blog.serializers import PostModelSerializer, CategoryModelSerializer
from blog.models import Post, Category
from common.paginations import BasePagination
from common.permissions import IsAuthenticatedAndIsVerified

class PostModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedAndIsVerified]
    serializer_class = PostModelSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'author', 'status']
    search_fields = ['title', 'content', 'author__first_name', 'author___full_name']
    ordering_fields = ['created_date']
    pagination_class = BasePagination

class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedAndIsVerified]
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
