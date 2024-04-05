from django.shortcuts import render, redirect, reverse,get_object_or_404
from .forms import *
from django.http import HttpResponse
from .models import *
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from decimal import Decimal
from django.db.models import F, FloatField, ExpressionWrapper

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
        for project in projects:
            project.pictures = Picture.objects.filter(project=project)
        return render(request, "user_projects.html", context={"projects": projects})
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

        # ============================ Rating ============================ 

        # ===> prepare average rating.
        rating = list(Rate.objects.filter( project_id=proID).values_list('rateValue', flat=True))
        average_rating = 0
        if len(rating) > 0:
            for value in rating:
                average_rating+=value
            average_rating= int(average_rating/len(rating))

        # ===> add rate.
        project = Project.objects.get(id=proID)
        user = User.objects.get(id=userID)
        rate_instance = Rate.objects.filter(project=project, user=user).first()

        try:
            rateform = AddRate(instance=rate_instance) 
        except:
            rateform = AddRate()

        if request.method == 'POST' and 'rate_submit' in request.POST:
            
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
    
            
        # ============================ Comments ============================ 

        # ===> prepare the project comments to be displayed at first.
        comments = Comment.objects.filter(project_id=proID)
        for i in range(0, len(comments)):
            user = User.objects.get(id=comments[i].user_id)
            comments[i].user_profile_picture = user.image_url
            comments[i].user_name = user.__str__()

        # ===> add comment.

        commentForm = AddComment()

        if request.method == 'POST' and 'comment_submit' in request.POST:
            
            commentForm = AddComment(request.POST)
            commentForm.instance.project_id=proID
            commentForm.instance.user_id=userID

            if commentForm.is_valid():

                comment = commentForm.save()  
                url = reverse('other project desc', args=[userID, proID])
                return redirect(url)

            
        # ============================ donation ============================ 
            
        # ===> total donation
        donation = list(Donation.objects.filter(project_id=proID).values_list('donation_value', flat=True))
        total_donation = 0
        for don in donation:
            total_donation += don
        
        # ===> donation form
        project = Project.objects.get(id=proID)
        user = User.objects.get(id=userID)
        donation_instance = Donation.objects.filter(project=project, user=user).first()

        try:
            donationform = AddDonation(instance=donation_instance, max_value=(project.total_target-total_donation))
        except:
            donationform = AddDonation(max_value=(project.total_target-total_donation))

        if request.method == 'POST' and 'donation_submit' in request.POST:
            
            if donation_instance:
                donationform = AddDonation(request.POST, instance=donation_instance, max_value=(project.total_target-total_donation)) 
            else:
                donationform = AddDonation(request.POST, max_value=(project.total_target-total_donation))
                donationform.instance.project_id=proID
                donationform.instance.user_id=userID

            if donationform.is_valid():

                if donationform.instance.donation_value == 0:
                    Donation.objects.get(project=project, user=user).delete()

                else:
                    donation = donationform.save()  

            
            url = reverse('other project desc', args=[userID, proID])
            return redirect(url)
        
        
        # ======================= reporting projects ========================= 
                
        reportform = AddReport()

        if request.method == 'POST' and 'report_submit' in request.POST:
            
            reportform = AddReport(request.POST)
            reportform.instance.project_id=proID
            reportform.instance.user_id=userID

            if reportform.is_valid():
                report = reportform.save()  
                url = reverse('other projects', args=[userID,])
                return redirect(url)

        

        # ======================= similar projects ========================= 

        # 4 other similar projects based on project tags.
        assosiated_tags = list(Project.objects.get(id=proID).tags.all().values_list('name', flat=True)) 
        reported_projects = list(Report.objects.filter(user_id=userID).values_list('project_id', flat=True))
        similar_projects = Project.objects.exclude(p_owner_id=userID)
        similar_projects = similar_projects.exclude(id__in=reported_projects) 
        similar_projects = similar_projects.filter(tags__name__in=assosiated_tags)

        if len(similar_projects) > 4:
            similar_projects = similar_projects[:4]

        for i in range(0, len(similar_projects)):
                similar_projects[i].category_name = Category.objects.get(id=similar_projects[i].category_id)
                similar_projects[i].owner_name = User.objects.get(id=similar_projects[i].p_owner_id)


        # ================================================================== 

        # project pictures to be displayed in a slider.
        pictures = Picture.objects.filter(project_id=proID)

        # project data.
        project = Project.objects.get(id=proID)
        project.category_name = Category.objects.get(id=project.category_id)
        project.owner_name = User.objects.get(id=project.p_owner_id)


        return render(request, r"other_project_desc.html", context={"project": project, "userID": userID, "averageRate": average_rating, "images": pictures, "comments": comments, "similarProjects": similar_projects, "totalDonation": total_donation, "rateForm": rateform, "commentForm": commentForm, "donationForm": donationform, "reportForm": reportform})
    
    except Exception as e:
        return HttpResponse(e)
    

def deleteComment(request, userID, proID, commentID):

    comment = Comment.objects.get(id=commentID)
    comment.delete()
    url = reverse('other project desc', args=[userID, proID])
    return redirect(url)


@login_required
def project_edit(request, id):
    try:
        project = get_object_or_404(Project, id=id)
        if request.method == 'POST':
            form = ProjectForm(request.POST, request.FILES, instance=project)  # Include request.FILES here for handling file uploads
            if form.is_valid():
                # Save the project form
                project = form.save(commit=False)
                
                # Process tags
                tags_input = request.POST.get('tags', '')
                tag_names = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
                project.tags.clear()  # Clear existing tags
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    project.tags.add(tag)
                
                # Save the project
                project.save()

                # Handle project pictures
                if 'picture' in request.FILES:
                    # Delete old pictures associated with the project
                    project.picture_set.all().delete()
                    
                    # Save new pictures
                    for file in request.FILES.getlist('picture'):
                        Picture.objects.create(project=project, picture=file)

                return redirect('user projects', id=project.p_owner_id)
            else:
                print("Form errors:", form.errors)
        else:
            form = ProjectForm(instance=project)
        return render(request, 'edit_project.html', {'form': form, 'project': project})
    except Project.DoesNotExist:
        return HttpResponse("Project not found")
    
    

def project_details(request, id):
    try:
        project = get_object_or_404(Project, id=id)
        project_pictures = Picture.objects.filter(project=project)

        # Retrieve all comments for the project
        comments = Comment.objects.filter(project=project)

        # Set the user_profile_picture attribute for each comment
        for comment in comments:
            user = User.objects.get(id=comment.user_id)
            comment.user_profile_picture = user.image_url

        
        total_donation = Donation.objects.filter(project=project).aggregate(Sum('donation_value'))['donation_value__sum']
        total_donation = total_donation or 0
        
       
        # Rating
        average_rating = calculate_average_rating(project)
        
        total_target = project.total_target
        total_donation_percentage = (total_donation / total_target) * 100 if total_target != 0 else 0
        can_delete_project = total_donation_percentage <= 25

        return render(request, 'project_details.html', {
            'project': project,
            'project_pictures': project_pictures,
            'comments': comments,
            'average_rating': average_rating,
            'total_donation': total_donation,
            # 'total_rate': total_rate,
            # 'total_rate_count': total_rate_count,
            'can_delete_project': can_delete_project
        })
    except Project.DoesNotExist:
        return HttpResponse("Project not found")


def delete_project(request, project_id):
    project = Project.objects.get(id=project_id)
    total_donation = project.total_donation
    total_target = project.total_target

    if total_donation < Decimal('0.25') * total_target:
        project.delete()  # Hard delete the project
        messages.success(request, 'Project has been deleted successfully.')
        # Redirect to user projects view with the owner's ID
        return redirect(reverse('user projects', kwargs={'id': project.p_owner_id}))  
    else:
        messages.error(request, 'Project cannot be deleted as donations exceed 25% of the target.')
        # Redirect to project details view with the project ID
        return redirect('project_details', project_id=project_id)


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    project_id = comment.project.id  # Retrieve the project ID before deleting the comment
    comment.delete()
    return redirect('project_details', id=project_id)


def calculate_average_rating(project):
    # Retrieve all ratings for the project
    ratings = project.rate_set.all()

    # Check if there are any ratings for the project
    if ratings.exists():
        # Calculate the sum of all ratings
        total_rating = sum(rating.rateValue for rating in ratings)
        # Calculate the average rating
        average_rating = (total_rating / (ratings.count() * 5)) * 100  # Assuming rating scale is from 1 to 5
    else:
        average_rating = 0

    # Format the average rating as a percentage string with one decimal place
    formatted_rating = "{:.0f}%".format(average_rating)

    
    return formatted_rating

def get_category_projects(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    projects = Project.objects.filter(category=category)
    context = {
        'category': category,
        'projects': projects
    }
    return render(request, 'category_projects.html', context)



def search_projects(request):
    query = request.GET.get('search_query')
    projects = Project.objects.all()
    if query:
        # Filter projects by category name
        category_query = Q(category__category_name__icontains=query)
        # Filter projects by tags
        tags_query = Q(tags__name__icontains=query)
        print('-'*50)
        print(tags_query)
        print(category_query)
        print('-'*50)
        # Combine the queries using OR condition
        projects = projects.filter(category_query | tags_query).distinct()
    
    return render(request, 'search_results.html', {'projects': projects, 'query':query})


