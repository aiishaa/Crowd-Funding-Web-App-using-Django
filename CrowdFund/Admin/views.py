from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.urls import reverse
from Project.forms import CategoryForm, FeaturedProjectsForm
from User.forms import LoginForm
from Project.models import FeaturedProjects, Project

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
def manage_featured_projects(request):
    try:
        featured_projects = list(FeaturedProjects.objects.all().values_list('project_id', flat=True))

        if request.method == 'POST':
            form = FeaturedProjectsForm(request.POST, initial={'previous_projects': featured_projects})
            if form.is_valid():
                
                print('-'*40)
                print(form.data)
                print('-'*40)

                selected_projects = form.data.getlist('projects')

                print('-'*40)
                print(selected_projects)
                print('-'*40)

                # Remove previous featured projects
                FeaturedProjects.objects.all().delete()  
                
                for pid in selected_projects:
                    project = Project.objects.get(id=pid)
                    FeaturedProjects.objects.create(project=project)
                
                messages.success(request, 'Projects added successfully.')
                url = reverse('featured_projects')
                return redirect(url)
            
            else:
                print('-'*40)
                print("Form errors:", form.errors)  
                print('-'*40)
        else:
            form = FeaturedProjectsForm(initial={'previous_projects': featured_projects})
    
        return render(request, 'customadmin/featured_projects.html', {'form': form})
    
    except Exception as e:
        return HttpResponse(e)





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

