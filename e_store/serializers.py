from django.db.models import Avg
from rest_framework import serializers
from e_store.models import Category, Group, Product, Image


class CategoryModelSerializer(serializers.ModelSerializer):
    group_count = serializers.SerializerMethodField()

    def get_group_count(self, obj):
        return obj.groups.count()

    class Meta:
        model = Category
        fields = '__all__'


class GroupModelSerializer(serializers.ModelSerializer):
    # categories = CategoryModelSerializer(many=True, read_only=True)
    # category = CategoryModelSerializer(read_only=True)
    category_slug = serializers.SlugField(source='category.slug', read_only=True)

    class Meta:
        model = Group
        fields = '__all__'


class ProductModelSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    group_slug = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    def get_primary_image(self, obj):
        image = Image.objects.get(pk=obj.pk, is_primary=True)
        return str(image)

    def get_group_slug(self, obj):
        return obj.group.slug

    def get_rating(self, obj):
        return obj.comments.aggregate(avg=Avg('rating'))['avg']

    class Meta:
        model = Product
        fields = '__all__'
