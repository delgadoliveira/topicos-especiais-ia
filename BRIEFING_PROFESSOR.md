# 🎓 Briefing do professor — Encontros 5 e 6

> **Para que serve este documento.** O `GUIA_PROFESSOR.md` diz *como conduzir*:
> quanto tempo em cada slide, o que perguntar à turma, o que cortar. Ele pressupõe
> que você já domina o conteúdo. **Este documento é o contrário:** ele ensina o
> conteúdo a você, no nível em que um aluno pode te testar.
>
> Cada verbete tem a mesma estrutura:
>
> - **Em uma frase** — a definição que você pode dar de improviso.
> - **Por que existe** — o problema concreto que fez a ideia aparecer. É isto que
>   transforma vocabulário em entendimento.
> - **O erro comum** — a imprecisão que quase todo mundo comete ao explicar, e que
>   um aluno mais atento percebe.
> - **Se perguntarem** — a pergunta que a turma faz de verdade, com a resposta curta.
> - **Fundo** — o que ler se quiser ir além. Opcional.
>
> **Como estudar:** leia os verbetes do Encontro 5 na ordem — eles formam um
> argumento. Os do Encontro 6 podem ser lidos soltos.

---

# Parte I — Encontro 5

Os nove verbetes abaixo estão na ordem do argumento da aula. Se você entender
os verbetes 3, 4 e 6, você dá o encontro inteiro com segurança — eles são o
núcleo, e todo o resto é consequência deles.

---

## 1 · Tarefa longa (long-horizon task)

**Em uma frase.** Um trabalho cujo resultado não cabe em uma única interação,
porque depende de muitas decisões encadeadas, de espera externa, ou de ambas.

**Por que existe.** Porque "longo" confunde três coisas diferentes que precisam
de soluções diferentes:

| O que é longo | Exemplo | O que isso exige |
|---|---|---|
| A **resposta** | um relatório de 40 páginas | nada de especial — é um output grande |
| A **espera** | pedir um documento e aguardar o cliente | estado que sobrevive à espera |
| A **cadeia de decisões** | decidir 400 reembolsos, um a um | critério estável + registro por item |

Só os dois últimos são tarefa longa. O primeiro é só um texto grande.

**O erro comum.** Chamar de tarefa longa tudo que demora. Um modelo que pensa por
três minutos antes de responder **não** está executando uma tarefa longa — está
produzindo uma resposta devagar. A diferença é se o resultado de um passo vira
entrada do próximo.

**Se perguntarem.** *"Então é só uma questão de quantidade de tokens?"* Não. Uma
tarefa curta pode gastar muitos tokens (um resumo de livro) e um workflow longo
pode gastar poucos, porque passa a maior parte do tempo **esperando** — um
e-mail ser respondido, um pagamento compensar, um humano aprovar. O que define
tarefa longa é a **dependência entre passos**, não o consumo.

---

## 2 · Sessão e contexto

**Em uma frase.** **Contexto** é o texto que o modelo enxerga nesta chamada;
**sessão** é a conversa que acumula esse texto ao longo do tempo.

**Por que existe.** Um modelo de linguagem é, por construção, **sem memória**.
Cada chamada é independente: ele recebe um bloco de texto e devolve outro. A
sensação de que "ele lembra" vem de o programa reenviar o histórico inteiro a
cada vez. O contexto tem um teto (a janela de contexto). Quando o histórico
cresce além desse teto, alguma coisa precisa sair.

**O erro comum.** Dizer que o modelo "esqueceu". Ele nunca soube — a informação
simplesmente não foi reenviada. Essa distinção importa porque muda a solução: você
não precisa de um modelo com mais memória, precisa de um sistema que decida
**o que** reenviar.

**Se perguntarem.** *"Janelas de contexto estão ficando enormes. Isso não resolve?"*
Não resolve, por três razões. (a) Custo e latência crescem com o tamanho do
contexto. (b) Modelos degradam em contextos muito longos — informação no meio é
usada pior que informação no começo ou no fim; é o fenômeno conhecido como
*lost in the middle*. (c) Mesmo com janela infinita, a sessão pode cair: processo
reiniciado, token expirado, máquina trocada. **Uma janela maior adia o problema;
não o elimina.**

---

## 3 · Harness ⭐

**Em uma frase.** O programa comum — sem modelo dentro — que fica em volta do
modelo e faz o loop acontecer: monta o contexto, chama o modelo, lê o que ele
pediu, decide se aceita, executa, registra e repete.

**Por que existe.** Porque o modelo não faz nada disso. Ele é uma função de
texto para texto. Tudo o que é "agente" — manter estado, chamar ferramenta,
tentar de novo, parar — é código escrito por alguém.

**O erro comum — e este é o mais importante do encontro.** Dizer que "o modelo
executa a ferramenta". **Ele não executa.** A saída do modelo é um texto
estruturado que *pede* uma ação: `enviar_email(para="x", assunto="y")`. Quem lê
esse pedido, confere se a ferramenta existe, se o valor está dentro do limite, se
aquilo já não foi feito, e então **executa de fato** — com credenciais que o
modelo nunca vê — é o harness.

> **A frase para levar ao quadro:** *o modelo pede, o harness faz.*

Isso tem uma consequência prática que vale dizer em voz alta: **toda a segurança
real mora no harness.** Pedir educadamente ao modelo que não faça algo é uma
sugestão; não dar a ferramenta é um controle.

**O segundo erro comum: tratar harness e agente como sinônimos.** Modelo e
harness são duas peças de software — arquivos que existem no disco, que alguém
escreveu e que você pode abrir. **Agente não é uma terceira peça**: é o nome do
arranjo das duas em loop, perseguindo um objetivo. Ninguém instala um agente;
instala um harness que chama um modelo. Dois testes que resolvem na hora:

- *"Qual arquivo eu abro para mudar isso?"* — para modelo e harness existe
  resposta; para agente e sistema, não.
- *"Desligue o modelo."* — o agente desaparece; o harness continua lá, rodando,
  só sem ninguém a quem perguntar.

Isso importa porque muda onde se põe limite. Quem acha que agente e harness são
a mesma coisa tenta controlar o agente — e a única forma de fazer isso é pelo
prompt, que é sugestão. Quem separa as duas coisas controla o harness, que é
código.

**Se perguntarem.** *"Mas o harness tem um modelo dentro para decidir?"* Não. Ele
é código determinístico: `if`, `try`, lista de ferramentas permitidas, limite de
valor, contador de tentativas. Um harness pode *consultar* um modelo para alguma
decisão, mas as decisões que importam — o que é permitido, o que já foi feito,
quando parar — são regras fixas, justamente porque precisam ser previsíveis.

**Fundo.** Se quiser um exemplo concreto de harness para olhar, qualquer agente
de codificação open-source serve: o loop, a lista de ferramentas e as regras de
parada estão todos em código legível.

---

## 4 · Tool call ⭐

**Em uma frase.** Um pedido de ação, em formato estruturado, emitido pelo modelo
como texto — e executado por outra pessoa no sistema.

**Por que existe.** Um modelo só produz texto. Para que ele afete o mundo, alguém
precisou combinar um formato: "quando quiser agir, escreva assim". O modelo foi
treinado para produzir esse formato; o harness foi programado para entendê-lo.

**O erro comum.** Imaginar que o modelo "tem acesso" aos sistemas. Ele não tem
acesso a nada. Ele tem uma **lista de nomes de ferramentas** com a descrição do
que cada uma faz. O acesso é do harness.

**Se perguntarem.** *"E se o modelo pedir uma ferramenta que não existe, ou com
parâmetro inválido?"* O harness rejeita e devolve o erro como texto na próxima
chamada — o modelo lê "essa ferramenta não existe" e tenta outra coisa. É por
isso que um agente consegue se recuperar de alguns erros sozinho: o erro vira
parte do contexto. É também por isso que ele entra em loop quando o erro não
muda: ele lê a mesma mensagem e repete o mesmo pedido.

---

## 5 · Reset de contexto e compaction

**Em uma frase.** Quando o histórico ultrapassa a janela, o sistema resume o que
passou (**compaction**) ou recomeça (**reset**) — e, nos dois casos, alguma coisa
se perde.

**Por que existe.** É consequência direta do verbete 2. Não é um defeito de
implementação: é aritmética. O histórico cresce sem limite; a janela, não.

**O erro comum.** Achar que compaction é uma versão suave do reset. É pior do que
isso: **o resumo preserva o que parece importante, e o que parece importante é o
que foi dito muitas vezes.** Um critério definido uma única vez no início —
"aprovar só com comprovante anexado" — é exatamente o tipo de coisa que um resumo
descarta, porque apareceu uma vez só. Por isso o caso de abertura da aula tem o
agente aprovando 60 pedidos sem conferir o comprovante: ele não ficou burro,
ele ficou sem o critério.

**Se perguntarem.** *"Como eu sei se houve compaction?"* Na maioria das
ferramentas de consumo, você não sabe — é silencioso. Essa é, por si só, uma boa
pergunta para fazer a um fornecedor: *"quando o contexto estoura, o que acontece,
e eu fico sabendo?"*

---

## 6 · Handoff e artefatos ⭐

**Em uma frase.** Em vez de confiar que a próxima sessão vai *lembrar*, você
escreve fora da conversa o que ela precisa *ler* para continuar.

**Por que existe.** Porque é a única defesa que funciona contra os verbetes 2 e 5.
Se o estado mora na conversa, ele morre com a conversa. Se mora em um arquivo, em
uma tabela ou em um ticket, ele sobrevive — ao reset, à troca de ferramenta, à
troca de modelo e à troca de pessoa.

**Os quatro campos de um handoff utilizável:**

| Campo | Pergunta que responde | Exemplo da fila de reembolsos |
|---|---|---|
| **Critério** | com que régua eu decido? | "aprovar até R$ 500 com comprovante legível; acima disso, escalar" |
| **Estado** | onde eu parei? | "pedidos 1 a 90 decididos; 30 aguardando documento" |
| **Pendências** | o que está esperando algo? | "pedidos 91 a 120: e-mail enviado em 10/10, prazo 17/10" |
| **Definição de pronto** | como eu sei que acabou? | "todos os 400 com decisão registrada e comprovante conferido" |

O campo que mais falta na prática é o último. Sem ele, "pronto" vira opinião.

**O erro comum.** Tratar handoff como um resumo da conversa. Não é. Resumo é
narrativa do passado; handoff é **instrução para o futuro**. Se o texto começa
com "conversamos sobre...", é resumo.

**Por que isto é a habilidade central do Encontro 5.** É a única coisa da aula
que o aluno aplica na segunda-feira sem comprar nada, sem código e sem permissão
de ninguém — inclusive em trabalho entre humanos. A gravação demonstra essa
ideia; o laboratório 1 fica como prática complementar opcional.

---

## 7 · Sandbox

**Em uma frase.** Um ambiente descartável onde o agente executa, separado do
lugar onde moram os dados e os sistemas de verdade.

**Por que existe.** Porque um agente de horizonte longo gera e roda coisas que
ninguém revisou. Se isso acontece no mesmo lugar onde está o banco de produção, o
custo de um erro deixa de ser "resposta ruim" e passa a ser "incidente".

**O erro comum.** Confundir sandbox com permissão. Sandbox limita **onde** a ação
acontece; permissão limita **qual** ação é possível. Um agente em sandbox com
credencial de administrador continua perigoso.

**Se perguntarem.** *"Isso não deixa o agente inútil?"* Não, porque ele não
precisa de acesso direto: ele pede ao harness, que executa a ação específica e
devolve o resultado. A diferença é que o harness executa *aquela* ação, com
aquele limite — em vez de entregar a chave do sistema inteiro.

---

## 8 · Planner, Generator, Verifier

**Em uma frase.** Separar quem planeja, quem produz e quem **confere** — em vez de
pedir as três coisas ao mesmo modelo na mesma conversa.

**Por que existe.** Por um motivo bem documentado: modelos são maus juízes do
próprio trabalho. Pedir "revise o que você acabou de escrever" produz muito mais
"está ótimo" do que correções, porque o texto produzido já está no contexto e
funciona como evidência a favor de si mesmo.

**O erro comum.** Achar que basta usar outra chamada do mesmo modelo. Ajuda um
pouco, mas o verifier forte **não é um modelo**: é uma regra. "O campo
comprovante está preenchido?" é uma consulta, não um julgamento. Sempre que o
critério puder virar código, ele deve.

**Se perguntarem.** *"E quando o critério não cabe em código?"* Aí use um modelo
como verifier, mas com três cuidados: contexto separado (ele não vê a conversa que
gerou o resultado), critério escrito antes, e uma amostra conferida por humano
para saber o quanto ele acerta. E registre que a verificação foi feita por
julgamento, não por regra.

---

## 9 · Idempotência

**Em uma frase.** A propriedade de uma ação que, repetida, não produz efeito novo.

**Por que existe.** Porque em tarefa longa a repetição é certa, não hipotética: a
sessão cai, alguém reexecuta, o sistema tenta de novo depois de um timeout. Se
"enviar e-mail de cobrança" não for idempotente, o cliente recebe quatro
cobranças.

**O erro comum.** Achar que é um detalhe de engenharia. Não é — é o que separa
"o agente retomou" de "o agente retomou e fez tudo de novo". No caso de abertura
da aula, é exatamente isto que falha quando o agente reenvia e-mails já enviados.

**Como se consegue na prática.** Dando a cada ação uma **chave** derivada do caso,
não do momento: `reembolso-1874-pedido-documento`. Antes de executar, o harness
pergunta: já existe registro com essa chave? Se existe, pula.

---

# Parte II — Encontro 6

A aula agora tem **29 slides e 120 minutos**, centrados na tarefa de Ana.
Para prepará-la, priorize **testar e melhorar o pedido** (21) e **avaliar o
resultado** (16), junto com os exemplos resolvidos no guia do professor.

Os demais verbetes são **aprofundamento opcional do professor**, não conteúdo
obrigatório da gravação. Traduza os fundamentos em perguntas de uso: qual conta,
quais arquivos, quais ações, quem aprova e como parar. Não transforme o encontro
numa sequência de principal, capability, lease, control plane ou protocolos.

---

## 10 · Principal e identidade de agente

**Em uma frase.** **Principal** é uma identidade reconhecida pelo sistema:
pessoa, serviço ou agente. Não é sinônimo de solicitante.

**Por que existe.** Sistemas já executavam automações sem presença humana.
Agentes ampliam o conjunto de decisões que podem ocorrer sob essa identidade.
O registro deve distinguir solicitante, executor e autorização aplicável.

**O erro comum.** Falar em "identidade do agente" como se fosse só um cadastro.
O registro precisa ligar ação, identidade, política ou aprovação e responsável.
A integração pode atuar como serviço ou em nome de usuário. Dono do processo,
sponsor e aprovador podem ser diferentes; nenhum cadastro resolve sozinho a
responsabilidade jurídica.

**Se perguntarem.** *"Não dá para dar um usuário próprio ao agente?"* Dá, e é o
caminho que o mercado seguiu. Mas um usuário próprio sem um humano responsável
atrás só move o problema: na auditoria, a resposta vira "foi o agente", que é
exatamente a resposta que ninguém aceita.

---

## 11 · Mandato ⭐

**Em uma frase.** O registro, feito **antes** da ação, do que foi autorizado — por
quem, para quê, até quanto, até quando e como se prova.

**Por que existe.** Acesso técnico não significa autorização para qualquer uso.
Permissões também podem ser temporárias. O mandato registra a delegação
específica: ação, limites, validade e evidências. Escrevê-lo no prompt não
configura automaticamente esses limites na plataforma.

**Os quatro campos:**

1. **Responsável** — quem delega e qual aprovador ou política autoriza a ação.
2. **O quê e até quanto** — a ação e o teto.
3. **Até quando** — prazo e condições de suspensão ou revisão.
4. **Como se prova** — o que fica registrado para alguém conferir depois.

Esses campos são um **roteiro didático**, não o schema técnico do AP2.

**O erro comum.** Escrever o campo 4 como "fica no log". Log não é prova se
ninguém consegue responder, a partir dele, *qual ação pertenceu a qual mandato*.

**Se perguntarem.** *"Isso não é burocracia que trava tudo?"* A pergunta que
desarma: *se este agente fizer algo indevido amanhã, como alguém descobre, e em
quanto tempo?* Se a resposta for "alguém perceberia", não há mandato — há
esperança. O mandato existe para que a autonomia possa **crescer**: sem ele,
toda ampliação de escopo é uma aposta.

---

## 12 · Capability e lease

**Em uma frase.** **Capability** é uma permissão estreita o bastante para caber na
frase da tarefa; **lease** é essa permissão com prazo de validade.

**Por que existe.** Papéis amplos podem conceder mais acesso que a tarefa exige.
O exemplo didático é "pode pagar reembolsos até R$ 500 nesta fila, hoje",
em vez de acesso irrestrito ao financeiro. Sistemas podem combinar papéis,
atributos, escopo, orçamento e prazo.

**O erro comum.** Confundir expiração de um acesso com cancelamento de todas as
ações. A política deve ser revalidada na execução, inclusive em tarefas em fila.
Férias não revogam automaticamente credenciais; pode ser preciso suspender,
transferir e revisar a delegação.

---

## 13 · Catálogo, portaria e cofre ⭐

**Em uma frase.** Três controles fora da **decisão textual do modelo**:
o que ele pode usar (catálogo), por onde ele passa (portaria), e onde ficam as
credenciais que não devem entrar no contexto do modelo (cofre).

**Por que existe.** Se a regra está só no prompt, ela compete com outros textos —
inclusive com texto que veio de fora, de um e-mail ou de um documento que o agente
leu. O harness, um gateway e os serviços de destino podem aplicar controles
independentes da decisão do modelo. Esse código também precisa ser correto,
configurado e testado; não é infalível só por estar fora do prompt.

| Controle | Pergunta que responde | Onde mora |
|---|---|---|
| **Catálogo** | quais ferramentas existem para este agente? | registro do sistema |
| **Portaria** | esta chamada específica pode passar? | gateway, antes da execução |
| **Cofre** | quem tem a credencial? | serviço de segredos; o executor a usa sem expô-la ao modelo |

**O erro comum.** Apresentar isso como tema de segurança da informação. É tema de
**operação**: é o que permite ampliar autonomia sem refazer a análise de risco
toda vez, porque o limite não depende de o agente se comportar bem.

**Se perguntarem.** *"Mas o modelo não poderia simplesmente ser instruído a não
fazer isso?"* Poderia, e vai obedecer na maioria das vezes. A questão não é a
maioria das vezes: é que uma instrução não dá garantia, e por isso não dá para
confiar só nela. Remover a ferramenta perigosa reduz o alcance; ainda é preciso
verificar acessos indiretos e outros canais disponíveis.

---

## 14 · MCP e A2A

**Em uma frase.** Dois protocolos abertos: **MCP** padroniza como um agente
conversa com ferramentas e dados; **A2A**, como agentes conversam entre si.

**Por que existe.** Padrões podem reduzir integrações sob medida. Não eliminam
trabalho de migração de dados, regras, estado e histórico. Um conector próprio
não é automaticamente inadequado.

**O erro comum — e é o ponto do slide.** Tratar interoperabilidade como se fosse
confiança. **Falar o mesmo protocolo não é estar autorizado.** MCP resolve o
"como conversar"; quem pode pedir o quê continua sendo decisão sua, no catálogo e
na portaria. Um agente externo falando MCP perfeitamente continua sendo um
desconhecido.

**Para situar.** MCP nasceu na Anthropic e integra a AAIF. A2A nasceu no Google
e é um projeto da Linux Foundation. Não fundir as duas governanças. Em ambos,
suportar o protocolo não prova segurança nem dá acesso aos sistemas da empresa.

---

## 15 · Não repúdio

**Em uma frase.** Evidência verificável de autoria e integridade que permite
sustentar a atribuição de uma ação ou autorização. Não é uma garantia jurídica
automática nem um campo de cadastro.

**Por que existe.** Porque sem ela a discussão depois do incidente não termina.
É o termo que conecta o encontro ao mundo de pagamentos, onde essa necessidade
já era resolvida há décadas — e é por isso que o comércio agêntico virou um tema
de infraestrutura, não de IA.

**O erro comum.** Confundir com log. Log registra que algo aconteceu. Não repúdio
exige que o registro esteja ligado a **uma autorização prévia identificável** — ou
seja, ao mandato, com mecanismos adequados de integridade e autenticação.
Registrar um sponsor ajuda na governança, mas não prova cada autorização.

---

## 16 · Métricas de resultado ⭐

**Em uma frase.** Medir o trabalho concluído e aceito, não o esforço gasto nem a
atividade gerada.

**Por que existe.** Porque as métricas fáceis de coletar são todas de input —
conversas iniciadas, tarefas disparadas, tokens consumidos — e todas sobem quando
o agente está indo mal. Um agente que erra e tenta de novo gera mais atividade
que um agente que acerta de primeira.

| Pergunta de negócio | Métrica que responde | Métrica que engana |
|---|---|---|
| Ele resolve sozinho e corretamente? | casos elegíveis aceitos sem intervenção, com qualidade e reabertura acompanhadas | casos fechados sem conferir resolução |
| O que entrega é aceito? | aceitação na primeira revisão | tarefas iniciadas |
| Quanto custa cada resultado? | custo por caso resolvido, **incluindo** retentativas e revisão | custo por token |
| Dá para confiar de novo? | retrabalho nas semanas seguintes | satisfação declarada logo após o uso |

**O erro comum.** Medir só depois de ligar. Sem **linha de base** — quanto custa e
quanto demora o mesmo trabalho feito hoje, do jeito atual — não existe comparação
possível, e a discussão vira anedota. A linha de base precisa ser levantada
*antes* do piloto, com a mesma régua que será usada depois.

**Se perguntarem.** *"E ganho de produtividade?"* Traduza para entrega aceita,
prazo e custo total, sem presumir que minutos poupados viram receita ou redução
de quadro. No exemplo do slide 22 do E6: R$ 2.000/80 aceitos = R$ 25 por aceito,
igual à linha de base de R$ 2.500/100. Custou menos porque entregou menos;
qualidade, cobertura e pendências ainda precisam ser examinadas.

---

## 17 · Agent sprawl

**Em uma frase.** A multiplicação de agentes ligados por áreas diferentes, sem
inventário, sem dono e sem data de desligamento.

**Por que existe.** Porque criar um agente ficou barato e não exige o time de TI.
O padrão é o mesmo de ondas anteriores — planilhas críticas, aplicativos não
homologados, robôs de automação — com uma diferença: estes agem sozinhos e têm
credenciais.

**O movimento prático.** Comece uma lista: agente, finalidade, responsável e
substituto, conexões, ações, frequência, revisão e caminho de suspensão.
O inventário inicia o trabalho; não prova que acessos foram limitados.
Compartilhar ou agendar amplia alcance e exige nova conferência.

---

## 18 · Agentic misalignment e o Project Vend

**Em uma frase.** Situações documentadas em que agentes, sob pressão de objetivo,
escolheram ações que ninguém pediu e que contrariavam a intenção de quem delegou.

**Por que existe no encontro.** Não como alarme, mas como evidência de um ponto
operacional: **o problema não foi o agente errar uma resposta — foi ele perseguir
o objetivo dado com mais literalidade do que se esperava.** Um agente otimiza o
que foi escrito, não o que foi pretendido.

**O erro comum.** Contar o caso como curiosidade sobre IA se comportar mal. O
valor do caso é outro: ele mostra que, quanto mais longo o horizonte, mais
decisões acontecem sem ninguém olhando — e mais o limite precisa estar na
ferramenta, não na intenção.

**Se perguntarem.** *"Isso é risco real ou laboratório?"* As situações de
chantagem e autopreservação do relatório da Anthropic são simulações
controladas; suas taxas não medem incidência em empresas. Project Vend é outro
tipo de experimento, uma loja operada com ferramentas e apoio humano. A fonte
aponta melhorias no modelo e no scaffolding como caminhos complementares.
O incidente do verbete 19 tem impacto real, mas não prova que os mecanismos de
chantagem das simulações tenham ocorrido em produção.

---

## 19 · O incidente relatado pela Hugging Face ⭐

**Em uma frase.** O [comunicado primário de julho de 2026](https://huggingface.co/blog/security-incident-july-2026)
relata uma intrusão conduzida por um sistema autônomo de agentes, acesso a
dados internos e credenciais e medidas de detecção, contenção e recuperação.

**Por que existe no encontro.** Mostra a necessidade de registrar trajetórias,
detectar ações inesperadas, revogar credenciais e conferir efeitos nos sistemas.
A lição para o usuário é interromper e reportar, não improvisar recuperação.

**Limite da fonte.** O comunicado inicial ainda não identifica o modelo.
Não atribuir a ele números de agentes, motivações ou detalhes de relatórios
posteriores. Não inferir que todos os controles estavam ausentes.

**Se perguntarem.** *"Vazou dado de cliente?"* O comunicado relatava acesso a
um conjunto limitado de dados internos e credenciais, e avaliação de impacto
ainda em curso. Não havia evidência de adulteração de modelos, datasets ou
Spaces públicos; isso não é a mesma coisa que provar ausência de todo vazamento.
Um incidente real não mede frequência nem valida todos os cenários simulados.

---

## 20 · Demonstrações dos dois encontros ⭐

**Encontro 5:** o slide 22 mantém o simulador de travessia de reset. Há oito
artefatos possíveis; transcrição completa e token não são um bom handoff.

**Encontro 6:** os slides 10–16 mostram casos de teste, uma resposta errada,
a correção e a comparação entre versões do pedido. São exemplos preparados
com fontes fictícias, não medições de desempenho de um modelo.

O simulador de autorização de reembolsos da versão anterior saiu do deck e
não é mais carregado na página. A aula mantém o mesmo caso de cotação de Ana,
sem abrir outra fila nem uma taxonomia de controles.

**Como usar no Encontro 5 assíncrono.** Grave primeiro o cenário com só a
transcrição completa: a tarefa não atravessa. Acrescente os campos necessários
e explique por que cada resultado muda. Quem assiste pode explorar por conta
própria, mas não precisa interromper a gravação nem fazer um laboratório.

**O erro comum.** Mudar controles sem explicar a relação entre o campo salvo
e a falha evitada. A demonstração precisa fazer sentido sem participação ao vivo.

---

## 21 · Testar e melhorar o pedido ⭐

**Em uma frase.** É o ciclo do usuário: definir o esperado, executar uma versão,
comparar com evidência, corrigir a causa e retestar. “Inner loop de validação”
é um nome possível, não um conceito que o aluno precise decorar. Não é o loop
de execução do agente nem uma ordem para revisar indefinidamente a própria resposta.

**Como fazer sem programar.** Separe quatro casos fictícios: um completo, um com
informação ausente, um fora do escopo e um com instrução em documento externo.
Escreva o gabarito antes. Rode cada caso em conversa nova, com as mesmas fontes,
modelo e ferramentas restritas. Registre versão, saída e passa/falha para
conteúdo, evidência, formato e ações.

**Exemplo.** Se o prompt v1 inventa renovação automática, explicite em v2:
“quando a proposta não informar essa condição, marque não informado e pendente”.
Reteste todos os casos, não só o que falhou. Acrescente casos novos e repita os
críticos; uma execução boa não mede variabilidade.

**O erro comum.** Pedir “dê uma nota de 0 a 10 para meu prompt” e tratar uma nota
alta como aprovação. O avaliador deve comparar saídas com critérios e fontes;
outro chat ou modelo também pode errar. Sem evidência não passa. Nenhuma média
compensa ação não autorizada.

**Quando parar de reescrever.** Se falta acesso, a fonte está errada ou não existe
bloqueio de ferramenta, a causa não é resolvida com mais palavras. Reduza o
escopo ou peça apoio. No pequeno lote didático, quatro de quatro sem violação
crítica permite o próximo teste controlado, não uma expansão automática.
O roteiro completo e o prompt de comparação estão no guia, slides 10–14 do E6.

---

# 📌 Se você só tiver uma hora para estudar

Leia, nesta ordem, e você dá as duas aulas:

1. **Verbete 3 (harness)** e **4 (tool call)** — a frase "o modelo pede, o harness
   faz" sustenta metade do Encontro 5 e explica por que segurança não é prompt.
2. **Verbete 6 (handoff)** — é o princípio aplicado na demonstração de reset.
3. **Verbete 21 (testar e melhorar)** — prepara a demonstração central do E6:
   fonte, erro, correção e comparação de versões.
4. **Verbete 16 (métricas de resultado)** — liga uso a qualidade, prazo e custo.
5. **Verbete 20 (demonstrações)** e o guia — prepare os exemplos antes da gravação.
   Os verbetes técnicos da Parte II ficam disponíveis para dúvidas, não para leitura sequencial.

---

# 🙋 As cinco perguntas que a turma faz todo semestre

**"Qual ferramenta/modelo devo usar?"**
Comece pela plataforma aprovada e disponível na organização. Confira se oferece
as fontes, ações e controles necessários para a tarefa. O nome do modelo não
substitui um teste pequeno com resultado que o usuário consiga conferir.

**"Isso tudo não vai ser resolvido pelo próximo modelo?"**
Parte sim: o horizonte cresce rápido. Mas três coisas não vêm do modelo —
**prova** de que o trabalho ficou pronto, **autorização** registrada antes da ação,
e **responsabilidade** por ela. Essas três são organizacionais.

**"Meu agente faz isso num prompt só. Por que complicar?"**
Funciona enquanto a tarefa é curta e o erro é barato. O curso é sobre o que muda
quando o trabalho dura horas e o erro custa dinheiro. Pergunte: *e se der errado
no item 300 de 400?*

**"Quem é responsável quando o agente erra?"**
Registre quem pediu, quem pode aprovar e quem trata uma exceção. Responsabilidade
jurídica depende das regras e circunstâncias; não decorre automaticamente de
quem apertou “iniciar”. No caso de Ana, análise e compra são decisões separadas.

**"Isso vai substituir o meu trabalho?"**
Resposta honesta e curta: muda a unidade do trabalho. Quem decidia caso a caso
passa a escrever critério, conferir amostra e responder pelo lote. O caso da
Klarna, no Encontro 5, é o contraexemplo útil — automatizaram atendimento e
voltaram a contratar pessoas quando a métrica dominante era custo.
