from rest_framework import serializers
from portfolio.models import (
    PersonalProfile,
    Designation,
    SkillCategory,
    Skill,
    Experience,
    Education,
    Project,
    ProjectImage,
    Service,
    Certification,
    ContactMessage,
)


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['id', 'title', 'display_order']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'proficiency', 'icon_class', 'is_featured', 'display_order']


class SkillCategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'display_order', 'skills']


class ExperienceSerializer(serializers.ModelSerializer):
    tech_list = serializers.ReadOnlyField()
    bullets = serializers.ReadOnlyField()

    class Meta:
        model = Experience
        fields = [
            'id', 'job_title', 'company', 'location',
            'start_date', 'end_date', 'is_current',
            'description', 'technologies', 'tech_list', 'bullets',
            'company_logo', 'display_order'
        ]


class EducationSerializer(serializers.ModelSerializer):
    coursework_list = serializers.ReadOnlyField()

    class Meta:
        model = Education
        fields = [
            'id', 'degree', 'institution', 'location',
            'start_year', 'end_year', 'grade_gpa',
            'coursework', 'coursework_list', 'description'
        ]


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'caption']


class ProjectSerializer(serializers.ModelSerializer):
    tech_list = serializers.ReadOnlyField()
    bullets = serializers.ReadOnlyField()
    gallery = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'category',
            'short_description', 'detailed_description',
            'thumbnail', 'technologies', 'tech_list', 'bullets',
            'github_url', 'live_demo_url', 'is_featured',
            'completion_date', 'gallery', 'display_order'
        ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'icon', 'display_order']


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = [
            'id', 'name', 'issuing_organization',
            'issue_date', 'credential_id', 'credential_url',
            'certificate_file', 'description'
        ]


class PersonalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalProfile
        fields = '__all__'


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters.")
        return value.strip()

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters.")
        return value.strip()
