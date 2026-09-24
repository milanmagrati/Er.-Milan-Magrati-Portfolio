from django.contrib import admin
from .models import (
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


@admin.register(PersonalProfile)
class PersonalProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'phone', 'location', 'is_available', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'profile_image', 'availability_status', 'is_available')
        }),
        ('Hero & About Narratives', {
            'fields': ('bio', 'about_text')
        }),
        ('Contact & Links', {
            'fields': ('email', 'phone', 'location', 'website', 'github_url', 'linkedin_url')
        }),
        ('Key Metrics', {
            'fields': ('years_of_experience', 'projects_completed', 'technologies_count', 'code_commits')
        }),
    )


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    ordering = ('display_order',)


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    fields = ('name', 'proficiency', 'icon_class', 'display_order', 'is_featured', 'is_active')


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'skill_count')
    list_editable = ('display_order',)
    inlines = [SkillInline]

    def skill_count(self, obj):
        return obj.skills.count()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'display_order', 'is_featured', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('name',)
    list_editable = ('proficiency', 'display_order', 'is_featured', 'is_active')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company', 'start_date', 'end_date', 'is_current', 'display_order', 'is_active')
    list_filter = ('is_current', 'is_active', 'company')
    search_fields = ('job_title', 'company', 'description', 'technologies')
    list_editable = ('display_order', 'is_active')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_year', 'end_year', 'grade_gpa', 'display_order')
    list_editable = ('display_order',)
    search_fields = ('degree', 'institution')


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'institution', 'location', 'display_order')
    list_editable = ('display_order',)
    search_fields = ('title', 'institution')


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'display_order', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('title', 'short_description', 'detailed_description', 'technologies')
    list_editable = ('is_featured', 'display_order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    search_fields = ('title', 'description')


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuing_organization', 'issue_date', 'display_order')
    list_editable = ('display_order',)
    search_fields = ('name', 'issuing_organization')


@admin.register(ResumeFile)
class ResumeFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'is_active', 'uploaded_at')
    list_editable = ('is_active',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'ip_address', 'created_at')
    list_editable = ('is_read',)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'enable_about', 'enable_skills', 'enable_experience', 'enable_projects', 'enable_contact')


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'icon_name', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
