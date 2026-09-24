from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Auth
    path('login/', views.dashboard_login_view, name='login'),
    path('logout/', views.dashboard_logout_view, name='logout'),

    # Home
    path('', views.dashboard_home, name='home'),

    # Profile
    path('profile/', views.profile_edit, name='profile'),

    # Designations
    path('designations/', views.designations_list, name='designations'),
    path('designations/<int:pk>/edit/', views.designation_edit, name='designation-edit'),
    path('designations/<int:pk>/delete/', views.designation_delete, name='designation-delete'),

    # Skills
    path('skills/', views.skills_list, name='skills'),
    path('skills/add/', views.skill_create, name='skill-create'),
    path('skills/<int:pk>/edit/', views.skill_edit, name='skill-edit'),
    path('skills/<int:pk>/delete/', views.skill_delete, name='skill-delete'),
    path('skills/category/add/', views.category_create, name='category-create'),

    # Projects
    path('projects/', views.projects_list, name='projects'),
    path('projects/add/', views.project_create, name='project-create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project-edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project-delete'),
    path('projects/<int:pk>/image/add/', views.project_image_add, name='project-image-add'),
    path('projects/image/<int:pk>/delete/', views.project_image_delete, name='project-image-delete'),

    # Experience
    path('experience/', views.experience_list, name='experience'),
    path('experience/add/', views.experience_create, name='experience-create'),
    path('experience/<int:pk>/edit/', views.experience_edit, name='experience-edit'),
    path('experience/<int:pk>/delete/', views.experience_delete, name='experience-delete'),

    # Education & Training
    path('education/', views.education_list, name='education'),
    path('education/add/', views.education_create, name='education-create'),
    path('education/<int:pk>/edit/', views.education_edit, name='education-edit'),
    path('education/<int:pk>/delete/', views.education_delete, name='education-delete'),

    # Services
    path('services/', views.services_list, name='services'),
    path('services/add/', views.service_create, name='service-create'),
    path('services/<int:pk>/edit/', views.service_edit, name='service-edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='service-delete'),

    # Certifications
    path('certifications/', views.certifications_list, name='certifications'),
    path('certifications/add/', views.certification_create, name='certification-create'),
    path('certifications/<int:pk>/edit/', views.certification_edit, name='certification-edit'),
    path('certifications/<int:pk>/delete/', views.certification_delete, name='certification-delete'),

    # Resume
    path('resume/', views.resume_list, name='resume'),
    path('resume/<int:pk>/activate/', views.resume_set_active, name='resume-activate'),
    path('resume/<int:pk>/delete/', views.resume_delete, name='resume-delete'),

    # Messages
    path('messages/', views.messages_list, name='messages'),
    path('messages/<int:pk>/', views.message_detail, name='message-detail'),
    path('messages/<int:pk>/toggle-read/', views.message_toggle_read, name='message-toggle-read'),
    path('messages/<int:pk>/delete/', views.message_delete, name='message-delete'),

    # Settings
    path('settings/', views.settings_edit, name='settings'),
]
