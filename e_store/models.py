from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, null=False, blank=True, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to='categories')

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, null=False, blank=True, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to='groups')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='groups')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, null=False, blank=True, unique=True)
    price = models.FloatField()
    description = models.TextField()
    discount = models.PositiveIntegerField(default=0)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='products')
    is_liked = models.ManyToManyField(User)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='products')
    is_primary = models.BooleanField(default=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.image.url


class Comment(models.Model):
    class RatingChoice(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5
    rating = models.PositiveIntegerField(choices=RatingChoice, default=RatingChoice.zero.value, null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')


class AttributeKey(models.Model):
    key_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.key_name


class AttributeValue(models.Model):
    value_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.value_name


class Attribute(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='attributes')
    key = models.ForeignKey('AttributeKey', on_delete=models.CASCADE)
    value = models.ForeignKey('AttributeValue', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title
