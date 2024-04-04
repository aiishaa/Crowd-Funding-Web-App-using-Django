from django import forms
from .models import Project, Category, Rate, Comment, Donation, Report, FeaturedProjects
from django.core.validators import MaxValueValidator

class ProjectForm(forms.ModelForm):
    tags = forms.CharField(max_length=100, required=False, help_text="Enter tags separated by commas")

    class Meta:
        model = Project
        fields = ('title', 'description', 'category', 'tags', 'total_target', 'start_time', 'end_time')
        
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        to_field_name='id',
        required=True
    )

    def clean_end_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        if (end_time > start_time):
            return end_time
        else:
            raise forms.ValidationError("End date must be after start date")

class CategoryForm(forms.ModelForm):
    category_name = forms.CharField(
        max_length=50, 
        required=False
    )
    class Meta:
        model = Category
        fields = ['category_name']
        
class AddRate(forms.ModelForm):
    
    class Meta:
        model= Rate
        fields= ('rateValue',)

class AddComment(forms.ModelForm):
    
    class Meta:
        model= Comment
        fields= ('comment_description',)


class AddDonation(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        max_value = kwargs.pop('max_value', None)
        super(AddDonation, self).__init__(*args, **kwargs)
        if max_value is not None:
            self.fields['donation_value'].validators.append(MaxValueValidator(max_value))
    
    class Meta:
        model= Donation
        fields= ('donation_value',)


class AddReport(forms.ModelForm):
    
    class Meta:
        model= Report
        fields= ()
        

class FeaturedProjectsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        previous_projects = kwargs.pop('initial', {}).get('previous_projects', [])
        super(FeaturedProjectsForm, self).__init__(*args, **kwargs)
        if previous_projects:
            selected_projects = Project.objects.filter(id__in=previous_projects)
            self.fields['projects'].initial = selected_projects


    projects = forms.ModelMultipleChoiceField(queryset=Project.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = FeaturedProjects
        fields = []  

    def clean_projects(self):
        selected_projects = self.cleaned_data['projects']
        if len(selected_projects) > 5:
            raise forms.ValidationError("You can only select maximum 5 projects.")
        return selected_projects

    





    

    
