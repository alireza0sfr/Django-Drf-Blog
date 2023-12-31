from django.urls import include, path

from api.router import router
from blog.views import PostModelViewSet, CategoryViewSet
from comment.views import CommentViewSet
from accounts.urls import urlpatterns as accounts_urlpatterns

router.register('posts', PostModelViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/', include(accounts_urlpatterns)),
]