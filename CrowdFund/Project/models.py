from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def project_images_path(instance, filename):
    folder_name = instance.project.title.replace(" ", "_") 
    return f'projects/{folder_name}/{filename}'

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.category_name

class Tag(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    p_owner = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    description = models.TextField()
    total_target = models.DecimalField(max_digits=20, decimal_places=5)
    start_time = models.DateField()
    end_time = models.DateField()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Picture(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=project_images_path, blank=True)
    
    @property
    def image_url(self):
        return f'/media/{self.picture}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    comment_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donation_value = models.DecimalField(max_digits=20, decimal_places=5)
    created_at = models.DateTimeField(auto_now_add=True)

class Rate(models.Model):
    rate_choices = { 0: '0', 1:'1', 2:'2', 3: '3', 4:'4', 5:'5' }
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rateValue = models.IntegerField(choices=rate_choices)
