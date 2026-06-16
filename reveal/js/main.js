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
  const sidebarItems = document.querySelectorAll('.sidebar-item');
  const sidebarTopics = document.querySelectorAll('.sidebar-topics li');
  const sidebarGroups = document.querySelectorAll('.sidebar-group');
  const sidebarProgressBar = document.getElementById('sidebar-progress-bar');
  const sidebarCounter = document.getElementById('sidebar-counter');
  const sidebarToggle = document.getElementById('sidebar-toggle');
  const sidebarNav = document.getElementById('sidebar-nav');

  // Toggle sidebar open/close
  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = sidebarNav.classList.toggle('open');
      const overlay = document.getElementById('sidebar-overlay');
      if (overlay) overlay.classList.toggle('active', isOpen);
    });
  }

  // Click main section items to navigate
  sidebarItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.stopPropagation();
      const sectionIdx = parseInt(item.dataset.section);
      if (!isNaN(sectionIdx)) {
        deck.slide(sectionIdx, 0);
        // On mobile, close after nav
        if (window.innerWidth < 768) sidebarNav.classList.remove('open');
      }
    });
  });

  // Click subtopics to navigate to specific slide
  sidebarTopics.forEach(topic => {
    topic.addEventListener('click', (e) => {
      e.stopPropagation();
      const sectionIdx = parseInt(topic.dataset.section);
      const slideIdx = parseInt(topic.dataset.slide) || 0;
      if (!isNaN(sectionIdx)) {
        deck.slide(sectionIdx, slideIdx);
        if (window.innerWidth < 768) sidebarNav.classList.remove('open');
      }
    });
  });

  function updateNav() {
    const indices = deck.getIndices();
    const total = deck.getTotalSlides();
    const current = deck.getSlidePastCount() + 1;
    const pct = Math.round((current / total) * 100);

    // Bottom nav
    navProgress.textContent = `${current} / ${total}`;

    // Sidebar: highlight active section and expand its group
    sidebarItems.forEach(item => {
      const sectionIdx = parseInt(item.dataset.section);
      item.classList.toggle('active', sectionIdx === indices.h);
    });

    // Expand active group, collapse others
    sidebarGroups.forEach(group => {
      const groupItem = group.querySelector('.sidebar-item');
      if (groupItem) {
        const sectionIdx = parseInt(groupItem.dataset.section);
        group.classList.toggle('expanded', sectionIdx === indices.h);
      }
    });

    // Highlight closest subtopic
    sidebarTopics.forEach(topic => {
      const sectionIdx = parseInt(topic.dataset.section);
      const slideIdx = parseInt(topic.dataset.slide) || 0;
      // Mark active if same section and current vertical >= this topic's slide
      const isSection = sectionIdx === indices.h;
      const nextTopicSlide = topic.nextElementSibling ? parseInt(topic.nextElementSibling.dataset.slide) || 999 : 999;
      const isActive = isSection && indices.v >= slideIdx && indices.v < nextTopicSlide;
      topic.classList.toggle('active', isActive);
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

  // Close sidebar when clicking outside
  document.addEventListener('click', (e) => {
    if (sidebarNav && sidebarNav.classList.contains('open') && 
        !sidebarNav.contains(e.target) && !sidebarToggle.contains(e.target)) {
      sidebarNav.classList.remove('open');
      const overlay = document.getElementById('sidebar-overlay');
      if (overlay) overlay.classList.remove('active');
    }
  });

  // Sidebar overlay click to close
  const sidebarOverlay = document.getElementById('sidebar-overlay');
  if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', () => {
      sidebarNav.classList.remove('open');
      sidebarOverlay.classList.remove('active');
    });
  }

  // Sidebar close button
  const sidebarClose = document.getElementById('sidebar-close');
  if (sidebarClose) {
    sidebarClose.addEventListener('click', (e) => {
      e.stopPropagation();
      sidebarNav.classList.remove('open');
      if (sidebarOverlay) sidebarOverlay.classList.remove('active');
    });
  }

  // ─── Expandable Cards (event delegation) ───
  // Use delegation on the reveal container so dynamically loaded cards work
  document.querySelector('.reveal').addEventListener('click', (e) => {
    const card = e.target.closest('.card.expandable');
    if (card) {
      e.stopPropagation();
      card.classList.toggle('expanded');
    }
  });

  // Vocab cards (encontro-1 vocabulary slide)
  document.querySelectorAll('.vocab-card').forEach(card => {
    card.addEventListener('click', (e) => {
      e.stopPropagation();
      card.classList.toggle('expanded');
    });
  });
}
