# Tópicos Especiais em IA — Agentes de IA (Zero to Hero)

Apresentação em **Slidev** para a disciplina *Tópicos Especiais em IA — Agentes de IA*, ministrada em **4 encontros de 3h** (assíncrono).

## Como rodar

```powershell
# 1. Instalar dependências (uma vez)
npm install

# 2. Rodar em modo dev (abre no navegador, hot-reload)
npm run dev

# 3. Build estático (gera ./dist com HTML/JS/CSS)
npm run build

# 4. Exportar para PDF (precisa Playwright instalado)
npm run export-pdf
```

Pré-requisito: **Node.js ≥ 18**.

## Estrutura

```
slides.md                 # arquivo de entrada (capa + imports)
pages/
  historia.md             # Sessão extra: história — dos primeiros modelos aos agentes
  encontro-1.md           # Introdução e Fundamentos
  encontro-2.md           # Reasoning, Planning & Tool Execution
  encontro-3.md           # Skills, Memória & Contexto
  encontro-4.md           # Problemas comuns & State-of-the-Art
```

## Navegação durante a aula

- `→` / `Space` — próximo slide / próximo passo de `<v-click>`
- `←` — slide anterior
- `o` — visão geral (overview de todos os slides)
- `d` — modo dark/light
- `f` — fullscreen
- `g` — ir para slide específico
- `s` — modo apresentador (notas do palestrante)

## Customização

Tema base: `seriph` (acadêmico, limpo). Para trocar, edite o `theme:` no início de `slides.md`.

Cores e estilos custom estão em `slides.md` (bloco `<style>`).

## Conteúdo

| Módulo | Carga | Tópicos |
|---|---|---|
| História (extra) | ~45 min | Pré-Transformer → GPT-1 → GPT-3 → ChatGPT → Agentes modernos |
| Encontro 1 | 3h | Fundamentos, anatomia, ReAct, primeiro agente em Python |
| Encontro 2 | 3h | Chain-of-Thought, Tree-of-Thoughts, Planning, Function Calling, frameworks |
| Encontro 3 | 3h | Skills, MCP, context window, RAG, memória, multi-agentes |
| Encontro 4 | 3h | Falhas comuns, avaliação, observabilidade, Cursor/Claude Code/Devin, projeto final |

Linguagem: **Português**. Código: **Python**.
