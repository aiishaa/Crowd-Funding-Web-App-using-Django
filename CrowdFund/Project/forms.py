from django import forms
from .models import Project, Category, Rate, Comment, Donation, Report
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
    

    