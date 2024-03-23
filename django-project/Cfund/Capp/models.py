from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

class CustomUserManager(BaseUserManager):
    def _validate_mobile_phone(self, value):
        # Custom validation for Egyptian phone numbers
        if not re.match(r'^\+20\d{10}$', value):
            raise ValidationError('Please enter a valid Egyptian phone number.')

    def _validate_password_strength(self, value):
        # Custom validation for password strength
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not any(char.isdigit() for char in value):
            raise ValidationError('Password must contain at least one digit.')
        if not any(char.isalpha() for char in value):
            raise ValidationError('Password must contain at least one letter.')

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        self._validate_password_strength(password)
        self._validate_mobile_phone(extra_fields.get('mobile_phone', ''))
        extra_fields.setdefault('is_active', True) #true by default -Temporarily-
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile_phone = models.CharField(max_length=13, validators=[RegexValidator(regex=r'^\+20\d{10}$', message='Please enter a valid Egyptian phone number.')])
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    activation_key = models.CharField(max_length=40, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile_phone']

    class Meta:
        app_label = 'Capp'
    def __str__(self):
        return self.email


