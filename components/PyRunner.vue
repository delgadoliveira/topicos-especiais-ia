<template>
  <div class="py-runner">
    <div class="code-area">
      <textarea
        v-model="source"
        :readonly="readOnly"
        :style="{ height }"
        spellcheck="false"
      />
    </div>
    <div class="controls">
      <button @click="run" :disabled="loading">
        {{ loading ? '⏳ Carregando...' : '▶ Executar' }}
      </button>
      <span v-if="loading" class="loading-badge">⏳ Carregando Python...</span>
      <span v-else-if="ready" class="ready-badge">✓ Python pronto</span>
    </div>
    <div class="output" v-if="output">
      <pre>{{ output }}</pre>
    </div>
    <div class="error" v-if="error">
      <pre>{{ error }}</pre>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const PYODIDE_CDN = 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js'

let pyodideScriptPromise: Promise<void> | null = null
let pyodideReadyPromise: Promise<any> | null = null
let pyodideInstance: any = null
let runnerCounter = 0

declare global {
  interface Window {
    loadPyodide?: (options?: Record<string, unknown>) => Promise<any>
  }
}

function ensurePyodideScript() {
  if (typeof window === 'undefined') {
    return Promise.reject(new Error('Pyodide só pode ser carregado no navegador.'))
  }

  if (window.loadPyodide) {
    return Promise.resolve()
  }

  if (pyodideScriptPromise) {
    return pyodideScriptPromise
  }

  pyodideScriptPromise = new Promise<void>((resolve, reject) => {
    const existingScript = document.querySelector<HTMLScriptElement>('script[data-pyodide-loader="true"]')

    if (existingScript) {
      existingScript.addEventListener('load', () => resolve(), { once: true })
      existingScript.addEventListener('error', () => reject(new Error('Falha ao carregar o script do Pyodide.')), { once: true })
      return
    }

    const script = document.createElement('script')
    script.src = PYODIDE_CDN
    script.async = true
    script.dataset.pyodideLoader = 'true'
    script.onload = () => resolve()
    script.onerror = () => reject(new Error('Falha ao carregar o script do Pyodide.'))
    document.head.appendChild(script)
  })

  return pyodideScriptPromise
}

async function getPyodide() {
  if (pyodideInstance) {
    return pyodideInstance
  }

  if (pyodideReadyPromise) {
    return pyodideReadyPromise
  }

  pyodideReadyPromise = (async () => {
    await ensurePyodideScript()

    if (!window.loadPyodide) {
      throw new Error('API do Pyodide não encontrada após carregar o script.')
    }

    pyodideInstance = await window.loadPyodide({
      indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/',
    })

    return pyodideInstance
  })()

  try {
    return await pyodideReadyPromise
  } catch (err) {
    pyodideReadyPromise = null
    throw err
  }
}

export default defineComponent({
  name: 'PyRunner',
  props: {
    code: {
      type: String,
      default: '',
    },
    readOnly: {
      type: Boolean,
      default: false,
    },
    height: {
      type: String,
      default: '180px',
    },
  },
  setup(props) {
    const source = ref(props.code)
    const output = ref('')
    const error = ref('')
    const loading = ref(true)
    const ready = ref(false)
    const runnerId = `py-runner-${++runnerCounter}`
    let readyTimer: ReturnType<typeof setTimeout> | null = null

    const flashReady = () => {
      ready.value = true
      if (readyTimer) {
        clearTimeout(readyTimer)
      }
      readyTimer = setTimeout(() => {
        ready.value = false
      }, 1800)
    }

    const initialize = async () => {
      loading.value = true
      error.value = ''

      try {
        await getPyodide()
        flashReady()
      } catch (err) {
        error.value = err instanceof Error ? err.message : String(err)
      } finally {
        loading.value = false
      }
    }

    const run = async () => {
      loading.value = true
      output.value = ''
      error.value = ''

      try {
        const pyodide = await getPyodide()
        const resultJson = await pyodide.runPythonAsync(`
import io, json, traceback
from contextlib import redirect_stdout, redirect_stderr

_code = ${JSON.stringify(source.value)}
_runner_id = ${JSON.stringify(runnerId)}
_registry = globals().setdefault("__slidev_runner_namespaces__", {})
_namespace = _registry.setdefault(_runner_id, {"__name__": "__main__"})
_stdout = io.StringIO()
_stderr = io.StringIO()
_error = ""

try:
    with redirect_stdout(_stdout), redirect_stderr(_stderr):
        exec(_code, _namespace)
except Exception:
    _error = traceback.format_exc()

json.dumps({
    "stdout": _stdout.getvalue(),
    "stderr": _stderr.getvalue(),
    "error": _error,
}, ensure_ascii=False)
        `)

        const result = JSON.parse(resultJson)
        output.value = result.stdout || ''
        error.value = [result.stderr, result.error].filter(Boolean).join('\n')
      } catch (err) {
        error.value = err instanceof Error ? err.message : String(err)
      } finally {
        loading.value = false
      }
    }

    watch(
      () => props.code,
      (newCode) => {
        source.value = newCode
      },
    )

    onMounted(() => {
      void initialize()
    })

    onBeforeUnmount(() => {
      if (readyTimer) {
        clearTimeout(readyTimer)
      }
    })

    return {
      error,
      loading,
      output,
      ready,
      readOnly: props.readOnly,
      run,
      source,
      height: props.height,
    }
  },
})
</script>

<style scoped>
.py-runner {
  background: #1e1e2e;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 0.85rem;
  color: #e2e8f0;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.code-area textarea {
  width: 100%;
  min-height: 120px;
  resize: vertical;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  background: #181825;
  color: #f8fafc;
  padding: 0.75rem;
  font-family: 'Fira Code', 'Consolas', 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.45;
  outline: none;
}

.controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.65rem;
  flex-wrap: wrap;
}

.controls button {
  border: none;
  border-radius: 999px;
  padding: 0.5rem 1rem;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, #8b5cf6, #d946ef);
  cursor: pointer;
  transition: transform 0.15s ease, opacity 0.15s ease;
}

.controls button:hover:not(:disabled) {
  transform: translateY(-1px);
}

.controls button:disabled {
  cursor: wait;
  opacity: 0.7;
}

.loading-badge,
.ready-badge {
  font-size: 0.82rem;
  font-weight: 700;
}

.loading-badge {
  color: #f9e2af;
}

.ready-badge {
  color: #a6e3a1;
}

.output,
.error {
  margin-top: 0.7rem;
  border-radius: 10px;
  padding: 0.7rem 0.8rem;
  background: #11111b;
}

.output {
  color: #a6e3a1;
}

.error {
  color: #f38ba8;
}

.output pre,
.error pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: 'Fira Code', 'Consolas', 'Courier New', monospace;
  font-size: 0.85rem;
  line-height: 1.4;
}
</style>
