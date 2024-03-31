from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import CustomForm
from django.contrib.auth import get_user_model

User = get_user_model()
class SignupForm(UserCreationForm):
    class Meta:
        model = CustomForm
        fields = ["first_name", "last_name", "username", "email", "phone", "profile_picture", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.startswith('+20') or len(phone) > 13:
            raise forms.ValidationError('Please enter a valid Egyptian phone number starting with +20')
        return phone

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), required=False, initial='')
    password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomForm
        fields = ["first_name", "last_name", "username", "email", "phone", "profile_picture", "birthdate", "facebook_profile", "country"]

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.startswith('+20') or len(phone) > 13:
            raise forms.ValidationError('Please enter a valid Egyptian phone number starting with +20')
        return phone

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2