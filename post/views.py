from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from post.serializers import PostModelSerializer

from post.models import Post


class PostViewSet(ModelViewSet):
    serializer_class = PostModelSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = Post.objects.all().select_related('author').prefetch_related('tags')
        return queryset
