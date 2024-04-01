from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.urls import reverse
from Project.forms import CategoryForm
from User.forms import LoginForm

# Create your views here.

User = get_user_model()

def admin_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return render(request, 'customadmin/index.html')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'error': 'Authentication failed'})

@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully')
            return render(request, 'customadmin/add_category.html', {'form': form})  
    else:
        form = CategoryForm()

    return render(request, 'customadmin/add_category.html', {'form': form})

