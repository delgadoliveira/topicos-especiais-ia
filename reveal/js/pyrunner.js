/* ═══════════════════════════════════════════════════════
   PYRUNNER.JS — Pyodide-based Python executor
   Vanilla JS implementation for Reveal.js slides
   ═══════════════════════════════════════════════════════ */

const PyRunner = (() => {
  const CDN = 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/';
  let pyodide = null;
  let loading = false;
  let loadPromise = null;

  async function ensureLoaded() {
    if (pyodide) return pyodide;
    if (loadPromise) return loadPromise;
    
    loadPromise = (async () => {
      // Load Pyodide script
      if (!window.loadPyodide) {
        await new Promise((resolve, reject) => {
          const script = document.createElement('script');
          script.src = CDN + 'pyodide.js';
          script.onload = resolve;
          script.onerror = () => reject(new Error('Falha ao carregar Pyodide'));
          document.head.appendChild(script);
        });
      }
      pyodide = await window.loadPyodide({ indexURL: CDN });
      return pyodide;
    })();

    return loadPromise;
  }

  async function run(code) {
    const py = await ensureLoaded();
    const result = await py.runPythonAsync(`
import io, json, traceback
from contextlib import redirect_stdout, redirect_stderr

_code = ${JSON.stringify(code)}
_stdout = io.StringIO()
_stderr = io.StringIO()
_error = ""

try:
    with redirect_stdout(_stdout), redirect_stderr(_stderr):
        exec(_code, {"__name__": "__main__"})
except Exception:
    _error = traceback.format_exc()

json.dumps({
    "stdout": _stdout.getvalue(),
    "stderr": _stderr.getvalue(),
    "error": _error,
}, ensure_ascii=False)
    `);
    return JSON.parse(result);
  }

  /** Initialize all PyRunner containers on the page */
  function initAll() {
    document.querySelectorAll('.pyrunner-container').forEach(container => {
      if (container.dataset.initialized) return;
      container.dataset.initialized = 'true';

      const textarea = container.querySelector('textarea');
      const btn = container.querySelector('.run-btn');
      const outputEl = container.querySelector('.pyrunner-output');

      // Load from src if specified
      const src = container.dataset.src;
      if (src) {
        fetch(src)
          .then(r => r.text())
          .then(code => { textarea.value = code; })
          .catch(() => { textarea.value = '# Erro ao carregar exercício'; });
      }

      btn.addEventListener('click', async () => {
        btn.disabled = true;
        btn.textContent = '⏳ Executando...';
        outputEl.textContent = '';
        outputEl.className = 'pyrunner-output';

        try {
          const result = await run(textarea.value);
          if (result.error || result.stderr) {
            outputEl.textContent = result.error || result.stderr;
            outputEl.classList.add('pyrunner-error');
          } else {
            outputEl.textContent = result.stdout || '(sem output)';
          }
        } catch (err) {
          outputEl.textContent = err.message;
          outputEl.classList.add('pyrunner-error');
        } finally {
          btn.disabled = false;
          btn.textContent = '▶ Executar';
        }
      });
    });
  }

  return { ensureLoaded, run, initAll };
})();

window.PyRunner = PyRunner;
