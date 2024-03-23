from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from Capp.models import CustomUser
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import UpdateView
# from Capp.utils import send_activation_email, send_password_reset_email
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
# from .utils import generate_token
# from django.core.mail import EmailMessage
# from django.conf import settings
# import threading

"""class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('crowdfunding/activate.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    EmailThread(email).start()


def activate_user(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = CustomUser.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('login'))

    return render(request, 'crowdfunding/activate-failed.html', {"user": user})

#
def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = CustomUser.objects.get(email=email)
                send_password_reset_email(user)  # Send password reset email
                return redirect('password_reset_done')
            except CustomUser.DoesNotExist:
                pass  # Handle invalid email gracefully
    else:
        form = PasswordResetForm()
    return render(request, 'crowdfunding/resetpass.html', {'form': form})

    class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = '/password-reset/done/'

"""


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #user = form.save(commit=False)
            #user.is_active = False
            #user.save()
            #send_activation_email(user, request)
            return redirect('registration_success')
    else:
        form = RegistrationForm()
    return render(request, 'crowdfunding/registration.html', {'form': form})


def registration_success(request):
    return render(request, 'crowdfunding/login.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        #if user is not None and user.is_active: #for activation func
        if user is not None:

            login(request, user)
            return redirect('crowdfunding/project_start.html')  # Redirect to dashboard or any other page
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'crowdfunding/login.html')

def project_start(request):
    return render(request, 'crowdfunding/project_start.html')





    