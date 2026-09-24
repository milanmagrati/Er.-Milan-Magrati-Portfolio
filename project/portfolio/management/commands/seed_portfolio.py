import os
import shutil
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from portfolio.models import (
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
    SiteSettings,
    SocialLink,
)


class Command(BaseCommand):
    help = "Seed database with Milan Magrati's authentic data from Milan_Magrati_CV_2026.pdf"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding portfolio data for Milan Magrati..."))

        # 1. Superuser Creation
        admin_username = os.getenv("ADMIN_USERNAME", "admin")
        admin_email = os.getenv("ADMIN_EMAIL", "milanmagrati68@gmail.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{admin_username}'."))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser '{admin_username}' already exists."))

        # 2. Seed Resume File from Milan_Magrati_CV_2026.pdf
        cv_source_path = os.path.join(settings.BASE_DIR, "Milan_Magrati_CV_2026.pdf")
        cv_media_dir = os.path.join(settings.MEDIA_ROOT, "resumes")
        os.makedirs(cv_media_dir, exist_ok=True)
        cv_target_filename = "Milan_Magrati_CV_2026.pdf"
        cv_target_path = os.path.join(cv_media_dir, cv_target_filename)

        if os.path.exists(cv_source_path):
            shutil.copy2(cv_source_path, cv_target_path)
            ResumeFile.objects.all().update(is_active=False)
            resume_obj, created = ResumeFile.objects.get_or_create(
                title="Milan Magrati CV 2026",
                defaults={"file": f"resumes/{cv_target_filename}", "is_active": True},
            )
            if not created:
                resume_obj.file = f"resumes/{cv_target_filename}"
                resume_obj.is_active = True
                resume_obj.save()
            self.stdout.write(self.style.SUCCESS("Seeded active CV from Milan_Magrati_CV_2026.pdf."))

        # 3. Personal Profile
        profile, created = PersonalProfile.objects.get_or_create(
            id=1,
            defaults={
                "name": "Milan Magrati",
                "title": "Python Full Stack Developer",
                "bio": (
                    "Python Full Stack Developer with hands-on experience building web applications "
                    "and RESTful APIs using Django, DRF, and FastAPI. Skilled in PostgreSQL, MySQL, "
                    "Git/GitHub, Postman, and frontend technologies including HTML, CSS, and JavaScript. "
                    "Experienced in AI-assisted development with Claude Code, GitHub Copilot, and Antigravity, "
                    "with a strong focus on clean code, debugging, and delivering reliable solutions."
                ),
                "about_text": (
                    "I am a passionate software engineer based in Kathmandu, Nepal, with a Bachelor of "
                    "Engineering in Information Technology from Pokhara University. I specialize in backend "
                    "engineering, scalable API architectures, and crafting responsive user-centric web applications.\n\n"
                    "At Knockout System Pvt. Ltd., I engineer full-stack features for production e-commerce platforms, "
                    "design secure REST APIs for product workflows, orders, and authentication, and optimize database "
                    "queries for high responsiveness. I combine structured software development practices with cutting-edge "
                    "AI developer tools like Claude Code, GitHub Copilot, and Antigravity to accelerate sprint cycles while "
                    "retaining clean, modular codebases."
                ),
                "email": "milanmagrati68@gmail.com",
                "phone": "+977 986-6041157",
                "location": "Kathmandu, Nepal",
                "github_url": "https://github.com/milanmagrati",
                "linkedin_url": "https://linkedin.com/in/milan-magrati",
                "availability_status": "Available for Full-time Roles & Contracts",
                "is_available": True,
                "years_of_experience": 2,
                "projects_completed": 8,
                "technologies_count": 18,
                "code_commits": 500,
            },
        )
        self.stdout.write(self.style.SUCCESS("Seeded Personal Profile."))

        # 4. Designations (Hero Animated Rotating Titles)
        Designation.objects.all().delete()
        designations_data = [
            ("Python Full Stack Developer", 1),
            ("Backend Developer", 2),
            ("Django & DRF Specialist", 3),
            ("FastAPI & REST API Engineer", 4),
            ("AI-Assisted Software Developer", 5),
        ]
        for title, order in designations_data:
            Designation.objects.create(title=title, display_order=order, is_active=True)
        self.stdout.write(self.style.SUCCESS("Seeded animated hero designations."))

        # 5. Skill Categories & Skills
        SkillCategory.objects.all().delete()
        skills_structure = [
            (
                "Backend Frameworks",
                1,
                [
                    ("Django", 96, "django", True),
                    ("Django REST Framework (DRF)", 94, "api", True),
                    ("FastAPI", 88, "fastapi", True),
                    ("RESTful API Design", 95, "code-slash", True),
                    ("JWT & Token Authentication", 90, "shield-lock", False),
                ],
            ),
            (
                "Programming Languages",
                2,
                [
                    ("Python", 96, "python", True),
                    ("JavaScript (ES6+)", 82, "javascript", False),
                    ("HTML5", 92, "html5", False),
                    ("CSS3", 88, "css3", False),
                ],
            ),
            (
                "Databases & Storage",
                3,
                [
                    ("PostgreSQL", 90, "postgresql", True),
                    ("MySQL", 88, "mysql", True),
                    ("SQLite", 92, "sqlite", False),
                    ("Database Schema Design & ORM", 92, "database", True),
                ],
            ),
            (
                "Tools & Testing",
                4,
                [
                    ("Postman", 95, "postman", True),
                    ("Git", 92, "git", True),
                    ("GitHub", 92, "github", True),
                    ("VS Code", 95, "vscode", False),
                    ("Linux (Basics)", 80, "terminal", False),
                    ("PythonAnywhere", 85, "cloud", False),
                ],
            ),
            (
                "AI-Assisted Engineering",
                5,
                [
                    ("Claude Code", 94, "cpu", True),
                    ("GitHub Copilot", 92, "robot", True),
                    ("Antigravity", 92, "terminal-box", True),
                    ("AI Workflow Acceleration", 90, "lightning", False),
                ],
            ),
            (
                "Frontend & UI",
                6,
                [
                    ("Bootstrap", 90, "bootstrap", False),
                    ("Vanilla CSS3 & Flexbox/Grid", 90, "palette", False),
                    ("Responsive Mobile-First UI", 92, "display", False),
                    ("DOM Manipulation & AJAX", 85, "cursor", False),
                ],
            ),
            (
                "Software Engineering Practices",
                7,
                [
                    ("Clean Code Architecture", 95, "check-circle", True),
                    ("Debugging & Profiling", 92, "bug", False),
                    ("Modular Development", 90, "puzzle", False),
                    ("Agile & Scrum Fundamentals", 88, "kanban", False),
                ],
            ),
        ]

        for cat_name, cat_order, skills in skills_structure:
            cat = SkillCategory.objects.create(name=cat_name, display_order=cat_order)
            for skill_order, (s_name, s_prof, s_icon, s_feat) in enumerate(skills, start=1):
                Skill.objects.create(
                    category=cat,
                    name=s_name,
                    proficiency=s_prof,
                    icon_class=s_icon,
                    display_order=skill_order,
                    is_featured=s_feat,
                    is_active=True,
                )
        self.stdout.write(self.style.SUCCESS("Seeded all categorized skills."))

        # 6. Experiences
        Experience.objects.all().delete()
        Experience.objects.create(
            job_title="Python Full Stack Developer",
            company="Knockout System Pvt. Ltd.",
            location="Kathmandu, Nepal",
            start_date="September 2024",
            end_date="Present",
            is_current=True,
            description=(
                "• Develop secure and scalable web applications using Python, Django, Django REST Framework, and PostgreSQL.\n"
                "• Build responsive, user-friendly front-end interfaces with HTML, CSS, JavaScript, and Bootstrap.\n"
                "• Design and integrate RESTful APIs covering authentication, product management, shopping cart, order management, and admin features.\n"
                "• Troubleshoot and debug applications, optimize performance, and write clean, maintainable code following industry best practices.\n"
                "• Collaborate with cross-functional team members to deliver high-quality software on schedule while ensuring client satisfaction.\n"
                "• Leverage AI-assisted development tools such as Claude Code, GitHub Copilot, and Antigravity to accelerate coding, debugging, and overall development velocity."
            ),
            technologies="Python, Django, Django REST Framework, PostgreSQL, HTML, CSS, JavaScript, Bootstrap, Claude Code, GitHub Copilot, Antigravity",
            display_order=1,
            is_active=True,
        )
        Experience.objects.create(
            job_title="Python Backend Developer Intern",
            company="Sipalaya Info Tech Pvt. Ltd.",
            location="Koteshwor, Kathmandu",
            start_date="April 2025",
            end_date="July 2025",
            is_current=False,
            description=(
                "• Assisted in developing backend components using Python and Django.\n"
                "• Gained hands-on experience with CRUD operations, RESTful API development, and database management using PostgreSQL.\n"
                "• Collaborated with the team using Git/GitHub for version control.\n"
                "• Performed API testing using Postman and helped debug backend modules.\n"
                "• Followed clean coding practices and learned Agile workflow fundamentals."
            ),
            technologies="Python, Django, PostgreSQL, Git, GitHub, Postman, REST APIs, Agile",
            display_order=2,
            is_active=True,
        )
        self.stdout.write(self.style.SUCCESS("Seeded Professional Experience."))

        # 7. Education & Training
        Education.objects.all().delete()
        Education.objects.create(
            degree="Bachelor of Engineering in Information Technology",
            institution="Pokhara University",
            location="Pokhara, Nepal",
            start_year="July 2021",
            end_year="August 2025",
            grade_gpa="Degree Completed",
            coursework="Data Structures & Algorithms, DBMS, Computer Networks, Operating Systems, Software Engineering, Web Development, Artificial Intelligence, Cloud Computing",
            description="Four-year rigorous engineering program focusing on computer science fundamentals, full-stack systems engineering, database theory, algorithms, and distributed computing.",
            display_order=1,
        )

        Training.objects.all().delete()
        Training.objects.create(
            title="Python Backend Developer Trainee",
            institution="Sipalaya Info Tech Pvt. Ltd.",
            location="Kathmandu, Nepal",
            description=(
                "• Completed intensive training in Python, Django, Django REST Framework, and full-stack development fundamentals.\n"
                "• Developed real-world backend projects, including authentication systems, CRUD applications, and e-commerce modules.\n"
                "• Designed and implemented RESTful APIs with proper request handling and validation.\n"
                "• Worked with PostgreSQL and SQLite for database management, and used Git/GitHub for version control and Postman for API testing."
            ),
            display_order=1,
        )
        self.stdout.write(self.style.SUCCESS("Seeded Education & Training."))

        # 8. Projects (6 Real projects from CV)
        Project.objects.all().delete()
        projects_data = [
            {
                "title": "E-Commerce Website",
                "category": "Full Stack",
                "short_description": "Full-stack e-commerce application built with Django and DRF featuring JWT authentication, product catalog, cart, and automated order processing.",
                "detailed_description": (
                    "• Developed a scalable full-stack e-commerce application using Django and Django REST Framework.\n"
                    "• Implemented user authentication, product management, shopping cart, and order processing workflows.\n"
                    "• Designed RESTful APIs for products, users, and orders, integrating PostgreSQL/SQLite for data persistence.\n"
                    "• Followed clean code practices and rigorously tested all API endpoints using Postman."
                ),
                "technologies": "Python, Django, Django REST Framework, PostgreSQL, SQLite, HTML5, CSS3, Postman",
                "github_url": "https://github.com/milanmagrati",
                "live_demo_url": "",
                "is_featured": True,
                "completion_date": "2025",
                "display_order": 1,
            },
            {
                "title": "Event & Decoration Booking Platform",
                "category": "Web Systems",
                "short_description": "Full-stack balloon and event decoration booking platform with a custom Django admin/CMS panel for instant content, pricing, and visual updates.",
                "detailed_description": (
                    "• Developed a full-stack event decoration and balloon booking platform using Django and MySQL.\n"
                    "• Built a custom admin/CMS panel for managing site content, pricing, packages, and gallery images without any code changes.\n"
                    "• Designed a responsive front-end using vanilla HTML, CSS, and JavaScript with zero framework overhead for ultra-fast performance.\n"
                    "• Focused on lightweight, optimized page load metrics and high mobile responsiveness."
                ),
                "technologies": "Python, Django, MySQL, HTML5, CSS3, JavaScript, Custom CMS",
                "github_url": "https://github.com/milanmagrati",
                "live_demo_url": "",
                "is_featured": True,
                "completion_date": "2025",
                "display_order": 2,
            },
            {
                "title": "E-Learning Platform",
                "category": "Full Stack",
                "short_description": "Comprehensive online learning platform with course management, quiz engine, student progress tracking, and role-based access control.",
                "detailed_description": (
                    "• Built an online learning system with course syllabus management, interactive quizzes, and student progress tracking.\n"
                    "• Developed REST APIs for user enrollment, course content delivery, and automated assessments.\n"
                    "• Implemented role-based access control (RBAC) separating student, instructor, and admin privileges.\n"
                    "• Optimized PostgreSQL database queries with indexes and prefetching for high-concurrency throughput."
                ),
                "technologies": "Python, Django, DRF, PostgreSQL, Role-Based Access Control, REST APIs",
                "github_url": "https://github.com/milanmagrati",
                "live_demo_url": "",
                "is_featured": True,
                "completion_date": "2025",
                "display_order": 3,
            },
            {
                "title": "Online Momo Ordering System",
                "category": "Web Systems",
                "short_description": "Specialized online food ordering platform with customer registration, live order placement, status tracking, and validated backend cart logic.",
                "detailed_description": (
                    "• Created an online food ordering platform with user registration, customized order placement, and live order status tracking.\n"
                    "• Designed robust backend logic for secure request handling, transaction atomicity, and schema validation.\n"
                    "• Utilized SQLite and PostgreSQL for structured data persistence and rapid query execution."
                ),
                "technologies": "Python, Django, SQLite, PostgreSQL, HTML5, CSS3, JavaScript",
                "github_url": "https://github.com/milanmagrati",
                "live_demo_url": "",
                "is_featured": False,
                "completion_date": "2024",
                "display_order": 4,
            },
            {
                "title": "Healthcare Management System",
                "category": "Backend & APIs",
                "short_description": "Backend-driven clinical management platform with patient registration, appointment scheduling, doctor calendars, and role-based authorization.",
                "detailed_description": (
                    "• Built a backend-driven healthcare management system with patient registration, appointment scheduling, and doctor roster management.\n"
                    "• Designed RESTful APIs for patients, doctors, and appointments, enforcing role-based permissions across admin, doctors, and patients.\n"
                    "• Integrated PostgreSQL/SQLite for encrypted, secure data storage and implemented error handling with Postman API validation."
                ),
                "technologies": "Python, Django, Django REST Framework, PostgreSQL, SQLite, RBAC, Postman",
                "github_url": "https://github.com/milanmagrati",
                "live_demo_url": "",
                "is_featured": True,
                "completion_date": "2024",
                "display_order": 5,
            },
            {
                "title": "Weather Web Application",
                "category": "Backend & APIs",
                "short_description": "Live meteorological web app integrating external REST APIs to report real-time temperature, humidity, and weather conditions with error resilience.",
                "detailed_description": (
                    "• Developed a Django web application integrating an external weather REST API to fetch real-time temperature, humidity, and conditions.\n"
                    "• Handled asynchronous API responses, timeout errors, and input sanitation with thorough Postman endpoint testing.\n"
                    "• Created a clean, minimalist user interface with dynamic weather condition visuals."
                ),
                "technologies": "Python, Django, REST API Integration, JSON, Postman, Responsive CSS",
                "github_url": "https://github.com/milanmagrati",
                "live_demo_url": "",
                "is_featured": False,
                "completion_date": "2024",
                "display_order": 6,
            },
        ]

        for p_data in projects_data:
            Project.objects.create(**p_data, is_active=True)
        self.stdout.write(self.style.SUCCESS("Seeded all 6 real projects."))

        # 9. Services
        Service.objects.all().delete()
        services_data = [
            (
                "Backend & API Architecture",
                "Engineering robust, scalable, and secure backend systems using Python, Django, DRF, and FastAPI with RESTful standards, token authentication, and clean modular code.",
                "code",
                1,
            ),
            (
                "Full Stack Web Development",
                "Building end-to-end web applications combining powerful Django backends with modern, responsive, and accessible user interfaces that engage users and drive conversions.",
                "layout",
                2,
            ),
            (
                "Database Design & Optimization",
                "Architecting relational databases in PostgreSQL and MySQL, schema normalization, query indexing, and ORM query optimization to guarantee sub-millisecond response times.",
                "database",
                3,
            ),
            (
                "Custom CMS & Admin Portals",
                "Developing custom, intuitive administration portals that empower non-technical teams to effortlessly manage content, media, pricing, and business logic without code updates.",
                "shield",
                4,
            ),
            (
                "REST API Integration & Testing",
                "Connecting external third-party services, payment processors, and REST APIs with comprehensive Postman test collections and strict error recovery strategies.",
                "api",
                5,
            ),
            (
                "AI-Assisted Accelerated Engineering",
                "Leveraging Claude Code, GitHub Copilot, and Antigravity to accelerate rapid prototyping, unit test generation, code refactoring, and dependable delivery.",
                "cpu",
                6,
            ),
        ]
        for title, desc, icon, order in services_data:
            Service.objects.create(
                title=title,
                description=desc,
                icon=icon,
                display_order=order,
                is_active=True,
            )
        self.stdout.write(self.style.SUCCESS("Seeded Services."))

        # 10. Certifications
        Certification.objects.all().delete()
        certifications_data = [
            (
                "Full Stack Developer – Experience Certificate",
                "Knockout System Pvt. Ltd.",
                "September 2026",
                "KS-FSD-2026",
                "",
                "Verified certificate commemorating full stack development contributions on production Django & PostgreSQL e-commerce platforms.",
                1,
            ),
            (
                "Python Django Backend Development",
                "Sipalaya Info Tech Pvt. Ltd.",
                "July 2025",
                "SIT-PYDJ-2025",
                "",
                "Hands-on intensive engineering certification covering Django, DRF, REST API architecture, PostgreSQL, and Git/GitHub.",
                2,
            ),
            (
                "HTML, CSS & JavaScript Fundamentals",
                "freeCodeCamp",
                "2024",
                "FCC-WEB-2024",
                "https://www.freecodecamp.org",
                "Comprehensive curriculum covering responsive modern web standards, semantic HTML, modern CSS styling, and JavaScript logic.",
                3,
            ),
        ]
        for name, org, date, cred_id, url, desc, order in certifications_data:
            Certification.objects.create(
                name=name,
                issuing_organization=org,
                issue_date=date,
                credential_id=cred_id,
                credential_url=url if url else None,
                description=desc,
                display_order=order,
            )
        self.stdout.write(self.style.SUCCESS("Seeded Certifications."))

        # 11. Social Links
        SocialLink.objects.all().delete()
        SocialLink.objects.create(
            platform="GitHub",
            url="https://github.com/milanmagrati",
            icon_name="github",
            display_order=1,
            is_active=True,
        )
        SocialLink.objects.create(
            platform="LinkedIn",
            url="https://linkedin.com/in/milan-magrati",
            icon_name="linkedin",
            display_order=2,
            is_active=True,
        )
        SocialLink.objects.create(
            platform="Email",
            url="mailto:milanmagrati68@gmail.com",
            icon_name="envelope",
            display_order=3,
            is_active=True,
        )
        SocialLink.objects.create(
            platform="Phone",
            url="tel:+9779866041157",
            icon_name="telephone",
            display_order=4,
            is_active=True,
        )
        self.stdout.write(self.style.SUCCESS("Seeded Social Links."))

        # 12. Site Settings
        SiteSettings.objects.all().delete()
        SiteSettings.objects.create(
            site_title="Milan Magrati | Python Full Stack Developer",
            meta_description="Milan Magrati - Professional Python Full Stack Developer specializing in Django, DRF, FastAPI, PostgreSQL, and AI-assisted development. Based in Kathmandu, Nepal.",
            meta_keywords="Milan Magrati, Python Developer, Django, DRF, FastAPI, PostgreSQL, Kathmandu, Nepal, Full Stack Developer, Software Engineer",
            enable_about=True,
            enable_skills=True,
            enable_experience=True,
            enable_education=True,
            enable_projects=True,
            enable_services=True,
            enable_certifications=True,
            enable_contact=True,
        )
        self.stdout.write(self.style.SUCCESS("Seeded Site Settings."))

        self.stdout.write(self.style.SUCCESS("All portfolio data successfully seeded from Milan_Magrati_CV_2026.pdf!"))
