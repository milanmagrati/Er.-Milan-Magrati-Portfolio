from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Custom CMS Admin Dashboard (Primary Content Management)
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),

    # REST APIs
    path('api/', include('api.urls', namespace='api')),

    # Standard Django Admin
    path('admin/', admin.site.urls),

    # Public Portfolio Website
    path('', include('portfolio.urls', namespace='portfolio')),
]

# Serve media files in development
if settings.DEBUG or True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

