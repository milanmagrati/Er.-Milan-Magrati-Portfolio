from django import forms
from portfolio.models import (
    PersonalProfile,
    Designation,
    SkillCategory,
    Skill,
    Experience,
    Education,
    Training,
    Project,
    ProjectImage,
    Service,
    Certification,
    ResumeFile,
    SiteSettings,
    SocialLink,
)


class BaseStyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control file-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control', 'rows': 4})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class PersonalProfileForm(BaseStyledForm):
    class Meta:
        model = PersonalProfile
        fields = '__all__'


class DesignationForm(BaseStyledForm):
    class Meta:
        model = Designation
        fields = '__all__'


class SkillCategoryForm(BaseStyledForm):
    class Meta:
        model = SkillCategory
        fields = '__all__'


class SkillForm(BaseStyledForm):
    class Meta:
        model = Skill
        fields = '__all__'
        widgets = {
            'proficiency': forms.NumberInput(attrs={'min': 1, 'max': 100}),
        }


class ExperienceForm(BaseStyledForm):
    class Meta:
        model = Experience
        fields = '__all__'


class EducationForm(BaseStyledForm):
    class Meta:
        model = Education
        fields = '__all__'


class TrainingForm(BaseStyledForm):
    class Meta:
        model = Training
        fields = '__all__'


class ProjectForm(BaseStyledForm):
    class Meta:
        model = Project
        fields = [
            'title', 'category', 'short_description', 'detailed_description',
            'thumbnail', 'technologies', 'github_url', 'live_demo_url',
            'is_featured', 'completion_date', 'display_order', 'is_active'
        ]


class ProjectImageForm(BaseStyledForm):
    class Meta:
        model = ProjectImage
        fields = ['image', 'caption', 'display_order']


class ServiceForm(BaseStyledForm):
    class Meta:
        model = Service
        fields = '__all__'


class CertificationForm(BaseStyledForm):
    class Meta:
        model = Certification
        fields = '__all__'


class ResumeFileForm(BaseStyledForm):
    class Meta:
        model = ResumeFile
        fields = ['title', 'file', 'is_active']


class SiteSettingsForm(BaseStyledForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'


class SocialLinkForm(BaseStyledForm):
    class Meta:
        model = SocialLink
        fields = '__all__'
