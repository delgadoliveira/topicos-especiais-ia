---
layout: section
---

# 💾 Encontro 3
## Skills, Memória & Contexto

<div class="text-sm opacity-60 mt-4">3 horas · Context window, RAG, vector DBs, memória, skills, MCP, multi-agentes</div>

---
layout: center
class: text-center
---

# 💭 Onde paramos…

<div class="text-xl mt-6 opacity-90">
Seu agente já <b>pensa</b> (CoT, Planning) e <b>age com precisão</b> (Function Calling).<br>
Mas tem um problema grave:
</div>

<div class="mt-6 text-2xl text-red-400 font-bold">
Ele é amnésico.
</div>

<div class="mt-6 text-sm opacity-60">
Não lembra da conversa de ontem. Não sabe quem você é. Não tem acesso aos seus documentos.<br>
Hoje vamos dar <b>memória</b>, <b>conhecimento</b> e <b>habilidades reutilizáveis</b> ao agente.
</div>

---

# 🗺️ Agenda do Encontro 3

<div class="grid grid-cols-2 gap-6 mt-6">

<div>

**Bloco 1 — Contexto e Memória (~90 min)**
- 3.1 O problema da context window
- 3.2 Estratégias de context management
- 3.3 RAG (Retrieval-Augmented Generation)
- 3.4 Vector DBs (Chroma, Qdrant, pgvector)
- 3.5 Memória de curto e longo prazo

</div>

<div>

**Bloco 2 — Skills e Multi-Agent (~90 min)**
- 3.6 Skills — capacidades reutilizáveis
- 3.7 MCP — Model Context Protocol
- 3.8 Padrões multi-agente
- 3.9 Hands-on: agente com RAG + memória
- 3.10 Exercícios

</div>

</div>

---

# 🧭 Vocabulário do dia — em 1 frase cada

<div class="grid grid-cols-1 gap-2 text-sm mt-3">

<div class="p-3 rounded-lg bg-purple-500/10 border border-purple-500/30">
<b>🎯 Grounding</b> — toda afirmação do agente é <b>rastreável até uma fonte</b>. É a diferença entre <i>"li no Wikipedia"</i> (grounded) e <i>"alguém me disse"</i> (não grounded).
</div>

<div class="p-3 rounded-lg bg-cyan-500/10 border border-cyan-500/30">
<b>🧪 Synthesis</b> — combinar várias fontes em <b>uma resposta coerente</b>, sem contradição. Como escrever a revisão de literatura do TCC a partir de 30 artigos.
</div>

<div class="p-3 rounded-lg bg-green-500/10 border border-green-500/30">
<b>📚 RAG (Retrieval-Augmented Generation)</b> — antes de responder, o agente <b>busca</b> documentos relevantes e os <b>passa para o LLM</b> junto com a pergunta. É como dar a um aluno os livros abertos na hora da prova.
</div>

<div class="p-3 rounded-lg bg-amber-500/10 border border-amber-500/30">
<b>🧮 Embedding</b> — converter texto em uma lista de números que <b>capturam o significado</b>. Textos parecidos ficam com números parecidos. É a "impressão digital semântica" da frase.
</div>

<div class="p-3 rounded-lg bg-pink-500/10 border border-pink-500/30">
<b>🗄️ Vector DB</b> — banco de dados especializado em achar <b>textos com significado parecido</b> (não com palavras iguais). <i>Ex: Pinecone, Chroma, pgvector.</i>
</div>

<div class="p-3 rounded-lg bg-blue-500/10 border border-blue-500/30">
<b>🪟 Context window</b> — quantos tokens (~palavras) o LLM consegue "ver" de uma vez. Imagine como o <b>tamanho da mesa</b> onde ele lê seus papéis.
</div>

<div class="p-3 rounded-lg bg-purple-500/10 border border-purple-500/30">
<b>💾 Memória de longo prazo</b> — informações que o agente <b>guarda entre conversas</b>. Como o ChatGPT lembrar que você é vegetariano sem você dizer toda vez.
</div>

</div>

---

# 🧩 Onde você já viu isso

<div class="grid grid-cols-2 gap-3 text-sm">

<div class="p-3 rounded-lg bg-purple-500/10 border border-purple-500/30">
<b>🎯 Grounding em produto</b><br>
• <b>Perplexity</b> mostra os links das fontes embaixo de cada parágrafo — esse é o "grounding visível"<br>
• <b>Bing Chat</b> e <b>Google AI Overviews</b> citam as páginas usadas
</div>

<div class="p-3 rounded-lg bg-cyan-500/10 border border-cyan-500/30">
<b>📚 RAG em produto</b><br>
• <b>Notion AI Q&A</b> responde sobre <i>seus</i> documentos<br>
• <b>Glean</b> faz "Google" dentro da empresa (Slack, Drive, Jira)<br>
• <b>NotebookLM</b> do Google conversa com PDFs que você sobe
</div>

<div class="p-3 rounded-lg bg-green-500/10 border border-green-500/30">
<b>💾 Memória em produto</b><br>
• <b>ChatGPT</b> "Memory" lembra preferências entre sessões<br>
• <b>Claude Projects</b> mantém contexto compartilhado<br>
• <b>Cursor</b> indexa seu repositório e lembra a arquitetura
</div>

<div class="p-3 rounded-lg bg-amber-500/10 border border-amber-500/30">
<b>🪟 Context window — implicação prática</b><br>
• Quando o ChatGPT "esquece" o que você falou 50 mensagens atrás → contexto saturou<br>
• Por isso <b>Claude 200k</b> e <b>Gemini 1M</b> viraram diferencial competitivo
</div>

</div>

<div class="mt-3 p-3 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-xs">
🎯 <b>Insight</b>: todo agente que parece "inteligente sobre o seu negócio" está fazendo <b>RAG + grounding</b> por baixo. Não há mágica.
</div>

---

---
layout: center
class: text-center
---

# 🧠 Parte 1: O desafio do contexto

<div class="text-lg mt-6 opacity-90">
Um LLM lê <b>tudo</b> a cada chamada — e paga por cada token lido.<br>
Quando a conversa cresce, três coisas acontecem:
</div>

<div class="mt-6 grid grid-cols-3 gap-4 text-sm">
<div class="p-3 rounded bg-red-500/10 border border-red-500/30">💸 Custo explode</div>
<div class="p-3 rounded bg-red-500/10 border border-red-500/30">🐢 Latência sobe</div>
<div class="p-3 rounded bg-red-500/10 border border-red-500/30">🧠 Qualidade cai</div>
</div>

<div class="mt-6 text-sm opacity-60">
Vamos entender por quê — e as soluções que o mercado usa.
</div>

---

# 3.1 O problema da context window

A janela é grande, mas **não é infinita** — e cada token custa.

```mermaid {scale: 0.8}
flowchart LR
  subgraph CW["Context window (ex: 128k tokens)"]
    S[System prompt<br/>500]
    H[Histórico longo<br/>20.000]
    D[Documentos colados<br/>50.000]
    T[Tool definitions<br/>3.000]
    R[Buffer p/ resposta<br/>4.000]
  end
  X[❌ Estouro: 77.500 + nova msg = ?]
  CW -.-> X
  
  style X fill:#ef4444,color:#fff
```

<div class="mt-4 p-4 rounded-xl bg-amber-500/10 border border-amber-500/30">
⚠️ <b>Os 3 problemas da context window:</b><br>
1. <b>Limite duro</b> — passou, a API rejeita.<br>
2. <b>Custo</b> — você paga por TODOS os tokens, toda chamada.<br>
3. <b>"Lost in the middle"</b> — modelos esquecem info no <i>meio</i> do contexto longo (Liu et al., 2023).
</div>

---

# Lost in the Middle — o efeito U

```mermaid {scale: 0.7}
xychart-beta
  title "Acurácia vs posição da informação relevante no contexto"
  x-axis ["Início", "25%", "Meio", "75%", "Fim"]
  y-axis "Acurácia (%)" 0 --> 100
  line [85, 60, 45, 55, 80]
```

<div class="mt-4 text-sm">
Em contextos longos (>10k tokens), modelos prestam <b>mais atenção ao início e fim</b>, e tendem a "esquecer" o meio. Por isso colocar instruções importantes <b>no começo</b> e a pergunta <b>no fim</b> ajuda.
</div>

---

# 3.2 Estratégias de context management

<div class="grid grid-cols-2 gap-4 mt-4">

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<div class="font-bold mb-2">✂️ Truncamento (sliding window)</div>
<div class="text-sm">Mantém só as últimas N mensagens.<br>
<b>Prós:</b> simples. <b>Contras:</b> perde contexto antigo importante.</div>
</div>

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<div class="font-bold mb-2">📝 Sumarização</div>
<div class="text-sm">Periodicamente, comprime histórico antigo em resumo.<br>
<b>Prós:</b> mantém essência. <b>Contras:</b> +1 chamada LLM, perde detalhes.</div>
</div>

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<div class="font-bold mb-2">🔍 RAG (retrieval)</div>
<div class="text-sm">Busca só os trechos relevantes no contexto.<br>
<b>Prós:</b> escala para milhões de docs. <b>Contras:</b> qualidade depende do retriever.</div>
</div>

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<div class="font-bold mb-2">🗄️ Sub-agentes / handoffs</div>
<div class="text-sm">Sub-agente processa o contexto pesado e retorna síntese.<br>
<b>Prós:</b> isola contextos. <b>Contras:</b> orquestração complexa.</div>
</div>

</div>

<div class="mt-4 p-3 rounded bg-cyan-500/10 border border-cyan-500/30 text-sm">
🎯 <b>Padrão moderno (Claude/Cursor):</b> combinação de <b>sumarização automática</b> + <b>file system como memória externa</b> + <b>sub-agentes</b> para tarefas isoladas.
</div>

---

# Exemplo: sumarização automática

<div class="mb-3 p-3 rounded bg-sky-500/10 border border-sky-500/30 text-sm">
📖 <b>Em palavras:</b> antes de cada chamada ao LLM, você conta os tokens. Se passou do limite, <b>mantém as últimas 4 mensagens intactas</b> (contexto recente, mais importante) e <b>pede para o próprio LLM resumir o resto</b> em 200 palavras. Resultado: o histórico nunca cresce sem controle, mas as decisões importantes ficam preservadas no resumo.
</div>

```python
def manage_context(messages: list, max_tokens: int = 8000):
    """Se passar do limite, sumariza as mensagens antigas."""
    total = count_tokens(messages)
    if total < max_tokens:
        return messages
    
    # Mantém as últimas 4 mensagens, sumariza o resto
    keep = messages[-4:]
    to_summarize = messages[:-4]
    
    summary = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Resuma esta conversa em 200 palavras, "
                                           "preservando fatos importantes e decisões."},
            *to_summarize
        ]
    ).choices[0].message.content
    
    return [
        {"role": "system", "content": f"Resumo do histórico anterior:\n{summary}"},
        *keep
    ]
```

---

# 3.3 RAG — Retrieval-Augmented Generation

A ideia: **busque** trechos relevantes de uma base externa e **injete** no prompt.

```mermaid {scale: 0.7}
flowchart LR
  Q[Pergunta do usuário] --> E1[Embed pergunta]
  E1 --> S[🔍 Busca semântica<br/>no Vector DB]
  
  subgraph DB["Vector DB"]
    D1[chunk 1 + vetor]
    D2[chunk 2 + vetor]
    D3[chunk N + vetor]
  end
  
  S --> DB
  DB --> TOP[Top-K chunks relevantes]
  TOP --> P["Prompt: contexto + pergunta"]
  P --> L[🧠 LLM]
  L --> R[Resposta fundamentada]
  
  style L fill:#7c5cff,color:#fff
  style R fill:#22c55e,color:#000
  style S fill:#2dd4bf,color:#000
```

---

# RAG — anatomia da indexação (offline)

```mermaid {scale: 0.7}
flowchart LR
  D[📄 Documentos<br/>PDFs, MD, HTML] --> C[🔪 Chunking<br/>~500 tokens]
  C --> E[🧮 Embedding<br/>text-embedding-3-small]
  E --> V[💾 Vector DB<br/>Chroma/Qdrant/pgvector]
  
  style V fill:#7c5cff,color:#fff
```

<div class="mt-4 grid grid-cols-3 gap-4 text-sm">

<div class="p-3 rounded bg-white/5">
<b>1. Loaders</b><br>
PyPDF, BeautifulSoup, Unstructured, Markdown loader.
</div>

<div class="p-3 rounded bg-white/5">
<b>2. Splitters</b><br>
RecursiveCharacterTextSplitter, SemanticChunker, by-header (para Markdown).
</div>

<div class="p-3 rounded bg-white/5">
<b>3. Embeddings</b><br>
OpenAI <code>text-embedding-3</code>, Cohere, BGE, ou local (sentence-transformers).
</div>

</div>

---

# Hands-on: RAG completo com Chroma

```python
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1) Indexação (offline)
docs = TextLoader("manual.txt").load()
chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(docs)
vstore = Chroma.from_documents(chunks, OpenAIEmbeddings(model="text-embedding-3-small"))

# 2) Retriever
retriever = vstore.as_retriever(search_kwargs={"k": 4})

# 3) Chain de QA
prompt = ChatPromptTemplate.from_template(
    "Responda baseado APENAS no contexto:\n\n{context}\n\nPergunta: {input}"
)
combine = create_stuff_documents_chain(ChatOpenAI(model="gpt-4o-mini"), prompt)
chain = create_retrieval_chain(retriever, combine)

# 4) Query
print(chain.invoke({"input": "Como configuro o produto?"})["answer"])
```

---

# Advanced RAG — quando o básico não basta

RAG ingênuo (embeddings + top-K) tem **muitos pontos de falha**. Em produção, usa-se um pipeline:

```mermaid {scale: 0.65}
flowchart LR
  Q[Pergunta] --> QR[1. Query Rewriting]
  QR --> MQ[2. Multi-Query]
  MQ --> HY[3. HyDE]
  HY --> R[4. Retrieval híbrido]
  R --> RR[5. Reranking]
  RR --> CTX[6. Context compression]
  CTX --> G[LLM]
  
  style QR fill:#7c5cff,color:#fff
  style MQ fill:#7c5cff,color:#fff
  style HY fill:#7c5cff,color:#fff
  style RR fill:#f59e0b,color:#000
  style CTX fill:#2dd4bf,color:#000
```

<div class="mt-3 text-sm">
Cada estágio recupera <b>+5-15% de qualidade</b> em benchmarks como BEIR, MS MARCO.
</div>

---

# Padrão 1 · Query Rewriting

A pergunta do usuário **raramente** é uma boa query de busca.

<div class="mt-4 grid grid-cols-2 gap-4 text-sm">

<div class="p-3 rounded bg-red-500/10 border border-red-500/30">
<b>❌ Pergunta do usuário</b><br>
<i>"e o problema que falei ontem, ainda tá acontecendo?"</i><br>
→ vetor sem contexto, retrieval inútil
</div>

<div class="p-3 rounded bg-green-500/10 border border-green-500/30">
<b>✅ Query reescrita pelo LLM</b><br>
<i>"erro 504 timeout no endpoint /api/login mencionado em 03/11/2025"</i><br>
→ vetor rico, retrieval certeiro
</div>

</div>

```python
def reescrever_query(historico, pergunta):
    return llm.invoke(f"""
    Histórico: {historico}
    Pergunta atual: {pergunta}
    Reescreva como query de busca standalone, com todos os termos técnicos.
    """)
```

---

# Padrão 2 · Multi-Query & HyDE

<div class="grid grid-cols-2 gap-4 mt-4">

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<b>🔁 Multi-Query</b><br>
Gere <b>N variações</b> da pergunta e busque com todas.

```python
queries = llm.invoke(f"""
Gere 4 reformulações da pergunta:
{pergunta}
""").split("\n")

docs = []
for q in queries:
    docs += vectordb.search(q, k=5)
docs = dedupe(docs)
```
<br>
Melhora <b>recall</b> 20-40%.
</div>

<div class="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/30">
<b>🎭 HyDE</b> — <i>Hypothetical Document Embeddings</i>

```python
# 1) Pede ao LLM uma resposta hipotética
hipo = llm.invoke(f"""
Escreva um trecho que responderia:
{pergunta}
""")

# 2) Usa o embedding DA RESPOSTA
docs = vectordb.search(hipo, k=5)
```
<br>
Funciona porque "resposta-pra-resposta" está mais perto no espaço vetorial que "pergunta-pra-resposta".
</div>

</div>

---

# Padrão 3 · Parent-Child Chunks & Agentic RAG

<div class="grid grid-cols-2 gap-4 mt-4">

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<b>👨‍👦 Parent-Child Chunks</b><br>
Indexe pedaços <b>pequenos</b> (alta precisão), mas devolva o pedaço <b>grande</b> ao LLM (contexto rico).

```mermaid {scale: 0.55}
flowchart LR
  Q --> S[chunks 200 tokens] --> P[parent 2000 tokens] --> LLM
```
</div>

<div class="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/30">
<b>🤖 Agentic RAG</b><br>
O LLM <b>decide</b> se precisa buscar, em qual fonte, e refina a busca iterativamente.

```mermaid {scale: 0.55}
flowchart LR
  Q --> A[Agent]
  A --> T1[search docs]
  A --> T2[search code]
  A --> T3[search web]
  T1 --> A
  T2 --> A
  T3 --> A
  A --> R[Resposta]
```
</div>

</div>

<div class="mt-3 p-3 rounded bg-amber-500/10 border border-amber-500/30 text-sm">
🎯 Agentic RAG é o que <b>Perplexity</b>, <b>ChatGPT Search</b>, <b>Cursor @docs</b> usam por baixo.
</div>

---

# 3.4 Vector DBs comparativo

| DB | Quando usar | Open source | Notas |
|---|---|---|---|
| **Chroma** | Dev local, protótipos | ✅ | Mais fácil de começar |
| **Qdrant** | Produção, escala média | ✅ | Rust, rápido, ótimo filtro híbrido |
| **pgvector** | Já uso Postgres | ✅ | Extensão PG — uma coisa a menos pra operar |
| **Pinecone** | SaaS gerenciado | ❌ | Caro mas zero ops |
| **Weaviate** | Multi-modal, GraphQL | ✅ | Bom para casos complexos |
| **Milvus / Zilliz** | Bilhões de vetores | ✅/❌ | Casos extremos |
| **LanceDB** | Embedded + cloud | ✅ | Formato em disco, S3-friendly |

<div class="mt-4 p-3 rounded bg-cyan-500/10 border border-cyan-500/30 text-sm">
💡 <b>Recomendação 2025:</b> comece com Chroma local. Quando for pra produção, considere <b>pgvector</b> (se já usa Postgres) ou <b>Qdrant</b>.
</div>

---

# Search híbrido — porque puro vetor não basta

```mermaid {scale: 0.75}
flowchart LR
  Q[Pergunta] --> A[🧮 Busca semântica<br/>embeddings]
  Q --> B[🔤 Busca lexical<br/>BM25 / full-text]
  A --> M[🔀 Merge + rerank]
  B --> M
  M --> R[Top-K final]
  
  style M fill:#7c5cff,color:#fff
```

<div class="mt-4 grid grid-cols-2 gap-4 text-sm">

<div class="p-3 rounded bg-white/5">
<b>Semântico</b> entende sinônimos, conceitos.<br>
Falha em <b>termos exatos</b>, números, códigos.
</div>

<div class="p-3 rounded bg-white/5">
<b>Lexical (BM25)</b> acerta <b>termos exatos</b>, IDs.<br>
Não entende sinônimos.
</div>

</div>

<div class="mt-4 p-3 rounded bg-amber-500/10 border border-amber-500/30 text-sm">
🥇 <b>Reranker:</b> depois do retrieval, passe os top-20 por um modelo cross-encoder (Cohere Rerank, BGE-reranker) que reorganiza por relevância real. Melhora qualidade em 10-30%.
</div>

---
layout: section
---

# 🎯 Grounding

A base de tudo. Sem isso, agente é gerador de ficção.

---

# O que é Grounding?

<div class="mt-4 p-5 rounded-xl bg-cyan-500/10 border-2 border-cyan-500/40">
<div class="text-lg text-center">
<b>Grounding</b> = ancorar cada afirmação do modelo em uma <b>fonte verificável</b>.<br>
Toda resposta precisa responder: <b>"de onde isso veio?"</b>
</div>
</div>

<div class="mt-6 grid grid-cols-2 gap-4 text-sm">

<div class="p-4 rounded bg-red-500/10 border border-red-500/30">
<b>❌ Sem grounding</b><br>
<i>"O contrato exige aviso prévio de 60 dias."</i><br>
→ Verdade? Inventado? Impossível auditar.
</div>

<div class="p-4 rounded bg-green-500/10 border border-green-500/30">
<b>✅ Com grounding</b><br>
<i>"O contrato exige 60 dias de aviso prévio <b>[Cláusula 14.3, contrato_v3.pdf]</b>."</i><br>
→ Auditável, rastreável, defensável.
</div>

</div>

<div class="mt-4 p-3 rounded bg-purple-500/10 border border-purple-500/30 text-xs">
📚 <b>Leitura essencial:</b> Rashkin et al. (2023) — <i>"Measuring Attribution in NLG Models"</i> formaliza o conceito <b>AIS</b> (<i>Attributable to Identified Sources</i>). Bohnet et al. (2022) — <i>"Attributed Question Answering"</i> propõe o benchmark AQA. Em jurídico, médico e financeiro, grounding deixou de ser opcional — virou <b>compliance</b>.
</div>

---

# Por que grounding falha

```mermaid {scale: 0.7}
flowchart TB
  P[Pergunta] --> R[Retrieval]
  R --> C[Contexto<br/>100 chunks]
  C --> L[LLM gera resposta]
  L --> F1[❌ Cita chunk errado]
  L --> F2[❌ Mistura fatos<br/>de fontes diferentes]
  L --> F3[❌ Inventa citação]
  L --> F4[❌ Ignora contexto<br/>usa conhecimento interno]
  
  style F1 fill:#ef4444,color:#fff
  style F2 fill:#ef4444,color:#fff
  style F3 fill:#ef4444,color:#fff
  style F4 fill:#ef4444,color:#fff
```

<div class="mt-3 text-sm">
Mesmo com RAG, a <b>"grounding rate"</b> (% de afirmações ancoradas) raramente passa de 70-80% sem técnicas dedicadas.
</div>

---

# Técnicas de grounding (1/2)

<div class="grid grid-cols-1 gap-3 text-sm mt-3">

<div class="p-3 rounded bg-purple-500/10 border border-purple-500/30">
<b>1. 🆔 Inline citations com IDs únicos</b><br>
Cada chunk recebe <code>[doc_id:chunk_id]</code>. Prompt pede citação após cada frase.
</div>

<div class="p-3 rounded bg-purple-500/10 border border-purple-500/30">
<b>2. 📋 "According to X" prompting</b><br>
Forçar prefixo "Segundo [fonte X]…" reduz alucinação em 20% (Weller et al., 2023).
</div>

<div class="p-3 rounded bg-purple-500/10 border border-purple-500/30">
<b>3. 🚪 Refusal explícito</b><br>
Prompt: <i>"Se o contexto não contém a resposta, responda 'Não encontrei nos documentos fornecidos.'"</i>
</div>

<div class="p-3 rounded bg-purple-500/10 border border-purple-500/30">
<b>4. 🔍 Contextual grounding check</b><br>
Após gerar, um <b>segundo LLM</b> verifica: "Cada afirmação é suportada pelo contexto?"
</div>

</div>

---

# Técnicas de grounding (2/2) — em código

<div class="mb-3 p-3 rounded bg-sky-500/10 border border-sky-500/30 text-sm">
📖 <b>Em palavras:</b> duas camadas. <b>(1)</b> No prompt, você manda o LLM responder <i>só</i> com base nos documentos, citar a fonte de cada afirmação e admitir quando não sabe. <b>(2)</b> Depois, um <b>segundo passo de verificação</b> pega a resposta e checa frase por frase se está apoiada no contexto — separando o que é fato citado do que é "alucinação".
</div>

```python
SYSTEM = """Responda APENAS com base nos documentos abaixo.
Para CADA afirmação, adicione [doc_id] da fonte.
Se não souber, responda exatamente: "Não encontrei nos documentos."
NÃO use conhecimento externo."""

contexto = "\n\n".join([
    f"[doc_{d.id}] {d.content}" for d in docs_retrieved
])

resposta = llm.invoke(f"{SYSTEM}\n\n{contexto}\n\nPergunta: {q}")

# Verificação automática
verificacao = llm.invoke(f"""
Resposta: {resposta}
Contexto disponível: {contexto}

Para cada afirmação na resposta, marque:
- SUPORTADA (existe no contexto)
- NÃO_SUPORTADA (alucinação)
- PARCIAL (parcialmente apoiada)

JSON: {{"afirmacoes": [{{"texto": ..., "status": ...}}]}}
""")
```

<div class="mt-3 p-3 rounded bg-cyan-500/10 border border-cyan-500/30 text-sm">
🎯 Métricas a monitorar: <b>Groundedness</b> (% afirmações apoiadas), <b>Citation accuracy</b> (citações apontam pra chunk certo), <b>Answer relevance</b>.
</div>

---

# Frameworks que ajudam com grounding

| Ferramenta | O que faz |
|---|---|
| **RAGAS** | Métricas automáticas: faithfulness, answer_relevancy, context_precision |
| **TruLens** | Tracing + avaliação de grounding em produção |
| **Vertex AI Grounding** | Google força citações em URL real |
| **Bing Grounding (Azure)** | Tool nativo para citar web |
| **Anthropic Citations API** | Citações estruturadas garantidas pelo modelo (2024) |
| **DeepEval** | Suite de testes incluindo hallucination + faithfulness |

<div class="mt-4 p-3 rounded bg-amber-500/10 border border-amber-500/30 text-sm">
⚠️ <b>"Faithfulness"</b> ≠ <b>"Correctness"</b>. Resposta pode ser <b>fiel</b> ao contexto mas o <b>contexto</b> estar errado. Garantir grounding é necessário, não suficiente.
</div>

---
layout: section
---

# 🧬 Synthesis

Combinar múltiplas fontes com coerência. O passo que separa um chatbot de um agente analítico.

---

# O problema da Synthesis

Recuperei 20 chunks de 5 fontes. **E agora?**

```mermaid {scale: 0.7}
flowchart TB
  D1[📄 Doc A diz: 'X é 30%']
  D2[📄 Doc B diz: 'X é 40%']
  D3[📄 Doc C diz: 'X cresceu em 2024']
  D4[📄 Doc D contradiz Doc A]
  D5[📄 Doc E é tangencial]
  
  D1 & D2 & D3 & D4 & D5 --> S[🧬 Synthesizer]
  S --> O[Resposta única<br/>coerente<br/>citando todos<br/>sinalizando conflitos]
  
  style S fill:#7c5cff,color:#fff
```

<div class="mt-3 text-sm">
Synthesis ≠ Retrieval. É um <b>passo de raciocínio</b> que requer: dedup, resolução de conflito, hierarquização, citação atribuída.
</div>

---

# Padrão 1 · Map-Reduce sobre documentos

Para muitos docs ou docs grandes — não cabem todos no contexto.

```mermaid {scale: 0.7}
flowchart TB
  Q[Pergunta] --> D1[Doc 1] & D2[Doc 2] & D3[Doc N]
  D1 --> M1[🔎 Map: extrai info relevante]
  D2 --> M2[🔎 Map]
  D3 --> M3[🔎 Map]
  M1 & M2 & M3 --> R[🧬 Reduce: combina<br/>resolve conflitos<br/>resposta final]
  
  style R fill:#7c5cff,color:#fff
```

<div class="mt-3 text-sm">
<b>Map:</b> rodar em paralelo, barato (modelo menor). <b>Reduce:</b> modelo maior, com instruções de citação.<br>
Variante: <b>Refine</b> — atualiza resposta incrementalmente conforme lê cada doc.
</div>

---

# Padrão 2 · Resolução de conflitos

Quando fontes discordam, o agente **não pode** simplesmente escolher uma.

```python
SYNTH_PROMPT = """Sintetize a resposta usando os trechos abaixo.

REGRAS:
1. Se fontes CONCORDAM, afirme com confiança e cite todas.
2. Se fontes DISCORDAM, apresente as visões DIVERGENTES explicitamente:
   "Segundo [A], X = 30%. Já [B] reporta X = 40%."
3. Se a divergência tem causa identificável (data, escopo), explique:
   "A diferença pode se dever a [A] ser de 2023 e [B] de 2024."
4. NUNCA invente uma 'média' entre fontes contraditórias.
5. Cite com [doc_id] após cada afirmação.

Trechos:
{contexto}

Pergunta: {pergunta}
"""
```

<div class="mt-3 p-3 rounded bg-amber-500/10 border border-amber-500/30 text-sm">
⚠️ <b>Anti-padrão clássico:</b> "média de alucinações" — pegar 3 números diferentes e dar a média. Pior que escolher um.
</div>

---

# Padrão 3 · Hierarchical Summarization

Para corpora gigantes (livros, repositórios, milhares de tickets):

```mermaid {scale: 0.6}
flowchart TB
  C1[📄] & C2[📄] & C3[📄] & C4[📄] & C5[📄] & C6[📄] & C7[📄] & C8[📄] --> S1[Sumário lvl 1]
  C9[📄] & C10[📄] & C11[📄] & C12[📄] --> S2[Sumário lvl 1]
  S1 --> S3[Sumário lvl 2]
  S2 --> S3
  S3 --> Q[💬 Resposta final<br/>citando origens]
  
  style S3 fill:#7c5cff,color:#fff
```

<div class="mt-3 text-sm">
Cada nível mantém <b>ponteiros</b> para o nível anterior — assim a resposta final ainda pode citar chunks específicos.<br>
Usado em: <b>Claude Projects</b>, <b>NotebookLM</b>, <b>Cursor codebase indexing</b>.
</div>

---

# Synthesis na prática · LangChain

```python
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# 1) Map-reduce nativo
from langchain.chains.summarize import load_summarize_chain
chain = load_summarize_chain(llm, chain_type="map_reduce")

# 2) Refine — resposta evolui doc a doc
chain_refine = load_summarize_chain(llm, chain_type="refine")

# 3) Stuff — joga tudo no contexto (só se cabe)
chain_stuff = load_summarize_chain(llm, chain_type="stuff")
```

| Chain type | Quando usar | Pro | Contra |
|---|---|---|---|
| **Stuff** | Cabem todos os docs | Simples | Limitado por context window |
| **Map-Reduce** | Muitos docs | Paralelizável | Perde contexto cross-doc |
| **Refine** | Docs sequenciais | Mantém contexto | Sequencial, sem paralelizar |

---

# 🧪 Context Engineering — o novo nome do jogo

<div class="mt-4 p-5 rounded-xl bg-cyan-500/10 border-2 border-cyan-500/40 text-center">
<b>Prompt engineering</b> → <b>Context engineering</b>
</div>

<div class="mt-4 text-sm">
Em 2025, a discussão amadureceu. Não é só "escreva o prompt mágico". É <b>desenhar todo o contexto</b> que o LLM vê:
</div>

<div class="mt-3 grid grid-cols-2 gap-3 text-sm">

<div class="p-3 rounded bg-purple-500/10 border border-purple-500/30">
<b>📦 O que entra na janela</b><br>
System, exemplos, retrievals, memória, tool results, histórico — em qual ordem?
</div>

<div class="p-3 rounded bg-purple-500/10 border border-purple-500/30">
<b>🗑️ O que sai</b><br>
Compressão, summarization, eviction policies, "lost in the middle" mitigation
</div>

<div class="p-3 rounded bg-purple-500/10 border border-purple-500/30">
<b>🎚️ Quanto e quando</b><br>
Dynamic context: só recupera quando precisa, gasta tokens onde importa
</div>

<div class="p-3 rounded bg-purple-500/10 border border-purple-500/30">
<b>🔁 Como evolui</b><br>
Como contexto muda turn-a-turn — não é estático
</div>

</div>

<div class="mt-3 p-3 rounded bg-amber-500/10 border border-amber-500/30 text-sm">
📚 Termos atuais: <b>Context engineering</b> (Karpathy), <b>Context rot</b> (Anthropic), <b>Context economy</b>.
</div>

---

# 💰 Prompt Caching — 90% de economia

Anthropic (ago/2024), OpenAI (out/2024), Gemini (mai/2024) — todos lançaram cache de prompt.

<div class="mt-4 p-4 rounded-xl bg-green-500/10 border-2 border-green-500/40">
<b>Como funciona:</b> partes <b>estáveis</b> do prompt (system, docs, exemplos) são "congeladas" no servidor. Próximas chamadas reusam, pagando ~10% do custo desses tokens.
</div>

```python
# Anthropic — usando cache_control
response = client.messages.create(
    model="claude-sonnet-4-5",
    system=[
        {"type": "text", "text": "Você é um assistente legal..."},
        {
            "type": "text",
            "text": MEGA_DOCUMENTO_50K_TOKENS,  # ← caching
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": pergunta}]
)
```

<div class="mt-3 grid grid-cols-3 gap-2 text-sm">
<div class="p-2 rounded bg-white/5"><b>1ª chamada</b><br>100% do custo (escreve cache)</div>
<div class="p-2 rounded bg-white/5"><b>Subsequentes</b><br>10% do custo do trecho cacheado</div>
<div class="p-2 rounded bg-white/5"><b>TTL típico</b><br>5 min (ephemeral) — basta um chat ativo</div>
</div>

<div class="mt-3 p-3 rounded bg-amber-500/10 border border-amber-500/30 text-sm">
🎯 <b>Padrão:</b> coloque conteúdo <b>estável no início</b> (system + docs), <b>dinâmico no fim</b> (mensagem do user). Inverter quebra o cache.
</div>

---

# 3.5 Memória — curto vs longo prazo

```mermaid {scale: 0.7}
flowchart TB
  A[🤖 Agente] --> S[💬 Short-term<br/>histórico da sessão<br/>na context window]
  A --> L[💾 Long-term<br/>persistente entre sessões]
  
  L --> L1[Episódica<br/>"o que aconteceu"]
  L --> L2[Semântica<br/>"o que sei"]
  L --> L3[Procedural<br/>"como faço"]
  
  L1 --> VDB[(Vector DB<br/>resumos de sessões)]
  L2 --> KG[(Knowledge graph<br/>ou vector DB)]
  L3 --> CODE[(Skills/Tools<br/>código reutilizável)]
  
  style A fill:#7c5cff,color:#fff
  style VDB fill:#2dd4bf,color:#000
  style KG fill:#2dd4bf,color:#000
  style CODE fill:#2dd4bf,color:#000
```

---

# Tipos de memória de longo prazo

<div class="grid grid-cols-3 gap-4 mt-6">

<div class="p-4 rounded-xl bg-white/5 border border-white/10">
<div class="text-2xl mb-2">📖</div>
<b>Episódica</b><br>
<span class="text-sm opacity-80">"O que aconteceu" — eventos, conversas passadas, ações tomadas.</span><br><br>
<i class="text-xs">Ex: ChatGPT memory, Claude Projects.</i>
</div>

<div class="p-4 rounded-xl bg-white/5 border border-white/10">
<div class="text-2xl mb-2">🧠</div>
<b>Semântica</b><br>
<span class="text-sm opacity-80">"O que sei sobre o mundo" — fatos, preferências do usuário, contexto persistente.</span><br><br>
<i class="text-xs">Ex: "usuário prefere respostas curtas".</i>
</div>

<div class="p-4 rounded-xl bg-white/5 border border-white/10">
<div class="text-2xl mb-2">⚙️</div>
<b>Procedural</b><br>
<span class="text-sm opacity-80">"Como fazer" — habilidades, ferramentas, scripts aprendidos.</span><br><br>
<i class="text-xs">Ex: Skills do Claude, comandos custom.</i>
</div>

</div>

---

# Frameworks de memória persistente

<div class="grid grid-cols-2 gap-4 mt-6">

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<b>mem0</b><br>
<span class="text-sm">Layer de memória plug-and-play. Detecta automaticamente o que vale a pena lembrar.</span><br>
<code class="text-xs mt-2 block">pip install mem0ai</code>
</div>

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<b>Zep</b><br>
<span class="text-sm">Open source. Knowledge graph temporal + vector. Foco em produção.</span><br>
<code class="text-xs mt-2 block">getzep.com</code>
</div>

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<b>LangGraph + checkpoints</b><br>
<span class="text-sm">Persiste o estado completo do agente em Postgres/Redis. Você controla tudo.</span>
</div>

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<b>Letta (ex-MemGPT)</b><br>
<span class="text-sm">Papers seminais sobre "OS para agentes" com memória hierárquica.</span>
</div>

</div>

---

# Exemplo: memória com mem0

<div class="mb-3 p-3 rounded bg-sky-500/10 border border-sky-500/30 text-sm">
📖 <b>Em palavras:</b> o mem0 funciona como um <b>caderno do usuário</b>. Você <code>add()</code> fatos que o agente aprende ("prefere PT-BR", "trabalha com Python"). Na próxima conversa — mesmo dias depois — você faz <code>search()</code> com a pergunta atual e ele te devolve só as memórias <i>relevantes</i> pra injetar no prompt. É como um CRM, mas pra LLM.
</div>

```python
from mem0 import Memory

m = Memory()
user_id = "alan"

# Salva durante interações
m.add("Prefiro respostas em português, tom técnico", user_id=user_id)
m.add("Trabalho com Python e TypeScript", user_id=user_id)
m.add("Não gosto de emojis em código", user_id=user_id)

# Em outra sessão, recupera relevantes
def chat(pergunta: str):
    memorias = m.search(pergunta, user_id=user_id, limit=5)
    contexto = "\n".join(m["memory"] for m in memorias["results"])
    
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Sobre o usuário:\n{contexto}"},
            {"role": "user", "content": pergunta}
        ]
    ).choices[0].message.content

print(chat("Me ajude a escrever uma função"))
# → vai responder em português, técnico, sem emojis
```

---

---
layout: center
class: text-center
---

# 🔧 Parte 2: Habilidades e colaboração

<div class="text-lg mt-6 opacity-90">
O agente já tem <b>memória</b> e <b>conhecimento externo</b> (RAG).<br>
Agora vamos dar a ele <b>habilidades permanentes</b> — e a capacidade de <b>trabalhar em equipe</b>.
</div>

<div class="mt-6 text-sm opacity-60">
Skills, MCP, e padrões multi-agente.
</div>

---

# 3.6 Skills — capacidades reutilizáveis

📅 Lançado pela Anthropic em **outubro/2025**.

**Conceito:** uma "skill" é uma **pasta** com:
- Um `SKILL.md` descrevendo o que faz e quando usar
- Scripts auxiliares (Python, bash)
- Templates, dados, recursos

O agente **descobre** skills disponíveis e **carrega só o necessário** quando relevante.

```
~/.claude/skills/
├── pdf-extractor/
│   ├── SKILL.md          ← "use isto para extrair texto de PDFs"
│   └── extract.py
├── jira-integration/
│   ├── SKILL.md
│   └── jira_client.py
└── excel-formatter/
    ├── SKILL.md
    └── format.py
```

---

# Skills vs Tools — qual a diferença?

<div class="grid grid-cols-2 gap-4 mt-6">

<div class="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/30">
<div class="font-bold mb-2">🛠️ Tool (function calling)</div>
<ul class="text-sm">
<li>Sempre presente no contexto</li>
<li>Schema JSON estático</li>
<li>1 função = 1 tool</li>
<li>Consome tokens mesmo se não usada</li>
</ul>
</div>

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<div class="font-bold mb-2">🎓 Skill</div>
<ul class="text-sm">
<li>Carregada <b>sob demanda</b></li>
<li>Pode incluir docs, exemplos, scripts</li>
<li>1 skill = competência inteira</li>
<li><b>Quase zero overhead</b> de contexto</li>
</ul>
</div>

</div>

<div class="mt-6 p-4 rounded-xl bg-amber-500/10 border border-amber-500/30">
💡 <b>Analogia:</b> tools são como funções na biblioteca padrão (sempre lá). Skills são como pacotes <code>pip install</code> que você instala quando precisa.
</div>

---

# 3.7 MCP — Model Context Protocol

📅 Lançado pela **Anthropic em novembro/2024**. Adotado por OpenAI, Google e a maioria dos frameworks em 2025.

<div class="mt-6 p-5 rounded-xl bg-cyan-500/10 border-2 border-cyan-500/40 text-center">
<div class="text-xl">
MCP é o <b>"USB-C"</b> dos agentes:<br>
um protocolo padrão para conectar LLMs a <b>qualquer</b> fonte de dados ou ferramenta.
</div>
</div>

<div class="mt-6 grid grid-cols-2 gap-4 text-sm">

<div class="p-3 rounded bg-red-500/10 border border-red-500/30">
<b>Antes do MCP:</b><br>
Cada framework (LangChain, LlamaIndex, CrewAI…) tinha sua API de tools.<br>
Integrar com Slack? 5 implementações diferentes.
</div>

<div class="p-3 rounded bg-green-500/10 border border-green-500/30">
<b>Com MCP:</b><br>
1 servidor MCP do Slack → funciona em <b>todos</b> os agentes/clientes que falam MCP.<br>
Hoje: Claude Desktop, Cursor, VS Code, Cline, Continue…
</div>

</div>

---

# MCP — arquitetura

```mermaid {scale: 0.7}
flowchart LR
  subgraph Client["🤖 MCP Client (host)"]
    AG[Claude Desktop / Cursor / Seu app]
  end
  
  subgraph Servers["🔌 MCP Servers"]
    S1[Filesystem]
    S2[GitHub]
    S3[Postgres]
    S4[Slack]
    S5[Custom seu]
  end
  
  AG <--> S1
  AG <--> S2
  AG <--> S3
  AG <--> S4
  AG <--> S5
  
  style AG fill:#7c5cff,color:#fff
  style S1 fill:#2dd4bf,color:#000
  style S2 fill:#2dd4bf,color:#000
  style S3 fill:#2dd4bf,color:#000
  style S4 fill:#2dd4bf,color:#000
  style S5 fill:#f59e0b,color:#000
```

<div class="mt-4 text-sm">
Comunicação por <b>JSON-RPC</b> (stdio local ou HTTP/SSE remoto). Cada servidor expõe:
<b>tools</b> (ações), <b>resources</b> (dados), <b>prompts</b> (templates).
</div>

---

# MCP em ação — servidor mínimo (Python)

```python
# servidor MCP que expõe uma tool "soma"
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("minha-calculadora")

@mcp.tool()
def somar(a: int, b: int) -> int:
    """Soma dois números inteiros."""
    return a + b

@mcp.tool()
def multiplicar(a: int, b: int) -> int:
    """Multiplica dois números inteiros."""
    return a * b

if __name__ == "__main__":
    mcp.run()
```

<div class="mt-4 p-3 rounded bg-cyan-500/10 border border-cyan-500/30 text-sm">
Pronto. Esse servidor funciona em <b>Claude Desktop</b>, <b>Cursor</b>, <b>VS Code Copilot</b>, ou qualquer cliente MCP, sem mudar uma linha. <b>Esse é o ponto</b>.
</div>

---

# Ecossistema MCP — alguns servidores prontos

<div class="grid grid-cols-3 gap-3 text-sm">

<div class="p-3 rounded bg-white/5"><b>filesystem</b> · ler/escrever arquivos</div>
<div class="p-3 rounded bg-white/5"><b>github</b> · issues, PRs, código</div>
<div class="p-3 rounded bg-white/5"><b>postgres / sqlite</b> · queries SQL</div>
<div class="p-3 rounded bg-white/5"><b>slack</b> · mensagens, canais</div>
<div class="p-3 rounded bg-white/5"><b>brave-search</b> · busca web</div>
<div class="p-3 rounded bg-white/5"><b>puppeteer</b> · navegação automatizada</div>
<div class="p-3 rounded bg-white/5"><b>memory</b> · KV store persistente</div>
<div class="p-3 rounded bg-white/5"><b>fetch</b> · HTTP requests</div>
<div class="p-3 rounded bg-white/5"><b>google-drive</b> · arquivos GDrive</div>

</div>

<div class="mt-4 text-center text-sm opacity-70">
Lista oficial: <a href="https://github.com/modelcontextprotocol/servers">github.com/modelcontextprotocol/servers</a> — centenas de servidores comunitários.
</div>

---

# 3.8 Padrões multi-agente

```mermaid {scale: 0.65}
flowchart TB
  subgraph SUP["1. Supervisor / Orchestrator"]
    O[Supervisor] --> A1[Agente A]
    O --> A2[Agente B]
    O --> A3[Agente C]
  end
  
  subgraph HAN["2. Handoff / Swarm"]
    H1[Agente 1] -.passa bola.-> H2[Agente 2]
    H2 -.-> H3[Agente 3]
  end
  
  subgraph HIE["3. Hierárquico"]
    HC[CEO] --> HM1[Manager 1]
    HC --> HM2[Manager 2]
    HM1 --> HW1[Worker]
    HM1 --> HW2[Worker]
  end
  
  style O fill:#7c5cff,color:#fff
  style HC fill:#7c5cff,color:#fff
```

---

# Quando usar multi-agente?

<div class="grid grid-cols-2 gap-4 mt-6">

<div class="p-4 rounded-xl bg-green-500/10 border border-green-500/30">
<div class="font-bold mb-2 text-green-300">✅ Use quando</div>
<ul class="text-sm">
<li>Tarefa tem fases muito distintas (pesquisa → escrita → revisão)</li>
<li>Cada fase precisa de prompt/contexto diferente</li>
<li>Você quer especialistas com tools diferentes</li>
<li>Você precisa de paralelismo real (vários sub-agentes)</li>
</ul>
</div>

<div class="p-4 rounded-xl bg-red-500/10 border border-red-500/30">
<div class="font-bold mb-2 text-red-300">❌ Evite quando</div>
<ul class="text-sm">
<li>Um único agente bem-prompted resolve</li>
<li>Latência é crítica (cada handoff custa)</li>
<li>Custo precisa ser previsível (chamadas se multiplicam)</li>
<li>Você ainda não mediu se vale</li>
</ul>
</div>

</div>

<div class="mt-4 p-3 rounded bg-amber-500/10 border border-amber-500/30 text-sm">
🎯 <b>Conselho da Anthropic:</b> "Single-agent com bom contexto bate multi-agent ruim 9 vezes em 10." Só vá multi quando a tarefa <i>realmente</i> exigir.
</div>

---

# Frameworks multi-agente

<div class="grid grid-cols-2 gap-4 mt-6">

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<b>CrewAI</b><br>
<span class="text-sm">"Crew" de agentes com roles (researcher, writer, reviewer). Sintaxe declarativa.</span>
</div>

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<b>AutoGen (Microsoft)</b><br>
<span class="text-sm">Agentes conversam entre si. Forte em geração de código colaborativa.</span>
</div>

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<b>LangGraph (multi-agent)</b><br>
<span class="text-sm">Cada nó do grafo = 1 agente. Controle total, padrão moderno.</span>
</div>

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<b>OpenAI Swarm / Agents SDK</b><br>
<span class="text-sm">Handoffs leves entre agentes. Lançado em 2024.</span>
</div>

</div>

---

# Exemplo: Crew com CrewAI

<div class="mb-3 p-3 rounded bg-sky-500/10 border border-sky-500/30 text-sm">
📖 <b>Em palavras:</b> imagine uma <b>equipe de funcionários</b>. Cada <code>Agent</code> tem um cargo (role), um objetivo e um "currículo" (backstory) — isso vira parte do prompt dele. Cada <code>Task</code> é uma entrega esperada, atribuída a um agente. O <code>Crew</code> orquestra: o pesquisador entrega, o escritor pega o resultado dele como contexto e produz o artigo. <b>Divisão de trabalho automatizada.</b>
</div>

```python
from crewai import Agent, Task, Crew

pesquisador = Agent(
    role="Pesquisador",
    goal="Encontrar informações precisas sobre o tema",
    backstory="Você é um analista meticuloso.",
    tools=[busca_web, leitor_pdf],
)

escritor = Agent(
    role="Escritor técnico",
    goal="Transformar pesquisa em artigo claro",
    backstory="Você escreve para devs juniores.",
)

t1 = Task(description="Pesquise tudo sobre {tema}", agent=pesquisador)
t2 = Task(description="Escreva artigo de 500 palavras baseado na pesquisa",
          agent=escritor, context=[t1])

crew = Crew(agents=[pesquisador, escritor], tasks=[t1, t2])
print(crew.kickoff(inputs={"tema": "agentes de IA"}))
```

---

# 3.9 Hands-on integrado — agente com RAG + memória

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
# ... imports do RAG (Chroma, embeddings)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    context_docs: list[str]

def retrieve_node(state):
    """Busca docs relevantes no Chroma."""
    q = state["messages"][-1].content
    docs = retriever.invoke(q)
    return {"context_docs": [d.page_content for d in docs]}

def agent_node(state):
    """LLM responde usando os docs como contexto."""
    sys = f"Use APENAS este contexto:\n{state['context_docs']}"
    msgs = [SystemMessage(sys)] + state["messages"]
    return {"messages": [llm.invoke(msgs)]}

graph = StateGraph(State)
graph.add_node("retrieve", retrieve_node)
graph.add_node("agent", agent_node)
graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "agent")
graph.add_edge("agent", END)

# Memória persistente entre execuções
memory = SqliteSaver.from_conn_string("checkpoints.db")
app = graph.compile(checkpointer=memory)
```

---
layout: section
---

# 🏋️ 3.10 Exercícios — Encontro 3

5 atividades · Memória, RAG, skills, multi-agente

---

# Exercício 3.1 · RAG sobre seus próprios docs

<div class="p-5 rounded-xl bg-purple-500/10 border-2 border-purple-500/40">

**Tarefa:** monte um RAG sobre <b>3-5 PDFs ou Markdowns reais</b> (manual técnico, artigos, sua tese, qualquer coisa).

**Requisitos:**
- Use Chroma local
- Chunking de 500 tokens com overlap de 50
- Top-K = 4
- Mostre os documentos recuperados antes da resposta

**Teste com 5 perguntas:**
- 2 fáceis (estão literais no doc)
- 2 difíceis (exigem síntese de 2+ trechos)
- 1 "pegadinha" (não está no doc — o agente deve dizer "não sei")

</div>

---

# Exercício 3.2 · Memória entre sessões

<div class="p-5 rounded-xl bg-purple-500/10 border-2 border-purple-500/40">

**Tarefa:** use **mem0** ou **LangGraph + SqliteSaver** para criar um chat que **lembra** do usuário entre execuções.

**Cenário:**
1. Sessão 1: usuário diz "me chamo Maria, sou engenheira de dados, prefiro Python"
2. Encerre o programa
3. Sessão 2 (novo `python script.py`): pergunta "qual minha profissão?"

O agente deve responder corretamente **sem** receber a info novamente.

</div>

---

# Exercício 3.3 · Crie um MCP server

<div class="p-5 rounded-xl bg-purple-500/10 border-2 border-purple-500/40">

**Tarefa:** crie um servidor MCP simples que expõe **2 ferramentas** úteis:

1. `listar_arquivos(diretorio: str)` — lista arquivos de um diretório
2. `contar_linhas(caminho_arquivo: str)` — conta linhas de um arquivo

**Conecte ao Claude Desktop** (ou Cursor) editando o `claude_desktop_config.json`.

**Teste:** pergunte ao Claude "quantas linhas tem o maior arquivo .py da pasta X?"

**O que isso ensina:** seu agente passa a ter ferramentas custom em <b>qualquer cliente MCP</b>, não só num script Python.

</div>

---

# Exercício 3.4 · Crew de 2 agentes

<div class="p-5 rounded-xl bg-purple-500/10 border-2 border-purple-500/40">

**Tarefa:** use **CrewAI** ou **LangGraph** para montar:

- **Agente 1 — Pesquisador:** recebe um tema, faz 3 buscas web, retorna fatos
- **Agente 2 — Crítico:** recebe os fatos, avalia se são confiáveis, marca os duvidosos

**Teste:** *"Quais foram os 3 maiores avanços em IA em 2025?"*

**Análise:** compare com a resposta de um único agente fazendo a mesma tarefa. O multi-agente foi melhor? Pior? Mais caro?

</div>

---

# Exercício 3.5 · Análise de context window

<div class="p-5 rounded-xl bg-cyan-500/10 border-2 border-cyan-500/40">

**Tarefa de análise (sem código obrigatório):**

Escolha um agente real que você usa (Cursor, Claude Code, ChatGPT, etc) e responda:

1. Qual a janela de contexto do modelo subjacente?
2. Como ele lida com **históricos longos** (você já viu o "histórico antigo" sumir)?
3. Ele usa **RAG**? Em que parte (busca no seu código? em docs?)
4. Tem memória **entre sessões**? Como ela funciona (na sua percepção)?
5. Que **falhas de contexto** você já viu? (Ex: "esqueceu" algo que você disse no início.)

Escreva 1 página. Será discutido no Encontro 4.

</div>

---
layout: center
class: text-center
---

---

---

# 🌐 Mercado: RAG, grounding & memória

<div class="grid grid-cols-2 gap-3 text-xs">

<div class="p-3 rounded-lg bg-purple-500/10 border border-purple-500/30">
<b>🗄️ Vector DBs líderes</b><br>
• <b>Pinecone</b> (US$ 750M valuation)<br>
• <b>Weaviate</b>, <b>Qdrant</b>, <b>Chroma</b><br>
• <b>pgvector</b> (Postgres) — adotado por Supabase, Neon<br>
• <b>Turbopuffer</b>, <b>LanceDB</b> (serverless)<br>
• <b>Elasticsearch / OpenSearch</b> com vetores
</div>

<div class="p-3 rounded-lg bg-cyan-500/10 border border-cyan-500/30">
<b>🔎 RAG-as-a-service / search</b><br>
• <b>Exa</b> (busca neural para agentes)<br>
• <b>Tavily</b> (search API focada em LLM)<br>
• <b>Perplexity API</b>, <b>You.com API</b><br>
• <b>Brave Search API</b><br>
• <b>Azure AI Search</b>, <b>Vertex AI Search</b>
</div>

<div class="p-3 rounded-lg bg-green-500/10 border border-green-500/30">
<b>🧠 Memória para agentes</b><br>
• <b>Mem0</b> (open source, fork de embedchain)<br>
• <b>Letta</b> (ex-MemGPT, papers de Berkeley)<br>
• <b>Zep</b> (memory + temporal KG)<br>
• <b>ChatGPT Memory</b>, <b>Claude Projects</b><br>
• <b>Cursor codebase indexing</b>
</div>

<div class="p-3 rounded-lg bg-amber-500/10 border border-amber-500/30">
<b>📦 Casos reais</b><br>
• <b>Notion AI Q&A</b> (busca no workspace)<br>
• <b>Glean</b> (US$ 4,6B) — enterprise search<br>
• <b>Harvey</b> — RAG jurídico em 235 firmas<br>
• <b>Perplexity</b> — RAG + web em tempo real<br>
• <b>Klarna</b> — RAG sobre políticas de atendimento
</div>

</div>

<div class="mt-3 p-2 rounded-lg bg-blue-500/10 border border-blue-500/30 text-xs">
🧩 <b>Analogia de mercado</b>: pense em <b>Glean</b> como o "Google interno da empresa" — agente que faz grounding sobre Slack, Drive, Jira, Confluence. Esse é o produto-tipo que toda empresa Fortune 500 está construindo (ou comprando) em 2025.
</div>

---

# 📚 Referências públicas — Encontro 3

<div class="grid grid-cols-2 gap-3 text-xs mt-3">

<div class="p-3 rounded bg-purple-500/10 border border-purple-500/30">
<b>RAG & Context</b>
<ul class="mt-1">
<li>Lewis et al. (2020) — <i>RAG for Knowledge-Intensive NLP</i> · <a href="https://arxiv.org/abs/2005.11401">arXiv:2005.11401</a></li>
<li>Gao et al. (2022) — <i>HyDE</i> · <a href="https://arxiv.org/abs/2212.10496">arXiv:2212.10496</a></li>
<li>Liu et al. (2023) — <i>Lost in the Middle</i> · <a href="https://arxiv.org/abs/2307.03172">arXiv:2307.03172</a></li>
<li>Gao et al. (2024) — <i>RAG Survey</i> · <a href="https://arxiv.org/abs/2312.10997">arXiv:2312.10997</a></li>
</ul>
</div>

<div class="p-3 rounded bg-cyan-500/10 border border-cyan-500/30">
<b>Grounding & Attribution</b>
<ul class="mt-1">
<li>Rashkin et al. (2023) — <i>Measuring Attribution in NLG</i> (AIS) · <a href="https://aclanthology.org/2023.cl-4.2/">aclanthology.org/2023.cl-4.2</a></li>
<li>Bohnet et al. (2022) — <i>Attributed QA</i> · <a href="https://arxiv.org/abs/2212.08037">arXiv:2212.08037</a></li>
<li>Anthropic (2024) — <i>Citations API</i> · <a href="https://docs.anthropic.com/en/docs/build-with-claude/citations">docs.anthropic.com</a></li>
</ul>
</div>

<div class="p-3 rounded bg-green-500/10 border border-green-500/30">
<b>Memória & Skills</b>
<ul class="mt-1">
<li>Packer et al. (2023) — <i>MemGPT</i> · <a href="https://arxiv.org/abs/2310.08560">arXiv:2310.08560</a></li>
<li>Park et al. (2023) — <i>Generative Agents</i> · <a href="https://arxiv.org/abs/2304.03442">arXiv:2304.03442</a></li>
<li>Anthropic (2024) — <i>Prompt Caching</i> · <a href="https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching">docs.anthropic.com</a></li>
<li>Anthropic (2024) — <i>MCP Specification</i> · <a href="https://modelcontextprotocol.io/">modelcontextprotocol.io</a></li>
</ul>
</div>

<div class="p-3 rounded bg-amber-500/10 border border-amber-500/30">
<b>Multi-agente & Frameworks</b>
<ul class="mt-1">
<li>Wu et al. (2023) — <i>AutoGen</i> · <a href="https://arxiv.org/abs/2308.08155">arXiv:2308.08155</a></li>
<li>CrewAI Docs · <a href="https://docs.crewai.com/">docs.crewai.com</a></li>
<li>Chroma · <a href="https://docs.trychroma.com/">docs.trychroma.com</a> · Qdrant · <a href="https://qdrant.tech/documentation/">qdrant.tech</a> · pgvector · <a href="https://github.com/pgvector/pgvector">github.com/pgvector</a></li>
</ul>
</div>

</div>

<div class="mt-2 text-xs opacity-70">
Todo conteúdo deste encontro é de domínio público. Marcas mencionadas pertencem aos respectivos donos; uso exclusivamente educacional.
</div>

---

---

# 🔄 Recap — O que construímos no Encontro 3

<div class="grid grid-cols-2 gap-4 text-sm">

<div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30">
<b>📜 Evolução que acompanhamos:</b>
<ul class="text-xs mt-2">
<li><b>2020:</b> Paper RAG (Lewis et al.) — buscar antes de responder</li>
<li><b>2023:</b> Vector DBs explodem (Pinecone, Chroma, Weaviate)</li>
<li><b>2024:</b> MCP (Anthropic) — protocolo universal de tools</li>
<li><b>2025:</b> Multi-agentes em produção (OpenAI Swarm, CrewAI)</li>
</ul>
</div>

<div class="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/30">
<b>🔧 O que você agora sabe fazer:</b>
<ul class="text-xs mt-2">
<li>Gerenciar context window (truncar, resumir, RAG)</li>
<li>Construir pipeline RAG completo com embeddings</li>
<li>Implementar memória de longo prazo</li>
<li>Criar Skills + usar MCP</li>
<li>Orquestrar multi-agentes (e quando NÃO usar)</li>
</ul>
</div>

<div class="p-4 rounded-xl bg-green-500/10 border border-green-500/30">
<b>🏢 Produtos que usam isso:</b>
<ul class="text-xs mt-2">
<li>Perplexity — RAG em escala (busca + citação)</li>
<li>NotebookLM — grounding em documentos do usuário</li>
<li>Claude Projects — memória persistente por projeto</li>
<li>GitHub Copilot — MCP para extensões</li>
</ul>
</div>

<div class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30">
<b>❓ Perguntas que ficaram abertas:</b>
<ul class="text-xs mt-2">
<li>E quando o agente falha em produção? (→ E4: Falhas)</li>
<li>Como medir se o agente é bom? (→ E4: Avaliação)</li>
<li>Quais produtos estão ganhando? (→ E4: State-of-art)</li>
</ul>
</div>

</div>

---

# ✅ Fim do Encontro 3

Você agora sabe:

- Gerenciar context window (truncate, summarize, RAG)
- Construir um pipeline RAG completo
- Implementar memória de longo prazo
- Conceituar e criar Skills + MCP
- Orquestrar multi-agentes (e quando NÃO usar)

<div class="mt-12 text-xl text-cyan-400">
Próximo: <b>Encontro 4 — Problemas Comuns & State-of-the-Art</b>
</div>

<div class="mt-4 text-sm opacity-60">
Onde tudo isso encontra a <i>realidade</i>: falhas, custos, e os produtos que estão ganhando o mercado.
</div>
