from django.shortcuts import render, redirect
from .forms import ProjectForm
from .models import Project, Tag, Picture
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

@login_required
def createProject(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        f_project = ProjectForm(request.POST)
        if f_project.is_valid():
            project = f_project.save(commit=False)
            project.p_owner = user
            project.save()

            # Process tags
            tags_input = request.POST.get('tags', '')
            tag_names = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag, created= Tag.objects.get_or_create(name=tag_name)
                project.tags.add(tag)
                
            # Process images
            images = request.FILES.getlist('picture')
            for image in images:
                Picture.objects.create(project = project, picture = image)
    else:
        f_project = ProjectForm()
    return render(request, 'create_project.html', context={"projectForm": f_project})
