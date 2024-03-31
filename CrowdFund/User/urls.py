from django.urls import path
from .views import createUser, goHome, login_user, logout_user, verificationView, showProfile, editProfile,delete_account

urlpatterns = [
    path('register/', createUser, name="register"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('activate<uidb64>/<token>/', verificationView.as_view(), name="activate"),
    path('home/', goHome, name="home"),
    path('profile/<int:id>', showProfile, name="show profile"),
    path('delete_account/', delete_account, name="delete_account"),
    path('editprofile/<int:id>', editProfile, name="edit profile")
] 
