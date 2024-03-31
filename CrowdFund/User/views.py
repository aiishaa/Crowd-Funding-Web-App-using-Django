# from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, EditProfileForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from .utils import token_generator
from django.urls import reverse
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import os
from django.conf import settings

User = get_user_model()

class verificationView(View):
    def isTokenExpired(self, activationTime):
        # Set expiry duration to 1 day
        expiryDuration = timedelta(days=1)
        expiryDate = activationTime + expiryDuration
        now = timezone.localtime(timezone.now())
        return now > expiryDate


    def get(self, request, uidb64, token):
        try:
            id = urlsafe_base64_decode(force_str(uidb64))
            user = User.objects.get(pk=id)
            if not user.is_active:
                if token_generator.check_token(user, token):
                    if self.isTokenExpired(user.date_joined):
                        messages.error(request, "Activation link has expired, Another one will be sent to you")
                        print("Activation link has expired, Another one will be sent to you")
                        sendMail(request, user)
                    else:  
                        user.is_active = True
                        user.save()
                        messages.success(request, "Account activated successfully")
                        print("Account activated successfully")
                        return redirect("login")
                else:
                    messages.error(request, "Invalid activation link")
                    print("Invalid activation link")
            else:
                messages.error(request, "User is already activated")
                print("User is already activated")
                return redirect('login')
        except Exception as e:
            print(e)
            print(User.objects.all())
        return redirect("login")
    
#send email
def sendMail(request, user):
    domain = get_current_site(request).domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
    activate_url = "http://" + domain + link

    email_subject = "Verification mail"
    email_body = f"Hi {user.username},\n\
        Please verify your email to be able to login into your account by clicking the following link:\n \
        {activate_url}"
    from_email = 'aishafathy999@example.com'
    recipient_list = [user.email]

    send_mail(email_subject, email_body, from_email, recipient_list)

# go to the landing page
def landing(request):
    return render(request, 'landing.html')

# Create your views here.
def createUser(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set user as inactive until email verification
            # user.date_joined = datetime.now()
            user.save()
            sendMail(request, user)
            messages.success(request, "Your account has been created successfully")
            # print(form)
            return redirect("landing") 
            # return HttpResponse("Account created successfully")
        else:
            messages.error(request, "Error")
    else:
        form = SignupForm()
    return render(request, "register.html", context={"form": form})

#Login to the system
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if(user is not None and user.is_active):
                login(request, user)
                return redirect("home") 
        else:
            messages.error(request, "Wrong email or password")
    else:
        form = LoginForm()
    return render(request, "login.html", context={"form": form})

# Logout from the system
@login_required
def logout_user(request):
    logout(request)
    return redirect('landing')

@login_required
def goHome(request):
    return render(request, 'home.html')

@login_required
def showProfile(request, id):
    user = User.objects.get(id=id)
    return render(request, 'user/profile.html', context={"user": user})

@login_required
def editProfile(request, id):
    user = User.objects.get(id=id)
    old_profile_pic = user.profile_picture
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # Remove old image if user upload a new one or clear the field
            new_profile_pic = form.cleaned_data.get('profile_picture')
            if old_profile_pic and new_profile_pic != old_profile_pic:
                old_picture_path = os.path.join(settings.MEDIA_ROOT, str(old_profile_pic))
                if os.path.exists(old_picture_path):
                    os.remove(old_picture_path)
            form.save()
            return redirect('show profile', id=user.id)
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'user/editProfile.html', context={"form": form})



@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if request.user.check_password(password):
            # User entered correct password
            user = request.user
            user.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect('landing')
        else:
            # Incorrect password
            messages.error(request, "Incorrect password. Please try again.")
    return render(request, 'delete_account.html')
