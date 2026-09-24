from django.urls import path
from .views import (
    ProfileAPIView,
    SkillCategoryListAPIView,
    ExperienceListAPIView,
    EducationListAPIView,
    ProjectListAPIView,
    ProjectDetailAPIView,
    ServiceListAPIView,
    CertificationListAPIView,
    ContactCreateAPIView,
)

app_name = 'api'

urlpatterns = [
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('skills/', SkillCategoryListAPIView.as_view(), name='skills'),
    path('experience/', ExperienceListAPIView.as_view(), name='experience'),
    path('education/', EducationListAPIView.as_view(), name='education'),
    path('projects/', ProjectListAPIView.as_view(), name='projects'),
    path('projects/<slug:slug>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('services/', ServiceListAPIView.as_view(), name='services'),
    path('certifications/', CertificationListAPIView.as_view(), name='certifications'),
    path('contact/', ContactCreateAPIView.as_view(), name='contact-submit'),
]
