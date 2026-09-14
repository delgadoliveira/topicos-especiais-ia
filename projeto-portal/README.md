# Portal Multi-Agente — imersao offline-first

Projeto didatico dos encontros 5 e 6. Cada aluno cria um agente de tarefa unica,
valida o contrato, executa casos de teste e apresenta o resultado localmente.
No modo padrao, uma funcao Python simula a resposta: nenhum modelo de IA e
executado. A IA real e opcional e usa `Qwen/Qwen2.5-7B-Instruct` pela API do
Hugging Face, limitada a um checkpoint coletivo.

Tutorial completo:
[`../public/tutorials/imersao-agente-local.html`](../public/tutorials/imersao-agente-local.html)

Laboratorio no navegador, sem instalacao:
[`../public/tutorials/simulador-agente.html`](../public/tutorials/simulador-agente.html)

Guia local do professor:
[`../public/tutorials/guia-professor-imersao.html`](../public/tutorials/guia-professor-imersao.html)

## O que o aluno entrega

- `agents/<slug>.py`, criado a partir de `agents/_template_agent.py`;
- `eval/cases/<slug>.yaml`, com tres casos de teste;
- uma demonstracao de dois minutos que tambem funciona sem internet.

## 1. Preparar o ambiente

Abra esta pasta no VS Code e crie um terminal.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### macOS ou Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Valide a instalacao sem usar rede:

```bash
python check_agent.py agents/example_resumidor.py
```

## 2. Criar o agente

Copie `agents/_template_agent.py` para `agents/<slug>.py`. O slug deve usar apenas
letras minusculas, numeros e hifens.

Altere `slug`, `name`, `description` e o prompt dentro de `run()`. Preserve o contrato:

```python
class MeuAgente:
    slug = "organizador-estudos"
    name = "Organizador de Estudos"
    emoji = "📚"
    description = "Transforma anotacoes em um plano de estudo curto."

    def run(self, message, history):
        # Preserve a estrutura do template e troque a instrucao do sistema.
        ...


AGENT = MeuAgente()
```

Rode o preflight:

```bash
python check_agent.py agents/organizador-estudos.py
```

## 3. Abrir o portal

```bash
python app.py
```

Abra <http://127.0.0.1:7860>. O modo padrao e offline e nao requer token.
Ele usa um simulador deterministico, nao um modelo de IA local. O simulador
repete parte da entrada para que a turma valide o fluxo, o formato, os
guardrails e os testes sem depender da qualidade de uma resposta generativa.

## 4. Avaliar

Copie `eval/cases/_template.yaml` para `eval/cases/<slug>.yaml` e escreva:

1. um caso normal;
2. um caso dificil;
3. um caso inadequado ou vazio.

Execute:

```bash
python eval/run_eval.py organizador-estudos
```

O avaliador deterministico verifica conteudo obrigatorio, tamanho, latencia e
erros. O juiz por LLM e opcional.

## 5. Usar a API real com limite

Somente no checkpoint orientado pelo professor, copie `.env.example` para
`.env` e configure:

```dotenv
HF_TOKEN=seu_token
MOCK_LLM=0
MAX_REAL_CALLS=3
LLM_CACHE=1
```

- Cada tentativa ao provedor consome uma chamada.
- Erros transitorios podem gerar nova tentativa, sem ultrapassar o orcamento.
- Entradas identicas usam o cache em memoria enquanto o processo estiver ativo.
- Ao atingir o limite, o portal mostra um erro claro. Volte para
  `MOCK_LLM=1` e reinicie.
- Nunca coloque o token em codigo, prints, screenshots ou commits.

## 6. Empacotar e entregar

Crie um unico ZIP com identificacao, agente e casos:

```powershell
python prepare_submission.py `
  --id "12345" `
  --nome "Nome Sobrenome" `
  --agente "organizador-estudos"
```

O arquivo aparece em `entregas/`. No portal, abra **Entregar trabalho**, envie o
ZIP e clique em **Avaliar e registrar**. A avaliacao:

- valida uma politica restrita de Python, remove credenciais do ambiente,
  executa em subprocesso somente com `MOCK_LLM=1` e aplica timeout;
- calcula contrato, smoke test, casos, guardrail e observabilidade;
- registra cada tentativa em `submissions/grades.db`;
- disponibiliza `submissions/notas.csv` para download.

A politica bloqueia imports externos, acesso a atributos privados e funcoes como
`open`, `exec` e `eval`. O subprocesso reduz o impacto de travamentos, mas nao e
uma sandbox completa. O professor deve usar essa funcao apenas localmente, sem
publicar a aba na internet.

## Configuracao

| Variavel | Padrao | Funcao |
|---|---:|---|
| `MOCK_LLM` | `1` | Usa um simulador Python; nenhum modelo de IA ou API |
| `HF_TOKEN` | vazio | Token usado apenas com `MOCK_LLM=0` |
| `MODEL` | `Qwen/Qwen2.5-7B-Instruct` | Modelo real acessado pela API do Hugging Face |
| `MAX_REAL_CALLS` | `3` | Orcamento por processo; `0` remove o limite |
| `LLM_CACHE` | `1` | Reaproveita respostas identicas em memoria |
| `JUDGE_ENABLED` | `0` | Habilita juiz LLM opcional |
| `MAX_WORKERS` | `4` | Paralelismo do portal |
| `REQUEST_TIMEOUT_S` | `60` | Timeout das chamadas |

## Solucao rapida de problemas

| Problema | Acao |
|---|---|
| `python` nao encontrado | No Windows, tente `py`; confirme Python 3.10+ |
| PowerShell bloqueou ativacao | `Set-ExecutionPolicy -Scope Process Bypass` |
| Modulo ausente | Ative `.venv` e reinstale `requirements.txt` |
| Agente nao aparece | Rode `check_agent.py` e confira se existe `AGENT` |
| HTTP 429 | Limite do provedor; volte para `MOCK_LLM=1` |
| HTTP 503 ou timeout | Servico indisponivel; use a demonstracao offline |
| Limite local atingido | Nao reinicie para contornar; consulte o professor |

## Estrutura

```text
projeto-portal/
├── app.py
├── check_agent.py
├── prepare_submission.py
├── agents/
│   ├── _template_agent.py
│   └── example_resumidor.py
├── eval/
│   ├── run_eval.py
│   └── cases/
├── portal/
│   ├── base.py
│   ├── evaluation.py
│   ├── llm.py
│   ├── submission_worker.py
│   └── submissions.py
└── .env.example
```

## Privacidade

Nao envie dados pessoais, sigilosos ou de terceiros. O log local registra
metadados operacionais, nao o texto completo da conversa.
