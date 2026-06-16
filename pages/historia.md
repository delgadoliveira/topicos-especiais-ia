---
layout: section
---

# 📜 História
## Dos primeiros modelos aos Agentes de IA

<div class="text-sm opacity-60 mt-4">~45 min · Por que entender a história importa</div>

---
layout: center
class: text-center
---

# Por que olhar para trás?

<v-clicks>

<div class="text-xl mt-6 opacity-80">Cada decisão de design de um agente moderno…</div>

<div class="text-2xl mt-4 text-cyan-400">…é resposta a um problema descoberto há décadas.</div>

<div class="text-base mt-12 opacity-60 max-w-2xl mx-auto">
"Agente" não é uma palavra nova. O que mudou foi <b>quem</b> está no controle: antes eram regras escritas por humanos; hoje é um modelo estatístico treinado em ~todo o texto da internet.
</div>

</v-clicks>

---

# A linha do tempo de 70 anos — visão geral

```mermaid {scale: 0.55}
timeline
    title 70 anos de IA — em uma página
    1950s : Perceptron (1958)
          : Teste de Turing
    1960s : ELIZA (1966)
          : 1º "chatbot" baseado em regras
    1970s : Primeiro AI Winter
    1980s : Sistemas Especialistas
          : Backpropagation popularizado
    1990s : Deep Blue vence Kasparov (1997)
    2000s : Estatística + Internet
          : Modelos de linguagem N-gram
    2010s : Deep Learning explode
          : Word2Vec, seq2seq, LSTM
    2017  : Transformer "Attention is All You Need"
    2018  : GPT-1 + BERT
    2020  : GPT-3 (175B) — in-context learning
    2022  : ChatGPT + ReAct + Chain-of-Thought
    2023  : GPT-4, AutoGPT, function calling
    2024  : Claude 3, MCP, Computer Use, o1
    2025  : Cursor, Claude Code, Devin, Manus
          : Era dos agentes
```

---
layout: two-cols
---

# 🏛️ Pré-história (1950–2010)

<div class="text-sm">

**1950** · Turing — **Teste de Turing**

**1958** · Rosenblatt — **Perceptron** (1º modelo neural)

**1966** · Weizenbaum — **ELIZA** (chatbot com regex)

**1980s** · **Sistemas Especialistas** (regras if-then)

**1997** · **Deep Blue** vence Kasparov

</div>

::right::

<div class="mt-8 p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-sm">
Por <b>50 anos</b>, "IA" significou:<br>
<b>👨‍💻 Humano escreve regras → máquina executa</b>
</div>

<div class="mt-4 p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-sm">
A revolução de 2017–2022 inverteu:<br>
<b>📚 Máquina aprende padrões → humano dá objetivos</b>
</div>

<div class="mt-4 text-xs opacity-70">
Os "agentes" dos anos 80 (Soar, BDI) tinham arquitetura parecida — mas o "cérebro" era <code>if-else</code>, não um LLM.
</div>

---
layout: two-cols
---

# 🌊 Deep Learning (2012–2017)

<div class="text-sm">

**2012** · **AlexNet** — CNNs dominam visão computacional

**2013** · **Word2Vec** — palavras viram vetores (*"rei − homem + mulher ≈ rainha"*)

**2014** · **Seq2Seq** — encoder/decoder para tradução

**2015** · **Attention** — modelo "olha" partes relevantes da entrada

**2016** · **AlphaGo** vence Lee Sedol (RL + busca)

</div>

::right::

# Por que importa?

<v-clicks>

<div class="mt-3 p-2 rounded-lg bg-white/5 text-sm">
🧮 <b>Word2Vec</b> → semântica numérica → base dos <b>embeddings/RAG</b>
</div>

<div class="mt-2 p-2 rounded-lg bg-white/5 text-sm">
👁️ <b>Attention</b> → foco em palavras-chave → <b>coração do Transformer</b>
</div>

<div class="mt-2 p-2 rounded-lg bg-white/5 text-sm">
🎮 <b>AlphaGo</b> → planejamento sobre-humano → inspirou <b>Tree-of-Thoughts</b>
</div>

</v-clicks>

---

# 2017 · O artigo que mudou tudo

<div class="grid grid-cols-2 gap-4 mt-2 text-sm">
<div class="space-y-2">
### *Attention Is All You Need*
<div class="text-xs opacity-80">Vaswani et al., Google Brain · jun/2017</div>
<div><b>8 autores, 11 páginas, indústria reescrita.</b></div>
<div><b>Sacada:</b> remove RNN/LSTM e convolução; fica com <b>só atenção</b> → paralelizável em GPU.</div>
<div><b>Efeito:</b> ⚡ treino muito mais rápido · 📈 escala com dados/parâmetros · 🌍 funciona para qualquer sequência.</div>
</div>
<div>
```mermaid {scale: 0.5}
flowchart TB
  I[Tokens de entrada] --> E[Embeddings + Positional]
  E --> A1[Self-Attention]
  A1 --> F1[Feed Forward]
  F1 --> A2[Self-Attention]
  A2 --> F2[Feed Forward]
  F2 --> O[Próximo token probável]
  style A1 fill:#7c5cff,color:#fff
  style A2 fill:#7c5cff,color:#fff
  style O fill:#22c55e,color:#000
```
<div class="text-xs opacity-60 text-center mt-1">Arquitetura Transformer (simplificada) — base de todos os LLMs modernos.</div>
</div>
</div>

---

# 2018 · A corrida começa

<div class="grid grid-cols-2 gap-6">

<div class="p-5 rounded-xl border border-purple-500/40 bg-purple-500/5">

### 🔵 GPT-1
**OpenAI · Junho 2018**

- **117 milhões** de parâmetros
- Treinado em **BooksCorpus** (~7 mil livros)
- "Improving Language Understanding by Generative Pre-Training"
- Demonstrou: pré-treino + fine-tuning bate modelos especializados
- Praticamente ignorado pela mídia

</div>

<div class="p-5 rounded-xl border border-cyan-500/40 bg-cyan-500/5">

### 🟢 BERT
**Google · Outubro 2018**

- **340 milhões** de parâmetros
- Bidirectional Encoder
- Bateu 11 benchmarks de NLP
- Foi a **estrela do momento** — dominou pesquisa por 2 anos
- Mas: bom em *entender*, ruim em *gerar*

</div>

</div>

<div class="mt-8 p-4 rounded-xl bg-amber-500/10 border border-amber-500/30">
<b>Curiosidade:</b> em 2018, a comunidade apostava em <b>BERT</b> (Google) como o futuro. Quase ninguém previu que a abordagem <i>generative-only</i> da OpenAI venceria.
</div>

---
layout: two-cols
---

# 2019 · GPT-2

<div class="text-sm">

**Fevereiro de 2019.** OpenAI anuncia o GPT-2:

- **1.5 bilhão** de parâmetros (13× GPT-1)
- Geração de texto **assustadoramente coerente**
- OpenAI **se recusa a publicar** → polêmica "ClosedAI"

</div>

::right::

# 🎯 Por que importou

<v-clicks>

<div class="mt-4 p-3 rounded-lg bg-white/5 text-sm">
Primeiro modelo que gerou texto <b>passável por humano</b> em parágrafos curtos.
</div>

<div class="mt-2 p-3 rounded-lg bg-white/5 text-sm">
Iniciou o debate <b>"AI Safety"</b> no mainstream.
</div>

<div class="mt-3 p-3 rounded-lg bg-white/5">
Validou a tese: <b>mais parâmetros + mais dados = melhor</b>. A "Bitter Lesson" de Sutton se confirmava.
</div>

<div class="mt-3 p-3 rounded-lg bg-white/5">
<b>Sem fine-tuning</b>, o modelo já mostrava sinais de aprender tarefas só de ver exemplos no prompt.
</div>

</v-clicks>

---

# 2020 · GPT-3 — a virada

<div class="text-center text-3xl my-6">
175 <span class="text-cyan-400">bilhões</span> de parâmetros
</div>

<div class="grid grid-cols-3 gap-3 text-sm">
<div class="p-3 rounded-xl bg-white/5 border border-white/10">
### 📦 Escala
175B parâmetros, 100× GPT-2, ~500B tokens e treino estimado em <b>US$ 5–10 mi</b>.
</div>
<div class="p-3 rounded-xl bg-white/5 border border-white/10">
### 💡 ICL
<b>In-Context Learning</b>: com 1–5 exemplos no prompt, aprende a tarefa sem fine-tuning. Aqui nasce o <b>few-shot prompting</b>.
</div>
<div class="p-3 rounded-xl bg-white/5 border border-white/10">
### 🌐 API privada
Sem open source; acesso por API e waitlist. Isso catalisou o ecossistema <b>GPT-as-a-Service</b>.
</div>
</div>

<div class="mt-4 p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-sm">
💬 Aqui nasce a <b>engenharia de prompts</b>: pela primeira vez, programar IA significava <b>escrever em inglês</b>, não em Python.
</div>

---
layout: two-cols
---

# 2021 · Codex e o despertar

<div class="text-sm">

**Jul/2021** · **Codex** (GPT-3 fine-tuned em código) → motor do **GitHub Copilot**

**Set/2021** · **WebGPT** — LLM navegando na web (clica links, lê páginas)

📚 Academia pergunta: *"Como dar ferramentas a um LLM?"*

</div>

::right::

# 🌱 Sementes de agentes

<v-clicks>

<div class="mt-3 p-2 rounded-lg bg-white/5 text-sm">
🧑‍💻 <b>Codex</b> → LLM produz <b>código executável</b> → "code as action"
</div>

<div class="mt-2 p-2 rounded-lg bg-white/5 text-sm">
🌐 <b>WebGPT</b> → primeiro "agente" web da OpenAI
</div>

<div class="mt-2 p-2 rounded-lg bg-white/5 text-sm">
📄 Primeiros papers sobre <b>"LLMs as Tool Users"</b> — ideia que domina 2023
</div>

</v-clicks>

---

# 2022 · O ano em que tudo aconteceu

```mermaid {scale: 0.55}
timeline
    title 2022 — o ano-zero dos agentes
    Janeiro    : Chain-of-Thought paper (Google)
               : "Let's think step by step"
    Março      : InstructGPT (OpenAI)
               : RLHF entra no mainstream
    Abril      : DALL-E 2 + Imagen
    Maio       : Gato (DeepMind) — agente multi-tarefa
    Outubro    : ReAct paper (Yao et al.)
               : Thought + Action + Observation
    Novembro   : 🚀 ChatGPT é lançado (30/11)
               : 100M usuários em 2 meses
    Dezembro   : Toolformer (Meta)
               : LLMs aprendem a chamar APIs sozinhos
```

---
layout: two-cols
---

# Os 3 papers de 2022 que criaram "agentes"

<div class="mt-2 text-sm space-y-3">
<div><b>1️⃣ Chain-of-Thought</b> (Wei et al., jan/22)<br><span class="text-xs opacity-80">"Let's think step by step" melhora reasoning em 20–40%.</span></div>
<div><b>2️⃣ ReAct</b> (Yao et al., out/22)<br><span class="text-xs opacity-80"><b>Re</b>asoning + <b>Act</b>ing: verbalizar antes de agir reduz erros e aumenta interpretabilidade.</span></div>
<div><b>3️⃣ Toolformer</b> (Schick et al., dez/22)<br><span class="text-xs opacity-80">LLMs aprendem sozinhos quando chamar APIs como calculadora, busca e tradução.</span></div>
</div>

::right::

# E o ChatGPT?

<div class="mt-4 text-center">
<div class="text-5xl font-bold text-cyan-400">30/nov/2022</div>
<div class="text-lg opacity-80 mt-2">Lançamento do ChatGPT</div>
</div>

<v-clicks>

<div class="mt-6 p-3 rounded-lg bg-white/5">
📱 <b>5 dias</b> para 1 milhão de usuários<br>
<i>(Netflix levou 3,5 anos; Instagram, 2,5 meses)</i>
</div>

<div class="mt-3 p-3 rounded-lg bg-white/5">
🌍 <b>2 meses</b> para 100 milhões de usuários
</div>

<div class="mt-3 p-3 rounded-lg bg-cyan-500/10 border border-cyan-500/30">
<b>Não era nada tecnicamente novo</b> — era GPT-3.5 + interface de chat + RLHF.<br>
A revolução foi <b>de acesso</b>, não de modelo.
</div>

</v-clicks>

---

# 2023 · A explosão Cambriana dos agentes (1º semestre)

<div class="grid grid-cols-2 gap-3 mt-2 text-sm">
<div class="p-3 rounded-lg bg-white/5"><b>Março</b> · GPT-4 — multimodal, raciocínio muito melhor</div>
<div class="p-3 rounded-lg bg-white/5"><b>Março</b> · LangChain explode (10k → 60k ⭐ no GitHub)</div>
<div class="p-3 rounded-lg bg-white/5"><b>Março</b> · <b>AutoGPT</b> viraliza como primeiro agente "autônomo" (150k ⭐ em 1 mês)</div>
<div class="p-3 rounded-lg bg-white/5"><b>Abril</b> · <b>BabyAGI</b> populariza loop com to-do list e memória vetorial</div>
<div class="p-3 rounded-lg bg-white/5"><b>Maio</b> · LlamaIndex vira referência em RAG</div>
<div class="p-3 rounded-lg bg-white/5"><b>Junho</b> · OpenAI lança <b>Function Calling</b> oficial</div>
</div>

<div class="mt-4 p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-sm">
🎢 <b>Realidade check:</b> AutoGPT impressionava, mas quase nunca concluía tarefas. Mesmo assim, mostrou ao mercado o que <i>poderia</i> existir.
</div>

---

# 2023 · A explosão Cambriana dos agentes (2º semestre)

<div class="grid grid-cols-2 gap-3 mt-2 text-sm">
<div class="p-3 rounded-lg bg-white/5"><b>Julho</b> · Llama 2 — primeiro LLM open source competitivo</div>
<div class="p-3 rounded-lg bg-white/5"><b>Setembro</b> · Mistral 7B — open source eficiente</div>
<div class="p-3 rounded-lg bg-white/5"><b>Novembro</b> · GPTs e Assistants API no OpenAI DevDay</div>
<div class="p-3 rounded-lg bg-white/5"><b>Novembro</b> · <b>Tree of Thoughts</b> (Yao) leva busca em árvore ao raciocínio</div>
</div>

<div class="mt-4 p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-sm">
🧠 O saldo de 2023: agentes saem do paper e viram <b>categoria de produto</b>, mesmo com UX frágil, loops e custos altos.
</div>

---
layout: two-cols
---

# 2024 · Maturidade e novos paradigmas

**Março** · **Claude 3** (Anthropic) — primeiro modelo a bater GPT-4 em benchmarks gerais.

**Maio** · **GPT-4o** — multimodal nativo, voz em tempo real.

**Setembro** · **OpenAI o1** — primeiro modelo com **reasoning explícito** treinado via RL. Pensa antes de responder.

**Outubro** · **Computer Use** (Anthropic) — Claude controla mouse e teclado.

**Novembro** · **MCP** (Model Context Protocol) — padrão aberto para conectar LLMs a ferramentas.

**Dezembro** · **Devin** (Cognition) e **o3** anunciados.

::right::

# 🔑 Mudanças paradigmáticas

<v-clicks>

<div class="mt-4 p-3 rounded-lg bg-purple-500/10 border border-purple-500/30">
<b>Reasoning treinado</b> (o1) — não é mais só "prompt engineering". O modelo <b>aprendeu</b> a pensar passo a passo durante o RL.
</div>

<div class="mt-3 p-3 rounded-lg bg-cyan-500/10 border border-cyan-500/30">
<b>Computer Use</b> — quebra a barreira "LLM só fala". Agora ele <b>opera computadores</b> como nós.
</div>

<div class="mt-3 p-3 rounded-lg bg-green-500/10 border border-green-500/30">
<b>MCP</b> — finalmente um padrão (tipo USB) para ferramentas. Antes, cada framework tinha o seu.
</div>

</v-clicks>

---

# 2025 · A era dos produtos agentic

<div class="grid grid-cols-3 gap-3 mt-2 text-sm">
<div class="p-3 rounded-xl bg-white/5 border border-white/10">
### 🎯 Coding Agents
<b>Cursor</b>, <b>Claude Code</b>, <b>GitHub Copilot Agent</b>, <b>Devin</b>, <b>Aider</b>, <b>Cline</b> e <b>Continue</b> levam agentes direto para o fluxo de desenvolvimento.
</div>
<div class="p-3 rounded-xl bg-white/5 border border-white/10">
### 🌐 General Agents
<b>Manus</b>, <b>OpenAI Operator</b>, <b>ChatGPT Tasks / Agents</b> e <b>Perplexity Comet</b> vendem a ideia de agente generalista para o público.
</div>
<div class="p-3 rounded-xl bg-white/5 border border-white/10">
### 🏢 Enterprise
<b>Salesforce Agentforce</b>, <b>Microsoft Copilot Studio</b>, <b>Google Agentspace</b>, <b>smolagents</b>, <b>CrewAI</b>, <b>AutoGen</b> e <b>LangGraph</b> puxam a adoção corporativa.
</div>
</div>

<div class="mt-4 p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-sm">
🎯 <b>O que mudou em 2025:</b> agentes deixaram de ser demos virais e viraram <b>produtos com receita</b>. Cursor sozinho chegou a US$ 100M ARR em 12 meses.
</div>

---

# Crescimento de parâmetros — escala visual

<div class="mt-6">

| Modelo | Ano | Parâmetros | Cresc. vs anterior |
|---|---|---|---|
| GPT-1 | 2018 | 117 M | — |
| BERT-large | 2018 | 340 M | 3× |
| GPT-2 | 2019 | 1.5 B | 4× |
| T5 | 2019 | 11 B | 7× |
| GPT-3 | 2020 | 175 B | 16× |
| PaLM | 2022 | 540 B | 3× |
| GPT-4 (estimado) | 2023 | ~1.7 T (MoE) | 3× |
| Claude 3 Opus / Gemini Ultra | 2024 | ? (não divulgado) | — |

</div>

<div class="mt-4 p-4 rounded-xl bg-amber-500/10 border border-amber-500/30">
🧊 <b>Plot twist (2024+):</b> a corrida por mais parâmetros desacelerou. O foco virou <b>melhor treinamento</b>, <b>reasoning</b> e <b>arquiteturas MoE</b> (Mixture of Experts) — mais eficientes.
</div>

---
layout: two-cols
---

# 🧬 Da pesquisa ao produto

<div class="mt-2 text-xs space-y-1.5">
<div>📄 <b>2017</b> — Transformer</div>
<div>🔬 <b>2018–2020</b> — modelos maiores, ainda no laboratório</div>
<div>💬 <b>2022</b> — ChatGPT acerta a UX e vira produto viral</div>
<div>🛠️ <b>2023</b> — function calling: LLM vira <i>orquestrador</i></div>
<div>🤖 <b>2024</b> — reasoning treinado + uso de computador</div>
<div>💼 <b>2025</b> — agentes em produção com SLA, métricas e receita</div>
</div>

::right::

# 🧠 O que aprendemos em 7 anos?

<v-clicks>
<div class="mt-2 text-sm space-y-2">
<div class="p-2 rounded-lg bg-white/5"><b>1. Escala funciona</b> — mais dados e parâmetros ajudam, até saturar.</div>
<div class="p-2 rounded-lg bg-white/5"><b>2. RLHF é crucial</b> — sem alinhamento, o modelo é ruim para humanos.</div>
<div class="p-2 rounded-lg bg-white/5"><b>3. Ferramentas > parâmetros</b> — Python + busca pode vencer um modelo 10× maior.</div>
<div class="p-2 rounded-lg bg-white/5"><b>4. Reasoning pode ser treinado</b> — o1 e DeepSeek-R1 provam isso.</div>
<div class="p-2 rounded-lg bg-white/5"><b>5. O loop importa</b> — agente = controle de execução, não só conversa.</div>
</div>
</v-clicks>

---
layout: center
class: text-center
---

# 🎬 Resumo executivo

<div class="text-lg mt-8 max-w-3xl mx-auto opacity-90 leading-relaxed">

De <b>1958 (Perceptron)</b> a <b>2017</b>, foram <b>59 anos</b> para chegar ao Transformer.

De <b>2017</b> a <b>2022 (ChatGPT)</b>, <b>5 anos</b> para sair da pesquisa e virar produto de massa.

De <b>2022</b> a <b>2025 (agentes em produção)</b>, <b>3 anos</b>.

</div>

<div class="text-2xl mt-12 text-cyan-400 font-bold">
A próxima curva está acontecendo agora.
</div>

<div class="text-sm mt-4 opacity-70">
…e vocês vão construí-la.
</div>

---
layout: section
---

# ✅ Fim da sessão histórica

Agora que sabemos *como chegamos aqui*, vamos entender *o que é* um agente.

→ Próximo: **Encontro 1 — Fundamentos**

---

# 📚 Referências públicas — Sessão histórica

<div class="grid grid-cols-2 gap-3 text-xs mt-3">
<div class="p-3 rounded bg-purple-500/10 border border-purple-500/30">
<b>Marcos da IA</b>
<ul class="mt-1">
<li>Rosenblatt (1958) — <i>The Perceptron</i> · Psychological Review</li>
<li>Rumelhart, Hinton & Williams (1986) — <i>Learning Representations by Back-propagating Errors</i> · Nature</li>
<li>LeCun et al. (1998) — <i>Gradient-Based Learning Applied to Document Recognition</i> (LeNet)</li>
<li>Krizhevsky, Sutskever & Hinton (2012) — <i>ImageNet Classification with Deep CNNs</i> (AlexNet)</li>
<li>Mikolov et al. (2013) — <i>word2vec</i> · <a href="https://arxiv.org/abs/1301.3781">arXiv:1301.3781</a></li>
</ul>
</div>

<div class="p-3 rounded bg-cyan-500/10 border border-cyan-500/30">
<b>Era Transformer & LLMs</b>
<ul class="mt-1">
<li>Vaswani et al. (2017) — <i>Attention Is All You Need</i> · <a href="https://arxiv.org/abs/1706.03762">arXiv:1706.03762</a></li>
<li>Devlin et al. (2018) — <i>BERT</i> · <a href="https://arxiv.org/abs/1810.04805">arXiv:1810.04805</a></li>
<li>Radford et al. (2018) — <i>GPT-1</i> · <a href="https://openai.com/research/language-unsupervised">openai.com/research</a></li>
<li>Brown et al. (2020) — <i>GPT-3, Language Models are Few-Shot Learners</i> · <a href="https://arxiv.org/abs/2005.14165">arXiv:2005.14165</a></li>
<li>Ouyang et al. (2022) — <i>InstructGPT (RLHF)</i> · <a href="https://arxiv.org/abs/2203.02155">arXiv:2203.02155</a></li>
</ul>
</div>
</div>

---

# 📚 Referências públicas — Sessão histórica (continuação)

<div class="grid grid-cols-2 gap-3 text-xs mt-3">

<div class="p-3 rounded bg-green-500/10 border border-green-500/30">
<b>Era dos agentes</b>
<ul class="mt-1">
<li>Yao et al. (2022) — <i>ReAct</i> · <a href="https://arxiv.org/abs/2210.03629">arXiv:2210.03629</a></li>
<li>Significant-Gravitas (2023) — <i>Auto-GPT</i> · <a href="https://github.com/Significant-Gravitas/AutoGPT">github.com/Significant-Gravitas/AutoGPT</a></li>
<li>Park et al. (2023) — <i>Generative Agents</i> · <a href="https://arxiv.org/abs/2304.03442">arXiv:2304.03442</a></li>
<li>Anthropic (2024) — <i>MCP</i> · <a href="https://modelcontextprotocol.io/">modelcontextprotocol.io</a></li>
<li>Google (2025) — <i>A2A Protocol</i> · <a href="https://a2a-protocol.org/">a2a-protocol.org</a></li>
</ul>
</div>

<div class="p-3 rounded bg-amber-500/10 border border-amber-500/30">
<b>Recursos didáticos</b>
<ul class="mt-1">
<li>Goodfellow, Bengio & Courville (2016) — <i>Deep Learning</i> · <a href="https://www.deeplearningbook.org/">deeplearningbook.org</a> (livre)</li>
<li>Stanford CS25 — <i>Transformers United</i> · <a href="https://web.stanford.edu/class/cs25/">web.stanford.edu/class/cs25</a></li>
<li>3Blue1Brown — <i>Neural Networks series</i> · YouTube</li>
<li>Andrej Karpathy — <i>Neural Networks: Zero to Hero</i> · YouTube</li>
</ul>
</div>
</div>

<div class="mt-2 text-xs opacity-70">
Todo conteúdo é de domínio público. Marcas mencionadas pertencem aos respectivos donos; uso exclusivamente educacional.
</div>
