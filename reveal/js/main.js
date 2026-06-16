/* ═══════════════════════════════════════════════════════
   MAIN.JS — Reveal.js initialization + custom nav
   ═══════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
  // ─── Load external sections ───
  const sectionFiles = [
    { id: 'encontro-1', file: 'reveal/sections/encontro-1.html' },
    { id: 'encontro-2', file: 'reveal/sections/encontro-2.html' },
    { id: 'encontro-3', file: 'reveal/sections/encontro-3.html' },
    { id: 'encontro-4', file: 'reveal/sections/encontro-4.html' },
  ];

  const loadPromises = sectionFiles.map(({ id, file }) => 
    fetch(file)
      .then(r => r.ok ? r.text() : '')
      .then(html => {
        const el = document.getElementById(id);
        if (el && html) el.innerHTML = html;
      })
      .catch(() => {})
  );

  Promise.all(loadPromises).then(initReveal);
});

function initReveal() {
  const deck = new Reveal({
    hash: true,
    history: true,
    transition: 'slide',
    transitionSpeed: 'fast',
    backgroundTransition: 'fade',
    center: false,
    width: 1280,
    height: 720,
    margin: 0.08,
    controls: false,
    controlsLayout: 'none',
    progress: true,
    slideNumber: false,
    keyboard: true,
    overview: true,
    touch: true,
    fragments: true,
    plugins: [RevealHighlight, RevealNotes, RevealMarkdown]
  });

  deck.initialize();

  // ─── Bottom Navigation ───
  const navPrev = document.getElementById('nav-prev');
  const navNext = document.getElementById('nav-next');
  const navProgress = document.getElementById('nav-progress');

  navPrev.addEventListener('click', () => deck.prev());
  navNext.addEventListener('click', () => deck.next());

  // ─── Sidebar Navigation ───
  const sidebarItems = document.querySelectorAll('.sidebar-section');
  const sidebarProgressBar = document.getElementById('sidebar-progress-bar');
  const sidebarCounter = document.getElementById('sidebar-counter');
  const sidebarToggle = document.getElementById('sidebar-toggle');
  const sidebarNav = document.getElementById('sidebar-nav');

  // Toggle sidebar on mobile
  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', () => {
      sidebarNav.classList.toggle('open');
    });
  }

  // Click to navigate to section
  sidebarItems.forEach(item => {
    item.addEventListener('click', () => {
      const sectionIdx = parseInt(item.dataset.section);
      deck.slide(sectionIdx, 0);
      sidebarNav.classList.remove('open');
    });
  });

  function updateNav() {
    const indices = deck.getIndices();
    const total = deck.getTotalSlides();
    const current = deck.getSlidePastCount() + 1;
    const pct = Math.round((current / total) * 100);

    // Bottom nav
    navProgress.textContent = `${current} / ${total}`;

    // Sidebar: highlight active section
    sidebarItems.forEach(item => {
      const sectionIdx = parseInt(item.dataset.section);
      item.classList.toggle('active', sectionIdx === indices.h);
    });

    // Sidebar progress
    if (sidebarProgressBar) {
      sidebarProgressBar.style.width = pct + '%';
    }
    if (sidebarCounter) {
      sidebarCounter.textContent = `${current} / ${total} (${pct}%)`;
    }
  }

  deck.on('slidechanged', (event) => {
    updateNav();
    if (window.Animations) {
      window.Animations.onSlideEnter(event.currentSlide);
    }
    if (window.PyRunner) {
      window.PyRunner.initAll();
    }
  });

  deck.on('fragmentshown', updateNav);
  deck.on('fragmenthidden', updateNav);

  // Initial state
  updateNav();
  const currentSlide = deck.getCurrentSlide();
  if (currentSlide && window.Animations) {
    window.Animations.onSlideEnter(currentSlide);
  }
  if (window.PyRunner) {
    window.PyRunner.initAll();
  }

  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', (e) => {
    if (sidebarNav && !sidebarNav.contains(e.target)) {
      sidebarNav.classList.remove('open');
    }
  });
}
