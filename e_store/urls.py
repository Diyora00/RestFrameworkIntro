from django.urls import path
from e_store.views import CategoryList


urlpatterns = [
    path('', CategoryList.as_view(), name='category_list'),
]
