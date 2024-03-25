from django.urls import path
from .views import createProject

urlpatterns = [
    path('create/<int:id>', createProject, name="create project")
]