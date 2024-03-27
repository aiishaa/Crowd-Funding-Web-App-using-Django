from django.shortcuts import render, redirect, reverse
from .forms import *
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
        if len(rating) > 0:
            for value in rating:
                average_rating+=value
            average_rating= int(average_rating/len(rating))

        # add rate.
        project = Project.objects.get(id=proID)
        user = User.objects.get(id=userID)
        rate_instance = Rate.objects.filter(project=project, user=user).first()

        try:
            rateform = AddRate(instance=rate_instance) 
        except:
            rateform = AddRate()

        if request.method == 'POST':
            
            if rate_instance:
                rateform = AddRate(request.POST, instance=rate_instance) 
            else:
                rateform = AddRate(request.POST)
                rateform.instance.project_id=proID
                rateform.instance.user_id=userID

            if rateform.is_valid():

                if rateform.instance.rateValue == 0:
                    Rate.objects.get(project=project, user=user).delete()
                else:
                    rate = rateform.save()  

                url = reverse('other project desc', args=[userID, proID])
                return redirect(url)


        # 4 other similar projects based on project tags.
        assosiated_tags = list(Project.objects.get(id=proID).tags.all().values_list('name', flat=True))
        similar_projects = Project.objects.exclude(p_owner_id=userID) 
        similar_projects = similar_projects.filter(tags__name__in=assosiated_tags)

        # project pictures to be displayed in a slider.
        pictures = Picture.objects.filter(project_id=proID)

        # project data.
        project = Project.objects.get(id=proID)
        project.category_name = Category.objects.get(id=project.category_id)
        project.owner_name = User.objects.get(id=project.p_owner_id)

        # project comments
        comments = Comment.objects.filter(project_id=proID)

        return render(request, r"other_project_desc.html", context={"project": project, "userID": userID, "averageRate": average_rating, "images": pictures, "comments": comments, "similarProjects": similar_projects, "rateForm": rateform})
    
    except Exception as e:
        return HttpResponse(e)

    