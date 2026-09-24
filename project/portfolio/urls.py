from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.portfolio_home, name='home'),
    path('project/<slug:slug>/', views.project_detail, name='project-detail'),
    path('contact/submit/', views.contact_submit, name='contact-submit'),
    path('download-cv/', views.download_resume, name='download-cv'),
    path('robots.txt', views.robots_txt, name='robots-txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap-xml'),
]
