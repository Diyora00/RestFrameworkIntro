from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from e_store.models import Category
from e_store.serializers import CategoryModelSerializer
from django.shortcuts import render


class CategoryList(generics.ListAPIView, generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


class CategoryDetailView(generics.RetrieveAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    permission_classes = [AllowAny, ]
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    lookup_field = 'slug'


class AddCategory(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryModelSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategoryModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# class CategoryDetailView(APIView):
#     def get(self, request, slug):
#         """
#         if filter() is used to get 1 object it won't work bcs it returns queryset
#         get() can retrieve info about 1 object
#         """
#         category = Category.objects.get(slug=slug)
#         serializer = CategoryModelSerializer(category, many=False)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, slug):
#         category = self.get_object(slug)
#         serializer = CategoryModelSerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#
#     def delete(self, request, slug):
#         category = Category.objects.get(slug=slug)
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class CategoryList(APIView):
#     permission_classes = [AllowAny, ]
#
#     def get(self, request):
#         categories = Category.objects.all()
#         # categories = [
#         #     {
#         #         'title': category.title,
#         #         'slug': category.slug,
#         #         'image': str(category.image)
#         #     }
#         #     for category in Category.objects.all()
#         # ]
#         serializer = CategoryModelSerializer(categories, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
