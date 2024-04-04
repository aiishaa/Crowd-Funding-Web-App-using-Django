from django.urls import path
from .views import admin_view, add_category, manage_featured_projects

urlpatterns = [
    path('', admin_view, name="admin page"),
    path('categories/add/', add_category, name='create_category'),
    path('featuredprojects/', manage_featured_projects, name='featured_projects'),
    # path('categories/', views.CategoryListView.as_view(), name='category_list'),
]
