# forms.py

from django import forms
from Capp.models import CustomUser

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password', 'mobile_phone', 'profile_picture']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        if not mobile_phone.startswith('+20'):
            raise forms.ValidationError("Please enter a valid Egyptian phone number")
        return mobile_phone