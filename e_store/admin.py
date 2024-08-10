from django.contrib import admin
from e_store.models import Category, Product, Group, Comment, Image, AttributeKey, Attribute, AttributeValue

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Group)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(AttributeKey)
admin.site.register(AttributeValue)
admin.site.register(Attribute)
