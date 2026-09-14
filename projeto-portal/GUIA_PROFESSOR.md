# Guia do professor — imersao local em dois encontros

Roteiro para duas aulas de 3h com alunos sem experiencia previa em computacao.
O objetivo nao e ensinar infraestrutura: e tornar visivel o ciclo de produto de
um agente — escopo, construcao, teste, guardrail, observabilidade e limite.

## Principios

1. **Offline-first:** toda entrega deve funcionar com `MOCK_LLM=1`.
2. **Uma tarefa:** o agente tem entrada e saida verificaveis.
3. **Checkpoint coletivo:** a turma avanca junta nas partes tecnicas.
4. **Erro como dado:** cada falha deve levar a uma mudanca observavel.
5. **API e comparacao:** no maximo tres chamadas reais por grupo.
6. **Plano B pronto:** indisponibilidade externa nao interrompe a aula.

## Dois modos, sem ambiguidade

- Com `MOCK_LLM=1`, nenhum modelo de IA e executado. Uma funcao Python local
  devolve uma resposta previsivel para validar fluxo, formato, guardrails e
  testes. Nao apresente esse modo como "IA local".
- Com `MOCK_LLM=0`, o modelo `Qwen/Qwen2.5-7B-Instruct` e acessado pela API
  OpenAI-compatible do Hugging Face. Esse modo requer internet e `HF_TOKEN`.
- "OpenAI-compatible" descreve o formato da API, nao o fornecedor do modelo.

Material do aluno:
[`../public/tutorials/imersao-agente-local.html`](../public/tutorials/imersao-agente-local.html)

Versao local navegavel deste guia:
[`../public/tutorials/guia-professor-imersao.html`](../public/tutorials/guia-professor-imersao.html)

## Preparacao antes da aula

- Execute o ensaio do zero em Windows e, se houver alunos usando macOS, valide
  tambem esse caminho.
- Tenha uma copia local ou ZIP do repositorio; Git nao e pre-requisito.
- Confirme Python 3.10+ e VS Code nos computadores.
- Deixe o portal funcionando com `MOCK_LLM=1`.
- Prepare um exemplo completo e um exemplo propositalmente quebrado.
- Projete o tutorial e mantenha seu link curto acessivel.
- Se usar API, confirme o token apenas no computador do professor e defina
  `MAX_REAL_CALLS=3`.

## Encontro 5 — construir offline (180 min)

| Tempo | Atividade | Evidencia |
|---:|---|---|
| 0–15 | Mostrar o produto pronto em modo offline | Turma entende entrada, saida e passos |
| 15–35 | Abrir pasta, criar `.venv`, instalar dependencias | Checkpoint 0 passa |
| 35–55 | Escrever a frase de escopo em linguagem comum | Entrada e saida verificaveis |
| 55–75 | Definir obrigatorios, proibido e exemplo | Criterio de qualidade escrito |
| 75–90 | Pausa e atendimento | Dificuldades agrupadas no quadro |
| 90–125 | Copiar template e editar quatro campos | Arquivo individual criado |
| 125–145 | Rodar preflight e depurar em dupla | Checkpoint 1 passa |
| 145–170 | Abrir portal e testar | Checkpoint 2 demonstrado |
| 170–180 | Exit ticket | Uma melhoria para o encontro 6 |

### Conducao dos checkpoints

- **Checkpoint 0:** ninguem edita codigo antes de a instalacao funcionar.
- **Checkpoint 1:** alunos com preflight verde ajudam uma dupla, sem assumir o
  teclado dela.
- **Checkpoint 2:** cada dupla mostra escopo, entrada e resposta. Nao avaliar
  “criatividade” do mock; avaliar se o contrato esta compreendido.

### Intervencoes recomendadas

- Se o escopo tiver “qualquer”, “tudo” ou varias tarefas, reduza para um verbo.
- Se a saida nao puder ser conferida, peca formato, quantidade e limites.
- Se metade da turma travar no mesmo ponto, pause e resolva coletivamente.
- Nao introduza Git, deploy ou token neste encontro.

## Encontro 6 — avaliar e proteger (180 min)

| Tempo | Atividade | Evidencia |
|---:|---|---|
| 0–15 | Retomar demo offline e Definition of Done | Base comum restabelecida |
| 15–45 | Criar caso normal, dificil e inadequado | Tres casos legiveis |
| 45–70 | Rodar avaliador e interpretar falhas | Checkpoint 3 executado |
| 70–90 | Melhorar prompt a partir de uma falha | Antes/depois registrado |
| 90–105 | Pausa | — |
| 105–125 | Adicionar entrada vazia e limite de tamanho | Guardrail demonstravel |
| 125–140 | Ler passos, latencia e log JSON | Evidencia de observabilidade |
| 140–160 | Checkpoint opcional com API | Ate tres chamadas por grupo |
| 160–175 | Empacotar, enviar e ler o resultado | Conceito registrado |
| 175–180 | Fechamento | Produto e limitacao explicados |

## Protocolo da API

1. Explique que o modelo e Qwen e roda na infraestrutura do Hugging Face.
2. Explique antes que cada tentativa, inclusive retry, consome o orcamento.
3. Libere a API apenas quando preflight e avaliacao offline passarem.
4. Use a mesma entrada no simulador e na API; depois repita para observar o cache.
5. Pare no primeiro 429 recorrente, 503 ou timeout. Nao transforme a aula em
   depuracao do provedor.
6. Volte para `MOCK_LLM=1`, reinicie e prossiga com a demo.
7. Token nunca e compartilhado em chat, projetor, codigo ou repositorio.

O objetivo do checkpoint e comparar variabilidade, custo e dependencia externa,
nao conseguir uma resposta “mais bonita”.

## Pontos de parada

Pode encerrar cada bloco quando:

- ambiente: o exemplo passa no preflight;
- construcao: o agente individual passa no preflight;
- avaliacao: tres casos foram executados, mesmo que algum falhe;
- robustez: um guardrail e visivel;
- apresentacao: a demo funciona em modo offline.

## Rubrica sugerida

| Criterio | Evidencia | Peso |
|---|---|---:|
| Escopo e utilidade | Uma tarefa, usuario, entrada e saida claros | 20% |
| Funcionamento | Preflight e portal offline | 25% |
| Avaliacao | Tres casos e melhoria baseada em falha | 25% |
| Responsabilidade | Guardrail, privacidade e limitacao | 20% |
| Comunicacao | Demo objetiva de dois minutos | 10% |

Nao penalize indisponibilidade de API. Ela e uma condicao externa coberta pelo
plano B.

## Entrega e registro automatico

O aluno gera um ZIP padronizado:

```powershell
python prepare_submission.py `
  --id "12345" `
  --nome "Nome Sobrenome" `
  --agente "organizador-estudos"
```

No portal, use a aba **Entregar trabalho**. O avaliador abre somente os tres
arquivos esperados, executa o agente offline em subprocesso com timeout e grava
o resultado em `submissions/grades.db`. A interface tambem fornece
`submissions/notas.csv`.

| Criterio automatico | Pontos |
|---|---:|
| Contrato | 20 |
| Smoke test offline | 20 |
| Tres casos | 15 |
| Taxa de aprovacao | 25 |
| Guardrail vazio ou acima de 4.000 caracteres | 10 |
| Passos de observabilidade | 10 |

Conversao: A = 90–100; B = 75–89; C = entrega parcial. D e reservado para
ausencia de entrega. Use a justificativa por criterio como apoio e faca revisao
manual quando o resultado nao representar a aprendizagem observada.

O avaliador bloqueia imports e operacoes perigosas, remove credenciais do
ambiente e usa subprocesso offline com timeout. Essas medidas oferecem
isolamento parcial, nao uma sandbox completa. Nao publique a aba de upload na
internet; use-a apenas no computador de aula.

## Ensaio local obrigatorio

Use uma pasta temporaria e aja como iniciante:

1. Copie o projeto sem `.venv`, `.env`, caches ou logs.
2. Siga apenas o tutorial, sem conhecimento implicito.
3. Crie ambiente e instale dependencias.
4. Rode o exemplo, crie um agente e valide.
5. Abra o portal e confirme o rodape offline.
6. Crie tres casos e rode a avaliacao.
7. Adicione o guardrail e repita os testes.
8. Simule token ausente, limite local e resposta em cache.
9. Gere um ZIP, avalie no portal e confira o registro SQLite/CSV.
10. Registre comandos confusos, corrija o material e repita os trechos afetados.

## Diagnostico durante a aula

| Sintoma | Diagnostico | Resposta didatica |
|---|---|---|
| `python` nao encontrado | Instalacao/PATH | Tentar `py`; usar dupla de apoio |
| Ativacao bloqueada | Politica do PowerShell | Liberar somente o processo atual |
| Modulo ausente | Ambiente nao ativo | Ativar `.venv` e reinstalar |
| Agente nao aparece | Contrato/import | Rodar preflight, nao adivinhar |
| YAML invalido | Sintaxe | Validar recuo, dois-pontos e hifens |
| 429 | Cota do provedor | Voltar ao mock imediatamente |
| 503/timeout | Instabilidade externa | Executar plano B offline |
| Limite local | Controle funcionando | Discutir custo; nao contornar |

## Definition of Done da imersao

- todos conseguem executar um agente offline;
- cada entrega tem tres testes;
- ao menos uma melhoria surgiu de uma falha observada;
- ha um guardrail explicavel;
- API real nao e dependencia da avaliacao;
- cada aluno consegue explicar uma limitacao do proprio agente.
