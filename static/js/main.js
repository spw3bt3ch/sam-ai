/**
 * main.js — Samuel Seye Portfolio
 * Handles: navbar scroll effects, mobile menu toggle,
 *          smooth scrolling, scroll reveal, contact form.
 */

(function () {
  "use strict";

  /* ─────────────────────────────────────────────
     1. NAVBAR — scroll-aware styling
  ───────────────────────────────────────────── */
  const navbar = document.getElementById("navbar");
  const NAV_SCROLLED_CLASSES = [
    "py-3",
    "bg-slate-900/95",
    "backdrop-blur-xl",
    "shadow-lg",
    "shadow-black/20",
    "border-b",
    "border-white/5",
  ];
  const NAV_DEFAULT_CLASSES = ["py-5"];

  function updateNavbar() {
    if (window.scrollY > 60) {
      NAV_DEFAULT_CLASSES.forEach((c) => navbar.classList.remove(c));
      NAV_SCROLLED_CLASSES.forEach((c) => navbar.classList.add(c));
    } else {
      NAV_SCROLLED_CLASSES.forEach((c) => navbar.classList.remove(c));
      NAV_DEFAULT_CLASSES.forEach((c) => navbar.classList.add(c));
    }
  }

  window.addEventListener("scroll", updateNavbar, { passive: true });
  updateNavbar(); // run on load


  /* ─────────────────────────────────────────────
     2. MOBILE MENU — toggle
  ───────────────────────────────────────────── */
  const menuBtn = document.getElementById("mobile-menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");
  const hamburgerLines = document.querySelectorAll(".hamburger-line");
  let menuOpen = false;

  function openMenu() {
    mobileMenu.classList.remove("hidden");
    setTimeout(() => mobileMenu.classList.add("opacity-100"), 10);
    hamburgerLines[0].style.transform = "translateY(8px) rotate(45deg)";
    hamburgerLines[1].style.opacity = "0";
    hamburgerLines[2].style.transform = "translateY(-8px) rotate(-45deg)";
    menuBtn.setAttribute("aria-expanded", "true");
    menuOpen = true;
  }

  function closeMenu() {
    mobileMenu.classList.add("hidden");
    hamburgerLines[0].style.transform = "";
    hamburgerLines[1].style.opacity = "";
    hamburgerLines[2].style.transform = "";
    menuBtn.setAttribute("aria-expanded", "false");
    menuOpen = false;
  }

  menuBtn.addEventListener("click", () => {
    menuOpen ? closeMenu() : openMenu();
  });

  // Close menu when a link is clicked
  document.querySelectorAll(".mobile-nav-link").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });

  // Close on outside click
  document.addEventListener("click", (e) => {
    if (menuOpen && !navbar.contains(e.target)) closeMenu();
  });


  /* ─────────────────────────────────────────────
     3. SMOOTH SCROLLING — anchor links
  ───────────────────────────────────────────── */
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");
      if (targetId === "#") return;
      const target = document.querySelector(targetId);
      if (!target) return;
      e.preventDefault();
      const navHeight = navbar.offsetHeight;
      const targetTop = target.getBoundingClientRect().top + window.scrollY - navHeight;
      window.scrollTo({ top: targetTop, behavior: "smooth" });
    });
  });


  /* ─────────────────────────────────────────────
     4. ACTIVE NAV LINK — highlight on scroll
  ───────────────────────────────────────────── */
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".nav-link");

  function highlightNavLink() {
    const scrollY = window.scrollY + navbar.offsetHeight + 60;
    let current = "";
    sections.forEach((section) => {
      if (section.offsetTop <= scrollY) {
        current = section.getAttribute("id");
      }
    });
    navLinks.forEach((link) => {
      link.classList.remove("active");
      if (link.getAttribute("href") === `#${current}`) {
        link.classList.add("active");
      }
    });
  }

  window.addEventListener("scroll", highlightNavLink, { passive: true });


  /* ─────────────────────────────────────────────
     5. SCROLL REVEAL — fade-in on scroll
  ───────────────────────────────────────────── */
  const revealElements = document.querySelectorAll(
    "section, .glass-card, h2, h3"
  );

  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.08 }
  );

  revealElements.forEach((el) => {
    // Only animate elements not already handled by CSS
    if (!el.classList.contains("animate-fade-in") &&
        !el.classList.contains("animate-slide-up")) {
      el.style.opacity = "0";
      el.style.transform = "translateY(20px)";
      el.style.transition = "opacity 0.6s ease, transform 0.6s ease";
      revealObserver.observe(el);
    }
  });


  /* ─────────────────────────────────────────────
     6. CONTACT FORM — client-side validation & mailto
  ───────────────────────────────────────────── */
  const contactForm = document.getElementById("contact-form");
  const feedback = document.getElementById("form-feedback");
  const submitBtn = document.getElementById("form-submit-btn");

  if (contactForm) {
    contactForm.addEventListener("submit", function (e) {
      e.preventDefault();

      const name = document.getElementById("contact-name").value.trim();
      const email = document.getElementById("contact-email").value.trim();
      const subject = document.getElementById("contact-subject").value.trim();
      const message = document.getElementById("contact-message").value.trim();

      // Basic validation
      if (!name || !email || !message) {
        showFeedback("Please fill in your name, email, and message.", "error");
        return;
      }

      if (!isValidEmail(email)) {
        showFeedback("Please enter a valid email address.", "error");
        return;
      }

      // Compose mailto link
      const mailtoSubject = encodeURIComponent(subject || `Portfolio Contact from ${name}`);
      const mailtoBody = encodeURIComponent(
        `Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`
      );
      const mailtoHref = `mailto:samueloluwapelumi8@gmail.com?subject=${mailtoSubject}&body=${mailtoBody}`;

      // Open mail client
      window.location.href = mailtoHref;

      // Show success feedback
      showFeedback("✅ Opening your mail client... Thank you for reaching out, " + name + "!", "success");
      contactForm.reset();
    });
  }

  function showFeedback(msg, type) {
    feedback.textContent = msg;
    feedback.classList.remove("hidden", "bg-green-500/10", "text-green-400", "border-green-500/30", "bg-red-500/10", "text-red-400", "border-red-500/30");
    if (type === "success") {
      feedback.classList.add("bg-green-500/10", "text-green-400", "border", "border-green-500/30");
    } else {
      feedback.classList.add("bg-red-500/10", "text-red-400", "border", "border-red-500/30");
    }
    feedback.classList.remove("hidden");
    setTimeout(() => feedback.classList.add("hidden"), 6000);
  }

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }


  /* ─────────────────────────────────────────────
     7. SKILL BARS — Animate on scroll
  ───────────────────────────────────────────── */
  const skillBars = document.querySelectorAll("[data-width]");

  const barObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const bar = entry.target;
          const targetWidth = bar.getAttribute("data-width");
          bar.style.width = "0%";
          setTimeout(() => {
            bar.style.transition = "width 1.2s cubic-bezier(0.4, 0, 0.2, 1)";
            bar.style.width = targetWidth + "%";
          }, 200);
          barObserver.unobserve(bar);
        }
      });
    },
    { threshold: 0.5 }
  );

  skillBars.forEach((bar) => {
    bar.style.width = "0%";
    barObserver.observe(bar);
  });


  /* ─────────────────────────────────────────────
     8. TYPING EFFECT — Hero tagline (optional)
  ───────────────────────────────────────────── */
  // Subtle cursor blink on hero tagline
  const heroParagraph = document.querySelector("#hero p.text-slate-400");
  // No destructive changes needed; CSS animations handle hero animations.

})();
