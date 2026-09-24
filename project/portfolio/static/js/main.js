/**
 * Milan Magrati - Python Full Stack Developer Portfolio
 * Interactive Features: Theme Engine, Typing Animator, Filtering, Modals, AJAX Contact
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeEngine();
  initDesignationTyper();
  initNavbarScrollSpy();
  initMobileNav();
  initSkillsFilter();
  initProjectsFilter();
  initProjectModal();
  initContactForm();
  initSmoothScroll();
  initScrollRevealOneByOne();
  initProfileTilt();
});

/* ==========================================================================
   1. THEME ENGINE (DARK / LIGHT WITH LOCALSTORAGE PERSISTENCE)
   ========================================================================== */
function initThemeEngine() {
  const toggleBtn = document.getElementById('theme-toggle-btn');
  if (!toggleBtn) return;

  const savedTheme = localStorage.getItem('milan_portfolio_theme') || 'dark';
  applyTheme(savedTheme);

  toggleBtn.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
  });
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('milan_portfolio_theme', theme);

  const toggleBtn = document.getElementById('theme-toggle-btn');
  if (!toggleBtn) return;

  const sunIcon = toggleBtn.querySelector('.icon-sun');
  const moonIcon = toggleBtn.querySelector('.icon-moon');

  if (theme === 'light') {
    if (sunIcon) sunIcon.style.display = 'none';
    if (moonIcon) moonIcon.style.display = 'block';
    toggleBtn.setAttribute('aria-label', 'Switch to dark theme');
  } else {
    if (sunIcon) sunIcon.style.display = 'block';
    if (moonIcon) moonIcon.style.display = 'none';
    toggleBtn.setAttribute('aria-label', 'Switch to light theme');
  }
}

/* ==========================================================================
   2. ANIMATED DESIGNATION TYPER
   ========================================================================== */
function initDesignationTyper() {
  const targetElement = document.getElementById('typing-designation');
  if (!targetElement) return;

  let designations = [];
  const scriptElem = document.getElementById('designation-data');
  if (scriptElem) {
    try {
      designations = JSON.parse(scriptElem.textContent);
    } catch (e) {}
  }

  if (!designations || designations.length === 0) {
    try {
      const rawData = targetElement.getAttribute('data-roles');
      if (rawData) designations = JSON.parse(rawData);
    } catch (e) {}
  }

  if (!designations || designations.length === 0) {
    designations = [
      "Python Full Stack Developer",
      "Backend Developer",
      "Django & DRF Specialist",
      "FastAPI & REST API Engineer",
      "AI-Assisted Software Developer"
    ];
  }

  // Reduced motion check
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReducedMotion) {
    targetElement.textContent = designations[0];
    return;
  }

  let roleIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  const typeSpeed = 70;
  const deleteSpeed = 35;
  const pauseEnd = 2400;
  const pauseStart = 400;

  function typeStep() {
    const currentRole = designations[roleIndex];

    if (isDeleting) {
      targetElement.textContent = currentRole.substring(0, charIndex - 1);
      charIndex--;
    } else {
      targetElement.textContent = currentRole.substring(0, charIndex + 1);
      charIndex++;
    }

    let nextDelay = isDeleting ? deleteSpeed : typeSpeed;

    if (!isDeleting && charIndex === currentRole.length) {
      isDeleting = true;
      nextDelay = pauseEnd;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      roleIndex = (roleIndex + 1) % designations.length;
      nextDelay = pauseStart;
    }

    setTimeout(typeStep, nextDelay);
  }

  typeStep();
}

/* ==========================================================================
   3. STICKY NAVBAR & SCROLLSPY
   ========================================================================== */
function initNavbarScrollSpy() {
  const header = document.querySelector('.site-header');
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link, .mobile-nav-link');

  window.addEventListener('scroll', () => {
    // Header shadow on scroll
    if (window.scrollY > 40) {
      header?.classList.add('scrolled');
    } else {
      header?.classList.remove('scrolled');
    }

    // Scrollspy active indicator
    let currentSection = '';
    const scrollPosition = window.scrollY + 140;

    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
        currentSection = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      const href = link.getAttribute('href');
      if (href === `#${currentSection}`) {
        link.classList.add('active');
      }
    });
  });
}

/* ==========================================================================
   4. MOBILE NAVIGATION DRAWER
   ========================================================================== */
function initMobileNav() {
  const hamburgerBtn = document.getElementById('hamburger-btn');
  const mobileDrawer = document.getElementById('mobile-nav-drawer');
  if (!hamburgerBtn || !mobileDrawer) return;

  hamburgerBtn.addEventListener('click', () => {
    const isOpen = mobileDrawer.classList.toggle('open');
    hamburgerBtn.setAttribute('aria-expanded', isOpen);
  });

  // Close on nav link click
  mobileDrawer.querySelectorAll('.mobile-nav-link').forEach(link => {
    link.addEventListener('click', () => {
      mobileDrawer.classList.remove('open');
      hamburgerBtn.setAttribute('aria-expanded', false);
    });
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!mobileDrawer.contains(e.target) && !hamburgerBtn.contains(e.target)) {
      mobileDrawer.classList.remove('open');
      hamburgerBtn.setAttribute('aria-expanded', false);
    }
  });
}

/* ==========================================================================
   5. SKILLS CATEGORY FILTER
   ========================================================================== */
function initSkillsFilter() {
  const skillTabs = document.querySelectorAll('.skill-tab-btn');
  const skillCards = document.querySelectorAll('.skill-card');
  if (!skillTabs.length) return;

  skillTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      skillTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const targetCategory = tab.getAttribute('data-category');

      skillCards.forEach(card => {
        const cardCategory = card.getAttribute('data-category');
        if (targetCategory === 'all' || cardCategory === targetCategory) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/* ==========================================================================
   6. PROJECTS CATEGORY FILTER
   ========================================================================== */
function initProjectsFilter() {
  const filterButtons = document.querySelectorAll('.project-filter-btn');
  const projectCards = document.querySelectorAll('.project-card');
  if (!filterButtons.length) return;

  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      filterButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filterVal = btn.getAttribute('data-filter');

      projectCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filterVal === 'All' || category === filterVal) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/* ==========================================================================
   7. PROJECT DETAILS MODAL
   ========================================================================== */
function initProjectModal() {
  const modal = document.getElementById('project-detail-modal');
  if (!modal) return;

  const closeBtn = modal.querySelector('.modal-close-btn');
  const modalTitle = document.getElementById('modal-project-title');
  const modalCategory = document.getElementById('modal-project-category');
  const modalSummary = document.getElementById('modal-project-summary');
  const modalBullets = document.getElementById('modal-project-bullets');
  const modalTechList = document.getElementById('modal-project-tech');
  const modalGithub = document.getElementById('modal-project-github');
  const modalLive = document.getElementById('modal-project-live');

  // Listen to open modal triggers
  document.querySelectorAll('.open-project-modal-btn').forEach(button => {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      const card = button.closest('.project-card');
      if (!card) return;

      const title = card.getAttribute('data-title') || '';
      const category = card.getAttribute('data-category') || '';
      const summary = card.getAttribute('data-summary') || '';
      const githubUrl = card.getAttribute('data-github') || '';
      const liveUrl = card.getAttribute('data-live') || '';
      
      let bullets = [];
      try {
        bullets = JSON.parse(card.getAttribute('data-bullets') || '[]');
      } catch (err) {
        bullets = [];
      }

      let techList = [];
      try {
        techList = JSON.parse(card.getAttribute('data-tech') || '[]');
      } catch (err) {
        techList = [];
      }

      if (modalTitle) modalTitle.textContent = title;
      if (modalCategory) modalCategory.textContent = category;
      if (modalSummary) modalSummary.textContent = summary;

      // Populate Bullets
      if (modalBullets) {
        modalBullets.innerHTML = '';
        bullets.forEach(bullet => {
          const li = document.createElement('li');
          li.textContent = bullet;
          modalBullets.appendChild(li);
        });
      }

      // Populate Tech Stack Tags
      if (modalTechList) {
        modalTechList.innerHTML = '';
        techList.forEach(tech => {
          const span = document.createElement('span');
          span.className = 'project-tech-chip';
          span.textContent = tech;
          modalTechList.appendChild(span);
        });
      }

      // Action Links
      if (modalGithub) {
        if (githubUrl) {
          modalGithub.href = githubUrl;
          modalGithub.style.display = 'inline-flex';
        } else {
          modalGithub.style.display = 'none';
        }
      }

      if (modalLive) {
        if (liveUrl) {
          modalLive.href = liveUrl;
          modalLive.style.display = 'inline-flex';
        } else {
          modalLive.style.display = 'none';
        }
      }

      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    });
  });

  function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });
}

/* ==========================================================================
   8. AJAX CONTACT FORM SUBMISSION
   ========================================================================== */
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  const submitBtn = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = form.querySelector('[name="name"]')?.value.trim();
    const email = form.querySelector('[name="email"]')?.value.trim();
    const subject = form.querySelector('[name="subject"]')?.value.trim();
    const message = form.querySelector('[name="message"]')?.value.trim();
    const csrfToken = form.querySelector('[name="csrfmiddlewaretoken"]')?.value;

    if (!name || name.length < 2) {
      showToast('Please enter your name (at least 2 characters).', 'error');
      return;
    }
    if (!email || !email.includes('@')) {
      showToast('Please enter a valid email address.', 'error');
      return;
    }
    if (!message || message.length < 10) {
      showToast('Please enter a message of at least 10 characters.', 'error');
      return;
    }

    const originalBtnText = submitBtn ? submitBtn.innerHTML : 'Send Message';
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `
        <span class="btn-text">Sending message...</span>
        <svg class="spin-icon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5">
          <circle cx="12" cy="12" r="10" stroke-opacity="0.2"/>
          <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round"/>
        </svg>
      `;
    }

    try {
      const formData = new FormData(form);

      const response = await fetch(form.action || '/contact/submit/', {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrfToken || '',
        },
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.success) {
        showToast(data.message || 'Message sent successfully! Milan will get back to you shortly.', 'success');
        form.reset();
      } else {
        showToast(data.error || 'Unable to submit your message. Please try again.', 'error');
      }
    } catch (err) {
      showToast('A network error occurred. Please try again or email directly.', 'error');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      }
    }
  });
}

function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4500);
}

/* ==========================================================================
   9. SMOOTH SCROLL FOR IN-PAGE ANCHORS
   ========================================================================== */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;

      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

/* ==========================================================================
   10. SCROLL REVEAL CASCADE: ANIMATE ONE BY ONE
   ========================================================================== */
function initScrollRevealOneByOne() {
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) return;

  const targetSelectors = [
    '.stat-card',
    '.skill-card',
    '.timeline-card',
    '.edu-card',
    '.project-card',
    '.service-card',
    '.cert-card',
    '.contact-status-card',
    '.contact-card',
    '.contact-form-card',
    '.section-header'
  ];

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        obs.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.12,
    rootMargin: '0px 0px -40px 0px'
  });

  targetSelectors.forEach(selector => {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el, index) => {
      el.classList.add('reveal-on-scroll');
      const delayClass = `delay-${(index % 6) + 1}`;
      el.classList.add(delayClass);
      observer.observe(el);
    });
  });
}

/* ==========================================================================
   11. INTERACTIVE 3D AVATAR TILT
   ========================================================================== */
function initProfileTilt() {
  const wrapper = document.querySelector('.profile-card-wrapper');
  if (!wrapper) return;

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) return;

  wrapper.addEventListener('mousemove', (e) => {
    const rect = wrapper.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    const rotateX = (-y / rect.height) * 14;
    const rotateY = (x / rect.width) * 14;

    wrapper.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
    wrapper.style.transition = 'transform 0.1s ease-out';
  });

  wrapper.addEventListener('mouseleave', () => {
    wrapper.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg) scale(1)';
    wrapper.style.transition = 'transform 0.5s ease-out';
  });
}

