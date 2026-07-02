---
title: Portal Multi-Agente
emoji: 🤖
colorFrom: indigo
colorTo: purple
sdk: gradio
app_file: app.py
pinned: false
---

# 🤖 Portal Multi-Agente

Um portal onde **cada aluno pluga o seu próprio agente** de tarefa única.
Todos os agentes falam a mesma "língua" (um contrato simples), então o portal
descobre e roda cada um automaticamente. 100% open source, roda no Google
Colab / Hugging Face Spaces com um **token gratuito** do Hugging Face.

Feito para os Encontros 5 e 6 de *Tópicos Especiais em IA* (Prof. Alan Delgado).

---

## 🗺️ Como funciona

```
projeto-portal/
├── app.py              # o portal (UI Gradio) — não precisa editar
├── check_agent.py      # valide seu agente antes de subir
├── portal/             # infraestrutura comum — NÃO edite
│   ├── base.py         #   contrato: AgentResult + validate_agent
│   ├── llm.py          #   acesso ao modelo (HF router, MOCK, retry)
│   ├── registry.py     #   descoberta automática dos agentes
│   ├── runner.py       #   fronteira de erro + latência + log
│   └── observability.py#   log local em JSONL
├── agents/             # 👈 VOCÊ trabalha AQUI (um arquivo por aluno)
│   ├── _template_agent.py   # copie este
│   └── example_resumidor.py # exemplo completo e funcional
└── eval/               # avaliação (checks + juiz LLM opcional)
    ├── run_eval.py
    └── cases/<slug>.yaml
```

**O contrato** (a única regra): seu agente é um objeto com
`slug`, `name`, `emoji`, `description` e um método
`run(message, history) -> AgentResult`.

```python
from portal.base import AgentResult

class MeuAgente:
    slug = "meu-agente"; name = "Meu Agente"; emoji = "🧠"
    description = "O que ele faz, em uma frase."
    def run(self, message, history):
        return AgentResult(answer="olá!", steps=[], citations=[])

AGENT = MeuAgente()
```

---

## 🚀 Começando (5 minutos)

```bash
pip install -r requirements.txt
cp .env.example .env        # e cole seu HF_TOKEN (ou deixe MOCK_LLM=1)
python app.py               # abre o portal em http://localhost:7860
```

Sem token ainda? Rode **offline**:

```bash
MOCK_LLM=1 python app.py
```

Pegue um token gratuito (role **read**) em
<https://huggingface.co/settings/tokens>.

---

## 🧑‍🎓 Fluxo do aluno

1. **Escope** seu agente em uma frase:
   > "Meu agente ajuda **[usuário]** a fazer **[tarefa]** usando **[entrada]**
   > e entregando **[saída verificável]**."

   Exemplos bons: *tutor de SQL que corrige uma query*, *gerador de mensagem
   de commit a partir de um diff*, *explicador de termos jurídicos*.
   Evite escopos vagos ("assistente geral", "responde qualquer coisa").

2. **Copie o template**: `agents/_template_agent.py` → `agents/<seu-slug>.py`.
   Escolha um `slug` único.

3. **Implemente `run()`**. Use `from portal import llm` e `llm.chat([...])`.

4. **Valide** (offline, sem gastar rede):
   ```bash
   python check_agent.py agents/<seu-slug>.py
   ```

5. **Teste no portal**: `python app.py`, escolha seu agente no menu.

6. **Avalie** (Encontro 6): crie `eval/cases/<seu-slug>.yaml` com 2-3 casos e
   rode `python eval/run_eval.py <seu-slug>`.

> ⚠️ Regras de convivência: edite **só o seu arquivo** em `agents/`. Não faça
> chamadas de rede no import (só dentro de `run()`). Um agente que quebra
> **não derruba** o portal, mas aparece na lista de erros.

---

## ✅ Avaliação (duas camadas)

- **Determinística** (sempre roda, offline): resposta não-vazia, latência
  dentro do limite, substrings obrigatórias/proibidas.
- **Juiz LLM** (opcional): uma pergunta sim/não sobre a qualidade. Só roda
  com token e sem `MOCK_LLM`.

```bash
python eval/run_eval.py            # todos os agentes
python eval/run_eval.py resumidor  # só um
```

---

## 🌐 Deploy no Hugging Face Spaces (grátis)

1. Crie um Space novo em <https://huggingface.co/new-space> → SDK **Gradio**.
2. Suba o conteúdo desta pasta (`app.py`, `requirements.txt`, este `README.md`
   com o cabeçalho YAML, `portal/`, `agents/`).
3. Em *Settings → Variables and secrets*, adicione o secret **HF_TOKEN**.
4. O Space builda sozinho e publica a URL. Pronto: portal no ar. 🎉

> O cabeçalho YAML no topo deste README é o que diz ao Spaces para usar Gradio
> e rodar `app.py`.

---

## 🧰 Modo offline / aula

`MOCK_LLM=1` faz o `llm.chat()` devolver uma resposta determinística sem tocar
a rede. Use para desenvolver o contrato, a UI e os evals sem depender de
internet, token ou rate limit — essencial para a aula não travar.

⚖️ Uso educacional. Modelos e ferramentas de terceiros pertencem aos seus donos.
