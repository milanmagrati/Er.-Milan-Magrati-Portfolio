from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
import os

from .models import (
    PersonalProfile,
    Designation,
    SkillCategory,
    Skill,
    Experience,
    Education,
    Training,
    Project,
    Service,
    Certification,
    ResumeFile,
    ContactMessage,
    SiteSettings,
    SocialLink,
)


def portfolio_home(request):
    profile = PersonalProfile.objects.first()
    designations = Designation.objects.filter(is_active=True).order_by('display_order')
    categories = SkillCategory.objects.prefetch_related('skills').order_by('display_order')
    experiences = Experience.objects.filter(is_active=True).order_by('display_order', '-id')
    educations = Education.objects.all().order_by('display_order', '-id')
    trainings = Training.objects.all().order_by('display_order', 'id')
    projects = Project.objects.filter(is_active=True).prefetch_related('gallery').order_by('display_order', '-id')
    services = Service.objects.filter(is_active=True).order_by('display_order')
    certifications = Certification.objects.all().order_by('display_order', '-id')
    active_resume = ResumeFile.objects.filter(is_active=True).first()
    site_settings = SiteSettings.objects.first()
    social_links = SocialLink.objects.filter(is_active=True).order_by('display_order')

    # Unique project categories for filter buttons
    project_categories = sorted(list(set(p.category for p in projects if p.category)))

    # Designation titles list for JavaScript typing animation
    designation_titles = [d.title for d in designations] if designations.exists() else [
        "Python Full Stack Developer",
        "Backend Developer",
        "Django Specialist",
        "FastAPI & REST API Developer",
        "AI-Assisted Software Engineer"
    ]

    context = {
        'profile': profile,
        'designation_titles': designation_titles,
        'categories': categories,
        'experiences': experiences,
        'educations': educations,
        'trainings': trainings,
        'projects': projects,
        'project_categories': project_categories,
        'services': services,
        'certifications': certifications,
        'active_resume': active_resume,
        'site_settings': site_settings,
        'social_links': social_links,
    }
    return render(request, 'portfolio/index.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_active=True)
    other_projects = Project.objects.filter(is_active=True).exclude(pk=project.pk).order_by('display_order')[:3]
    return render(request, 'portfolio/project_detail.html', {
        'project': project,
        'other_projects': other_projects,
    })


@require_POST
def contact_submit(request):
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    subject = request.POST.get('subject', '').strip()
    message = request.POST.get('message', '').strip()

    # Honeypot field check
    bot_check = request.POST.get('website_url', '').strip()
    if bot_check:
        # Bot detected
        return JsonResponse({'success': True, 'message': 'Message sent successfully.'})

    if not name or len(name) < 2:
        return JsonResponse({'success': False, 'error': 'Please provide a valid name (at least 2 characters).'}, status=400)
    if not email or '@' not in email:
        return JsonResponse({'success': False, 'error': 'Please provide a valid email address.'}, status=400)
    if not subject:
        subject = "New Contact via Portfolio"
    if not message or len(message) < 10:
        return JsonResponse({'success': False, 'error': 'Please provide a message with at least 10 characters.'}, status=400)

    # Get client IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    msg = ContactMessage.objects.create(
        name=name,
        email=email,
        subject=subject,
        message=message,
        ip_address=ip,
    )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({
            'success': True,
            'message': 'Thank you! Your message has been sent successfully. Milan will respond promptly.'
        })

    messages.success(request, 'Thank you! Your message has been sent successfully. Milan will respond promptly.')
    return redirect('/#contact')


def download_resume(request):
    """
    Directly serve the active uploaded CV, or fall back to the root Milan_Magrati_CV_2026.pdf
    """
    active_resume = ResumeFile.objects.filter(is_active=True).first()
    if active_resume and active_resume.file and os.path.exists(active_resume.file.path):
        return FileResponse(open(active_resume.file.path, 'rb'), as_attachment=True, filename=os.path.basename(active_resume.file.name))

    fallback_path = os.path.join(settings.BASE_DIR, 'Milan_Magrati_CV_2026.pdf')
    if os.path.exists(fallback_path):
        return FileResponse(open(fallback_path, 'rb'), as_attachment=True, filename='Milan_Magrati_CV_2026.pdf')

    raise Http404("Resume file not found")


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /dashboard/",
        "Disallow: /admin/",
        "Disallow: /api/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    base_url = request.build_absolute_uri('/')[:-1]
    projects = Project.objects.filter(is_active=True)
    xml_items = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <url>',
        f'    <loc>{base_url}/</loc>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>',
    ]
    for p in projects:
        xml_items.extend([
            '  <url>',
            f'    <loc>{base_url}/project/{p.slug}/</loc>',
            '    <changefreq>monthly</changefreq>',
            '    <priority>0.8</priority>',
            '  </url>'
        ])
    xml_items.append('</urlset>')
    return HttpResponse("\n".join(xml_items), content_type="application/xml")
