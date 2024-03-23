from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomForm(AbstractUser):
    phone = models.CharField(max_length=50, unique=True)
    profile_picture = models.ImageField(upload_to='user/profile_pictures/', blank=True)

    def __str__(self):
        return self.username
    
    @property
    def image_url(self):
        return f'/media/{self.profile_picture}'
