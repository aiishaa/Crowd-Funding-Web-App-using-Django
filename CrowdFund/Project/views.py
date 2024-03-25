from django.shortcuts import render, redirect
from .forms import ProjectForm
from django.http import HttpResponse
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import math

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


def userProjects(request, id):
    try:
        projects = Project.objects.filter(p_owner_id=id)
        for i in range(0, len(projects)):
            projects[i].category_name = Category.objects.get(id=projects[i].category_id)
            projects[i].owner_name = User.objects.get(id=projects[i].p_owner_id)
        return render(request, r"user_projects.html", context={"projects": projects})
    except Exception as e:
        return HttpResponse(e)


def otherProjects(request, id):
    try:
        reported_projects = list(Report.objects.filter(user_id=id).values_list('project_id', flat=True))
        projects = Project.objects.exclude(p_owner_id=id) 
        projects = projects.exclude(id__in=reported_projects)

        for i in range(0, len(projects)):
                projects[i].category_name = Category.objects.get(id=projects[i].category_id)
                projects[i].owner_name = User.objects.get(id=projects[i].p_owner_id)

        return render(request, r"other_projects.html", context={"projects": projects, "userID": id})
    
    except Exception as e:
        return HttpResponse(e)


def otherProjectDesc(request, userID, proID):

    try:

        # prepare average rating.
        rating = list(Rate.objects.filter( project_id=proID).values_list('rateValue', flat=True))
        average_rating = 0
        if len(rating) > 1:
            for value in rating:
                average_rating+=value
            average_rating= average_rating/len(rating)

        # 4 other similar projects based on project tags.
        assosiated_tags = list(Project.objects.get(id=proID).tags.all().values_list('name', flat=True))
        similar_projects = Project.objects.exclude(p_owner_id=userID) 
        similar_projects = similar_projects.filter(tags__name__in=assosiated_tags)

        # roject pictures to be displayed in a slider.
        pictures = Picture.objects.filter(project_id=proID)

        # project data.
        project = Project.objects.filter(id=proID)

        return render(request, r"other_project_desc.html", context={"project": project, "userID": userID, "averageRate": average_rating, "images": pictures, "similarProjects": similar_projects})
    
    except Exception as e:
        return HttpResponse(e)

    