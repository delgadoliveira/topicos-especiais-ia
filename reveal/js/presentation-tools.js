/* global Reveal */
(function () {
  const STORAGE_PREFIX = 'topicos-ia-annotations:v1:';
  const LOGICAL_WIDTH = 1280;
  const LOGICAL_HEIGHT = 720;
  const MODES = new Set(['cursor', 'pen', 'highlight', 'eraser', 'laser']);
  const COLORS = ['#f87171', '#facc15', '#22d3ee', '#a78bfa'];

  let deck = null;
  let canvas = null;
  let ctx = null;
  let toolbar = null;
  let laserDot = null;
  let mode = 'cursor';
  let color = COLORS[1];
  let strokes = [];
  let currentStroke = null;
  let activePointerId = null;
  let laserTimer = null;

  function init(activeDeck) {
    deck = activeDeck || window.revealDeck || window.Reveal;
    if (!deck || document.querySelector('.presentation-toolbar')) return;

    canvas = document.createElement('canvas');
    canvas.className = 'annotation-canvas';
    canvas.setAttribute('aria-hidden', 'true');
    document.body.appendChild(canvas);
    ctx = canvas.getContext('2d');

    toolbar = buildToolbar();
    document.body.appendChild(toolbar);
    document.body.appendChild(buildHint());

    laserDot = document.createElement('div');
    laserDot.className = 'annotation-laser-dot';
    document.body.appendChild(laserDot);

    bindCanvas();
    bindDeck();
    bindShortcuts();
    setMode('cursor');
    refreshSlide();
    window.PresentationTools = {
      setMode,
      setColor,
      clearSlide,
      clearAll,
      undo,
      exportAnnotations: () => JSON.stringify(strokes),
    };
  }

  function buildToolbar() {
    const el = document.createElement('div');
    el.className = 'presentation-toolbar';
    el.setAttribute('role', 'toolbar');
    el.setAttribute('aria-label', 'Ferramentas de apresentação');
    el.innerHTML = `
      <button type="button" data-mode="cursor" title="Cursor / navegar (Esc)">↖</button>
      <button type="button" data-mode="pen" title="Caneta (D)">✎</button>
      <button type="button" data-mode="highlight" title="Marca-texto (H)">▰</button>
      <button type="button" data-mode="eraser" title="Borracha (E)">⌫</button>
      <button type="button" data-mode="laser" title="Laser pointer (L)">●</button>
      <div class="toolbar-divider"></div>
      <div class="color-row" aria-label="Cores">
        ${COLORS.map((item) => `<button type="button" class="color-dot" data-color="${item}" style="background:${item}" title="Cor ${item}"></button>`).join('')}
      </div>
      <div class="toolbar-divider"></div>
      <button type="button" data-action="undo" title="Desfazer último traço (Ctrl+Z)">↶</button>
      <button type="button" data-action="clear" title="Limpar anotações deste slide (C)">🧹</button>
      <button type="button" data-action="collapse" title="Recolher/mostrar barra (P)">⫶</button>
    `;
    el.addEventListener('click', (event) => {
      event.stopPropagation();
      const button = event.target.closest('button');
      if (!button) return;
      if (button.dataset.mode) setMode(button.dataset.mode);
      if (button.dataset.color) setColor(button.dataset.color);
      if (button.dataset.action === 'undo') undo();
      if (button.dataset.action === 'clear') clearSlide();
      if (button.dataset.action === 'collapse') el.classList.toggle('is-collapsed');
    });
    return el;
  }

  function buildHint() {
    const el = document.createElement('div');
    el.className = 'annotation-hint';
    el.innerHTML = '<b>Ferramentas:</b> D caneta · H marca-texto · E borracha · L laser · Esc cursor · C limpa slide · Ctrl+Z desfaz · P recolhe.';
    return el;
  }

  function bindDeck() {
    const refresh = () => {
      refreshSlide();
      if (mode !== 'cursor') setMode('cursor');
    };
    if (deck && typeof deck.on === 'function') {
      deck.on('ready', refreshSlide);
      deck.on('slidechanged', refresh);
      deck.on('slidetransitionend', positionCanvas);
      deck.on('resize', positionCanvas);
      deck.on('overviewshown', () => document.body.classList.add('annotation-overview'));
      deck.on('overviewhidden', () => document.body.classList.remove('annotation-overview'));
    }
    window.addEventListener('resize', positionCanvas);
    window.addEventListener('orientationchange', positionCanvas);
  }

  function bindShortcuts() {
    const mappings = [
      { keyCode: 68, key: 'D', description: 'Caneta', handler: () => setMode('pen') },
      { keyCode: 72, key: 'H', description: 'Marca-texto', handler: () => setMode('highlight') },
      { keyCode: 69, key: 'E', description: 'Borracha', handler: () => setMode('eraser') },
      { keyCode: 76, key: 'L', description: 'Laser pointer', handler: () => setMode('laser') },
      { keyCode: 67, key: 'C', description: 'Limpar anotações do slide', handler: clearSlide },
      { keyCode: 80, key: 'P', description: 'Recolher ferramentas', handler: () => toolbar.classList.toggle('is-collapsed') },
    ];

    const registeredWithReveal = deck && typeof deck.addKeyBinding === 'function';
    mappings.forEach(({ keyCode, key, description, handler }) => {
      if (registeredWithReveal) {
        deck.addKeyBinding({ keyCode, key, description }, () => {
          if (!isEditableElement(document.activeElement)) handler();
        });
      }
    });

    document.addEventListener('keydown', (event) => {
      if (isEditableElement(event.target)) return;
      if (event.key === 'Escape') {
        setMode('cursor');
        return;
      }
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'z') {
        event.preventDefault();
        undo();
      }
      if (!registeredWithReveal && !event.ctrlKey && !event.metaKey && !event.altKey) {
        const shortcut = mappings.find((item) => item.key.toLowerCase() === event.key.toLowerCase());
        if (shortcut) shortcut.handler();
      }
    });
  }

  function bindCanvas() {
    canvas.addEventListener('pointerdown', (event) => {
      if (mode === 'cursor') return;
      event.preventDefault();
      event.stopPropagation();
      activePointerId = event.pointerId;
      canvas.setPointerCapture(activePointerId);

      if (mode === 'laser') {
        moveLaser(event.clientX, event.clientY);
        return;
      }

      const point = toLogicalPoint(event);
      if (!point) return;
      if (mode === 'eraser') {
        eraseAt(point);
        return;
      }

      currentStroke = {
        mode,
        color,
        width: mode === 'highlight' ? 24 : 5,
        points: [point],
      };
      draw();
    });

    canvas.addEventListener('pointermove', (event) => {
      if (event.pointerId !== activePointerId || mode === 'cursor') return;
      event.preventDefault();
      event.stopPropagation();
      if (mode === 'laser') {
        moveLaser(event.clientX, event.clientY);
        return;
      }
      const point = toLogicalPoint(event);
      if (!point) return;
      if (mode === 'eraser') {
        eraseAt(point);
        return;
      }
      if (currentStroke) {
        currentStroke.points.push(point);
        draw();
      }
    });

    canvas.addEventListener('pointerup', finishPointer);
    canvas.addEventListener('pointercancel', finishPointer);
  }

  function finishPointer(event) {
    if (event.pointerId !== activePointerId) return;
    event.preventDefault();
    event.stopPropagation();
    if (currentStroke && currentStroke.points.length > 1) {
      strokes.push(currentStroke);
      saveStrokes();
    }
    currentStroke = null;
    activePointerId = null;
    hideLaserSoon();
  }

  function setMode(nextMode) {
    if (!MODES.has(nextMode)) return;
    mode = nextMode;
    document.body.classList.toggle('annotation-active', mode !== 'cursor');
    document.body.classList.remove('annotation-mode-pen', 'annotation-mode-highlight', 'annotation-mode-eraser', 'annotation-mode-laser');
    document.body.classList.add(`annotation-mode-${mode}`);
    if (deck && typeof deck.configure === 'function') deck.configure({ touch: mode === 'cursor' });
    updateToolbar();
  }

  function setColor(nextColor) {
    if (!COLORS.includes(nextColor)) return;
    color = nextColor;
    updateToolbar();
  }

  function updateToolbar() {
    if (!toolbar) return;
    toolbar.querySelectorAll('[data-mode]').forEach((button) => {
      button.classList.toggle('is-active', button.dataset.mode === mode);
    });
    toolbar.querySelectorAll('[data-color]').forEach((button) => {
      button.classList.toggle('is-active', button.dataset.color === color);
    });
  }

  function refreshSlide() {
    strokes = loadStrokes();
    currentStroke = null;
    positionCanvas();
    draw();
  }

  function positionCanvas() {
    if (!canvas) return;
    const slides = document.querySelector('.reveal .slides');
    const rect = slides ? slides.getBoundingClientRect() : document.body.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.style.left = `${rect.left}px`;
    canvas.style.top = `${rect.top}px`;
    canvas.style.width = `${rect.width}px`;
    canvas.style.height = `${rect.height}px`;
    canvas.width = Math.max(1, Math.round(rect.width * dpr));
    canvas.height = Math.max(1, Math.round(rect.height * dpr));
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    draw();
  }

  function draw() {
    if (!ctx || !canvas) return;
    const rect = canvas.getBoundingClientRect();
    ctx.clearRect(0, 0, rect.width, rect.height);
    [...strokes, currentStroke].filter(Boolean).forEach((stroke) => drawStroke(stroke, rect));
  }

  function drawStroke(stroke, rect) {
    if (!stroke.points.length) return;
    ctx.save();
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.strokeStyle = stroke.color;
    ctx.lineWidth = scaleWidth(stroke.width, rect);
    ctx.globalAlpha = stroke.mode === 'highlight' ? 0.34 : 0.95;
    ctx.globalCompositeOperation = 'source-over';
    ctx.beginPath();
    stroke.points.forEach((point, index) => {
      const x = (point.x / LOGICAL_WIDTH) * rect.width;
      const y = (point.y / LOGICAL_HEIGHT) * rect.height;
      if (index === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
    ctx.restore();
  }

  function scaleWidth(width, rect) {
    return width * Math.min(rect.width / LOGICAL_WIDTH, rect.height / LOGICAL_HEIGHT);
  }

  function toLogicalPoint(event) {
    const rect = canvas.getBoundingClientRect();
    if (!rect.width || !rect.height) return null;
    return {
      x: clamp(((event.clientX - rect.left) / rect.width) * LOGICAL_WIDTH, 0, LOGICAL_WIDTH),
      y: clamp(((event.clientY - rect.top) / rect.height) * LOGICAL_HEIGHT, 0, LOGICAL_HEIGHT),
    };
  }

  function eraseAt(point) {
    const before = strokes.length;
    strokes = strokes.filter((stroke) => !stroke.points.some((item) => distance(item, point) < 18));
    if (strokes.length !== before) {
      saveStrokes();
      draw();
    }
  }

  function undo() {
    if (!strokes.length) return;
    strokes.pop();
    saveStrokes();
    draw();
  }

  function clearSlide() {
    strokes = [];
    saveStrokes();
    draw();
  }

  function clearAll() {
    Object.keys(localStorage)
      .filter((key) => key.startsWith(STORAGE_PREFIX))
      .forEach((key) => localStorage.removeItem(key));
    refreshSlide();
  }

  function moveLaser(clientX, clientY) {
    laserDot.style.left = `${clientX}px`;
    laserDot.style.top = `${clientY}px`;
    laserDot.classList.add('is-visible');
    window.clearTimeout(laserTimer);
  }

  function hideLaserSoon() {
    window.clearTimeout(laserTimer);
    laserTimer = window.setTimeout(() => laserDot.classList.remove('is-visible'), 350);
  }

  function loadStrokes() {
    try {
      const raw = localStorage.getItem(storageKey());
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }

  function saveStrokes() {
    try {
      const payload = JSON.stringify(strokes);
      if (payload.length < 250000) localStorage.setItem(storageKey(), payload);
    } catch {
      // If localStorage is unavailable or full, keep annotations for the current session only.
    }
  }

  function storageKey() {
    const slide = getCurrentSlide();
    const stableKey = slide?.id || slide?.dataset?.annotKey || hashString(slide?.textContent || window.location.hash || 'slide');
    return `${STORAGE_PREFIX}${window.location.pathname}:${stableKey}`;
  }

  function getCurrentSlide() {
    if (deck && typeof deck.getCurrentSlide === 'function') return deck.getCurrentSlide();
    return document.querySelector('.slides section.present');
  }

  function distance(a, b) {
    return Math.hypot(a.x - b.x, a.y - b.y);
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function hashString(value) {
    let hash = 0;
    for (let i = 0; i < value.length; i += 1) {
      hash = ((hash << 5) - hash + value.charCodeAt(i)) | 0;
    }
    return `slide-${Math.abs(hash)}`;
  }

  function isEditableElement(element) {
    if (!element) return false;
    return Boolean(element.closest('input, textarea, select, [contenteditable="true"]'));
  }

  window.addEventListener('reveal-ready', (event) => init(event.detail?.deck));
  document.addEventListener('DOMContentLoaded', () => {
    const wait = window.setInterval(() => {
      if (window.revealDeck) {
        window.clearInterval(wait);
        init(window.revealDeck);
      }
    }, 100);
    window.setTimeout(() => window.clearInterval(wait), 5000);
  });
})();
