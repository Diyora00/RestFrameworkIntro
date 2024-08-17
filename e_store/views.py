from rest_framework import generics
from e_store.permissions import CustomPermissionForProduct
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from e_store.models import Category, Group, Product, Attribute
from e_store.serializers import CategoryModelSerializer, GroupModelSerializer, ProductModelSerializer, AttributeModelSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class CategoryList(generics.ListAPIView, generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


class CategoryDetailView(generics.RetrieveAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    permission_classes = [AllowAny, ]
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    lookup_field = 'slug'


class GroupList(generics.ListCreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    # lookup_field = 'slug'

    # def get_queryset(self):
    #     return Group.objects.filter(category__slug=self.kwargs['slug'])


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny, ]
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    lookup_field = 'slug'


class ProductList(generics.ListCreateAPIView):
    permission_classes = [CustomPermissionForProduct, ]
    # authentication_classes = [JWTAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [CustomPermissionForProduct]
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'

    def get_serializer_context(self, ):
        context = super().get_serializer_context()
        obj = Product.objects.filter(slug=self.kwargs['slug']).first()
        images = obj.images.all()
        request = self.request
        context['all_images'] = [request.build_absolute_uri(image.image.url) for image in images]

        """ single dictionary format """
        attributes = {i.key.key_name: i.value.value_name for i in obj.attributes.all()}

        """ dict in list format"""
        # attributes = [{i.key.key_name: i.value.value_name} for i in obj.attributes.all()]
        context['attributes'] = attributes

        context['comments'] = obj.comments.all().values('message', 'rating', 'user__username')
        # print(obj.attributes.all().values('key__key_name', 'value__value_name'))
        return context


class AttributesView(generics.ListAPIView):
    serializer_class = AttributeModelSerializer
    queryset = Attribute.objects.all()
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
#         serializer = CategoryModelSerializer(categories, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = CategoryModelSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

