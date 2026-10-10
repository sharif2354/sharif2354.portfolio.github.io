'use strict';

/* =============================================================
   MD. Sharif Hosen — Interactive Portfolio Scripts
   ============================================================= */

document.addEventListener('DOMContentLoaded', () => {

  /* ==========================================================
     1. HELPER: ELEMENT CLASS TOGGLE
     ========================================================== */
  const elementToggleFunc = (elem) => {
    if (elem) elem.classList.toggle('active');
  };

  /* ==========================================================
     2. SIDEBAR TOGGLE (Mobile & Desktop)
     ========================================================== */
  const sidebar = document.querySelector('[data-sidebar]');
  const sidebarBtn = document.querySelector('[data-sidebar-btn]');

  if (sidebarBtn && sidebar) {
    sidebarBtn.addEventListener('click', () => {
      elementToggleFunc(sidebar);

      const span = sidebarBtn.querySelector('span');
      if (span) {
        span.textContent = sidebar.classList.contains('active')
          ? 'Hide Contacts'
          : 'Show Contacts';
      }
    });
  }

  /* ==========================================================
     3. RESEARCH / TESTIMONIALS MODAL
     ========================================================== */
  const testimonialsItems = document.querySelectorAll('[data-testimonials-item]');
  const modalContainer = document.querySelector('[data-modal-container]');
  const modalCloseBtn = document.querySelector('[data-modal-close-btn]');
  const overlay = document.querySelector('[data-overlay]');
  const modalImg = document.querySelector('[data-modal-img]');
  const modalTitle = document.querySelector('[data-modal-title]');
  const modalText = document.querySelector('[data-modal-text]');

  const toggleModal = () => {
    if (modalContainer) modalContainer.classList.toggle('active');
    if (overlay) overlay.classList.toggle('active');
  };

  if (modalContainer && modalCloseBtn && overlay) {
    testimonialsItems.forEach((item) => {
      item.addEventListener('click', function () {
        const avatar = this.querySelector('[data-testimonials-avatar]');
        const title = this.querySelector('[data-testimonials-title]');
        const text = this.querySelector('[data-testimonials-text]');

        if (modalImg && avatar) {
          modalImg.src = avatar.src;
          modalImg.alt = avatar.alt;
        }
        if (modalTitle && title) modalTitle.innerHTML = title.innerHTML;
        if (modalText && text) modalText.innerHTML = text.innerHTML;

        toggleModal();
      });
    });

    modalCloseBtn.addEventListener('click', toggleModal);
    overlay.addEventListener('click', toggleModal);

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modalContainer.classList.contains('active')) {
        toggleModal();
      }
    });
  }

  /* ==========================================================
     4. PORTFOLIO FILTERING (Dropdown & Buttons)
     ========================================================== */
  const select = document.querySelector('[data-select]');
  const selectItems = document.querySelectorAll('[data-select-item]');
  const selectValue = document.querySelector('[data-selecct-value]');
  const filterBtns = document.querySelectorAll('[data-filter-btn]');
  const filterItems = document.querySelectorAll('[data-filter-item]');

  if (select) {
    select.addEventListener('click', function (e) {
      e.stopPropagation();
      elementToggleFunc(this);
    });

    document.addEventListener('click', () => {
      select.classList.remove('active');
    });
  }

  const filterCategory = (selectedValue) => {
    const target = selectedValue.trim().toLowerCase();

    filterItems.forEach((item) => {
      const itemCategory = (item.dataset.category || '').trim().toLowerCase();
      if (target === 'all' || target === itemCategory) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });
  };

  // Mobile select list clicks
  selectItems.forEach((item) => {
    item.addEventListener('click', function (e) {
      e.stopPropagation();
      const val = this.innerText.trim();

      if (selectValue) selectValue.innerText = val;
      if (select) select.classList.remove('active');
      filterCategory(val);

      filterBtns.forEach((btn) => {
        btn.classList.toggle('active', btn.innerText.trim().toLowerCase() === val.toLowerCase());
      });
    });
  });

  // Desktop category buttons
  filterBtns.forEach((btn) => {
    btn.addEventListener('click', function () {
      const val = this.innerText.trim();

      if (selectValue) selectValue.innerText = val;
      filterCategory(val);

      filterBtns.forEach((b) => b.classList.remove('active'));
      this.classList.add('active');
    });
  });

  /* ==========================================================
     5. SPA TAB NAVIGATION (data-nav-link & data-page)
     ========================================================== */
  const navigationLinks = document.querySelectorAll('[data-nav-link]');
  const pages = document.querySelectorAll('[data-page]');

  navigationLinks.forEach((link) => {
    link.addEventListener('click', function () {
      const selectedPage = this.textContent.trim().toLowerCase();

      navigationLinks.forEach((l) => l.classList.remove('active'));
      pages.forEach((p) => p.classList.remove('active'));

      const matchingPage = Array.from(pages).find(
        (page) => (page.dataset.page || '').trim().toLowerCase() === selectedPage
      );

      if (matchingPage) {
        matchingPage.classList.add('active');
        this.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  });

  /* ==========================================================
     6. CONTACT FORM VALIDATION & SUBMISSION
     ========================================================== */
  const form = document.querySelector('[data-form]');
  const formInputs = document.querySelectorAll('[data-form-input]');
  const formBtn = document.querySelector('[data-form-btn]');

  if (form && formBtn) {
    const validateForm = () => {
      if (form.checkValidity()) {
        formBtn.removeAttribute('disabled');
      } else {
        formBtn.setAttribute('disabled', '');
      }
    };

    formInputs.forEach((input) => {
      input.addEventListener('input', validateForm);
      input.addEventListener('blur', validateForm);
    });

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (formBtn.hasAttribute('disabled')) return;

      const span = formBtn.querySelector('span');
      const originalText = span ? span.textContent : 'Send Message';

      if (span) span.textContent = 'Message Sent!';
      formBtn.setAttribute('disabled', '');

      setTimeout(() => {
        if (span) span.textContent = originalText;
        form.reset();
        validateForm();
      }, 2500);
    });
  }

  /* ==========================================================
     7. KEYBOARD SHORTCUTS
     ========================================================== */
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && select) {
      select.classList.remove('active');
    }
  });

});