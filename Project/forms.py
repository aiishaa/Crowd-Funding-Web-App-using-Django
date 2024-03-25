from django import forms
from .models import Project, Category

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
    

    