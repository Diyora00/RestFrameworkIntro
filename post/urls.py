from django.urls import path
from rest_framework.routers import DefaultRouter
from post import views


router = DefaultRouter()
router.register('post', views.PostViewSet, basename='post')

urlpatterns = [

] + router.urls
