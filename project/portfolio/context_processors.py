from .models import PersonalProfile, ResumeFile, SiteSettings, SocialLink, ContactMessage

def portfolio_globals(request):
    """
    Context processor to make profile, active resume, site settings,
    and unread messages count globally available across all templates.
    """
    profile = PersonalProfile.objects.first()
    active_resume = ResumeFile.objects.filter(is_active=True).first()
    settings = SiteSettings.objects.first()
    if not settings:
        settings = SiteSettings()  # In-memory default with all enable_* flags as True
    social_links = SocialLink.objects.filter(is_active=True).order_by('display_order')
    
    unread_count = 0
    if request.user.is_authenticated:
        unread_count = ContactMessage.objects.filter(is_read=False).count()

    return {
        'profile': profile,
        'active_resume': active_resume,
        'site_settings': settings,
        'social_links': social_links,
        'unread_messages_count': unread_count,
    }
