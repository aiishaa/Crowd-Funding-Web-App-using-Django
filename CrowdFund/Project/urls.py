from django.urls import path
from .views import *

urlpatterns = [
    path('create/<int:id>', createProject, name="create project"),
    path('userprojects/<int:id>/', userProjects, name="user projects"),
    path('otherprojects/<int:id>', otherProjects, name="other projects"),
    path('otherprojects/desc/<int:userID>/<int:proID>', otherProjectDesc, name="other project desc"),
    path('otherprojects/desc/<int:userID>/<int:proID>/<int:commentID>', deleteComment, name="delete comment"),
    path('edit/<int:id>/', project_edit, name='edit_project'),
    path('project/delete/<int:project_id>/', delete_project, name='delete_project'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('details/<int:id>/', project_details, name='project_details'),
    path('category/<int:category_id>/', get_category_projects, name='category_projects'),
    path('search/', search_projects, name='search_projects')
]