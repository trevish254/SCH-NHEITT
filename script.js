const menuButton = document.querySelector('.menu-toggle');
const menuPanel = document.querySelector('.menu-panel');

function setMenuOpen(open) {
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  menuPanel.setAttribute('aria-hidden', String(!open));
  menuPanel.inert = !open;
  menuPanel.classList.toggle('is-open', open);
}

menuButton.addEventListener('click', () => {
  setMenuOpen(menuButton.getAttribute('aria-expanded') !== 'true');
});

menuPanel.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => setMenuOpen(false));
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') setMenuOpen(false);
});

const brandGallery = document.querySelector('.brand-gallery');
const galleryScenes = brandGallery?.querySelectorAll('[data-gallery-scene]');
const galleryTheme = brandGallery?.querySelector('[data-gallery-theme]');
const galleryNumber = brandGallery?.querySelector('[data-gallery-number]');

if (brandGallery && galleryScenes?.length && galleryTheme && galleryNumber) {
  const galleryThemes = ['RADIANCE', 'RESTORE', 'RENEW'];
  let galleryFrame = 0;
  let currentThemeIndex = -1;

  const updateBrandGallery = () => {
    galleryFrame = 0;
    const sectionTop = brandGallery.getBoundingClientRect().top;
    const scrollRange = brandGallery.offsetHeight - window.innerHeight;
    const progress = Math.min(1, Math.max(0, -sectionTop / Math.max(1, scrollRange)));
    const scenePosition = progress * (galleryScenes.length - 1);
    const nextThemeIndex = Math.min(galleryScenes.length - 1, Math.round(scenePosition));

    galleryScenes.forEach((scene, index) => {
      const distance = index - scenePosition;
      scene.style.opacity = String(Math.max(0, 1 - Math.abs(distance)));
      scene.style.transform = `translate3d(0, ${distance * 12}svh, 0)`;
      scene.setAttribute('aria-hidden', String(index !== nextThemeIndex));
      scene.classList.toggle('is-active', index === nextThemeIndex);
    });

    const copyShift = scenePosition <= 1
      ? -12.5 * scenePosition
      : -12.5 - 2.5 * (scenePosition - 1);
    brandGallery.style.setProperty('--gallery-copy-shift', `${copyShift}svh`);

    if (nextThemeIndex !== currentThemeIndex) {
      currentThemeIndex = nextThemeIndex;
      galleryTheme.textContent = galleryThemes[currentThemeIndex];
      galleryNumber.textContent = String(currentThemeIndex + 1);
    }
  };

  const requestGalleryUpdate = () => {
    if (!galleryFrame) galleryFrame = window.requestAnimationFrame(updateBrandGallery);
  };

  window.addEventListener('scroll', requestGalleryUpdate, { passive: true });
  window.addEventListener('resize', requestGalleryUpdate);
  requestGalleryUpdate();
}

const testimonials = [
  {
        quote: 'A thoughtful moment of care. I left feeling calm, refreshed, and more like myself.',
    name: 'Spa guest',
    role: 'Studio guest',
    image: 'assets/face-tile.webp',
    alt: 'Guest portrait surrounded by flowers'
  },
  {
        quote: 'The treatment felt tailored to me, and my skin looked refreshed afterward.',
    name: 'Studio guest',
    role: 'Spa guest',
    image: 'assets/hero-portrait.webp',
    alt: 'Close-up beauty portrait'
  },
  {
        quote: 'The team made me feel at ease. A relaxing reset from start to finish.',
    name: 'Studio guest',
    role: 'Spa guest',
    image: 'assets/face-main.webp',
    alt: 'Skincare guest portrait'
  }
];

const testimonialsSection = document.querySelector('[data-testimonials]');
if (testimonialsSection) {
  const image = testimonialsSection.querySelector('[data-testimonial-image]');
  const quote = testimonialsSection.querySelector('[data-testimonial-quote]');
  const name = testimonialsSection.querySelector('[data-testimonial-name]');
  const role = testimonialsSection.querySelector('[data-testimonial-role]');
  const dots = [...testimonialsSection.querySelectorAll('[data-testimonial-dot]')];
  const previous = testimonialsSection.querySelector('[data-testimonial-prev]');
  const next = testimonialsSection.querySelector('[data-testimonial-next]');
  let activeTestimonial = 0;

  const showTestimonial = (index) => {
    activeTestimonial = (index + testimonials.length) % testimonials.length;
    const item = testimonials[activeTestimonial];
    image.src = item.image;
    image.alt = item.alt;
    quote.textContent = item.quote;
    name.textContent = item.name;
    role.textContent = item.role;
    dots.forEach((dot, dotIndex) => {
      dot.setAttribute('aria-pressed', String(dotIndex === activeTestimonial));
    });
  };

  previous.addEventListener('click', () => showTestimonial(activeTestimonial - 1));
  next.addEventListener('click', () => showTestimonial(activeTestimonial + 1));
  dots.forEach((dot) => {
    dot.addEventListener('click', () => showTestimonial(Number(dot.dataset.testimonialDot)));
  });
}

const contactForm = document.querySelector('[data-contact-form]');
contactForm?.addEventListener('submit', (event) => {
  event.preventDefault();
  const fields = new FormData(contactForm);
  const subject = `Appointment inquiry — ${fields.get('service')}`;
  const body = [
    `Name: ${fields.get('name')}`,
    `Email: ${fields.get('email')}`,
    `Interested in: ${fields.get('service')}`,
    '',
    'Message:',
    fields.get('message') || ''
  ].join('\n');
  window.location.href = `mailto:sales@loiseau.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
});
