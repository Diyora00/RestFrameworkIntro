from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from e_store.models import Category
from django.shortcuts import render


# Create your views here.
class CategoryList(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        categories = [
            {
                'title': category.title,
                'slug': category.slug,
                'image': str(category.image)
            }
            for category in Category.objects.all()
        ]
        return Response(categories, status=status.HTTP_200_OK)
