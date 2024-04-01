from django.urls import path
from .views import admin_view, add_category

urlpatterns = [
    path('', admin_view, name="admin page"),
    path('categories/add/', add_category, name='create_category'),
    # path('categories/', views.CategoryListView.as_view(), name='category_list'),
]
