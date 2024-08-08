from django.urls import path
from e_store.views import (CategoryList, CategoryDetailView, GroupList, GroupDetailView, ProductList, ProductDetailView,)

urlpatterns = [
    # Category
    path('category/', CategoryList.as_view(), name='category_list'),
    path('category/<slug:slug>/detail/', CategoryDetailView.as_view(), name='category_detail'),

    # Group
    path('category/group/', GroupList.as_view(), name='group_list'),
    path('category/group/<slug:slug>/', GroupDetailView.as_view(), name='group_detail'),

    # Product
    path('category/group/product', ProductList.as_view(), name='group_list'),
    path('category/group/product/<slug:slug>/', ProductDetailView.as_view(), name='group_detail'),
]
