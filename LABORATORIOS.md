# 🧪 Laboratórios — Encontros 5 e 6

> Material do aluno. Dois laboratórios, um por encontro, de 35 minutos cada.
> Nenhum exige programação. Nenhum exige ferramenta paga.

---

## Por que estes laboratórios existem

Os Encontros 5 e 6 explicam o que mantém um agente vivo e com que autoridade ele
age. Explicar é pouco. Ao final destes dois encontros você deve sair com **duas
coisas que sabe fazer**, não com duas coisas que ouviu falar:

| Encontro | Habilidade que você leva | Prova de que leva |
|---|---|---|
| 5 | Escrever um **handoff operacional** que faz um trabalho sobreviver à troca de sessão, de pessoa ou de ferramenta | O seu handoff funcionou numa sessão limpa — e você viu a versão sem ele falhar |
| 6 | Redigir e **auditar um mandato de agente** para um processo real da sua empresa | O seu mandato v2, com o furo que um colega encontrou e você fechou |

Ambas são transferíveis: não dependem de fornecedor, de modelo nem de linguagem
de programação. E ambas são, hoje, artefatos que empresas pedem por escrito.

---

# 🔬 Laboratório 1 — Faça a tarefa atravessar o reset

**Encontro 5 · 35 minutos · duplas**
**Habilidade:** escrever um handoff que preserva critério e progresso.

## O que você vai precisar

Qualquer assistente com sessões separadas — ChatGPT, Claude, Copilot, Gemini,
Mistral. A versão gratuita basta. **Importante:** você vai precisar abrir uma
*conversa nova* no meio do exercício, então não use uma ferramenta que mantenha
memória automática entre conversas (ou desligue a memória antes de começar).

## O material

Use esta fila fictícia de reembolsos. Copie como está.

```
ID  | Colaborador | Valor   | Categoria   | Comprovante | Observação
01  | Ana         | R$ 180  | Refeição    | sim         | jantar com cliente
02  | Bruno       | R$ 1.240| Hospedagem  | não         | —
03  | Carla       | R$ 92   | Transporte  | sim         | corrida aeroporto
04  | Diego       | R$ 610  | Equipamento | sim         | cadeira de escritório
05  | Elisa       | R$ 2.300| Passagem    | sim         | emitida fora da política
06  | Fábio       | R$ 47   | Refeição    | não         | —
07  | Gabi        | R$ 880  | Hospedagem  | sim         | 3 diárias
08  | Hugo        | R$ 155  | Transporte  | sim         | —
09  | Iara        | R$ 3.100| Equipamento | sim         | notebook pessoal
10  | João        | R$ 70   | Refeição    | sim         | —
11  | Kátia       | R$ 430  | Passagem    | não         | —
12  | Léo         | R$ 1.900| Hospedagem  | sim         | hotel acima do teto
```

E este critério de decisão. Entregue-o ao agente no início.

```
REGRA 1 · Sem comprovante → não aprove. Peça o documento.
REGRA 2 · Acima de R$ 1.000 → precisa de justificativa escrita do gestor.
REGRA 3 · Equipamento de uso pessoal → recuse, independentemente do valor.
Saída: para cada ID, uma de três decisões — APROVADO, PENDENTE (e o que falta)
ou RECUSADO (e por quê).
```

## Roteiro

### Passo 1 · Comece o trabalho (5 min)

Abra uma conversa e peça ao agente que aplique o critério à fila, **um pedido por
vez**, explicando cada decisão. Deixe chegar até o ID 06 e **pare**.

Anote num papel: quais decisões ele tomou e com que justificativa.

### Passo 2 · Simule o reset (5 min)

Abra uma **conversa nova**. Escreva apenas:

> “Continue de onde paramos.”

Observe o que acontece. Anote as três perguntas abaixo — elas são o relatório do
laboratório:

1. O que exatamente ele não sabe?
2. Se você insistisse, ele inventaria um critério? Qual?
3. Qual das três regras foi a primeira a se perder?

> ⚠️ Este é o passo que a maioria pula. Não pule. A sensação de “ué, mas ele
> estava indo tão bem” é o conteúdo do Encontro 5 acontecendo com você.

### Passo 3 · Escreva o handoff (10 min)

Volte à conversa original e peça:

> “Escreva um handoff para que outra pessoa, que não leu nada desta conversa,
> continue este trabalho exatamente como eu continuaria.”

Leia o que ele produziu e **corrija à mão**. Um handoff que funciona tem quatro
campos — se faltar algum, acrescente você:

| Campo | Pergunta que ele responde |
|---|---|
| **Critério** | Com que regra as decisões estão sendo tomadas? |
| **Estado** | O que já foi decidido, e o que foi decidido em cada caso? |
| **Pendências** | O que está parado esperando o quê? |
| **Definição de pronto** | Como eu sei que terminei — e que terminei direito? |

### Passo 4 · Teste o handoff (10 min)

Abra **outra conversa nova**. Cole só o handoff e peça para continuar do ID 07.

Compare com o passo 2:

- O critério se manteve nas três regras?
- Alguma decisão já tomada foi refeita ou contradita?
- Ele soube quais pedidos estavam pendentes e por quê?

### Passo 5 · Entregue (5 min)

Entregue **uma página**: o handoff que funcionou, e abaixo dele duas linhas
dizendo qual campo fez a maior diferença e por quê.

## O que discutir depois

- Quem escreveu o handoff: você ou o agente? Quem **deveria** escrever?
- Na sua empresa, onde já existe um handoff — e onde ele só existe na cabeça de alguém?
- Se o handoff é o que faz o trabalho sobreviver, de quem é a responsabilidade quando ele está errado?

---

# 🔬 Laboratório 2 — Escreva o mandato, fure o do colega

**Encontro 6 · 35 minutos · duplas**
**Habilidade:** redigir um mandato de agente e auditar o de outra pessoa.

## O material

Um processo **real** da sua empresa, da sua área, que hoje é feito por uma pessoa
e que você consideraria delegar a um agente. Exemplos que funcionam bem:
responder a um tipo de chamado, triar currículos, conferir notas fiscais, aprovar
descontos até certo limite, agendar visitas, cobrar inadimplentes.

Se você não tiver um, use este: *um agente que responde a pedidos de orçamento de
clientes, consulta a tabela de preços e envia a proposta por e-mail.*

## Passo 1 · O mandato (10 min)

Preencha os quatro campos. Escreva frases, não tópicos — um mandato que não cabe
numa frase é um mandato que ninguém vai conseguir auditar.

| Campo | O que escrever |
|---|---|
| **Quem pediu** | Em nome de qual pessoa ou cargo o agente age? Não vale “a empresa”. |
| **O quê e até quanto** | Qual ação, sobre quais objetos, com qual teto (valor, volume, alcance)? |
| **Até quando** | O mandato vence quando? Se não vence, por que não? |
| **Como se prova** | Depois que a ação acontecer, onde fica registrado que ela era autorizada? |

## Passo 2 · A escada de autonomia (10 min)

Liste **as ações concretas** que o agente executaria, uma por linha, e classifique
cada uma. Não classifique “o agente” — classifique cada ação.

| Nível | Significado | Exemplo do caso do orçamento |
|---|---|---|
| **Sozinho** | Executa e avisa depois | Consultar a tabela de preços |
| **Sozinho, reversível** | Executa, mas dá para desfazer em minutos | Montar o rascunho da proposta |
| **Pede aprovação** | Prepara tudo e espera um humano | Enviar proposta acima de R$ 50 mil |
| **Nunca** | Fora do mandato, em qualquer circunstância | Conceder desconto fora da tabela |

> 💡 Regra prática: se você não consegue dizer quanto custa o erro de uma ação,
> ela ainda não pode ficar no nível “sozinho”.

## Passo 3 · A auditoria (10 min)

Troque a folha com a dupla ao lado. Você agora é o auditor. Responda **sobre o
mandato do colega**, por escrito:

1. **O furo.** Qual ação cabe dentro deste mandato, tecnicamente permitida, que você não gostaria que acontecesse?
2. **A detecção.** Se o agente fizesse isso amanhã de manhã, como alguém descobriria? Em quanto tempo?
3. **A responsabilidade.** Deu errado — quem responde? Essa pessoa sabe que responde?

> ⚠️ A pergunta 2 é a que mais derruba mandatos. “Alguém perceberia” não é
> resposta. Onde, em qual tela, quem olha?

## Passo 4 · Feche o furo (5 min)

Pegue sua folha de volta e escreva o **mandato v2**, corrigindo o furo apontado.
Se o furo não puder ser fechado por escrito, escreva isso — é uma descoberta
legítima e vale a mesma nota.

## Entregável

Mandato v1 · o furo que o colega encontrou · mandato v2.

---

# 🔭 Exploração guiada — 15 minutos numa plataforma real

Opcional, mas é o que transforma os dois encontros em algo que você reconhece no
próximo fornecedor que entrar na sua sala.

Escolha **uma** plataforma com camada gratuita ou trial: Microsoft Copilot
Studio, Salesforce Agentforce, Google Agentspace, n8n, Zapier Agents, Make, ou a
própria área de *custom GPTs* / *Projects* / *Gems* do assistente que você já usa.

Não construa nada. Sua tarefa é **localizar cinco coisas** e anotar onde ficam:

| # | Procure por | Por que importa |
|---|---|---|
| 1 | Onde se define **quem o agente é** — identidade própria ou a sua conta? | Encontro 6, pergunta 1: quem agiu, afinal? |
| 2 | Onde se escolhe **quais ferramentas e dados** ele alcança | O catálogo. Se não existe, o escopo é “tudo”. |
| 3 | Onde fica o **registro** do que ele fez | Sem isso, não há como provar nem auditar |
| 4 | Onde se exige **aprovação humana** para uma ação | A escada de autonomia do Laboratório 2 |
| 5 | Onde se **desliga** o agente — e em quanto tempo | A pergunta que ninguém faz na demonstração |

Depois responda em duas linhas: **quais das cinco você não encontrou?** As que
faltam são exatamente as seis perguntas de compra do Encontro 5 deixando de ser
teoria.

---

## 📋 Para o professor

**Encaixe no tempo.** Cada laboratório consome 35 minutos. Os decks dos dois
encontros já somam mais conteúdo do que cabe em 120 minutos — rodar um
laboratório exige cortar, não espremer. Use a seção **“Rota de 120 minutos”** do
`GUIA_PROFESSOR.md` para escolher o que sai.

**Sugestão de formato:** laboratório logo após o bloco de virada, não no final.
Um laboratório no fim da aula vira tarefa de casa, e tarefa de casa não gera a
conversa que é o ponto do exercício.

**Avaliação.** Os dois entregáveis são curtos e corrigíveis em minutos. Avalie
pela qualidade do diagnóstico, não pela ferramenta: no Lab 1, o aluno que
identificou *qual* regra se perdeu primeiro entendeu mais do que o que produziu o
handoff mais bonito. No Lab 2, o aluno cujo mandato foi furado aprendeu mais do
que o que escreveu um mandato tão vago que ninguém conseguiu furar.

**Se faltar internet ou ferramenta:** o Laboratório 2 roda inteiro no papel. O
Laboratório 1 pode ser feito em dupla, com um aluno fazendo o papel do agente que
“esqueceu tudo” — funciona surpreendentemente bem e torna o ponto mais vívido.
