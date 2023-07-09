from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from serializers.comment.serializers import CommentModelSerializer
from comment.models import Comment
from common.paginations import BasePagination
from common.permissions import IsAuthenticatedAndIsVerified

class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedAndIsVerified]
    serializer_class = CommentModelSerializer
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['content', 'post', 'author', 'status']
    search_fields = ['content', 'post__title' 'author__first_name', 'author___full_name']
    ordering_fields = ['created_date']
    pagination_class = BasePagination