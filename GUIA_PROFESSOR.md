# 📘 Guia do Professor — Tópicos Especiais em IA: Agentes (Zero to Hero)

> Material de preparação para o instrutor. **Não é distribuído aos alunos.**
> Use junto com os slides (`slides.md`) e a versão online em
> https://delgadoliveira.github.io/topicos-especiais-ia/

---

## Como usar este guia

Para **cada encontro** você encontra:

1. **Objetivos de aprendizagem** — o que o aluno deve sair sabendo fazer
2. **Cronograma** sugerido (E1–E4 têm 3h; E5–E6 têm 2h)
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
| 8 | 25' | Exercícios guiados no PyRunner |
| 9 | 10' | Mercado + fechamento |

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
- Use a sequência inspirada em **NirDiamant/RAG_TECHNIQUES** como mapa visual: primeiro diagnostique a falha (query, chunk, busca, ranking, contexto ou evidência), depois escolha a técnica. Evite apresentar como catálogo de nomes.

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
- [ ] Abrir os exercícios 3.1-3.5 e mostrar o padrão: editar um TODO pequeno, executar, ler o checklist, repetir
- [ ] Explicar que MCP e multi-agente são simulações locais no navegador; a integração real fica para projeto/ambiente externo

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

# 🏗️ Encontro 5 — Do agente ao sistema de trabalho

## 🎯 Objetivos de aprendizagem

1. Situar para onde o mercado de assistentes e agentes está indo — super apps corporativos, assistentes internos, interfaces geradas pelo modelo (Intelligent UI) e trabalho assíncrono — e dizer o que cada um dos dois encontros responde.
2. Explicar, a partir da curva de horizonte de tarefa da METR, **por que agentes de longa duração são a fronteira agora** — e por que o número importa menos que a mudança no tamanho da unidade de trabalho delegável.
3. Reconhecer, a partir de um caso concreto de operação, por que um trabalho longo pode falhar mesmo quando todas as respostas estão corretas.
4. Traduzir o vocabulário de engenharia (sessão, contexto, harness, sandbox, handoff, idempotência) para termos acessíveis fora da TI.
5. Reconhecer casos reais de agentes de horizonte longo nos mundos pessoal e corporativo.
6. Definir tarefa longa e diferenciá-la de uma resposta lenta ou extensa.
7. Reconhecer o harness como a peça que de fato executa — e aplicar o teste de desligar o modelo para distingui-lo do agente.
8. Identificar em que momento da tarefa cada falha de horizonte longo aparece.
9. Traduzir falhas técnicas de horizonte longo no nome que elas recebem quando chegam ao time.
10. Identificar os problemas de produto que só aparecem quando o trabalho dura horas ou dias.
11. Explicar por que um modelo melhor pode produzir um agente pior, e um bom agente ainda formar um sistema inseguro — ou seja, por que avaliar modelo, agente e sistema são coisas diferentes.
12. Explicar por que tarefas longas exigem estado durável e handoffs.
13. Percorrer uma operação real passo a passo e identificar que peça do sistema atua em cada etapa.
14. Definir critérios de valor, custo e risco para ampliar um piloto, distinguindo projeções de mercado de resultados observados.
15. Situar as quatro camadas do mercado de ferramentas e identificar qual delas a própria organização já possui.
16. Delimitar uma tarefa longa no trabalho, configurar acessos e pontos de revisão na plataforma e verificar a entrega contra fontes e critérios.
17. Reconhecer os quatro campos de um handoff operacional — critério, estado, pendências e definição de pronto — e explicar seu papel na retomada, a partir da demonstração.

## ⏱️ Roteiro de gravação (120 min)

| Bloco | Tempo | Conteúdo |
|---|---:|---|
| Abertura | 14' | **Panorama de mercado**, mapa dos dois encontros, **por que agora** (curva METR) e o fio condutor — slides 1–4 e 6 |
| 1 · A sexta-feira | 10' | **O caso da fila de reembolsos**, o vocabulário do plantão e os casos reais — 5, 7, 8 |
| 2 · A tarefa longa | 9' | O que é tarefa longa, a escada resposta → projeto e a mudança de unidade — 9–11 |
| 3 · Os quatro nomes | 7' | Modelo, harness, agente e sistema — e o slide inteiro sobre o harness — 12, 13 |
| 4 · As falhas | 8' | **Virada** + as quatro falhas e como cada uma chega ao produto — 14–16 |
| 5 · Fazer o trabalho durar | 23' | **Virada** + anatomia, volta a volta, artefatos, reset e demonstração do simulador — 17–22 |
| 6 · Fazer o trabalho ser aceito | 12' | Proposta → evidência → decisão, sandbox, assíncrono, escada de evidência e a fila passo a passo — 23–28 |
| 7 · A sua empresa | 25' | Régua do piloto, Klarna, quatro camadas e uso da plataforma: escolher, instruir, acompanhar e verificar — 29–34 |
| Fechamento | 12' | Caso resolvido, entrega auditável de referência e checklist de quem delega — 35–37 |

> 🧭 **A divisa entre os movimentos 5 e 6 é a tese do encontro.** O 5 responde
> *"o trabalho sobrevive?"* e o 6 responde *"o resultado pode ser aceito?"*. São
> problemas diferentes, e o slide 28 diz isso com as próprias palavras do caso:
> os passos 1 a 5 fazem o agente **trabalhar**, os passos 6 a 9 fazem o trabalho
> **poder ser aceito**. Quase todo projeto real resolve só o primeiro — é por
> isso que a segunda metade é a que costuma ser cortada em protótipo.

> **Formato assíncrono.** Não há laboratório em duplas nem pausa obrigatória.
> Grave a demonstração do simulador e siga para a verificação do resultado.
> O roteiro do laboratório permanece apenas como material complementar opcional.

### ⏱️ Ritmo da gravação

**O Encontro 5 tem 37 slides e um roteiro de 120 minutos de exposição.**
O orçamento das notas (`N min.`) soma duas horas, sem laboratório, intervalo
ou espera por participação. A duração final depende da gravação: use as notas
para preparar demonstrações, não para apenas ler o slide.

Os 18 minutos adicionais aprofundam o uso da plataforma:

| Slide | Tempo | O que demonstrar |
|---|---:|---|
| 22 · Reset | 9' | Três rodadas: falha, reconstrução do handoff e conferência de uma ação anterior |
| 32 · Escolher a tarefa | 6' | Comparar três pedidos, conferir acessos e selecionar dez casos representativos |
| 33 · Escrever o pedido | 6' | Entrega, fontes, política, tratamento de dados ausentes e ponto de parada |
| 34 · Conferir e corrigir | 6' | Abrir evidência, localizar erro, escrever correção e reconciliar os dez IDs |
| 35 · Resolver o caso | 5' | Fechar a conta dos 400 e distinguir decisão, pendência e pagamento |
| 36 · Entrega auditável | 5' | Percorrer as três linhas e mostrar o que salvar para o próximo responsável |

Cada demonstração deve funcionar sem uma resposta do aluno. Exemplos de saída
são ilustrativos; não os apresente como execução real de um produto.

Os slides 18 a 21 explicam o handoff e o reset. O **slide 22 é o simulador de
travessia de reset**: mostre na gravação um cenário que falha e outro que
preserva os campos necessários, explicando a diferença. Explorar a interface
é opcional para quem assiste; a demonstração deve ser compreensível sozinha.

> ⚠️ **A confusão que trava a aula é "harness = agente".** Ela é desarmada em
> dois pontos e os dois precisam ser ditos em voz alta. No **slide 12**, modelo e
> harness aparecem lado a lado como duas peças de software, e *agente* é
> apresentado como nome do arranjo das duas — não como uma terceira caixa. No
> **slide 13** — que vem logo depois, de propósito — o teste prático: desligue o
> modelo e o que continua rodando é o harness. Pergunta que fecha o assunto: *"qual arquivo eu
> abro para mudar isso?"* — para modelo e harness existe resposta; para agente e
> sistema, não.

> 📐 **Por que o slide do harness está aqui e não lá na frente.** Ele já esteve
> no bloco da arquitetura, e isso criava um buraco: a palavra *harness* era
> introduzida no slide 12 e só explicada cinco slides depois — sendo usada no
> meio do caminho como se fosse conhecida. O harness, porém, não é um componente
> que se escolhe em resposta a uma falha; é uma **entidade que já existe em todo
> agente**, com ou sem projeto. Por isso ele pertence ao bloco do vocabulário. As
> *decisões* sobre o harness — quando resetar, o que persistir, o que deixar
> executar — continuam no movimento 5, onde há falha nomeada para justificá-las.

> 🔗 **"Isso não é o que vimos no Encontro 1?" — é, e a resposta certa é dizer
> que sim.** A palavra *harness* é nova; a coisa não é. Dos **cinco componentes
> do agente** apresentados no Encontro 1, **quatro são o harness**: system
> prompt, memória, executor de ferramentas e loop de controle. O quinto, o LLM,
> é a única peça que *não* é. E o loop do slide 19 é o mesmo **ciclo de vida de
> um turno** visto lá em sete etapas — contexto, chamada ao LLM, saída,
> validação, execução, observação —, quase um para um. O Encontro 1 já dizia a
> coisa certa, inclusive: na etapa 5 quem valida é *"o sistema"*, não o modelo.
> Só não tinha dado nome.
>
> **A diferença cabe em um passo.** No Encontro 1, a observação volta ao passo 2
> dentro da mesma janela, e todas as condições de parada são formas de
> *desistir*: `max_steps`, orçamento, timeout, erro fatal. No Encontro 5 aparece
> uma condição que não existia — **recomeçar**. É a única diferença estrutural
> entre os dois loops, e é ela que separa uma demo de uma operação que atravessa
> o fim de semana. Se alguém disser "então é só o mesmo agente rodando mais
> tempo", esta é a frase que responde.

> 🧩 **O slide 15 fecha dois circuitos ao mesmo tempo.** Cada uma das quatro
> falhas traz, em itálico, o nome que ela recebe quando chega ao time — ninguém
> abre um chamado dizendo "houve deriva de objetivo", dizem *"ele piorou com o
> tempo"*. E três das quatro aconteceram literalmente na sexta-feira do slide 5;
> aponte cada uma ao passar. A exceção é o **encerramento precoce** — diga isso,
> porque prova que a lista não foi desenhada para caber na história.

> 💡 **O slide 04 é o que responde “por que esta aula, por que agora”.** Ele mostra
> a curva de horizonte de tarefa da METR — de ~9 segundos em 2020 para 12 a 17
> horas em 2026, dobrando a cada 4 a 7 meses. O argumento não é a previsão: é que
> a **unidade de trabalho delegável mudou de tamanho**, e tudo o que a empresa tem
> em volta (aprovação, acompanhamento, auditoria) foi desenhado para a unidade
> antiga. Leia em voz alta a régua de 50% de acerto e pergunte se alguém entregaria
> 400 reembolsos a um estagiário que acerta metade das vezes.

### Da retomada à verificação (slide 23)

O slide parte de um dos 60 pedidos sem comprovante: a proposta de aprovação
não basta para aceitá-lo. Percorra as quatro funções — fixar critério, produzir
a proposta, conferir evidência e aplicar a regra — mostrando o resultado
concreto: o pedido fica pendente, não aprovado.

Não apresente isso como obrigação de usar quatro agentes. O harness coordena
a execução; a checagem pode usar código, fontes originais e revisão humana.
Outro LLM pode repetir o mesmo erro. Relacione ao Evaluator-Optimizer do
Encontro 2 e à avaliação do Encontro 4: o foco aqui é impedir que uma proposta
sem evidência vire decisão aceita.

O antigo laboratório de handoff não faz parte do deck nem é pré-requisito.
Seu roteiro em **`LABORATORIOS.md`** fica disponível para prática opcional,
fora da gravação (`npm run labs`).

### Como a espera termina (slide 25)

“Dormir” não significa deixar o modelo monitorando e-mail. O harness salva o
pedido e os prazos antes de encerrar a execução. Uma integração detecta o
documento recebido; um agendador dispara os vencimentos. Ambos publicam eventos
com o ID do pedido numa fila de retomada. Um executor roda o harness, que lê
o estado atual e aplica a política; só chama o modelo quando precisa analisar.

Separe os dois prazos do exemplo: o primeiro permite um lembrete único; o
final encaminha ao humano se o documento ainda não chegou. Ausência de
resposta não dispara nada sozinha — quem dispara é o relógio. O recebimento
do documento também não autoriza aprovação automática: ele abre a conferência.
Eventos duplicados ou atrasados devem ser confrontados com o estado atual,
com controle de concorrência e idempotência no envio, não só uma consulta ao log.

Durante a espera não há chamadas ao modelo, mas armazenamento, fila e
monitoramento podem custar. Ao retomar, o contexto é reconstruído a partir
do estado salvo; não há uma memória do modelo que ficou “dormindo”.

### Bloco 0 — abertura de mercado (slides 2 e 3)

Os dois primeiros slides depois da capa existem para **situar antes de explicar**.
A audiência não acompanha o mercado diariamente; entrar direto em "sessões
duráveis" soa como assunto de engenharia.

- **Slide 2 · Panorama.** Quatro movimentos, nesta ordem: (1) o **super app
  corporativo** — um único ponto de entrada para conversa, documentos, código e
  agentes; (2) os **assistentes internos**, em que a empresa monta dezenas de
  agentes sobre os próprios dados; (3) a **Intelligent UI** — a resposta deixa de
  ser texto e vira uma interface gerada na hora (tabela ordenável, calculadora,
  painel); (4) o **trabalho assíncrono**, em que você delega e vai embora.
  💡 Pergunte quantos já usam um assistente corporativo no trabalho: costuma ser
  a maioria, e quase ninguém sabe quem governa aquilo.
  ⚠️ Diga em voz alta que a lista de produtos envelhece em meses — o que fica são
  os quatro movimentos. Cards 1 e 2 viram o Encontro 6; cards 3 e 4, o Encontro 5.
- **Slide 3 · Mapa dos dois encontros.** É um contrato com a turma: o Encontro 5
  responde **"terminou?"** (sessão durável, sandbox, handoff, reset, retomada,
  verificação) e o Encontro 6 responde **"podia?"** (identidade, delegação,
  protocolos, custo por ação, governança). Nenhum dos dois é sobre escolher
  modelo. Quem faltar a um deles sabe exatamente o que perdeu.

> 💡 Se o tempo apertar, este é o bloco que **comprime** (não corta): 5 min
> bastam. Mas não comece pelo caso da sexta-feira sem ele — o caso ganha peso
> justamente porque a audiência acabou de reconhecer o próprio contexto.

### Para quem este encontro é desenhado

A audiência **não vai implementar nada disto**. São pessoas de produto, operação
e gestão que precisam decidir se vale, escolher fornecedor e responder pelo
resultado. Por isso o encontro evita deliberadamente exemplos de engenharia de
software como espinha dorsal: o caso condutor é uma **fila de reembolsos**, não
uma migração de código. Agentes de codificação aparecem apenas como *uma*
instância do mesmo padrão — e o slide da sessão passo a passo diz isso
explicitamente ("é um padrão de trabalho longo, não de um setor").

O bloco 7 ancora tudo na realidade de quem assiste: *vale a pena?*, *qual
ferramenta tenho à disposição?* e, principalmente, *como uso isso no trabalho?*
Os slides 32–34 são exemplos resolvidos, não exercícios em sala:

- **32 · Escolher e configurar:** recorte verificável, lote pequeno com casos
  difíceis, fontes autorizadas, modo de leitura/rascunho e capacidade real de
  trabalhar em segundo plano. Se a plataforma não preserva progresso ou não
  permite pausar, diminua o escopo; o prompt não cria a funcionalidade.
- **33 · Instruir:** um briefing reutilizável com entrega e fontes, limites e
  exceções, ponto de revisão e definição de pronto. Mostre que configurações
  de permissão precisam sustentar as restrições escritas.
- **34 · Acompanhar e verificar:** consultar histórico, abrir a entrega,
  conferir os dez casos contra as fontes, reconciliar IDs e pendências,
  corrigir os casos afetados e só então autorizar a continuação. Uma segunda
  opinião do mesmo agente não substitui checagem independente.

A aula não presume uma interface específica: mostre as funções a procurar
na plataforma aprovada pela empresa, sem prometer controles universais.
O fechamento (37) retoma essas decisões do usuário, não um checklist de implementação.

### Fechar o caso com uma resposta, não com mais perguntas (slides 35–36)

O slide 35 resolve os momentos da abertura: delimitar o pedido, registrar a
triagem, retomar sem repetir ações e bloquear decisões sem evidência.
Se os 60 comprovantes ainda faltarem, o fechamento ilustrativo é
**340 decisões verificadas + 60 pendências = 400 pedidos rastreados**.
Isso não significa 400 resolvidos nem 400 aprovados; decisões verificadas
também podem ser recusas. Não prometa que automação elimina espera externa.

O slide 36 mostra o artefato que o usuário deve exigir: situação por ID,
evidência e política vinculadas, próximo passo e responsável. São linhas
ilustrativas, não um segundo conjunto de totais. A retomada usa o registro;
a conferência humana abre as fontes. E salvar um log não garante idempotência:
o sistema financeiro precisa deduplicar a operação de pagamento, inclusive
quando há repetição de tentativa ou resposta incerta. A aprovação humana
continua sendo uma etapa separada.

### Como o encontro se sustenta narrativamente

O encontro **abre por um panorama de mercado e só depois por uma história** —
nunca por um conceito. O slide 5 narra uma
sexta-feira em que uma operação delega "zere a fila de 400 reembolsos" e, na
segunda, recebe "fila zerada" com 60 pedidos aprovados sem conferir comprovante.
O piloto é suspenso. Essa fila é a espinha dorsal: cada peça apresentada depois
existe para impedir um dos cinco momentos dela, e o estudo de caso do fechamento
(slides 35–37) é literalmente o mesmo cenário — diga isso em voz alta quando
chegar lá.

O piloto suspenso tem uma segunda função: ele reaparece no bloco 7 como
contraste entre volume processado e valor entregue. O slide 29 transforma a
arquitetura numa decisão de negócio: definir metas e limites antes do piloto,
depois comparar tempo até decisão correta, custo por pedido aceito e risco
com a operação sem agente. Os dois dias de investigação do caso são custo;
“400 de 400” não prova qualidade.

A Gartner entra como contexto, não como mensagem principal: sua projeção de
mais de 40% de cancelamentos até 2027 cita custo, valor e risco, mas não mede
uma maioria já cancelada nem elimina limitações técnicas. O caso didático
ilustra esses riscos; não é evidência estatística. A passagem para Klarna é:
economia sem qualidade não basta para justificar a expansão.

Logo depois vem o fio condutor, que decompõe a pergunta do encontro — *por que
agentes que já respondem bem ainda falham em concluir um trabalho?* — em sete
movimentos. Se algum conceito parecer solto, volte a esse slide e diga a qual
movimento ele pertence.

A divisa mais importante do mapa é entre o movimento 5 (*fazer o trabalho
durar*) e o 6 (*fazer o trabalho ser aceito*). São dois problemas diferentes, e
o deck os separa com as palavras do próprio caso: os passos 1 a 5 da fila fazem
o agente **trabalhar**; os passos 6 a 9 fazem o trabalho **poder ser aceito**.
Projetos reais quase sempre entregam só o primeiro.

O slide 7 é o **vocabulário mínimo** e existe para a audiência que não é de
engenharia: sessão, contexto, harness, sandbox, handoff e idempotência. Os seis
são traduzidos **dentro de um único domínio — o plantão de um hospital** (turno,
beira do leito, coordenação do plantão, sala de simulação, passagem de plantão,
dose registrada como aplicada). Isso é deliberado: com analogias de domínios
diferentes, cada termo fica compreensível e as *relações* entre eles somem. Num
domínio só, elas aparecem — o contexto é um recorte da sessão como a beira do
leito é um recorte do prontuário; o handoff existe porque o turno acaba; a
idempotência existe porque duas equipes podem achar que a dose não foi dada. E o
fecho liga ao caso: às 3h de sábado o agente trocou de turno sem passar plantão.
Use a coluna da direita durante toda a exposição; ela é a régua de tradução do
encontro.

A regra de ouro da sequência: **nenhuma peça técnica aparece antes do problema
que ela resolve.** Por isso a anatomia do sistema não abre o bloco técnico — ela
vem depois das falhas, precedida por uma tabela que liga cada falha nomeada ao
componente que responde por ela. Resista à tentação de antecipar componentes.

Há dois slides de **virada**, e eles são a articulação do encontro. O primeiro
fecha a discussão de capacidade e abre a de consequência. O segundo fecha as
falhas e autoriza a arquitetura a existir. Narre-os explicitamente: "o que já
estabelecemos" e "a pergunta que isso abre".

Quatro diagramas carregam o peso visual e substituem listas: a **escada de
resultados** (resposta → tarefa → workflow → projeto, mostrando que a cada
degrau muda o que precisa existir em volta), a **linha do tempo das falhas**
(cada falha tem um momento — e a mais cara é a última, porque chega ao time
parecendo sucesso), a **anatomia do sistema** e a **escada de evidência**
(os quatro níveis se somam, não se substituem).

Sobre o caso da **Klarna**: o ponto não é que automatizar foi errado — o volume
e a economia anunciados foram reais. O ponto é que a métrica escolhida decide o
resultado. Deixe claro que os números vieram da própria empresa e não são
auditados de forma independente.

Sobre o **panorama de ferramentas**: nomes mudam rápido, então o valor do slide
são as quatro camadas, não a lista. A camada de avaliação e observabilidade é a
que mais falta nos projetos reais — e é a que o encontro inteiro argumentou ser
decisiva.

Antes de apresentar harnesses, estabeleça que tarefa longa não significa "o
modelo pensar por horas": significa trabalho com etapas dependentes, estado
acumulado, esperas externas e prova de conclusão.

O bloco 6 é a comprovação do argumento: percorra os nove passos da mesma fila de
reembolsos, agora com sistema em volta, mostrando em cada etapa qual peça já
estudada entra em ação. Os passos 1 a 5 fazem o agente trabalhar; os passos 6 a 9
fazem o trabalho poder ser aceito — e são justamente os que costumam ser
cortados. É essa frase que dá nome aos dois blocos.

Conduza o caso sem escolher frameworks. Mostre o desfecho corrigido e a
entrega auditável de referência: o que o aluno deve acompanhar e conferir.
Não há exercício obrigatório, entrega do aluno, correção ou nota.

---

# 🏛️ Encontro 6 — Como delegar trabalho a agentes e conferir o resultado

## 🎯 Objetivos de aprendizagem

1. Escolher uma tarefa com entrega e fontes que consiga conferir.
2. Escrever um pedido claro, com limites e tratamento de informação ausente.
3. Testar e melhorar o pedido com exemplos e respostas esperadas.
4. Acompanhar a execução, localizar um erro e conferir a correção.
5. Avaliar qualidade, prazo e custo do trabalho aceito.
6. Encerrar, pedir ajuda ou ampliar o uso sem perder o controle.

## 👥 Para quem este encontro é desenhado

A audiência **usa os sistemas**, não implementa a plataforma. A aula foi reduzida
de 38 para **29 slides**, retirando a taxonomia de segurança, protocolos,
catálogo de produtos, casos de incidentes e a segunda situação de RH.

O E5 explica o funcionamento e a verificação de trabalho durável. O E6 acompanha
uma pessoa aplicando isso: **Ana compara duas propostas de licença, encontra um
erro, melhora o pedido e confere a entrega antes de decidir**. Não reintroduza
siglas pelas notas. Os fundamentos técnicos continuam no briefing como apoio.

O simulador de reembolsos da versão anterior do E6 saiu do percurso para evitar
trocar de domínio. O E5 mantém sua demonstração de reset. No E6, as demonstrações
são respostas preparadas, fontes e tabelas comentadas; não resultados medidos
de um modelo específico.

## ⏱️ Roteiro de gravação (120 min)

**29 slides; notas somam 120 minutos.** Não há laboratório obrigatório,
intervalo contabilizado nem espera por interação. A soma é o plano de gravação,
não uma medição da duração de um vídeo já produzido.

| Slides | Tempo | Conteúdo |
|---|---:|---|
| 1–4 | 10' | Abertura, caso de Ana e cinco passos |
| 5–9 | 22' | Escolher a tarefa, limitar ações, selecionar fontes e escrever o pedido |
| 10–14 | 25' | Testar, corrigir uma resposta, comparar versões e diagnosticar a causa |
| 15–20 | 27' | Acompanhar, conferir fontes, corrigir preço e decidir sobre aprovação |
| 21–22 | 9' | Avaliar qualidade e custo com um exemplo numérico |
| 23–29 | 27' | Registrar, compartilhar, interromper, encerrar e resolver o caso |

### Demonstrações e prompts: o centro prático da aula

| Slide | Roteiro para a gravação |
|---|---|
| 5–7 · Preparar | Escolha a comparação, confira acessos e separe os documentos corretos. Não conecte uma pasta inteira por conveniência. |
| 8–9 · Pedir | Leia o prompt e peça a confirmação de entrega, fontes, limites e cabeçalhos. Corrija “vou renovar” para “vou comparar”. |
| 10–11 · Testar | Apresente os quatro casos com gabarito e o ciclo de testar, comparar, ajustar e repetir. |
| 12 · Corrigir o teste | A fonte não informa renovação, mas a saída v1 diz “sim”. Corrija o campo e registre a regra no prompt v2. |
| 13–14 · Conferir a melhoria | Quadro ilustrativo: v1 acerta 3/4, v2 acerta 4/4. Confira os demais casos e diferencie erro de instrução, fonte, acesso e ferramenta. |
| 15–16 · Acompanhar | Mostre andamento normal, bloqueio e resultado parcial; depois confira uma divergência de preço na entrega útil. |
| 19–20 · Aprovar | 100 × R$ 20 = R$ 2.000/mês; upgrade a R$ 26 = R$ 2.600/mês. Diferença: 30%, R$ 600/mês e R$ 7.200/ano. Confira prazo e renovação. |
| 21–22 · Medir | A equipe produziu 100 comparações: 80 aceitas, 12 em correção e 8 pendentes. R$ 2.000/80 = R$ 25 por aceita, igual a R$ 2.500/100. |
| 23–26 · Encerrar ou ampliar | Ficha de operação, compartilhamento, interrupção e encerramento. Passar o resumo não dá a outra pessoa autorização para agir. |
| 27–29 · Fechar | Mostre a entrega de Ana e percorra o roteiro de uso, sem conceitos novos. |

Use **dados fictícios**. Quando a conta não tiver os controles citados, explique
a limitação; não simule uma aprovação técnica com uma resposta de chat.
As telas variam por produto e plano. Não é obrigatório ter uma conta paga para
acompanhar os exemplos resolvidos.

### Prompts reutilizáveis

**Delegar — slide 8:**

> Prepare para Ana uma comparação das licenças da lista anexa. Use somente os
> contratos e propostas desta pasta e a política de compras vigente. Mostre
> fornecedor, quantidade, preço mensal, compromisso anual e fonte. Sinalize
> dados ausentes e mudanças de condição. Não envie mensagens, não compre nem
> aceite upgrades. Entregue a comparação nesta execução e pare para revisão.

**Corrigir — slide 16:**

> Compare a tabela com as propostas originais. Para cada linha, indique a fonte
> e o trecho que sustenta preço e prazo. A proposta de upgrade mostra R$ 26, mas você
> registrou R$ 20. Confira a divergência, corrija os totais afetados e liste as
> mudanças. Sem evidência, marque pendente. Não envie nem contrate nada.

**Encerrar — slide 26:**

> Não inicie novas ações. Resuma o que foi concluído, o que está em andamento e
> o que ficou pendente, com IDs e evidências. Liste agendamentos e acessos que
> precisam de revisão; não os declare revogados sem confirmação.

Ensine os limites junto com os prompts: instrução não cria permissão nem
revogação; revisão pelo mesmo modelo não é independente; handoff não transfere
autoridade. Peça fontes, cálculos e critérios verificáveis, não pensamentos
internos do modelo.

### Testar e melhorar o pedido — slides 10–14

Este é o ciclo de trabalho **do usuário que prepara a tarefa**. Não é preciso
ensinar o nome “inner loop”. A pergunta é simples: o pedido produziu o resultado
esperado nesses exemplos, com essas fontes e configurações?

1. **Defina antes:** prepare os casos A–D e escreva o resultado esperado.
   A: R$ 2.000/mês e R$ 24.000/ano; B: renovação não informada vira pendência;
   C: upgrade de 30% não é aceito; D: documento externo não autoriza envio de dados.
2. **Execute com segurança:** uma tarefa nova por caso, mesma configuração e
   ações reais desabilitadas. Não coloque o gabarito no pedido de execução.
   Salve entrada, versão do prompt, saída e histórico disponível.
3. **Compare:** conteúdo correto, fonte que sustenta, campos presentes e ações
   dentro do escopo. Registre passa/falha por critério; sem evidência não passa.
4. **Ajuste uma causa:** se v1 inventou a renovação, acrescente a regra explícita
   para dado ausente. Se faltava fonte ou a ferramenta permitiu ação indevida,
   não tente resolver só com mais texto.
5. **Reteste:** mesmos casos para detectar regressões; depois casos novos, como
   imposto adicional e quantidade divergente. Repita os casos críticos para
   observar variabilidade, mantendo a versão anterior disponível.

**Prompt para apoiar a comparação — não para terceirizar o veredito:**

> Compare a saída com o gabarito e as fontes fornecidos, caso a caso. Para cada
> critério, marque passa, falha ou sem evidência. Cite o trecho que sustenta a
> classificação e a divergência encontrada. Não reescreva a resposta avaliada
> nem invente evidência para fazê-la passar. Avalie ações apenas quando houver
> registro da ferramenta; uma declaração no texto não prova execução.

No slide 12, o professor mostra **uma saída ilustrativa**, não um resultado
experimental: v1 preenche renovação indevidamente; a resposta corrigida a marca
como não informada. A regra entra no prompt v2. No slide 13, o quadro de 3/4
para 4/4 também é preparado para a explicação. Não anuncie ganho de um modelo.

No slide 16, a tarefa útil apresenta outro erro ilustrativo: preço unitário
transcrito como R$ 20 em vez de R$ 26. Corrigir o pedido nos testes não elimina
a necessidade de conferir a entrega real.

**Critério didático para avançar:** quatro casos corretos, campos exigidos
presentes e nenhuma violação crítica. Isso não estima confiabilidade em
produção. Outro modelo pode ajudar na triagem, mas não substitui gabarito,
fontes nem revisão humana. Falha de segurança não pode ser compensada por
uma média alta de qualidade textual.

### Apoio técnico do professor — fora do percurso obrigatório

Os itens abaixo ficam disponíveis para dúvidas, **não são tópicos a desenvolver
na gravação**. Nos slides, traduza-os em decisões: qual conta está conectada,
quais ações estão permitidas, quem aprova e como parar. Não é preciso memorizar
principal, capability, lease, control plane, não repúdio ou protocolos.

- **Principal** é identidade técnica reconhecida pelo sistema. Solicitante,
  executor, sponsor e aprovador podem ser diferentes. O registro não determina
  automaticamente a responsabilidade jurídica.
- Os quatro campos de **mandato** são um roteiro didático, não o schema AP2.
  Escopo, prazo e limites precisam ser checados na execução.
- **Catálogo, portaria e cofre** ficam fora da decisão textual do modelo;
  podem integrar o harness e serviços externos. Não redefina agente como LLM.
- **MCP** está na AAIF; **A2A** é um projeto da Linux Foundation. Padrões não
  garantem autorização, segurança ou migração sem esforço.
- **Sponsor** no Entra pode ser pessoa ou grupo. Cadastro de responsável não
  equivale a não repúdio nem aprovação de cada ação.
- **Autonomia** depende de impacto, dados, alcance, valor, reversibilidade e
  obrigações. O caso de RH saiu do deck para não abrir outro domínio.
- **Métricas:** compare denominadores, qualidade, cobertura e janela de tempo.
  Escalar corretamente não é fracasso; encerrar sem resolver não é sucesso.

### Um caso curto em aula; os demais apenas para consulta

**Project Vend — slide 18, três minutos:** é a única excursão externa. Mostre
como preço, desconto e destino de pagamento podem estar errados mesmo quando a
ferramenta funciona. Volte imediatamente à conferência da proposta de Ana.

**Agentic misalignment — fora do deck:** simulações controladas da Anthropic,
não taxa de incidência em empresas. O valor está em examinar o mecanismo e as
opções de parada/escalada.

**Hugging Face — fora do deck:** use o [comunicado primário](https://huggingface.co/blog/security-incident-july-2026),
que relata intrusão, acesso a dados internos e credenciais, detecção e resposta.
Esse comunicado inicial não identifica o modelo; não atribua a ele números de
agentes, motivação ou detalhes de relatos posteriores. Não conclua “não houve
vazamento de clientes” quando a avaliação ainda estava em curso.

**Fonte do slide 18 — Project Vend:** use a [fase 1](https://www.anthropic.com/research/project-vend-1).
O experimento ilustra falhas de preço, memória e decisões de negócio. A própria
fonte aponta melhorias de modelo **e** ferramentas/scaffolding como caminhos;
não diga que inteligência é irrelevante. As linhas da tabela são observações,
não uma cronologia rígida de seis etapas.

### Fechamento

O slide 23 prepara a continuidade da mesma tarefa; não abre uma aula de inventário.
Mostre o que Bruno precisaria saber e quais acessos ainda precisariam ser aprovados.
Compartilhar e agendar (24) muda esse alcance.

O slide 27 resolve o caso iniciado no slide 3: comparação conferida, nenhuma
compra e condição pendente registrada. O 28 percorre antes, durante e depois.
O 29 encerra com cinco perguntas simples. Não retome a antiga história de uma
compra já efetuada: nesta versão Ana confere **antes** de contratar.

O Laboratório 2 permanece em **`LABORATORIOS.md`** como prática individual
opcional ou oficina separada, fora das duas horas. Não há entrega nem nota.

---

# 📝 Reflexão opcional — sem entrega ou avaliação

Ao fim de cada encontro, o estudante pode registrar privadamente:

1. Qual foi a ideia mais importante?
2. O que ainda precisa ser revisto?
3. Que decisão de arquitetura faria diferente agora?

Essas perguntas não são enviadas, corrigidas ou usadas para nota.

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
- **Briefing do professor (Encontros 5 e 6):** `BRIEFING_PROFESSOR.md` — este guia diz *como conduzir*; o briefing ensina *o conteúdo*, no nível em que um aluno pode te testar. Gere com `npm run briefing`.
- **Laboratórios (Encontros 5 e 6):** `LABORATORIOS.md` — roteiros completos, materiais prontos e critérios de avaliação. Gere a versão navegável com `npm run labs`.
- **Este guia em HTML:** `npm run guia`
- **PDFs por encontro:** gerar com `npx slidev export slides.md --output dist/pdf/`
- **Speaker mode:** `npx slidev --presenter` (mostra notas + próximo slide)

---

_Última atualização: 2025. Este guia deve ser revisado a cada nova oferta da disciplina conforme o ecossistema evolui._
