from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.portfolio_home, name='home'),
    path('about', views.portfolio_home, {'section': 'about'}, name='about'),
    path('skills', views.portfolio_home, {'section': 'skills'}, name='skills'),
    path('experience', views.portfolio_home, {'section': 'experience'}, name='experience'),
    path('education', views.portfolio_home, {'section': 'education'}, name='education'),
    path('projects', views.portfolio_home, {'section': 'projects'}, name='projects'),
    path('services', views.portfolio_home, {'section': 'services'}, name='services'),
    path('certificates', views.portfolio_home, {'section': 'certifications'}, name='certificates'),
    path('contact', views.portfolio_home, {'section': 'contact'}, name='contact'),
    path('health/', views.health_check, name='health-check'),
    path('project/<slug:slug>/', views.project_detail, name='project-detail'),
    path('contact/submit/', views.contact_submit, name='contact-submit'),
    path('download-cv/', views.download_resume, name='download-cv'),
    path('robots.txt', views.robots_txt, name='robots-txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap-xml'),
]
