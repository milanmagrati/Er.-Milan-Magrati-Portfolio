from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from portfolio.models import (
    PersonalProfile,
    Designation,
    SkillCategory,
    Experience,
    Education,
    Project,
    Service,
    Certification,
    ContactMessage,
)
from .serializers import (
    PersonalProfileSerializer,
    DesignationSerializer,
    SkillCategorySerializer,
    ExperienceSerializer,
    EducationSerializer,
    ProjectSerializer,
    ServiceSerializer,
    CertificationSerializer,
    ContactMessageSerializer,
)


class ProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PersonalProfileSerializer

    def get_object(self):
        return PersonalProfile.objects.first()

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()
        if not profile:
            return Response({"error": "Profile not configured yet"}, status=status.HTTP_404_NOT_FOUND)
        
        profile_data = self.get_serializer(profile).data
        designations = Designation.objects.filter(is_active=True).order_by('display_order')
        profile_data['designations'] = DesignationSerializer(designations, many=True).data
        return Response(profile_data)


class SkillCategoryListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SkillCategorySerializer
    queryset = SkillCategory.objects.prefetch_related('skills').order_by('display_order')


class ExperienceListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.filter(is_active=True).order_by('display_order')


class EducationListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EducationSerializer
    queryset = Education.objects.all().order_by('display_order')


class ProjectListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        qs = Project.objects.filter(is_active=True).prefetch_related('gallery').order_by('display_order')
        category = self.request.query_params.get('category')
        if category and category != 'All':
            qs = qs.filter(category__iexact=category)
        return qs


class ProjectDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProjectSerializer
    queryset = Project.objects.filter(is_active=True).prefetch_related('gallery')
    lookup_field = 'slug'


class ServiceListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ServiceSerializer
    queryset = Service.objects.filter(is_active=True).order_by('display_order')


class CertificationListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CertificationSerializer
    queryset = Certification.objects.all().order_by('display_order')


class ContactCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        serializer.save(ip_address=ip)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "message": "Thank you! Your message has been received. Milan will get back to you shortly."},
            status=status.HTTP_201_CREATED
        )
