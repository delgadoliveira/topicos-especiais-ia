# 📘 Guia do Professor — Tópicos Especiais em IA: Agentes (Zero to Hero)

> Material de preparação para o instrutor. **Não é distribuído aos alunos.**
> Use junto com os slides (`slides.md`) e a versão online em
> https://delgadoliveira.github.io/topicos-especiais-ia/

---

## Como usar este guia

Para **cada encontro** você encontra:

1. **Objetivos de aprendizagem** — o que o aluno deve sair sabendo fazer
2. **Cronograma** sugerido (encontros são de 3h, considerando 15 min de intervalo)
3. **Roteiro slide-a-slide** com talking points, analogias, e o que **não** dizer
4. **Demos ao vivo** — checklist de preparação e o que mostrar
5. **Perguntas frequentes** + respostas curtas
6. **Misconceptions comuns** dos alunos e como corrigir
7. **Transições** entre seções (frases-ponte)
8. **Material de leitura recomendado** ao instrutor (além das refs públicas)

**Convenção:** 💡 = insight pedagógico, ⚠️ = armadilha comum, 🎬 = ação ao vivo, 📊 = mostrar dado/número.

---

## Filosofia da disciplina

- **Pragmática antes de teórica.** O aluno precisa rodar um agente nas primeiras 2h. Tudo o mais é contextualização.
- **Não vender hype.** Quando algo não funciona em produção, diga. Use os slides de "onde quebra".
- **Mostrar números.** Custos reais, latências reais, taxas de erro reais. Os alunos confiam mais em quem mostra a conta da API.
- **Referenciar fontes.** Cada afirmação não-óbvia tem uma fonte pública (papers, blogs oficiais). Os slides já citam — você pode aprofundar.
- **Reconhecer o que muda rápido.** Diga explicitamente: "esses números são de 2025; em 6 meses o cenário pode mudar". Evita parecer datado.

---

# 🧱 Encontro 1 — Introdução e Fundamentos

## 🎯 Objetivos de aprendizagem

Ao final, o aluno deve ser capaz de:

1. Definir **o que é** (e o que **não é**) um agente de IA, com critérios objetivos.
2. Identificar os **5 componentes** de um agente em qualquer produto comercial.
3. Explicar o padrão **ReAct** e por que ele é o ponto de partida.
4. **Rodar um agente em Python puro** (sem framework) na própria máquina.
5. **Diagnosticar** falhas básicas (loop infinito, tool errada, contexto saturado).

## ⏱️ Cronograma sugerido (180 min)

| Bloco | Tempo | Conteúdo |
|---|---|---|
| 1 | 10' | Abertura, roadmap, regras |
| 2 | 30' | "O que é um agente?" + espectro + regra de ouro |
| 3 | 35' | Anatomia detalhada (5 componentes + deep dives) |
| 4 | 10' | Panorama de mercado + business case |
| — | **15'** | **Intervalo** |
| 5 | 20' | Como o LLM pensa (tokens, contexto, temperatura) |
| 6 | 25' | ReAct + exemplo |
| 7 | 10' | Setup do ambiente |
| 8 | 30' | Hands-on: primeiro agente do zero |
| 9 | 15' | Exercícios + fechamento |

> 💡 Se atrasar: os deep dives da anatomia (slides 1.3) são onde cortar primeiro — eles são autossuficientes para leitura assíncrona depois.

## 📖 Roteiro slide-a-slide

### Bloco 1 — Abertura (10 min)

**Slides:** capa, agenda, roadmap, "como aproveitar".

- Comece dizendo: **"esta disciplina é hands-on; se você só assistir, vai esquecer em uma semana"**.
- Mostre o GitHub do material (https://github.com/delgadoliveira/topicos-especiais-ia) e diga que tudo é público.
- 💡 Combine **uma regra**: "perguntas a qualquer momento, mas durante as demos eu paro e respondo no final do bloco". Mantém o ritmo.

### Bloco 2 — "O que é um agente?" (30 min)

**Slides:** 1.2 (definição), espectro do script ao agente, regra de ouro.

- **Defina por exclusão primeiro**: um chatbot que só responde texto **não** é um agente. Um script que chama uma API **não** é um agente. O que define agente é: **autonomia para decidir quais ferramentas usar e quando parar**.
- 🧩 **Analogia central a usar aqui**: comparar com um **estagiário** vs uma **macro do Excel**.
  - Macro: você diz cada passo. Determinística. Funciona ou quebra.
  - Estagiário: você dá o objetivo, ele decide os passos. Pode errar, mas se adapta.
- 📊 Mostre o espectro: script → automação → workflow → agente. Pergunte: "onde está o ChatGPT? E o Cursor? E um Zapier?". Discussão de 3 min.
- **Regra de ouro** (slide específico): "se a tarefa pode ser resolvida com um workflow determinístico, **use o workflow**". Cite Anthropic "Building effective agents" (dez/2024).
- ⚠️ Misconception comum: "agente = chatbot bonito". Corrija: chatbot é **interface**, agente é **arquitetura**.

### Bloco 3 — Anatomia (35 min)

**Slides:** 1.3 + ciclo de vida + 5 deep dives + mensagens + estado + paradigmas + autonomia + onde quebram.

Este é o bloco mais denso. Sugestão de pacing:

- **Diagrama dos 5 componentes** (5 min) — apresente como "o esqueleto que vamos esquadrinhar".
- **Ciclo de vida de 1 turno** (5 min) — 🎬 desenhe o loop no quadro enquanto explica. Fundamental para o ReAct depois.
- **Deep dive de cada componente** (3 min cada × 5 = 15 min). Não leia o slide. Para cada um:
  - Estado-a-frase-chave de cada slide (vide tabela abaixo)
  - Aponte a analogia que está no slide
  - Cite **um** exemplo de mercado
- **Anatomia da mensagem** (4 min) — 🎬 abra o terminal e mostre uma resposta JSON real de tool_call. Mais didático que qualquer slide.
- **Paradigmas + Autonomia** (3 min) — fala rápida. "Hoje é ReAct, próxima aula é plan-and-execute e reflexão".
- **Onde quebram** (3 min) — diga "marquem essa tabela, vamos voltar nela no Encontro 4".

**Frase-chave por componente:**

| Componente | Frase para fixar |
|---|---|
| 🧠 LLM | "O estagiário brilhante e amnésico — lê tudo, esquece tudo." |
| 🛠️ Tools | "São as mãos. Sem elas, o LLM só descreve o que faria." |
| 💾 Memória | "Toda 'memória' é reconstruída a cada chamada — não existe estado mágico." |
| 🔄 Loop | "É **seu código** que decide quando parar. Não confie no LLM para isso." |
| 🎯 Objetivo | "O system prompt é a constituição. Versione como código." |

### Bloco 4 — Mercado (10 min)

**Slides:** panorama + business case.

- Use estes slides para **legitimar** a disciplina. "Não estamos estudando teoria — esses produtos faturam US$ bilhões hoje."
- 📊 Os dois números mais impactantes para destacar:
  - **130× queda de custo** GPT-3.5 → GPT-4o-mini em 2 anos
  - **SWE-bench 2% → 70%** em ~24 meses
- Pergunta para fazer à turma: "alguém aqui já usou Cursor, Copilot, ou Claude?" — sirva de calibração da turma.
- ⚠️ Não prometa empregos. Não diga "agente vai substituir desenvolvedor". Diga "está mudando como desenvolvedor trabalha".

### 🍫 Intervalo (15 min)

### Bloco 5 — Como o LLM pensa (20 min)

**Slides:** 1.4 + mental model.

- **Tokens** (5 min) — abra https://platform.openai.com/tokenizer e cole uma frase em português e em inglês. Mostre que PT consome ~1.5× mais tokens. 📊 Implicação direta no custo.
- **Context window** (5 min) — desenhe um retângulo no quadro com "200k tokens" e vá enchendo: system prompt (2k), histórico (10k), resultado de tool (20k)... mostre como **infla rápido**.
- **Temperature** (5 min) — diga "0 não é determinístico, é só 'menos aleatório'". Cite o paper "Non-determinism of GPT-4" se quiser aprofundar (mas opcional).
- **Função pura** (5 min) — 🧩 **a frase mais importante da aula**: "o LLM não tem memória entre chamadas. Toda a 'memória' do agente está no prompt que **você** monta a cada turno."

### Bloco 6 — ReAct (25 min)

**Slides:** 1.5 + exemplo.

- ReAct = **Reason + Act + Observe**, em loop.
- Cite Yao et al. 2022 (paper original) mas **não leia o paper**. Mostre o exemplo do slide.
- 🎬 No quadro, escreva o fluxo:
  ```
  Thought: preciso descobrir X
  Action: search_web("X")
  Observation: resultado
  Thought: agora preciso Y...
  ```
- ⚠️ Misconception: "o LLM faz reasoning real". Corrija: ele **gera texto que parece reasoning**. Função do mesmo modelo. Mas funciona surpreendentemente bem.
- Por que ReAct é importante: é o **template** de praticamente todo agente em produção hoje (mesmo que escondido atrás de frameworks).

### Bloco 7 — Setup (10 min)

**Slides:** 1.6 + alternativas grátis.

- 🎬 **Faça você o setup ao vivo** (venv, pip install, .env). Demora 3 min e mostra que é simples.
- Tenha **3 chaves de API de backup**: OpenAI, Anthropic, Groq (free tier). Se um aluno tem problema, ofereça Groq.
- ⚠️ **Bloqueio comum**: Windows + venv + PowerShell execution policy. Tenha o comando `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` pronto.

### Bloco 8 — Hands-on (30 min)

**Slides:** 1.7 + tool design + 4 partes do código.

- 🎬 Esta é a parte mais importante do encontro. **Construa o agente do zero ao vivo**, slide a slide.
- **Pause em pontos-chave** e peça à turma para prever:
  - "O que vocês acham que vai acontecer se a tool retornar erro?"
  - "Por que precisamos de `max_steps`?"
- Quando rodar pela primeira vez, **mostre o prompt completo** que está sendo enviado (faça `print(messages)` antes do `llm.chat`). Isso desmistifica o "agente".
- Se der erro, **não esconda**. Debugue ao vivo. É o aprendizado mais valioso do dia.

### Bloco 9 — Exercícios + fechamento (15 min)

**Slides:** 1.8 + slides finais.

- Não resolva os exercícios. Diga "vocês fazem em casa, traremos dúvidas na próxima aula".
- Termine com uma frase-gancho para o Encontro 2: **"Hoje vimos o esqueleto. Na próxima aula, colocamos cérebro pensante — reasoning e planning de verdade."**

## 🎬 Demos preparadas (checklist)

- [ ] Notebook com chave de API funcionando
- [ ] Tokenizer aberto no browser (https://platform.openai.com/tokenizer)
- [ ] Terminal com venv ativo, pronto para `pip install`
- [ ] Script `primeiro_agente.py` pronto, mas **vazio** (você digita ao vivo)
- [ ] Plano B: notebook Colab com o código completo, caso a internet local falhe
- [ ] Chaves de backup (Groq free tier = `gsk_...`)

## ❓ FAQ esperado

**P: "Por que não usar LangChain logo de cara?"**
R: Porque sem entender o loop em Python puro, você usa o framework como mágica. Vamos ver LangGraph no Encontro 2, quando você já souber o que ele está escondendo.

**P: "Qual modelo eu uso?"**
R: Para aprender, GPT-4o-mini ou Claude Haiku — baratos e bons. Em produção, depende do caso. Vamos discutir tradeoffs no Encontro 2.

**P: "Agentes são determinísticos?"**
R: Não. Mesmo com temperature 0, há variação. Por isso precisamos de avaliação (Encontro 4) e de loops com guard-rails.

**P: "Quanto custa rodar um agente?"**
R: Depende do modelo e do número de turnos. Exemplo: 5 turnos com GPT-4o-mini ≈ US$ 0,01. Com o1 ≈ US$ 0,50–1. Mostre a página de pricing no site da OpenAI.

**P: "Posso rodar local sem API?"**
R: Sim, com Ollama + Llama 3.1 ou Qwen 2.5. Mas o tool calling fica menos confiável em modelos &lt; 7B. Discussão mais profunda no Encontro 2.

## ⚠️ Misconceptions a corrigir explicitamente

1. **"Agente = chatbot."** → Não. Chatbot é interface; agente é arquitetura com tools + loop.
2. **"O LLM lembra das conversas anteriores."** → Não. Toda 'memória' é reconstruída no prompt.
3. **"Temperature 0 = determinístico."** → Não, só "menos aleatório".
4. **"Frameworks resolvem tudo."** → Não. Eles escondem o loop, mas você ainda precisa entender o que está dentro.
5. **"Agente que erra é bug."** → Às vezes é variabilidade inerente. Por isso evals existem.

## 📚 Leitura recomendada ao instrutor (além das refs públicas dos slides)

- Anthropic, "Building effective agents" (dez/2024) — **leitura obrigatória** antes da primeira aula.
- Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (2022) — o paper-base.
- Lilian Weng, "LLM Powered Autonomous Agents" (jun/2023) — overview clássico.
- OpenAI, "A practical guide to building agents" (2025) — PDF público.

---

# 🧠 Encontro 2 — Reasoning, Planning e Frameworks

## 🎯 Objetivos de aprendizagem

1. Diferenciar **reasoning models** (o1, R1, Claude Thinking) de modelos generalistas.
2. Implementar **planning** (Plan-and-Execute) e **reflexão** (Reflexion).
3. Conhecer os **5 padrões agentic** da Anthropic e quando usar cada um.
4. Comparar **frameworks** (LangGraph, OpenAI Agents SDK, LlamaIndex) com critérios objetivos.
5. Refatorar o agente do Encontro 1 usando um framework escolhido.

## ⏱️ Cronograma sugerido

| Bloco | Tempo | Conteúdo |
|---|---|---|
| 1 | 10' | Recap Encontro 1 + dúvidas dos exercícios |
| 2 | 30' | Reasoning models (o1, R1, chain-of-thought) |
| 3 | 25' | Structured outputs + por que importam para agentes |
| 4 | 25' | Os 5 padrões agentic da Anthropic |
| — | 15' | Intervalo |
| 5 | 30' | Planning: Plan-and-Execute, Reflexion |
| 6 | 25' | Comparativo de frameworks |
| 7 | 25' | Hands-on: refatorar agente usando LangGraph |
| 8 | 10' | Exercícios + fechamento |

## 📖 Roteiro slide-a-slide

### Bloco 1 — Recap (10 min)

- Pergunte: "alguém conseguiu rodar o agente em casa? Que dificuldades?". Endereçar 2-3 dúvidas comuns.
- 🧩 Frase-ponte: **"Vimos *como* um agente funciona. Hoje veremos *como fazê-lo pensar melhor*."**

### Bloco 2 — Reasoning models (30 min)

- Comece com a história: **set/2024 OpenAI lança o1**. Foi um salto.
- 📊 Mostre o gráfico do paper o1: AIME 13% (GPT-4o) → 83% (o1). Algo dessa magnitude raramente acontece.
- **Mecanismo central**: o modelo gera **muito mais tokens "de raciocínio" antes de responder**. Tradeoff: mais lento, mais caro, mas resolve problemas que generalistas não resolvem.
- 🧩 **Analogia**: generalista = aluno que responde sem rascunho; reasoning model = aluno que faz rascunho longo antes de escrever a resposta final.
- **DeepSeek R1** (jan/2025) — open weights, abalou o mercado. Demonstrou que reasoning pode ser treinado com RL puro sem SFT massivo.
- ⚠️ Não use reasoning models para tudo. Eles são piores em tarefas simples conversacionais (over-thinking) e custam 10–100× mais.
- **Quando usar**: matemática, código complexo, análise multi-step, planejamento. **Quando não**: chat, sumário, classificação simples.

### Bloco 3 — Structured outputs (25 min)

- Por que importa: agentes precisam de **outputs parseáveis** (JSON, function calls). Sem isso, regex e crashes.
- **OpenAI Structured Outputs** (ago/2024) e **JSON mode** — garantia 100% via constrained decoding.
- **Anthropic tool use** + **Pydantic** = padrão de facto.
- 🎬 Demo: peça ao agente para retornar JSON sem structured outputs, mostre que às vezes ele inclui markdown. Depois ative structured e mostre que **nunca** mais quebra.
- 🧩 **Analogia**: structured output é como **formulário com campos** vs **redação livre**. Você não precisa interpretar a letra, só ler os campos.

### Bloco 4 — Padrões agentic Anthropic (25 min)

Os 5 padrões do paper "Building effective agents" (dez/2024):

1. **Prompt chaining** — output de um vira input do próximo. Determinístico.
2. **Routing** — classificador decide qual subagente chamar.
3. **Parallelization** — várias chamadas em paralelo (mesma tarefa para voting, ou subtarefas).
4. **Orchestrator-workers** — orquestrador dinamicamente delega.
5. **Evaluator-optimizer** — gera → avalia → refina (Reflexion).

Para cada um:
- Diga **quando usar** (uma frase)
- 📊 Mostre **um exemplo de produto real** que usa
- Diga **uma armadilha**

🧩 **Analogia geral**: pense numa **agência de publicidade**.
- Prompt chaining = linha de montagem (briefing → criação → revisão → entrega)
- Routing = recepcionista que direciona o cliente
- Parallelization = três criativos pensando em paralelo
- Orchestrator = diretor de criação delegando dinamicamente
- Evaluator-optimizer = revisão do diretor antes de mandar ao cliente

### 🍫 Intervalo

### Bloco 5 — Planning & Reflexion (30 min)

- **Plan-and-Execute** (BabyAGI, LangChain) — faz plano completo upfront, depois executa.
  - ✅ Auditável, previsível
  - ❌ Plano fica obsoleto se o mundo muda
- **Reflexion** (Shinn et al. 2023) — executa → critica → tenta de novo.
  - 📊 Ganhos típicos: 10-30% de qualidade
  - ❌ Custo: 2-5× mais chamadas
- 🎬 Demo: implemente um Reflexion simples em 30 linhas, mostre a melhoria iterativa.

### Bloco 6 — Frameworks comparados (25 min)

| Framework | Force | Quando usar |
|---|---|---|
| **LangGraph** | grafo de estados explícito, debug fácil | sistemas complexos, multi-agent |
| **OpenAI Agents SDK** | handoffs simples, integração nativa | quem já está no ecossistema OpenAI |
| **LlamaIndex AgentWorkflow** | maduro em RAG | agentes que dependem muito de retrieval |
| **Pydantic AI** | type-safe, leve | times Python-puristas |
| **Smolagents** | mínimo, code-as-action | educacional, hackathons |

- 🧩 **Analogia**: como escolher framework web — Django (LangGraph) vs Flask (Smolagents) vs FastAPI (Pydantic AI).
- ⚠️ Não recomende um vencedor. Diga "depende do time e do problema". Mostre prós/contras.

### Bloco 7 — Hands-on refator (25 min)

- 🎬 Refatore o agente do Encontro 1 em LangGraph. Mostre lado a lado o `for step in range`... vs o grafo.
- Pause e pergunte: "o que ficou melhor? o que ficou pior?". Discussão.

### Bloco 8 — Fechamento (10 min)

- Gancho: **"Pensar melhor não basta. Próxima aula: agente que sabe do que está falando — grounding, RAG e memória."**

## 🎬 Demos preparadas

- [ ] Exemplo de prompt sem/com structured outputs (mostrar diferença)
- [ ] Reflexion mínimo em ~30 linhas
- [ ] Refatoração LangGraph do agente do Encontro 1

## ❓ FAQ esperado

**P: "Vale a pena usar o1 sempre?"** R: Não. Custo 50× maior, latência 10× maior. Só para tarefas que falham em modelos generalistas.

**P: "Qual framework é o melhor?"** R: Pergunta errada. Pergunta certa: "qual é o melhor para meu time e meu problema?".

**P: "Plan-and-Execute vs ReAct?"** R: ReAct para tarefas exploratórias; Plan-and-Execute para tarefas com etapas conhecidas e auditoria necessária.

## ⚠️ Misconceptions

1. **"Reasoning model é melhor para tudo."** → Não. Pior em chat conversacional.
2. **"Framework substitui entendimento do loop."** → Não. Vai te morder em produção.
3. **"Reflexion sempre melhora."** → Não. Em tarefas onde o modelo não sabe avaliar a si mesmo, piora.

---

# 🔎 Encontro 3 — Grounding, Synthesis, RAG e Memória

## 🎯 Objetivos de aprendizagem

1. Entender **grounding** e **synthesis** como duas etapas distintas.
2. Implementar **RAG** básico e conhecer técnicas avançadas (HyDE, multi-query, re-ranking).
3. Desenhar **context engineering** — o que entra e o que sai da janela.
4. Usar **prompt caching** para reduzir custo 10-90%.
5. Conhecer arquiteturas de **memória de longo prazo** (Mem0, Letta, Zep).

## ⏱️ Cronograma

| Bloco | Tempo | Conteúdo |
|---|---|---|
| 1 | 10' | Recap + dúvidas |
| 2 | 30' | Grounding: o que é e por que importa |
| 3 | 30' | Synthesis: o passo esquecido |
| 4 | 25' | RAG básico (revisão rápida) |
| — | 15' | Intervalo |
| 5 | 25' | Advanced RAG (HyDE, multi-query, re-ranking) |
| 6 | 20' | Context engineering & prompt caching |
| 7 | 25' | Memória de longo prazo |
| 8 | 10' | Mercado + exercícios |

## 📖 Roteiro slide-a-slide

### Bloco 2 — Grounding (30 min)

- **Definição** (Rashkin et al., Bohnet et al.): grounding = a resposta é **atribuível** a uma fonte verificável.
- 🧩 **Analogia**: é a diferença entre **"li no Wikipedia"** (grounded) e **"alguém me disse"** (não grounded).
- Por que importa: **alucinação** é o problema #1 de LLMs. Grounding é a defesa principal.
- 📊 Mostre exemplo: pergunta sobre evento de 2024 sem RAG → modelo inventa. Com RAG → cita fonte.

### Bloco 3 — Synthesis (30 min)

- **Synthesis = combinar múltiplas fontes em uma resposta coerente**.
- O passo esquecido: muita gente foca em retrieval (achar) e esquece de synthesis (compor bem).
- 🧩 **Analogia**: pesquisa para TCC. Achar 50 artigos = retrieval. Escrever a revisão de literatura coerente = synthesis.
- Técnicas: **citation insertion**, **conflict resolution** (quando fontes discordam), **abstractive summary**.

### Bloco 4 — RAG básico (25 min)

- Loop: query → embed → retrieve → rerank (opcional) → augment prompt → generate.
- 🎬 Demo: RAG sobre 5 PDFs em ~50 linhas com Chroma.

### 🍫 Intervalo

### Bloco 5 — Advanced RAG (25 min)

- **HyDE** (Hypothetical Document Embeddings): em vez de embeddar a query, peça ao LLM para gerar uma resposta hipotética e embedde **isso**. Melhora retrieval em queries curtas.
- **Multi-query**: gere N variações da query, retrieve para cada, una resultados.
- **Re-ranking** (Cohere Rerank, BGE-reranker): retrieva 50, reranqueia top-5 com modelo cross-encoder.
- 🧩 **Analogia**: re-ranking = passar o "filtro fino" depois do "filtro grosso" do vector search.

### Bloco 6 — Context engineering & caching (20 min)

- **Context engineering**: arte de decidir o que cabe na janela. Sliding window, sumarização recursiva, hierarchical summary.
- **Prompt caching** (Anthropic ago/2024, OpenAI out/2024): tokens repetidos custam 10× menos. 📊 Em agentes com system prompt grande, economia de **70-90%**.

### Bloco 7 — Memória de longo prazo (25 min)

- **Mem0**, **Letta** (ex-MemGPT), **Zep** — frameworks dedicados.
- Tipos: **episódica** (o que aconteceu), **semântica** (fatos), **procedural** (como fazer).
- 🧩 **Analogia**: como ChatGPT Memory lembra que você é vegetariano sem você dizer toda vez.

## 🎬 Demos

- [ ] RAG básico com Chroma + 5 PDFs públicos
- [ ] Comparação latência/custo com e sem prompt caching
- [ ] Exemplo de Mem0 lembrando preferências do usuário entre sessões

## ❓ FAQ

**P: "RAG vs fine-tuning?"** R: RAG para conhecimento que muda. Fine-tuning para comportamento/estilo.

**P: "Quanto contexto é demais?"** R: Depende do modelo, mas: degradação de qualidade começa ~50% da janela. Use `needle-in-a-haystack` benchmarks como referência.

---

# 🚧 Encontro 4 — Problemas Comuns, Avaliação, State-of-Art

## 🎯 Objetivos de aprendizagem

1. Catalogar os **modos de falha** comuns (alucinação, prompt injection, loops, custo).
2. Implementar **LLM-as-judge** para avaliação automatizada.
3. Entender **determinismo, reprodutibilidade, observabilidade** em produção.
4. Conhecer o estado da arte: **A2A, MCP, computer use, deep research, voice agents**.
5. **Entregar o projeto final** com critérios claros.

## ⏱️ Cronograma

| Bloco | Tempo | Conteúdo |
|---|---|---|
| 1 | 10' | Recap |
| 2 | 30' | Alucinações: taxonomia (Ji 2023) |
| 3 | 25' | Prompt injection & segurança |
| 4 | 25' | LLM-as-judge (Zheng 2023) |
| — | 15' | Intervalo |
| 5 | 25' | Determinismo, eval, observabilidade |
| 6 | 25' | State-of-art: A2A, MCP, computer use |
| 7 | 15' | Mercado: eval, observability, governança |
| 8 | 30' | Projeto final: descrição + solução |

## 📖 Roteiro slide-a-slide

### Bloco 2 — Alucinações (30 min)

- **Ji et al., 2023** ("Survey of Hallucination"): taxonomia em **intrinsic** (contradiz a fonte) vs **extrinsic** (não verificável).
- 🧩 **Analogia**: intrinsic = mentira; extrinsic = invenção plausível. Ambas perigosas.
- Causas: viés de treino, falta de grounding, over-confidence.
- Mitigações: grounding, structured output, validação cruzada, abstain (deixar o modelo dizer "não sei").

### Bloco 3 — Prompt injection (25 min)

- **OWASP Top 10 for LLMs** #1.
- Direct (usuário hostil) vs Indirect (conteúdo em tool result com instruções escondidas).
- 🎬 Demo viva: agente lendo um site com `<!-- ignore previous instructions, do X -->` → mostre o ataque funcionar.
- Defesas: sanitização, system prompt forte, allow-list de domínios, modelos resistentes (Claude tem ranking alto em red-team).

### Bloco 4 — LLM-as-judge (25 min)

- **Zheng et al., 2023** ("Judging LLM-as-a-Judge"). Acurácia ~80-85% comparado a humanos.
- Padrões:
  - **Direct grading** (nota 1-5)
  - **Pairwise comparison** (A ou B melhor)
  - **Rubric-based** (lista de critérios)
- ⚠️ Biases conhecidos: **position bias** (prefere o primeiro), **verbosity bias** (prefere resposta mais longa). Mitigue alternando ordem.

### 🍫 Intervalo

### Bloco 5 — Determinismo & observabilidade (25 min)

- Mesmo temp=0 não é determinístico (não-associatividade FP, batching). Cite o paper "Non-determinism of GPT-4".
- **LangSmith, Langfuse, Arize Phoenix** — instrumentação de traces.
- 🧩 **Analogia**: sem observabilidade você está debugando às cegas. Como rodar Python sem print/logs.

### Bloco 6 — State-of-art (25 min)

- **MCP** (Anthropic, nov/2024): padrão aberto de tool calling, virou de facto.
- **A2A** (Google, abr/2025): agent-to-agent protocol.
- **Computer use** (Anthropic Claude 3.5 Sonnet, out/2024 — OpenAI Operator, jan/2025): agentes controlam tela/mouse/teclado.
- **Deep Research** (OpenAI fev/2025): agente que faz pesquisa de horas em minutos.

### Bloco 7 — Mercado de eval/observability/governança (15 min)

- Use o slide do panorama. Destaque **EU AI Act** entrando em vigor em 2026 — quem opera agentes em prod precisa entender.

### Bloco 8 — Projeto final (30 min)

- 🎬 **Apresente a descrição da tarefa** com clareza. Tire dúvidas.
- **Apresente a solução de referência** em 3 slides:
  - tools (search, fetch, summarize)
  - loop ReAct
  - eval com LLM-as-judge
- Diga: **"a entrega é uma versão sua, não cópia da solução. A solução é referência arquitetural."**
- Critérios de avaliação:
  - Funciona end-to-end (40%)
  - Grounding verificável (20%)
  - Tratamento de falhas (15%)
  - Eval implementada (15%)
  - Documentação + README (10%)
- Prazo recomendado: 1-2 semanas após a aula.

## 🎬 Demos

- [ ] Ataque de prompt injection ao vivo
- [ ] LLM-as-judge comparando 2 outputs
- [ ] Trace no LangSmith/Langfuse mostrando um agente debugando

## ❓ FAQ

**P: "Como evitar 100% das alucinações?"** R: Não dá. Reduza com grounding, structured output, e detecção via LLM-as-judge.

**P: "EU AI Act vai me afetar?"** R: Se você opera para usuários na UE, sim. Mesmo que sua empresa esteja fora.

---

# 📊 Calibração & métricas pós-aula

Sugestão de mini-avaliação ao fim de cada encontro (3 min):

1. Em uma frase, qual foi a ideia mais importante de hoje?
2. O que ficou confuso?
3. O que você quer praticar antes da próxima aula?

Resultados informam o recap da próxima aula.

---

# 🔧 Plano B — quando algo der errado

| Situação | Plano B |
|---|---|
| Internet caiu durante demo | Notebook local com respostas mockadas pré-gravadas |
| Chave de API expirou | Use Groq free tier (Llama 3.x, rate-limited mas funciona) |
| Slide não carrega | Tudo está em markdown nos arquivos `pages/encontro-N.md` — projete o texto direto |
| Aluno trava no setup | Combine de fazer setup junto no intervalo. Ofereça Colab como alternativa. |
| Projeto final muito difícil | Solução de referência está nos slides — autorize cópia como ponto de partida. |

---

# 🗂️ Material de apoio

- **Repo:** https://github.com/delgadoliveira/topicos-especiais-ia
- **Slides online:** https://delgadoliveira.github.io/topicos-especiais-ia/
- **PDFs por encontro:** gerar com `npx slidev export slides.md --output dist/pdf/`
- **Speaker mode:** `npx slidev --presenter` (mostra notas + próximo slide)

---

_Última atualização: 2025. Este guia deve ser revisado a cada nova oferta da disciplina conforme o ecossistema evolui._
