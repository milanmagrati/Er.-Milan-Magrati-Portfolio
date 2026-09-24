from django.db import models
from django.utils.text import slugify


class PersonalProfile(models.Model):
    name = models.CharField(max_length=150, default="Milan Magrati")
    title = models.CharField(max_length=200, default="Python Full Stack Developer")
    bio = models.TextField(
        help_text="Short introduction displayed in the hero section."
    )
    about_text = models.TextField(
        help_text="Detailed narrative about your background, mindset, and experience."
    )
    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)
    email = models.EmailField(default="milanmagrati68@gmail.com")
    phone = models.CharField(max_length=50, default="+977 986-6041157")
    location = models.CharField(max_length=150, default="Kathmandu, Nepal")
    website = models.URLField(blank=True, null=True)
    github_url = models.URLField(default="https://github.com/milanmagrati")
    linkedin_url = models.URLField(default="https://linkedin.com/in/milan-magrati")
    availability_status = models.CharField(max_length=100, default="Available for Opportunities")
    is_available = models.BooleanField(default=True)
    
    # Metrics / Stats
    years_of_experience = models.PositiveIntegerField(default=2)
    projects_completed = models.PositiveIntegerField(default=8)
    technologies_count = models.PositiveIntegerField(default=18)
    code_commits = models.PositiveIntegerField(default=500)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Personal Profile"
        verbose_name_plural = "Personal Profile"

    def __str__(self):
        return f"{self.name} - Profile"


class Designation(models.Model):
    title = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.title


class SkillCategory(models.Model):
    name = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Skill Categories"
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.name


class Skill(models.Model):
    category = models.ForeignKey(
        SkillCategory, on_delete=models.CASCADE, related_name="skills"
    )
    name = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField(
        default=85, help_text="Proficiency percentage from 1 to 100"
    )
    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="Icon identifier (e.g. python, django, postgresql, git)",
    )
    display_order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category__display_order", "display_order", "id"]

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Experience(models.Model):
    job_title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=150, default="Kathmandu, Nepal")
    start_date = models.CharField(max_length=100, help_text="e.g. September 2024")
    end_date = models.CharField(
        max_length=100, blank=True, default="Present", help_text="e.g. Present or July 2025"
    )
    is_current = models.BooleanField(default=False)
    description = models.TextField(help_text="Bullet points or detailed responsibilities.")
    technologies = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated technologies used, e.g. Python, Django, DRF, PostgreSQL",
    )
    company_logo = models.ImageField(upload_to="experience/", blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "-id"]

    def __str__(self):
        return f"{self.job_title} at {self.company}"

    @property
    def tech_list(self):
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(",") if t.strip()]

    @property
    def bullets(self):
        lines = [line.strip().lstrip("•-*").strip() for line in self.description.split("\n")]
        return [line for line in lines if line]


class Education(models.Model):
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=150, default="Pokhara, Nepal")
    start_year = models.CharField(max_length=50, default="2021")
    end_year = models.CharField(max_length=50, default="2025")
    grade_gpa = models.CharField(max_length=50, blank=True, default="Completed")
    coursework = models.TextField(
        blank=True,
        help_text="Relevant coursework: Data Structures, DBMS, Operating Systems, AI, etc.",
    )
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Education"
        ordering = ["display_order", "-id"]

    def __str__(self):
        return f"{self.degree} - {self.institution}"

    @property
    def coursework_list(self):
        if not self.coursework:
            return []
        return [c.strip() for c in self.coursework.split(",") if c.strip()]


class Training(models.Model):
    title = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=150, default="Kathmandu, Nepal")
    description = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.title} - {self.institution}"

    @property
    def bullets(self):
        lines = [line.strip().lstrip("•-*").strip() for line in self.description.split("\n")]
        return [line for line in lines if line]


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("Full Stack", "Full Stack"),
        ("Backend & APIs", "Backend & APIs"),
        ("Web Systems", "Web Systems"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Full Stack")
    short_description = models.CharField(max_length=350)
    detailed_description = models.TextField()
    thumbnail = models.ImageField(upload_to="projects/", blank=True, null=True)
    technologies = models.CharField(
        max_length=400,
        help_text="Comma-separated technologies: Django, DRF, PostgreSQL, HTML5, CSS3, JS",
    )
    github_url = models.URLField(blank=True, null=True)
    live_demo_url = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    completion_date = models.CharField(max_length=100, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "-id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(",") if t.strip()]

    @property
    def bullets(self):
        lines = [line.strip().lstrip("•-*").strip() for line in self.detailed_description.split("\n")]
        return [line for line in lines if line]


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.project.title} - Image #{self.id}"


class Service(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon = models.CharField(
        max_length=100,
        default="code",
        help_text="Identifier: code, api, database, layout, cpu, shield",
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.title


class Certification(models.Model):
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.CharField(max_length=100)
    credential_id = models.CharField(max_length=150, blank=True)
    credential_url = models.URLField(blank=True, null=True)
    certificate_file = models.FileField(upload_to="certifications/", blank=True, null=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-id"]

    def __str__(self):
        return f"{self.name} ({self.issuing_organization})"


class ResumeFile(models.Model):
    title = models.CharField(max_length=150, default="Milan Magrati CV 2026")
    file = models.FileField(upload_to="resumes/")
    is_active = models.BooleanField(
        default=True,
        help_text="When checked, this will be the file downloaded from the 'Download CV' buttons.",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_active", "-uploaded_at"]

    def save(self, *args, **kwargs):
        if self.is_active:
            # Set other resumes to inactive
            ResumeFile.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({'Active' if self.is_active else 'Inactive'})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["is_read", "-created_at"]

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class SiteSettings(models.Model):
    site_title = models.CharField(
        max_length=200, default="Milan Magrati | Python Full Stack Developer"
    )
    meta_description = models.TextField(
        default="Milan Magrati - Python Full Stack Developer specializing in Django, DRF, FastAPI, PostgreSQL, RESTful APIs, and AI-assisted development."
    )
    meta_keywords = models.CharField(
        max_length=300,
        default="Milan Magrati, Python Developer, Django, DRF, FastAPI, PostgreSQL, Kathmandu, Nepal, Software Engineer",
    )
    # Section toggles
    enable_about = models.BooleanField(default=True)
    enable_skills = models.BooleanField(default=True)
    enable_experience = models.BooleanField(default=True)
    enable_education = models.BooleanField(default=True)
    enable_projects = models.BooleanField(default=True)
    enable_services = models.BooleanField(default=True)
    enable_certifications = models.BooleanField(default=True)
    enable_contact = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Global Site Settings"


class SocialLink(models.Model):
    platform = models.CharField(max_length=50)
    url = models.URLField()
    icon_name = models.CharField(max_length=50, default="globe")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.platform
