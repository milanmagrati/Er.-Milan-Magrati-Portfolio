import base64
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count

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
    ContactMessage,
    SiteSettings,
    SocialLink,
)
from .forms import (
    PersonalProfileForm,
    DesignationForm,
    SkillCategoryForm,
    SkillForm,
    ExperienceForm,
    EducationForm,
    TrainingForm,
    ProjectForm,
    ProjectImageForm,
    ServiceForm,
    CertificationForm,
    ResumeFileForm,
    SiteSettingsForm,
    SocialLinkForm,
)


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


# Authentication Views
def dashboard_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                next_url = request.GET.get('next', 'dashboard:home')
                return redirect(next_url)
            else:
                messages.error(request, "Access restricted to staff/admin accounts.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'dashboard/login.html', {'form': form})


@login_required
def dashboard_logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('dashboard:login')


# Dashboard Home
@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def dashboard_home(request):
    stats = {
        'total_projects': Project.objects.count(),
        'total_skills': Skill.objects.count(),
        'total_experience': Experience.objects.count(),
        'total_certifications': Certification.objects.count(),
        'total_messages': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'active_designations': Designation.objects.filter(is_active=True).count(),
        'total_services': Service.objects.count(),
    }
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
    recent_projects = Project.objects.order_by('-id')[:4]
    profile = PersonalProfile.objects.first()

    return render(request, 'dashboard/home.html', {
        'stats': stats,
        'recent_messages': recent_messages,
        'recent_projects': recent_projects,
        'profile': profile,
    })


# Profile Management
@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def profile_edit(request):
    profile = PersonalProfile.objects.first()
    if not profile:
        profile = PersonalProfile.objects.create(name="Milan Magrati")

    if request.method == 'POST':
        form = PersonalProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            instance = form.save(commit=False)
            
            # Check if cropped image base64 data was supplied
            cropped_data = request.POST.get('cropped_image_data', '').strip()
            if cropped_data and ';base64,' in cropped_data:
                try:
                    format_str, img_str = cropped_data.split(';base64,')
                    ext = 'jpg'
                    if 'png' in format_str:
                        ext = 'png'
                    elif 'webp' in format_str:
                        ext = 'webp'
                    file_name = f"profile_cropped_{instance.id or 'avatar'}.{ext}"
                    data = base64.b64decode(img_str)
                    instance.profile_image.save(file_name, ContentFile(data), save=False)
                except Exception as e:
                    pass

            instance.save()
            messages.success(request, "Profile updated successfully! Changes are live on your portfolio.")
            return redirect('dashboard:profile')
    else:
        form = PersonalProfileForm(instance=profile)

    return render(request, 'dashboard/profile_edit.html', {'form': form, 'profile': profile})


# Designations Management
@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def designations_list(request):
    designations = Designation.objects.order_by('display_order')
    form = DesignationForm()
    
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New designation added to animated hero text!")
            return redirect('dashboard:designations')

    return render(request, 'dashboard/designations_list.html', {
        'designations': designations,
        'form': form,
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def designation_edit(request, pk):
    item = get_object_or_404(Designation, pk=pk)
    if request.method == 'POST':
        form = DesignationForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Designation updated successfully.")
            return redirect('dashboard:designations')
    else:
        form = DesignationForm(instance=item)
    return render(request, 'dashboard/form_edit.html', {
        'form': form,
        'title': 'Edit Designation',
        'back_url': 'dashboard:designations',
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def designation_delete(request, pk):
    item = get_object_or_404(Designation, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Designation removed.")
    return redirect('dashboard:designations')


# Skills Management
@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def skills_list(request):
    categories = SkillCategory.objects.prefetch_related('skills').order_by('display_order')
    return render(request, 'dashboard/skills_list.html', {'categories': categories})


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def skill_create(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill added successfully.")
            return redirect('dashboard:skills')
    else:
        form = SkillForm()
    return render(request, 'dashboard/form_edit.html', {
        'form': form,
        'title': 'Add New Skill',
        'back_url': 'dashboard:skills',
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated.")
            return redirect('dashboard:skills')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'dashboard/form_edit.html', {
        'form': form,
        'title': f'Edit Skill: {skill.name}',
        'back_url': 'dashboard:skills',
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, f"Skill '{skill.name}' removed.")
    return redirect('dashboard:skills')


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def category_create(request):
    if request.method == 'POST':
        form = SkillCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New skill category created.")
            return redirect('dashboard:skills')
    else:
        form = SkillCategoryForm()
    return render(request, 'dashboard/form_edit.html', {
        'form': form,
        'title': 'Add Skill Category',
        'back_url': 'dashboard:skills',
    })


# Projects Management
@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def projects_list(request):
    projects = Project.objects.all().order_by('display_order', '-id')
    return render(request, 'dashboard/projects_list.html', {'projects': projects})


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            messages.success(request, f"Project '{project.title}' created successfully!")
            return redirect('dashboard:projects')
    else:
        form = ProjectForm()
    return render(request, 'dashboard/form_edit.html', {
        'form': form,
        'title': 'Add New Project',
        'back_url': 'dashboard:projects',
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f"Project '{project.title}' updated.")
            return redirect('dashboard:projects')
    else:
        form = ProjectForm(instance=project)
    
    gallery_form = ProjectImageForm()
    return render(request, 'dashboard/project_edit.html', {
        'form': form,
        'project': project,
        'gallery_form': gallery_form,
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def project_image_add(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.project = project
            img.save()
            messages.success(request, "Gallery image added.")
    return redirect('dashboard:project-edit', pk=project.pk)


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def project_image_delete(request, pk):
    img = get_object_or_404(ProjectImage, pk=pk)
    project_pk = img.project.pk
    if request.method == 'POST':
        img.delete()
        messages.success(request, "Gallery image deleted.")
    return redirect('dashboard:project-edit', pk=project_pk)


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, f"Project '{project.title}' deleted.")
    return redirect('dashboard:projects')


# Experience Management
@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def experience_list(request):
    experiences = Experience.objects.order_by('display_order', '-id')
    return render(request, 'dashboard/experience_list.html', {'experiences': experiences})


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def experience_create(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Experience record added.")
            return redirect('dashboard:experience')
    else:
        form = ExperienceForm()
    return render(request, 'dashboard/form_edit.html', {
        'form': form,
        'title': 'Add Work Experience',
        'back_url': 'dashboard:experience',
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def experience_edit(request, pk):
    item = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Experience updated.")
            return redirect('dashboard:experience')
    else:
        form = ExperienceForm(instance=item)
    return render(request, 'dashboard/form_edit.html', {
        'form': form,
        'title': f'Edit Experience: {item.company}',
        'back_url': 'dashboard:experience',
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def experience_delete(request, pk):
    item = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Experience deleted.")
    return redirect('dashboard:experience')


# Education & Training Management
@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def education_list(request):
    educations = Education.objects.order_by('display_order', '-id')
    trainings = Training.objects.order_by('display_order', '-id')
    return render(request, 'dashboard/education_list.html', {
        'educations': educations,
        'trainings': trainings,
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def education_create(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Education record added.")
            return redirect('dashboard:education')
    else:
        form = EducationForm()
    return render(request, 'dashboard/form_edit.html', {
        'form': form,
        'title': 'Add Education Record',
        'back_url': 'dashboard:education',
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def education_edit(request, pk):
    item = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Education updated.")
            return redirect('dashboard:education')
    else:
        form = EducationForm(instance=item)
    return render(request, 'dashboard/form_edit.html', {
        'form': form,
        'title': f'Edit Education: {item.degree}',
        'back_url': 'dashboard:education',
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def education_delete(request, pk):
    item = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Education deleted.")
    return redirect('dashboard:education')


# Services Management
@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def services_list(request):
    services = Service.objects.order_by('display_order')
    return render(request, 'dashboard/services_list.html', {'services': services})


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service added.")
            return redirect('dashboard:services')
    else:
        form = ServiceForm()
    return render(request, 'dashboard/form_edit.html', {
        'form': form,
        'title': 'Add New Service',
        'back_url': 'dashboard:services',
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def service_edit(request, pk):
    item = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated.")
            return redirect('dashboard:services')
    else:
        form = ServiceForm(instance=item)
    return render(request, 'dashboard/form_edit.html', {
        'form': form,
        'title': f'Edit Service: {item.title}',
        'back_url': 'dashboard:services',
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def service_delete(request, pk):
    item = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Service deleted.")
    return redirect('dashboard:services')


# Certifications Management
@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def certifications_list(request):
    certs = Certification.objects.order_by('display_order', '-id')
    return render(request, 'dashboard/certifications_list.html', {'certifications': certs})


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def certification_create(request):
    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Certification added.")
            return redirect('dashboard:certifications')
    else:
        form = CertificationForm()
    return render(request, 'dashboard/form_edit.html', {
        'form': form,
        'title': 'Add Certification',
        'back_url': 'dashboard:certifications',
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def certification_edit(request, pk):
    item = get_object_or_404(Certification, pk=pk)
    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Certification updated.")
            return redirect('dashboard:certifications')
    else:
        form = CertificationForm(instance=item)
    return render(request, 'dashboard/form_edit.html', {
        'form': form,
        'title': f'Edit Certification: {item.name}',
        'back_url': 'dashboard:certifications',
    })


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def certification_delete(request, pk):
    item = get_object_or_404(Certification, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Certification deleted.")
    return redirect('dashboard:certifications')


# Resume Manager
@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def resume_list(request):
    resumes = ResumeFile.objects.all()
    if request.method == 'POST':
        form = ResumeFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New CV uploaded and set as active download!")
            return redirect('dashboard:resume')
    else:
        form = ResumeFileForm()
    return render(request, 'dashboard/resume_list.html', {'resumes': resumes, 'form': form})


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def resume_set_active(request, pk):
    resume = get_object_or_404(ResumeFile, pk=pk)
    resume.is_active = True
    resume.save()
    messages.success(request, f"'{resume.title}' is now set as the active CV download.")
    return redirect('dashboard:resume')


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def resume_delete(request, pk):
    resume = get_object_or_404(ResumeFile, pk=pk)
    if request.method == 'POST':
        resume.delete()
        messages.success(request, "CV file deleted.")
    return redirect('dashboard:resume')


# Messages Inbox
@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def messages_list(request):
    msgs = ContactMessage.objects.order_by('is_read', '-created_at')
    return render(request, 'dashboard/messages_list.html', {'messages_list': msgs})


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save()
    return render(request, 'dashboard/message_detail.html', {'message_item': msg})


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def message_toggle_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = not msg.is_read
    msg.save()
    return redirect('dashboard:messages')


@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, "Message deleted.")
    return redirect('dashboard:messages')


# Site Settings
@user_passes_test(is_staff_user, login_url='/dashboard/login/')
def settings_edit(request):
    site_settings = SiteSettings.objects.first()
    if not site_settings:
        site_settings = SiteSettings.objects.create()

    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=site_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Site settings and section visibility updated!")
            return redirect('dashboard:settings')
    else:
        form = SiteSettingsForm(instance=site_settings)

    return render(request, 'dashboard/settings_edit.html', {'form': form, 'site_settings': site_settings})
