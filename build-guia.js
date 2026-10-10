/**
 * Gera GUIA_PROFESSOR.html a partir de GUIA_PROFESSOR.md.
 * HTML autocontido (sem rede): sumario lateral, busca e estilo de impressao.
 * Uso: npm run guia
 */
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');

const SRC = path.join(__dirname, 'GUIA_PROFESSOR.md');
const OUT = path.join(__dirname, 'GUIA_PROFESSOR.html');

const md = fs.readFileSync(SRC, 'utf8');

const toc = [];
const used = new Map();

function slugify(text) {
  const base = text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^\p{L}\p{N}]+/gu, '-')
    .replace(/^-+|-+$/g, '') || 'secao';
  const n = (used.get(base) || 0) + 1;
  used.set(base, n);
  return n === 1 ? base : `${base}-${n}`;
}

const renderer = new marked.Renderer();
const baseHeading = renderer.heading.bind(renderer);

renderer.heading = function (token) {
  const text = this.parser.parseInline(token.tokens);
  const plain = text.replace(/<[^>]+>/g, '').trim();
  const id = slugify(plain);
  if (token.depth <= 2) toc.push({ level: token.depth, id, text: plain });
  return `<h${token.depth} id="${id}"><a class="anchor" href="#${id}">#</a>${text}</h${token.depth}>\n`;
};

marked.setOptions({ renderer, gfm: true, breaks: false });

let body = marked.parse(md);

// Realca os marcadores pedagogicos usados no guia.
const MARKS = [
  ['💡', 'insight'],
  ['⚠️', 'alerta'],
  ['🎬', 'aovivo'],
  ['📊', 'dado'],
  ['🧩', 'analogia'],
];
for (const [emoji, cls] of MARKS) {
  body = body.replace(
    new RegExp(`<(li|p)>\\s*${emoji}`, 'g'),
    `<$1 class="mark mark-${cls}">${emoji}`
  );
}

const tocHtml = toc
  .map((h) => `<a class="toc-l${h.level}" href="#${h.id}">${h.text}</a>`)
  .join('\n');

const title = toc.length ? toc[0].text : 'Guia do Professor';
const generated = new Date().toLocaleDateString('pt-BR', {
  day: '2-digit', month: 'long', year: 'numeric',
});

const html = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<style>
:root{
  --bg:#f6f7f9; --panel:#ffffff; --ink:#15181d; --muted:#616b7a;
  --line:#e2e6ec; --accent:#1f6feb; --accent-soft:#e7f0fe;
  --warn:#b8690a; --warn-soft:#fdf3e3; --live:#8b3dca; --live-soft:#f5ecfd;
  --data:#0b7a63; --data-soft:#e4f5f1; --idea:#1f6feb; --idea-soft:#e7f0fe;
  --maxw:62rem;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font:16px/1.65 -apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  -webkit-font-smoothing:antialiased;
}
#layout{display:grid; grid-template-columns:19rem minmax(0,1fr); min-height:100vh}

/* ---------- sumario ---------- */
#side{
  position:sticky; top:0; align-self:start; height:100vh; overflow:auto;
  background:var(--panel); border-right:1px solid var(--line); padding:1.25rem 1rem 3rem;
}
#side h2{margin:0 0 .25rem; font-size:.78rem; letter-spacing:.09em; text-transform:uppercase; color:var(--muted)}
#side .sub{margin:0 0 .9rem; font-size:.78rem; color:var(--muted)}
#q{
  width:100%; padding:.5rem .65rem; margin-bottom:.9rem; font-size:.85rem;
  border:1px solid var(--line); border-radius:7px; background:#fbfcfd; color:var(--ink);
}
#q:focus{outline:2px solid var(--accent-soft); border-color:var(--accent)}
#toc a{
  display:block; padding:.3rem .55rem; margin:.1rem 0; border-radius:6px;
  color:var(--muted); text-decoration:none; font-size:.85rem; line-height:1.35;
}
#toc a:hover{background:var(--accent-soft); color:var(--accent)}
#toc a.toc-l1{margin-top:.85rem; font-weight:650; font-size:.9rem; color:var(--ink)}
#toc a.toc-l2{padding-left:1.1rem}
#toc a.active{background:var(--accent-soft); color:var(--accent); font-weight:600}
#toc a.hide{display:none}

/* ---------- conteudo ---------- */
main{padding:2.5rem clamp(1.1rem,4vw,3.5rem) 6rem; max-width:calc(var(--maxw) + 7rem)}
article{max-width:var(--maxw)}
h1,h2,h3,h4{line-height:1.25; scroll-margin-top:1.5rem}
h1{
  margin:3.2rem 0 1rem; padding:.85rem 0 .85rem 1rem; font-size:1.85rem; font-weight:700;
  border-left:5px solid var(--accent); background:linear-gradient(90deg,var(--accent-soft),transparent 70%);
  border-radius:0 10px 10px 0;
}
article > h1:first-of-type{margin-top:0}
h2{margin:2.4rem 0 .8rem; font-size:1.3rem; padding-bottom:.35rem; border-bottom:1px solid var(--line)}
h3{margin:1.8rem 0 .5rem; font-size:1.06rem; color:#2b3340}
h4{margin:1.3rem 0 .4rem; font-size:.95rem; color:var(--muted); text-transform:uppercase; letter-spacing:.05em}
p,li{font-size:.97rem}
a{color:var(--accent)}
.anchor{
  float:left; margin-left:-1.15rem; width:1.15rem; opacity:0; text-decoration:none;
  color:var(--muted); font-weight:400;
}
h1:hover .anchor,h2:hover .anchor,h3:hover .anchor{opacity:.5}
hr{border:0; border-top:1px dashed var(--line); margin:2.5rem 0}
blockquote{
  margin:1.2rem 0; padding:.75rem 1rem; background:var(--panel);
  border-left:4px solid var(--line); border-radius:0 8px 8px 0; color:#39414e;
}
blockquote p{margin:.35rem 0}
code{
  background:#eef1f5; padding:.12rem .35rem; border-radius:5px;
  font:0.86em/1.5 ui-monospace,"Cascadia Code",Consolas,monospace;
}
pre{
  background:#15181d; color:#e6edf3; padding:1rem; border-radius:10px; overflow:auto;
  font:0.85rem/1.55 ui-monospace,"Cascadia Code",Consolas,monospace;
}
pre code{background:none; padding:0; color:inherit}
table{
  border-collapse:collapse; width:100%; margin:1.1rem 0; background:var(--panel);
  border:1px solid var(--line); border-radius:10px; overflow:hidden; font-size:.9rem;
}
th,td{padding:.55rem .7rem; text-align:left; border-bottom:1px solid var(--line); vertical-align:top}
th{background:#eff2f6; font-weight:650; font-size:.82rem; text-transform:uppercase; letter-spacing:.03em}
tr:last-child td{border-bottom:0}
tbody tr:hover{background:#f9fafc}
ul,ol{padding-left:1.3rem}
li{margin:.3rem 0}
li::marker{color:var(--muted)}

/* ---------- marcadores pedagogicos ---------- */
.mark{
  list-style:none; margin-left:-1.3rem; padding:.5rem .75rem .5rem .8rem;
  border-left:3px solid var(--line); border-radius:0 7px 7px 0; background:var(--panel);
}
p.mark{margin-left:0}
.mark-insight{border-color:var(--idea); background:var(--idea-soft)}
.mark-alerta{border-color:var(--warn); background:var(--warn-soft)}
.mark-aovivo{border-color:var(--live); background:var(--live-soft)}
.mark-dado{border-color:var(--data); background:var(--data-soft)}
.mark-analogia{border-color:var(--data); background:var(--data-soft)}

#meta{
  margin-top:4rem; padding-top:1rem; border-top:1px solid var(--line);
  font-size:.8rem; color:var(--muted);
}
#top{
  position:fixed; right:1.4rem; bottom:1.4rem; width:2.6rem; height:2.6rem; border-radius:50%;
  border:1px solid var(--line); background:var(--panel); color:var(--muted); cursor:pointer;
  font-size:1rem; box-shadow:0 2px 10px rgba(0,0,0,.09);
}
#top:hover{color:var(--accent); border-color:var(--accent)}

@media (max-width:900px){
  #layout{grid-template-columns:1fr}
  #side{position:static; height:auto; max-height:17rem; border-right:0; border-bottom:1px solid var(--line)}
  main{padding:1.5rem 1.1rem 4rem}
}
@media print{
  #side,#top{display:none}
  #layout{display:block}
  body{background:#fff; font-size:11pt}
  main{padding:0; max-width:none}
  h1{break-before:page; background:none; border-left:4px solid #000}
  article > h1:first-of-type{break-before:avoid}
  h1,h2,h3{break-after:avoid}
  table,pre,blockquote,.mark{break-inside:avoid}
  .anchor{display:none}
}
</style>
</head>
<body>
<div id="layout">
  <nav id="side">
    <h2>Guia do Professor</h2>
    <p class="sub">Tópicos Especiais em IA · Agentes</p>
    <input id="q" type="search" placeholder="Filtrar seções…" autocomplete="off">
    <div id="toc">
${tocHtml}
    </div>
  </nav>
  <main>
    <article>
${body}
      <div id="meta">Gerado de <code>GUIA_PROFESSOR.md</code> em ${generated} · <code>npm run guia</code></div>
    </article>
  </main>
</div>
<button id="top" title="Voltar ao topo">↑</button>
<script>
(function(){
  var links = Array.prototype.slice.call(document.querySelectorAll('#toc a'));
  var q = document.getElementById('q');

  q.addEventListener('input', function(){
    var term = q.value.toLowerCase().trim();
    links.forEach(function(a){
      a.classList.toggle('hide', term !== '' && a.textContent.toLowerCase().indexOf(term) === -1);
    });
  });

  var byId = {};
  links.forEach(function(a){ byId[a.getAttribute('href').slice(1)] = a; });
  var heads = Object.keys(byId).map(function(id){ return document.getElementById(id); }).filter(Boolean);
  var current = null;

  function sync(){
    var best = null;
    for (var i = 0; i < heads.length; i++) {
      if (heads[i].getBoundingClientRect().top <= 90) best = heads[i]; else break;
    }
    if (!best || best === current) return;
    if (current && byId[current.id]) byId[current.id].classList.remove('active');
    current = best;
    var link = byId[best.id];
    if (link) {
      link.classList.add('active');
      var box = link.getBoundingClientRect(), side = document.getElementById('side').getBoundingClientRect();
      if (box.top < side.top || box.bottom > side.bottom) link.scrollIntoView({ block: 'nearest' });
    }
  }

  var ticking = false;
  window.addEventListener('scroll', function(){
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function(){ sync(); ticking = false; });
  }, { passive: true });
  sync();

  document.getElementById('top').addEventListener('click', function(){
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  document.addEventListener('keydown', function(e){
    if (e.key === '/' && document.activeElement !== q) { e.preventDefault(); q.focus(); }
    if (e.key === 'Escape' && document.activeElement === q) { q.value = ''; q.dispatchEvent(new Event('input')); q.blur(); }
  });
})();
</script>
</body>
</html>
`;

fs.writeFileSync(OUT, html, 'utf8');
console.log('✓ Guia gerado → ' + path.relative(__dirname, OUT));
console.log('  Seções no sumário: ' + toc.length);
