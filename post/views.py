from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from post.serializers import PostModelSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination
from post.models import Post
from rest_framework import status
from rest_framework.generics import ListAPIView


class PostView(APIView, PageNumberPagination):
    serializer_class = PostModelSerializer

    # @method_decorator(cache_page(60))
    def get(self, request, *args, **kwargs):
        post_key = 'post_list'
        posts = cache.get(post_key)
        if not posts:
            posts = Post.objects.all().prefetch_related('tags').select_related('author')
            result = self.paginate_queryset(posts, request, view=self)
            serializer = PostModelSerializer(result, many=True)
            cache.set(post_key, serializer.data, timeout=60*5)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(posts)


class PostDetailView(APIView):
    def get(self, request, *args, **kwargs):
        post_key = f'post_detail_{self.kwargs['pk']}'
        post = cache.get(post_key)
        if not post:
            post = Post.objects.get(pk=self.kwargs['pk'])
            serializer = PostModelSerializer(post)
            cache.set(post_key, serializer.data, timeout=60*5)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(post)
