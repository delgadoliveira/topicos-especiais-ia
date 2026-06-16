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
    controls: false,       // We use custom nav
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

  // ─── Custom Navigation ───
  const navPrev = document.getElementById('nav-prev');
  const navNext = document.getElementById('nav-next');
  const navProgress = document.getElementById('nav-progress');

  navPrev.addEventListener('click', () => deck.prev());
  navNext.addEventListener('click', () => deck.next());

  function updateNav() {
    const indices = deck.getIndices();
    const total = deck.getTotalSlides();
    const current = deck.getSlidePastCount() + 1;
    navProgress.textContent = `${current} / ${total}`;
  }

  deck.on('slidechanged', (event) => {
    updateNav();
    // Trigger animations on the new slide
    if (window.Animations) {
      window.Animations.onSlideEnter(event.currentSlide);
    }
    // Init PyRunner if this slide has one
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
}
