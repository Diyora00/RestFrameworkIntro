from django.urls import path
from rest_framework.routers import DefaultRouter
from post import views


# router = DefaultRouter()
# router.register('post', views.PostViewSet, basename='post')
#
# urlpatterns = [
#
# ] + router.urls
urlpatterns = [
    path('post-list/', views.PostView.as_view()),
    path('post-list/<int:pk>/', views.PostDetailView.as_view())
]
