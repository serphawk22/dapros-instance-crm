/* ==========================================================================
   DaPros - Digital Growth & Technology Landing Page
   Powered by SERP Hawk CRM
   Interactive Logic Script
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Theme Toggle & Local Storage Persistence
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const htmlElement = document.documentElement;

  const savedTheme = localStorage.getItem('dapros-theme');
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
    htmlElement.setAttribute('data-theme', 'dark');
  } else {
    htmlElement.setAttribute('data-theme', 'light');
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = htmlElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      
      htmlElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('dapros-theme', newTheme);
    });
  }

  // 2. Sticky Navbar Blur Effect on Scroll
  const header = document.getElementById('mainHeader');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      header?.classList.add('scrolled');
    } else {
      header?.classList.remove('scrolled');
    }
  });

  // 3. Mobile Navigation Drawer Toggle
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const mobileDrawerCloseBtn = document.getElementById('mobileDrawerCloseBtn');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const drawerOverlay = document.getElementById('drawerOverlay');

  function openMobileMenu() {
    mobileDrawer?.classList.add('open');
    drawerOverlay?.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileMenu() {
    mobileDrawer?.classList.remove('open');
    drawerOverlay?.classList.remove('active');
    document.body.style.overflow = '';
  }

  mobileMenuBtn?.addEventListener('click', openMobileMenu);
  mobileDrawerCloseBtn?.addEventListener('click', closeMobileMenu);
  drawerOverlay?.addEventListener('click', closeMobileMenu);

  document.querySelectorAll('.mobile-nav-link').forEach(link => {
    link.addEventListener('click', closeMobileMenu);
  });

  // 4. Client 360° Tab Switcher
  const client360Tabs = document.querySelectorAll('.client-360-tabs .tab-btn');
  const clientTabContents = document.querySelectorAll('.client-tab-content');

  client360Tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      client360Tabs.forEach(t => t.classList.remove('active'));
      clientTabContents.forEach(c => c.style.display = 'none');

      tab.classList.add('active');
      const targetId = tab.getAttribute('data-tab');
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        targetEl.style.display = 'grid';
      }
    });
  });

  // 5. FAQ Accordion Logic
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const questionBtn = item.querySelector('.faq-question');
    questionBtn?.addEventListener('click', () => {
      const isActive = item.classList.contains('active');
      faqItems.forEach(i => i.classList.remove('active'));
      if (!isActive) {
        item.classList.add('active');
      }
    });
  });

  // 6. Animated Number Counters on Scroll
  const counterElements = document.querySelectorAll('.count-up');
  let animatedCounters = new Set();

  function animateCounter(el) {
    const target = parseInt(el.getAttribute('data-target') || '0', 10);
    const suffix = el.getAttribute('data-suffix') || '';
    const duration = 2000;
    const stepTime = 20;
    const steps = duration / stepTime;
    const increment = target / steps;
    let current = 0;

    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      el.textContent = Math.floor(current).toLocaleString() + suffix;
    }, stepTime);
  }

  const observerOptions = { threshold: 0.3 };
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        if (!animatedCounters.has(el)) {
          animatedCounters.add(el);
          animateCounter(el);
        }
      }
    });
  }, observerOptions);

  counterElements.forEach(el => counterObserver.observe(el));

  // 7. Contact Form Handling
  const contactForm = document.getElementById('contactForm');
  const formStatus = document.getElementById('formStatusAlert');

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending Message...';
      }

      setTimeout(() => {
        if (formStatus) {
          formStatus.textContent = 'Thank you! Your request has been received. Our team in Guadalajara will follow up via SERP Hawk CRM within 24 hours.';
          formStatus.className = 'form-status-alert success';
        }
        contactForm.reset();
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = 'Send Message';
        }
      }, 800);
    });
  }
});
