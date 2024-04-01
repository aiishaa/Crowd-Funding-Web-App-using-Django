"""
URL configuration for CrowdFund project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from User.views import landing

urlpatterns = [
    path('admin/', include("Admin.urls")),
    # path('admin/', admin.site.urls),
    path('landing/', landing, name="landing"),
    path('', landing, name="landing"),
    path('user/', include("User.urls")), 
    path('project/', include("Project.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
