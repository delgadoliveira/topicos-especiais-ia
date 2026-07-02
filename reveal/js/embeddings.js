/* ═══════════════════════════════════════════════════════
   EMBEDDINGS.JS — interactive semantic-search playground
   Real in-browser embeddings via transformers.js (multilingual MiniLM).
   Two-tier: demo words render once the model loads; user types 2 words
   to see real cosine similarity + normalized euclidean distance + 2D plot.
   ═══════════════════════════════════════════════════════ */
(function () {
  const MODEL = 'Xenova/paraphrase-multilingual-MiniLM-L12-v2';
  const CDN = 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.2/dist/transformers.js';

  // Demo words grouped by concept (color-coded on the plot)
  const DEMO = [
    { w: 'gato', c: '#f472b6' }, { w: 'cachorro', c: '#f472b6' }, { w: 'cavalo', c: '#f472b6' },
    { w: 'carro', c: '#60a5fa' }, { w: 'ônibus', c: '#60a5fa' }, { w: 'bicicleta', c: '#60a5fa' },
    { w: 'arroz', c: '#fbbf24' }, { w: 'pão', c: '#fbbf24' }, { w: 'maçã', c: '#fbbf24' },
    { w: 'computador', c: '#34d399' }, { w: 'internet', c: '#34d399' }, { w: 'software', c: '#34d399' },
  ];
  // Multiple anchor pairs per axis (averaged) → more stable than a single pair.
  const AXIS_X = [['carro', 'cachorro'], ['mesa', 'gato'], ['computador', 'cavalo']]; // objeto − animal
  const AXIS_Y = [['formiga', 'elefante'], ['pequeno', 'grande'], ['leve', 'pesado']]; // pequeno − grande

  let extractorPromise = null;   // single shared model promise (no duplicate loads)
  let cache = new Map();         // text → Float32Array embedding
  let axes = null;               // { x:[], y:[] }
  let runId = 0;                 // guards against stale renders on rapid clicks
  let bound = false;

  function status(msg) {
    const el = document.getElementById('emb-status');
    if (el) el.innerHTML = msg;
  }

  async function getExtractor() {
    if (!extractorPromise) {
      extractorPromise = (async () => {
        const { pipeline, env } = await import(/* @vite-ignore */ CDN);
        env.allowLocalModels = false;
        env.useBrowserCache = true;
        return pipeline('feature-extraction', MODEL, { dtype: 'q8' });
      })();
    }
    return extractorPromise;
  }

  async function embed(text) {
    const key = text.trim().toLowerCase();
    if (cache.has(key)) return cache.get(key);
    const extractor = await getExtractor();
    const out = await extractor(key, { pooling: 'mean', normalize: true });
    const vec = Float32Array.from(out.data);
    cache.set(key, vec);
    return vec;
  }

  const dot = (a, b) => { let s = 0; for (let i = 0; i < a.length; i++) s += a[i] * b[i]; return s; };
  const sub = (a, b) => { const o = new Float32Array(a.length); for (let i = 0; i < a.length; i++) o[i] = a[i] - b[i]; return o; };
  const norm = (a) => { const n = Math.sqrt(dot(a, a)) || 1; const o = new Float32Array(a.length); for (let i = 0; i < a.length; i++) o[i] = a[i] / n; return o; };
  function euclid(a, b) { let s = 0; for (let i = 0; i < a.length; i++) { const d = a[i] - b[i]; s += d * d; } return Math.sqrt(s); }

  async function meanAxis(pairs) {
    const dim = (await embed('a')).length;
    const acc = new Float32Array(dim);
    for (const [pos, neg] of pairs) {
      const d = sub(await embed(pos), await embed(neg));
      for (let i = 0; i < dim; i++) acc[i] += d[i];
    }
    return norm(acc);
  }

  async function buildAxes() {
    if (axes) return axes;
    const x = await meanAxis(AXIS_X);
    let y = await meanAxis(AXIS_Y);
    // Gram-Schmidt: make Y orthogonal to X so the two axes aren't correlated.
    const proj = dot(y, x);
    const yo = new Float32Array(y.length);
    for (let i = 0; i < y.length; i++) yo[i] = y[i] - proj * x[i];
    axes = { x, y: norm(yo) };
    return axes;
  }

  function projectPoint(vec) {
    return [dot(vec, axes.x), dot(vec, axes.y)];
  }

  function render(points, pair) {
    const svg = document.getElementById('emb-plot');
    if (!svg) return;
    const W = 400, H = 320, PAD = 34;
    const xs = points.map(p => p.x), ys = points.map(p => p.y);
    const minX = Math.min(...xs), maxX = Math.max(...xs);
    const minY = Math.min(...ys), maxY = Math.max(...ys);
    const sx = v => PAD + (maxX === minX ? 0.5 : (v - minX) / (maxX - minX)) * (W - 2 * PAD);
    const sy = v => H - PAD - (maxY === minY ? 0.5 : (v - minY) / (maxY - minY)) * (H - 2 * PAD);
    let el = '';
    // axes cross
    el += `<line x1="${PAD}" y1="${H - PAD}" x2="${W - PAD}" y2="${H - PAD}" stroke="rgba(255,255,255,.25)"/>`;
    el += `<line x1="${PAD}" y1="${PAD}" x2="${PAD}" y2="${H - PAD}" stroke="rgba(255,255,255,.25)"/>`;
    el += `<text x="${W - PAD}" y="${H - PAD + 16}" fill="rgba(255,255,255,.5)" font-size="10" text-anchor="end">objeto →</text>`;
    el += `<text x="${PAD - 6}" y="${PAD - 6}" fill="rgba(255,255,255,.5)" font-size="10">↑ menor</text>`;
    // connecting line for the user pair
    if (pair) {
      const a = points.find(p => p.id === 'A'), b = points.find(p => p.id === 'B');
      if (a && b) el += `<line x1="${sx(a.x)}" y1="${sy(a.y)}" x2="${sx(b.x)}" y2="${sy(b.y)}" stroke="#22d3ee" stroke-width="1.5" stroke-dasharray="4 3"/>`;
    }
    for (const p of points) {
      const cx = sx(p.x), cy = sy(p.y);
      const r = p.user ? 7 : 4.5;
      const stroke = p.user ? '#fff' : 'none';
      el += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${p.color}" stroke="${stroke}" stroke-width="1.5"/>`;
      el += `<text x="${cx + r + 2}" y="${cy + 3}" fill="${p.user ? '#fff' : 'rgba(255,255,255,.8)'}" font-size="${p.user ? 12 : 10}" font-weight="${p.user ? 700 : 400}">${p.label}</text>`;
    }
    svg.innerHTML = el;
  }

  async function run() {
    const inA = document.getElementById('emb-word-a');
    const inB = document.getElementById('emb-word-b');
    const btn = document.getElementById('emb-run');
    const out = document.getElementById('emb-output');
    if (!inA || !inB) return;
    const wa = inA.value.trim(), wb = inB.value.trim();
    if (!wa || !wb) { status('✏️ Digite duas palavras.'); return; }

    const myRun = ++runId;
    if (btn) btn.disabled = true;
    status('⏳ Carregando modelo e calculando embeddings...');
    if (out) out.innerHTML = '';
    try {
      await buildAxes();
      const [va, vb] = [await embed(wa), await embed(wb)];
      if (myRun !== runId) return; // a newer click superseded this one

      const cos = dot(va, vb);                 // vectors are already normalized
      const eu = euclid(va, vb);               // == sqrt(2 - 2*cos) for normalized vecs

      // Plot demo words + the two user words
      const points = [];
      for (const d of DEMO) {
        const [x, y] = projectPoint(await embed(d.w));
        points.push({ x, y, color: d.c, label: d.w });
      }
      const [ax, ay] = projectPoint(va), [bx, by] = projectPoint(vb);
      points.push({ x: ax, y: ay, color: '#22d3ee', label: wa, user: true, id: 'A' });
      points.push({ x: bx, y: by, color: '#e879f9', label: wb, user: true, id: 'B' });
      if (myRun !== runId) return;
      render(points, true);

      const near = cos > 0.6 ? 'muito próximas 🟢' : cos > 0.35 ? 'relacionadas 🟡' : 'distantes 🔴';
      status(`✅ Modelo pronto — embeddings reais (${va.length} dims).`);
      if (out) out.innerHTML =
        `<div class="card card-cyan" style="padding:0.5rem 0.7rem;">` +
        `<div><b>${wa}</b> → [${Array.from(va.slice(0, 4)).map(v => v.toFixed(2)).join(', ')}, …]</div>` +
        `<div><b>${wb}</b> → [${Array.from(vb.slice(0, 4)).map(v => v.toFixed(2)).join(', ')}, …]</div>` +
        `<div style="margin-top:0.35rem;">Cosseno: <b>${cos.toFixed(3)}</b> · Distância euclidiana (norm.): <b>${eu.toFixed(3)}</b></div>` +
        `<div style="opacity:0.8;">→ ${near}</div></div>`;
    } catch (e) {
      if (myRun !== runId) return;
      status('⚠️ Não consegui carregar o modelo (sem internet ou CDN bloqueado). O conceito continua nos slides ao lado.');
      console.error('[embeddings widget]', e);
    } finally {
      if (btn && myRun === runId) btn.disabled = false;
    }
  }

  function bind() {
    if (bound) return;
    const btn = document.getElementById('emb-run');
    if (!btn) return;
    bound = true;
    btn.addEventListener('click', run);
    ['emb-word-a', 'emb-word-b'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.addEventListener('keydown', e => { if (e.key === 'Enter') run(); });
    });
  }

  // Sections are injected async; try now and again on every slide change.
  document.addEventListener('DOMContentLoaded', bind);
  window.addEventListener('reveal-ready', (ev) => {
    bind();
    const deck = ev.detail && ev.detail.deck;
    if (deck) deck.on('slidechanged', bind);
  });
})();
