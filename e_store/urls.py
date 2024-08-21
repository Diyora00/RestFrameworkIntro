from e_store.custom_token import CustomAuthToken
from django.urls import path
from e_store.auth_jwt import LogoutAPIView, LoginAPIView, RegisterAPIView
from e_store.auth import UserLoginAPIView, UserLogoutAPIView, UserRegisterAPIView
from e_store.views import (CategoryList, CategoryDetailView, GroupList, GroupDetailView, ProductList, ProductDetailView,
                           AttributesView)

urlpatterns = [
    # Category
    path('category/', CategoryList.as_view(), name='category_list'),
    path('category/<slug:slug>/detail/', CategoryDetailView.as_view(), name='category_detail'),

    # Group
    path('category/group/', GroupList.as_view(), name='group_list'),
    path('category/group/<slug:slug>/', GroupDetailView.as_view(), name='group_detail'),

    # Product
    path('category/product/', ProductList.as_view(), name='group_list'),
    path('category/product/<slug:slug>/', ProductDetailView.as_view(), name='group_detail'),

    # Attributes
    path('category/group/product/<slug:slug>/attributes/', AttributesView.as_view(), name='related_attributes'),
    path('attributes/', AttributesView.as_view(), name='attribute_list'),

    # TokenAuthentication
    path('login-page/', UserLoginAPIView.as_view(), name='login_page'),
    path('logout-page/', UserLogoutAPIView.as_view(), name='logout_page'),
    path('register-page/', UserRegisterAPIView.as_view(), name='register_page'),
    path('api-token-auth/', CustomAuthToken.as_view()),

    # JWTAuthentication (JSON Web Token)
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('register/', RegisterAPIView.as_view(), name='register'),

]
