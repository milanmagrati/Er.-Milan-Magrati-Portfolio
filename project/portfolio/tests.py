from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from portfolio.models import (
    PersonalProfile,
    Designation,
    Project,
    Skill,
    SkillCategory,
    ResumeFile,
    ContactMessage,
    SiteSettings,
)


class PortfolioTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.site_settings = SiteSettings.objects.create()
        # Seed test data
        self.profile = PersonalProfile.objects.create(
            name="Milan Magrati",
            title="Python Full Stack Developer",
            bio="Test bio for Milan Magrati.",
            about_text="Detailed about text narrative.",
            email="milanmagrati68@gmail.com",
            phone="+977 986-6041157",
            location="Kathmandu, Nepal",
        )
        self.designation = Designation.objects.create(
            title="Python Full Stack Developer",
            display_order=1,
            is_active=True
        )
        self.category = SkillCategory.objects.create(
            name="Backend Frameworks",
            display_order=1
        )
        self.skill = Skill.objects.create(
            category=self.category,
            name="Django",
            proficiency=95,
            is_active=True
        )
        self.project = Project.objects.create(
            title="E-Commerce Website",
            category="Full Stack",
            short_description="Test project short description.",
            detailed_description="• Bullet 1\n• Bullet 2",
            technologies="Python, Django, DRF, PostgreSQL",
            is_active=True
        )
        self.staff_user = User.objects.create_user(
            username="testadmin",
            password="testpassword123",
            is_staff=True
        )

    def test_homepage_status_and_content(self):
        response = self.client.get(reverse('portfolio:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Milan Magrati")
        self.assertContains(response, "Python Full Stack Developer")
        self.assertContains(response, "E-Commerce Website")

    def test_project_detail_view(self):
        response = self.client.get(reverse('portfolio:project-detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "E-Commerce Website")

    def test_contact_form_ajax_submission(self):
        data = {
            'name': 'Employer Recruiter',
            'email': 'recruiter@company.com',
            'subject': 'Job Opportunity',
            'message': 'We have an open role for a Python Full Stack Developer and would love to chat.',
            'website_url': '',  # Honeypot empty
        }
        response = self.client.post(
            reverse('portfolio:contact-submit'),
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(email='recruiter@company.com').exists())

    def test_api_profile_endpoint(self):
        response = self.client.get(reverse('api:profile'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], "Milan Magrati")

    def test_api_projects_endpoint(self):
        response = self.client.get(reverse('api:projects'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(len(data['results']), 1)

    def test_dashboard_login_required(self):
        # Unauthenticated user should be redirected to login
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard/login/', response.url)

    def test_dashboard_staff_access(self):
        self.client.login(username='testadmin', password='testpassword123')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Portfolio CMS")

    def test_robots_and_sitemap(self):
        robots_res = self.client.get(reverse('portfolio:robots-txt'))
        self.assertEqual(robots_res.status_code, 200)
        sitemap_res = self.client.get(reverse('portfolio:sitemap-xml'))
        self.assertEqual(sitemap_res.status_code, 200)
