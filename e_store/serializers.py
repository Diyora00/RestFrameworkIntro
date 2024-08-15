from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from e_store.models import Category, Group, Product, Image, Attribute


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
    category_title = serializers.CharField(source='group.category.title')
    group_title = serializers.CharField(source='group.title')
    is_liked = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    def get_primary_image(self, obj):
        # image = Image.objects.filter(product=obj, is_primary=True).first()
        image = obj.images.filter(is_primary=True).first()
        request = self.context['request']
        if image:
            return request.build_absolute_uri(image)
        return None

    def get_all_images(self, obj):
        return self.context.get('all_images', [])

    def get_attributes(self, instance):
        return self.context.get('attributes', [])

    def get_comments(self, obj):
        return self.context.get('comments', [])

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated and user in obj.is_liked.all():
            return True
        return False

    def get_rating(self, obj):
        return (obj.comments.aggregate(avg=Round(Avg('rating')))['avg'])

    class Meta:
        model = Product
        fields = '__all__'


class AttributeModelSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source='key.key_name')
    value = serializers.CharField(source='value.value_name')
    product = serializers.CharField(source='product.title')

    class Meta:
        model = Attribute
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name',]
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            detail = {
                "detail": "User already exist!"
            }
            raise ValidationError(detail=detail)
        return username

    def validate(self, instance):
        if instance['password'] != instance['password2']:
            raise ValidationError({"message": "Passwords do not match"})

        if User.objects.filter(email=instance['email']).exists():
            raise ValidationError({"message": "Email already exists !"})

        return instance

    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
