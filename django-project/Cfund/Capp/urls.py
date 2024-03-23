
from django.urls import path

from Capp.views import register,user_login,project_start

# from django.contrib import admin



urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('project-start/', project_start, name='project_start'),

    #path('activate/<str:activation_key>/', activate_account, name='activate_account'),
    # path('reset_password/', reset_password, name='reset_password'),
    # path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetView.as_view(), name='password_reset_confirm'),
   # path('activate-user/<uidb64>/<token>',activate_user, name='activate_user'),

]