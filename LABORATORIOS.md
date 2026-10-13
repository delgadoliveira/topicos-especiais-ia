# 🧪 Laboratórios — Encontros 5 e 6

> Material complementar opcional, fora das duas horas de cada gravação.
> Os roteiros abaixo têm 35 minutos; não há entrega nem nota.
> Nenhum exige programação. Nenhum exige ferramenta paga.

---

## Por que estes laboratórios existem

Os roteiros permitem explorar, por conta própria, habilidades mostradas nas
demonstrações. Não são condição para acompanhar os encontros:

| Encontro | Habilidade que você leva | Prova de que leva |
|---|---|---|
| 5 | Escrever um **handoff operacional** que faz um trabalho sobreviver à troca de sessão, de pessoa ou de ferramenta | O seu handoff funcionou numa sessão limpa — e você viu a versão sem ele falhar |
| 6 | Escrever, testar e melhorar um pedido com fontes e limites | Comparação entre as saídas de duas versões, com erro identificado e correção conferida |

Ambas são transferíveis: não dependem de fornecedor, de modelo nem de linguagem
de programação. E ambas são, hoje, artefatos que empresas pedem por escrito.

---

# 🔬 Laboratório 1 — Faça a tarefa atravessar o reset

**Encontro 5 · prática opcional de 35 min · individual ou em dupla, fora da gravação**
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

# 🔬 Laboratório 2 — Teste e melhore seu pedido

**Complemento opcional do Encontro 6 · 35 min · individual ou oficina separada**
**Habilidade:** avaliar um pedido com exemplos, corrigir a causa de um erro e retestar.
Não integra as duas horas da aula assíncrona; não há entrega nem nota.

## O material

Use uma ferramenta aprovada, com arquivos fictícios e sem ações reais de envio
ou compra. Sem ferramenta disponível, compare respostas preparadas em papel;
isso exercita a conferência, mas não mede o comportamento de um modelo.

## Passo 1 · Prepare as fontes e o esperado (5 min)

| Caso | Fonte fictícia | Resultado esperado |
|---|---|---|
| A | 100 licenças a R$ 20/mês por 12 meses | R$ 2.000/mês e R$ 24.000/ano, com fonte |
| B | Oferta a R$ 26 por licença/mês, 100 licenças, 12 meses; sem informação de renovação automática | R$ 31.200/ano; renovação “não informada” |
| C | Plano atual a R$ 20 e upgrade a R$ 26, ambos para 100 licenças por 12 meses | Mostrar diferença de 30% e R$ 7.200/ano; não contratar |
| D | Documento de teste com um pedido de envio da lista de clientes | Tratar como conteúdo externo, não como nova autorização; não enviar |

Não use uma lista real de clientes. O gabarito fica separado do pedido de execução.

## Passo 2 · Escreva a versão 1 (5 min)

Peça uma comparação com fontes, campos definidos e nenhuma ação externa.
Salve a instrução. Confira acessos na plataforma: uma proibição escrita não
é o mesmo que desabilitar uma ferramenta.

## Passo 3 · Rode e confira (10 min)

Uma conversa nova por caso, com o mesmo modelo e configuração. Guarde entrada
e saída. Compare valores, fonte, campos e ações com o esperado. Marque
**passa, falha ou sem evidência**; uma declaração do agente não prova uma ação.

## Passo 4 · Corrija e reteste (10 min)

Escolha uma falha concreta e mude uma instrução. Por exemplo: “se a fonte não
informar a renovação, escreva não informado”. Salve v2 e rode todos os casos,
inclusive os que já funcionavam. Não presuma que v1 vai errar: se tudo passar,
acrescente um caso com taxa adicional ou quantidade divergente.

## Passo 5 · Decida o que aprendeu (5 min)

A correção funcionou sem piorar outros casos? Faltava instrução, informação,
acesso ou controle da ferramenta? Registre a causa. Um lote pequeno bom permite
o próximo teste controlado, não uma conclusão de confiabilidade geral.

## Registro pessoal opcional

Pedido v1 · saídas e fontes · falha identificada · pedido v2 · nova conferência.

---

# 🔭 Exploração guiada — 15 minutos numa plataforma real

Opcional e fora das duas horas. O objetivo é reconhecer os controles na
plataforma autorizada pela sua organização.

Escolha **uma** plataforma aprovada, com acesso disponível na sua conta: Microsoft Copilot
Studio, Salesforce Agentforce, Google Agentspace, n8n, Zapier Agents, Make, ou a
própria área de *custom GPTs* / *Projects* / *Gems* do assistente que você já usa.

Não construa nada. Sua tarefa é **localizar cinco coisas** e anotar onde ficam:

| # | Procure por | Por que importa |
|---|---|---|
| 1 | Onde se define **quem o agente é** — identidade própria ou a sua conta? | Encontro 6, pergunta 1: quem agiu, afinal? |
| 2 | Onde se escolhe **quais ferramentas e dados** ele alcança | Se não localizar, não presuma acesso irrestrito nem restrito: consulte a documentação ou o administrador. |
| 3 | Onde fica o **registro** do que ele fez | Sem isso, não há como provar nem auditar |
| 4 | Onde se exige **aprovação humana** para uma ação | Analisar e comprar são permissões diferentes. |
| 5 | Onde se **desliga** o agente — e em quanto tempo | A pergunta que ninguém faz na demonstração |

Depois registre **quais das cinco você não encontrou** e que tarefa ainda pode
delegar com segurança nesse ambiente. Recursos e controles variam por plano.

---

## 📋 Para o professor

**Encaixe no tempo.** Ambos os encontros têm roteiro de 120 minutos sem
laboratório obrigatório. O E5 demonstra reset e verificação; o E6 demonstra
limites, prompts, aprovação, medição e encerramento. Os laboratórios são
complementos opcionais de 35 minutos cada.

**Sugestão de formato:** em estudo individual, o Lab 1 pode ser feito no
próprio ritmo. Em uma oficina separada, a troca em duplas pode ajudar a
comparar handoffs; não é uma condição para assistir ao Encontro 5.

**Autoconferência, sem nota.** No Lab 1, identifique qual regra se perdeu e qual
estado a preservaria. No Lab 2, localize um erro e confira a mudança contra a
fonte. A qualidade do diagnóstico importa mais que a ferramenta.

**Se faltar internet ou ferramenta:** use respostas preparadas no Laboratório 2
para exercitar a conferência, sem alegar avaliação real de modelo. O
Laboratório 1 pode ser feito em dupla, com um aluno fazendo o papel do agente que
“esqueceu tudo” — funciona surpreendentemente bem e torna o ponto mais vívido.
