# Milan Magrati — Professional Python Full Stack Developer Portfolio & CMS

A modern, high-performance, fully dynamic personal portfolio website and content management system (CMS) engineered for **Milan Magrati** as a **Python Full Stack Developer**.

Built with **Python**, **Django 5.2**, **Django REST Framework**, and modern responsive web standards (Vanilla CSS with custom design system, modern JavaScript, and zero external framework bloat). Populated directly with Milan's authentic background from `Milan_Magrati_CV_2026.pdf`.

---

## 🌟 Key Features

### 1. Public Portfolio
- **Default Dark & Light Themes**: Developer-centric deep slate/obsidian dark theme with a clean, high-contrast light theme. Persistent across sessions via `localStorage` with zero theme flash.
- **Hero Section**:
  - Prominent headline: **Milan Magrati**.
  - Circular profile portrait with breathing gradient glow, floating hover animation, and BE in IT credential badge.
  - Animated rotating designation typing effect (*Python Full Stack Developer*, *Backend Developer*, *Django Specialist*, *FastAPI & REST API Developer*, *AI-Assisted Software Engineer*) dynamically managed from the CMS.
  - Quick action buttons: **View Projects**, **Download CV**, **Contact Me**.
  - Direct tech stack pills (*Python 3*, *Django 5*, *DRF*, *FastAPI*, *PostgreSQL*, *Claude Code*, *Antigravity*).
- **About & Key Metrics**:
  - Authentic summary from Milan's CV.
  - Highlight metric counters (Years of Experience, Projects Completed, Technologies Count, Code Commits / API Endpoints).
  - Availability pill (*Available for Full-time Roles & Contracts*).
- **Categorized Skills**:
  - Interactive category filter tabs (*Backend Frameworks*, *Programming Languages*, *Databases*, *Tools & Testing*, *AI-Assisted Engineering*, *Frontend*, *Practices*).
  - Progress meters with proficiency ratings.
- **Professional Experience Timeline**:
  - Interactive connected vertical timeline with glowing nodes.
  - Production experience at **Knockout System Pvt. Ltd.** (Sept 2024 – Present) and **Sipalaya Info Tech Pvt. Ltd.** (Apr 2025 – Jul 2025).
  - Detailed responsibilities and technology tags.
- **Education & Training**:
  - **Bachelor of Engineering in Information Technology** from **Pokhara University** (2021–2025) with relevant coursework.
  - Python Backend Developer Trainee certification from **Sipalaya Info Tech**.
- **Interactive Projects Showcase**:
  - Filterable by category (*All*, *Full Stack*, *Backend & APIs*, *Web Systems*).
  - Detailed architecture modal with key accomplishments, technology tags, and source code links.
  - Dedicated SEO project pages at `/project/<slug>/`.
- **Services Offered**:
  - 6 Core engineering competencies (Backend & API Architecture, Full-Stack Web Development, Database Optimization, Custom CMS Portals, REST API Testing, AI-Assisted Accelerated Engineering).
- **Certifications & Achievements**:
  - Knockout System experience certificate, Sipalaya Info Tech Django certification, and freeCodeCamp certification.
- **Contact & Inquiries**:
  - Interactive AJAX contact form with instant validation, anti-spam honeypot, and animated toast feedback.
  - Messages saved directly to the database with sender IP logging.
- **CV Download**:
  - Download buttons stream the active CV (`Milan_Magrati_CV_2026.pdf`) dynamically.
  - Uploading a new resume file in the CMS immediately updates the download button without modifying any HTML.

---

### 2. Custom CMS Admin Dashboard (`/dashboard/`)
Manage 100% of website content dynamically with no code edits required:
- **Overview Dashboard**: Instant metric widgets (Projects, Skills, Experiences, Certifications, Inquiries, Unread count) with recent message previews.
- **Personal Profile**: Update bio, name, email, phone, location, links, highlight statistics, and upload an avatar with instant preview.
- **Designations Manager**: Add, reorder, edit, and toggle the animated roles rotating on the hero section.
- **Skills Manager**: Create categories, add skills, adjust proficiency ratings (1–100%), and toggle active/featured status.
- **Projects Manager**: Create and edit projects, write bullet points, assign categories, and upload screenshots and gallery images.
- **Experience & Education**: Manage career timeline entries, companies, degrees, and coursework tags.
- **Services & Certifications**: Add, update, and reorder service offerings and credentials.
- **Resume Manager**: Upload new PDF resumes, toggle which CV is active, and test the download link.
- **Messages Inbox**: Review client inquiries, view detailed messages, toggle read/unread status, and reply directly via email.
- **Site Settings**: Toggle entire sections on or off with a single click, and customize SEO meta titles, keywords, and descriptions.
- **Power Admin**: Direct link to the standard Django Admin (`/admin/`) for advanced operations.

---

### 3. RESTful API Endpoints (`/api/`)
- `GET /api/profile/` — Profile information and active hero designations
- `GET /api/skills/` — Categorized skills with proficiency scores
- `GET /api/experience/` — Career history and responsibilities
- `GET /api/education/` — Academic background and coursework
- `GET /api/projects/` — Filterable projects list (supports `?category=Full+Stack`)
- `GET /api/projects/<slug>/` — Individual project architecture and gallery
- `GET /api/services/` — List of engineering services
- `GET /api/certifications/` — List of credentials
- `POST /api/contact/` — Submit contact messages via API

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend Framework** | Python 3.14+, Django 5.2 |
| **API Architecture** | Django REST Framework (DRF) 3.17+ |
| **Database** | SQLite (Local Development) / PostgreSQL (Production ready) |
| **Static & Media** | WhiteNoise 6.12+, Pillow 12.1+ |
| **Frontend Styling** | Modern Vanilla CSS3, Custom Design System, CSS Variables |
| **Interactivity** | Modern Vanilla JavaScript (ES6+), Fetch API, Intersection Observer |
| **Security** | Django Auth, CSRF Protection, Anti-Spam Honeypot, Session Security |

---

## 🚀 Quick Start & Local Setup

### 1. Clone & Enter Directory
```bash
cd "c:\Users\milan\OneDrive\Desktop\Myportfolio"
```

### 2. Environment Configuration
Verify or customize your `.env` file (based on `.env.example`):
```ini
SECRET_KEY=django-insecure-milan-magrati-portfolio-key-change-in-production-2026!
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
DATABASE_URL=
ADMIN_USERNAME=admin
ADMIN_EMAIL=milanmagrati68@gmail.com
ADMIN_PASSWORD=admin123
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Seed Authentic CV Data
```bash
python manage.py migrate
python manage.py seed_portfolio
```
*The `seed_portfolio` command automatically imports all data from `Milan_Magrati_CV_2026.pdf`, copies the CV to media storage, and creates the default superuser.*

### 5. Start Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```

- **Live Portfolio**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Custom CMS Dashboard**: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
- **Django Power Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **REST APIs**: [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

**Default Admin Credentials**:
- **Username**: `admin`
- **Password**: `admin123`

---

## 🧪 Running Automated Tests
```bash
python manage.py test
```
All 8 automated tests verify homepage rendering, CV download, AJAX contact form validation, REST API responses, CMS authentication, and SEO endpoints.

---

## 🌐 Production Deployment Guide (Render + Supabase + Cloudinary)

This project is pre-configured for modern, serverless cloud deployment using:
- **Render**: Web service hosting (Gunicorn + WhiteNoise)
- **Supabase**: Managed PostgreSQL database (persistent free tier)
- **Cloudinary**: Cloud media and asset storage (dynamic image & PDF handling)

---

### Step 1: Create Supabase PostgreSQL Database
1. Go to [Supabase](https://supabase.com) and create or open your project.
2. Navigate to **Project Settings** &rarr; **Database** &rarr; **Connection String**.
3. Select the **URI** tab and choose **Session pooler** (port `5432` - recommended for IPv4):
   ```text
  postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres?sslmode=require
   ```
4. Copy this URI (replace `[YOUR-PASSWORD]` with your actual database password).

---

### Step 2: Get Cloudinary API Credentials
1. Go to [Cloudinary](https://cloudinary.com) and log in to the Dashboard / Console.
2. Note your 3 credentials from the **Product Environment** summary:
   - **Cloud Name** (`CLOUDINARY_CLOUD_NAME`)
   - **API Key** (`CLOUDINARY_API_KEY`)
   - **API Secret** (`CLOUDINARY_API_SECRET`)

---

### Step 3: Deploy to Render

#### Option A: One-Click Blueprint (`render.yaml`)
1. Push your code to GitHub.
2. Go to [Render Dashboard](https://dashboard.render.com/) &rarr; **New** &rarr; **Blueprint**.
3. Connect your GitHub repository `Er.-Milan-Magrati-Portfolio`.
4. Render will detect `render.yaml`. Fill in the prompted secret variables:
  - `DATABASE_URL`: Your Supabase connection string.
   - `CLOUDINARY_CLOUD_NAME`: Your Cloudinary Cloud Name.
   - `CLOUDINARY_API_KEY`: Your Cloudinary API Key.
   - `CLOUDINARY_API_SECRET`: Your Cloudinary API Secret.
   - `ADMIN_PASSWORD`: Your desired superuser password for `/dashboard/` & `/admin/`.
5. Click **Apply**.

#### Option B: Manual Web Service Setup
1. In Render Dashboard, click **New +** &rarr; **Web Service**.
2. Connect your GitHub repository.
3. Configure the settings:
   - **Name**: `milan-magrati-portfolio`
   - **Environment**: `Python 3`
   - **Region**: Choose the closest region (e.g., Singapore or Frankfurt)
   - **Branch**: `main`
   - **Build Command**: `./build.sh`
   - **Start Command**: `cd project && gunicorn project.wsgi:application`
   - **Plan**: `Free`
4. Add the following **Environment Variables**:
   | Key | Value | Notes |
   | :--- | :--- | :--- |
   | `DEBUG` | `False` | Production mode |
   | `PYTHON_VERSION` | `3.12.8` | Stable Python runtime |
   | `SECRET_KEY` | *(Generate a random 50-character string)* | Django security key |
  | `DATABASE_URL` | `postgresql://postgres...` | Your Supabase connection URI |
   | `CLOUDINARY_CLOUD_NAME` | *(Your Cloudinary Cloud Name)* | Cloudinary media storage |
   | `CLOUDINARY_API_KEY` | *(Your Cloudinary API Key)* | Cloudinary media storage |
   | `CLOUDINARY_API_SECRET` | *(Your Cloudinary API Secret)* | Cloudinary media storage |
   | `ADMIN_USERNAME` | `admin` | CMS & Django Admin superuser |
   | `ADMIN_EMAIL` | `milanmagrati68@gmail.com` | Notification & superuser email |
   | `ADMIN_PASSWORD` | *(Your secure password)* | Password for dashboard login |
5. Click **Deploy Web Service**.

---

### Step 4: Verification & Live Site
The `./build.sh` script automatically:
1. Installs all production dependencies.
2. Gathers and compresses static CSS/JS/SVG assets via WhiteNoise (`collectstatic`).
3. Applies database migrations to Supabase (`migrate`).
4. Seeds all authentic portfolio data, designations, projects, experience, education, and uploads your authentic CV and profile avatar directly to Cloudinary (`seed_portfolio`).

Your portfolio is immediately live at `https://<your-render-subdomain>.onrender.com`!

---

## 📄 License & Credits
Designed and engineered for **Milan Magrati**, Python Full Stack Developer.
Kathmandu, Nepal &bull; `milanmagrati68@gmail.com`
