from django.urls import path
from e_store.views import CategoryList, CategoryDetailView, AddCategory


urlpatterns = [
    path('category/', CategoryList.as_view(), name='category_list'),
    path('category/<slug:slug>/detail/', CategoryDetailView.as_view(), name='category_detail'),
    path('add_category', AddCategory.as_view())
]
