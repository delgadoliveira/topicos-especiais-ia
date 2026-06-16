---
theme: apple-basic
title: Tópicos Especiais em IA — Agentes de IA
info: |
  ## Tópicos Especiais em IA — Agentes de IA (Zero to Hero)
  Disciplina assíncrona em 4 encontros de 3h.
  Da história dos primeiros modelos até agentes em produção.
class: text-center
highlighter: shiki
lineNumbers: true
drawings:
  persist: false
transition: none
mdc: true
hideInToc: true
navigation: false
fonts:
  sans: 'Inter'
  mono: 'JetBrains Mono'
colorSchema: dark
---

# Tópicos Especiais em IA
## 🤖 Agentes de IA — *Zero to Hero*

<div class="text-xl opacity-80 mt-4">
4 encontros · 3h cada · 100% prático
</div>

<div class="abs-bl mx-14 my-12 flex gap-2 items-center opacity-60 text-sm">
  Prof. Alan · 2026 · Material assíncrono
</div>

<div class="abs-br mx-14 my-12 text-sm opacity-60">
  Aperte <kbd>Space</kbd> para começar →
</div>

<!--
Bem-vindos! Esta disciplina vai te levar de zero ao estado-da-arte em Agentes de IA.
São 4 encontros de 3h, mais uma sessão histórica opcional.
-->

---

# 🗺️ Mapa do curso — visão geral

<div class="text-xs mb-2">Use este mapa como referência ao longo dos 4 encontros.</div>

```mermaid {scale: 0.45}
mindmap
  root((Agentes de IA))
    E1: Fundamentos
      O que é um LLM
        Tokens, contexto, temperatura
        RLHF e alinhamento
      O que é um Agente
        Percepção → Raciocínio → Ação
        Loop ReAct
      Ferramentas (Tools)
        Function calling
        Design de tools
      Primeiro agente em Python
    E2: Raciocínio & Planejamento
      Chain-of-Thought
      Tree-of-Thoughts
      Reasoning models (o1, R1)
      Planning
        Plan-and-Execute
        Replanning
      Frameworks
        LangChain / LangGraph
      Boas práticas
    E3: Memória & Contexto
      Gestão de contexto
        Sliding window
        Summarization
      RAG
        Embeddings & vetores
        Chunking & retrieval
      Memória de longo prazo
      Multi-agentes
        Skills vs Tools
        Orquestração
    E4: Produção
      Avaliação & métricas
      Guardrails & segurança
      Observabilidade
      Deploy & escala
      Estado da arte 2025
      Projeto final
```

---
layout: two-cols
---

# 👋 Bem-vindos

Esta disciplina é **prática**. Em todo encontro vocês vão:

- 🐍 Escrever código Python
- 🛠️ Instalar e rodar agentes
- 🔬 Entender o que está acontecendo *por dentro*
- 💥 Quebrar coisas (e consertar)

Pré-requisitos:

- Python básico
- Curiosidade
- Vontade de errar e iterar

::right::

# 🎯 Ao final, você vai conseguir

<v-clicks>

- Explicar o que é (e o que **não** é) um agente
- Construir um agente do zero, sem framework
- Usar LangChain / LangGraph com propósito
- Implementar RAG, memória e ferramentas custom
- Avaliar e debugar agentes em produção
- Avaliar criticamente Cursor, Claude Code, Devin & cia

</v-clicks>

---
layout: section
---

# 📚 Sumário do curso

---

# Sumário

<div class="grid grid-cols-2 gap-6 mt-8">

<div class="p-5 rounded-xl border border-cyan-500/30 bg-cyan-500/5">
  <div class="text-cyan-400 font-mono text-xs">SESSÃO EXTRA · ~45min</div>
  <div class="text-xl font-bold mt-1">📜 História</div>
  <div class="text-sm opacity-70 mt-2">Dos primeiros modelos (anos 50) ao GPT-1, GPT-3, ChatGPT e a era dos agentes.</div>
</div>

<div class="p-5 rounded-xl border border-purple-500/30 bg-purple-500/5">
  <div class="text-purple-400 font-mono text-xs">ENCONTRO 1 · 3h</div>
  <div class="text-xl font-bold mt-1">🧱 Fundamentos</div>
  <div class="text-sm opacity-70 mt-2">O que é um agente, anatomia, padrão ReAct, primeiro agente em Python sem framework.</div>
</div>

<div class="p-5 rounded-xl border border-purple-500/30 bg-purple-500/5">
  <div class="text-purple-400 font-mono text-xs">ENCONTRO 2 · 3h</div>
  <div class="text-xl font-bold mt-1">🧠 Pensar e Agir</div>
  <div class="text-sm opacity-70 mt-2">Chain-of-Thought, Tree-of-Thoughts, Planning, Function Calling, LangChain/LangGraph.</div>
</div>

<div class="p-5 rounded-xl border border-purple-500/30 bg-purple-500/5">
  <div class="text-purple-400 font-mono text-xs">ENCONTRO 3 · 3h</div>
  <div class="text-xl font-bold mt-1">💾 Memória e Skills</div>
  <div class="text-sm opacity-70 mt-2">Janela de contexto, RAG, vector DBs, memória de longo prazo, skills, MCP, multi-agentes.</div>
</div>

<div class="p-5 rounded-xl border border-purple-500/30 bg-purple-500/5 col-span-2">
  <div class="text-purple-400 font-mono text-xs">ENCONTRO 4 · 3h</div>
  <div class="text-xl font-bold mt-1">🚀 Mundo Real & State-of-the-Art</div>
  <div class="text-sm opacity-70 mt-2">Falhas comuns, avaliação (SWE-bench, GAIA), observabilidade, Cursor / Claude Code / Devin / Manus, projeto final.</div>
</div>

</div>

---
layout: center
class: text-center
---

# 🧭 Como navegar

| Tecla | Ação |
|---|---|
| <kbd>→</kbd> / <kbd>Space</kbd> | Próximo passo |
| <kbd>←</kbd> | Anterior |
| <kbd>o</kbd> | Visão geral (overview) |
| <kbd>d</kbd> | Toggle dark mode |
| <kbd>f</kbd> | Fullscreen |
| <kbd>g</kbd> | Ir para slide N |

---

# Antes de começarmos…

<div class="text-2xl mt-12 text-center opacity-90">
Quase tudo que você vai ouvir nas próximas 12h<br>
<span class="text-cyan-400 font-bold">existe há menos de 3 anos.</span>
</div>

<div class="text-lg mt-8 text-center opacity-70">
Para entender <b>onde estamos</b>, precisamos entender <b>como chegamos aqui</b>.
</div>

<div class="text-center mt-12">
  <span class="text-3xl">📜</span>
  <div class="text-xl mt-2">Vamos para a sessão de história →</div>
</div>

---
src: ./pages/historia.md
---

---
src: ./pages/encontro-1.md
---

---
src: ./pages/encontro-2.md
---

---
src: ./pages/encontro-3.md
---

---
src: ./pages/encontro-4.md
---

---
layout: center
class: text-center
---

# 🎓 Fim do curso

<div class="text-xl opacity-80 mt-6">
Obrigado por chegar até aqui.<br>
Agora você está pronto para construir o próximo grande agente.
</div>

<div class="mt-12 text-sm opacity-60">
Material aberto · Use, adapte, compartilhe
</div>
