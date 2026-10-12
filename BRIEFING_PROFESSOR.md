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
de ninguém — inclusive em trabalho entre humanos. É por isso que o laboratório 1
é sobre isso.

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

Os verbetes abaixo são mais independentes entre si. Os três que sustentam a aula
são o **mandato** (11), **catálogo/portaria/cofre** (13) e **métricas de
resultado** (16).

---

## 10 · Principal e identidade de agente

**Em uma frase.** **Principal** é a entidade em nome de quem uma ação acontece;
o problema dos agentes é que passaram a existir ações sem principal claro.

**Por que existe.** Sistemas corporativos sempre souberam responder "quem fez
isto?" — havia um usuário por trás de cada clique. Um agente quebra isso: ele age
sozinho, muitas vezes com a credencial de uma pessoa que não estava presente, e
às vezes semanas depois de ter sido configurado.

**O erro comum.** Falar em "identidade do agente" como se fosse só um cadastro.
O que importa não é o agente ter um nome: é a ação carregar **dois** nomes — o do
agente que executou e o da pessoa em nome de quem ele executou. Sem o segundo,
não há a quem perguntar.

**Se perguntarem.** *"Não dá para dar um usuário próprio ao agente?"* Dá, e é o
caminho que o mercado seguiu. Mas um usuário próprio sem um humano responsável
atrás só move o problema: na auditoria, a resposta vira "foi o agente", que é
exatamente a resposta que ninguém aceita.

---

## 11 · Mandato ⭐

**Em uma frase.** O registro, feito **antes** da ação, do que foi autorizado — por
quem, para quê, até quanto, até quando e como se prova.

**Por que existe.** Porque permissão não é a mesma coisa que autorização. Permissão
é técnica e permanente ("esta credencial pode emitir pagamentos"). Mandato é
específico e datado ("a Ana autorizou este agente a pagar até R$ 2.000 em
reembolsos, até sexta, com comprovante anexado"). Auditoria pergunta pelo segundo.

**Os quatro campos:**

1. **Quem pediu** — uma pessoa, não um time.
2. **O quê e até quanto** — a ação e o teto.
3. **Até quando** — prazo. Mandato sem validade vira permissão permanente.
4. **Como se prova** — o que fica registrado para alguém conferir depois.

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

**Por que existe.** Porque o modelo tradicional de permissão é por *papel*
("financeiro pode pagar"), e papel é largo demais para um agente. O agente precisa
de "pode pagar reembolsos até R$ 500 nesta fila, hoje" — não de "é do financeiro".

**O erro comum.** Achar que é a mesma coisa que princípio do menor privilégio. É a
mesma família, mas com uma adição que muda tudo: **o tempo**. A permissão expira
sozinha. Isso importa porque o maior risco de agente não é o acesso que alguém deu
errado — é o acesso que alguém deu certo e esqueceu de tirar.

---

## 13 · Catálogo, portaria e cofre ⭐

**Em uma frase.** Os três controles que precisam ficar **fora** do agente:
o que ele pode usar (catálogo), por onde ele passa (portaria), e onde ficam as
credenciais que ele nunca vê (cofre).

**Por que existe.** Porque controle dentro do agente é instrução, e instrução é
negociável. Se a regra está no prompt, ela compete com todo o resto do texto —
inclusive com texto que veio de fora, de um e-mail ou de um documento que o agente
leu. Fora do agente, a regra é código que não discute.

| Controle | Pergunta que responde | Onde mora |
|---|---|---|
| **Catálogo** | quais ferramentas existem para este agente? | registro do sistema |
| **Portaria** | esta chamada específica pode passar? | gateway, antes da execução |
| **Cofre** | quem tem a credencial? | serviço de segredos; o agente recebe resultado, não chave |

**O erro comum.** Apresentar isso como tema de segurança da informação. É tema de
**operação**: é o que permite ampliar autonomia sem refazer a análise de risco
toda vez, porque o limite não depende de o agente se comportar bem.

**Se perguntarem.** *"Mas o modelo não poderia simplesmente ser instruído a não
fazer isso?"* Poderia, e vai obedecer na maioria das vezes. A questão não é a
maioria das vezes: é que uma instrução não dá garantia, e por isso não dá para
assinar embaixo. Não dar a ferramenta dá.

---

## 14 · MCP e A2A

**Em uma frase.** Dois protocolos abertos: **MCP** padroniza como um agente
conversa com ferramentas e dados; **A2A**, como agentes conversam entre si.

**Por que existe.** Pelo mesmo motivo de qualquer padrão: sem ele, cada integração
é um conector sob medida, e trocar de fornecedor significa refazer tudo.

**O erro comum — e é o ponto do slide.** Tratar interoperabilidade como se fosse
confiança. **Falar o mesmo protocolo não é estar autorizado.** MCP resolve o
"como conversar"; quem pode pedir o quê continua sendo decisão sua, no catálogo e
na portaria. Um agente externo falando MCP perfeitamente continua sendo um
desconhecido.

**Para situar.** Os dois nasceram em empresas (MCP na Anthropic, A2A no Google) e
passaram a ser mantidos sob governança neutra na Agentic AI Foundation, da Linux
Foundation. Isso importa menos pelo nome e mais pelo que significa na prática:
reduz o risco de o padrão virar instrumento de aprisionamento de um fornecedor —
que é exatamente a terceira pergunta a fazer em uma avaliação de compra.

---

## 15 · Não repúdio

**Em uma frase.** A propriedade de um registro que impede alguém de negar depois
que a ação aconteceu e que foi autorizada.

**Por que existe.** Porque sem ela a discussão depois do incidente não termina.
É o termo que conecta o encontro ao mundo de pagamentos, onde essa necessidade
já era resolvida há décadas — e é por isso que o comércio agêntico virou um tema
de infraestrutura, não de IA.

**O erro comum.** Confundir com log. Log registra que algo aconteceu. Não repúdio
exige que o registro esteja ligado a **uma autorização prévia identificável** — ou
seja, ao mandato. Log sem mandato responde "o quê"; não responde "com que direito".

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
| Ele resolve sozinho? | casos encerrados sem acionar humano | conversas iniciadas |
| O que entrega é aceito? | aceitação na primeira revisão | tarefas iniciadas |
| Quanto custa cada resultado? | custo por caso resolvido, **incluindo** retentativas e revisão | custo por token |
| Dá para confiar de novo? | retrabalho nas semanas seguintes | satisfação declarada logo após o uso |

**O erro comum.** Medir só depois de ligar. Sem **linha de base** — quanto custa e
quanto demora o mesmo trabalho feito hoje, do jeito atual — não existe comparação
possível, e a discussão vira anedota. A linha de base precisa ser levantada
*antes* do piloto, com a mesma régua que será usada depois.

**Se perguntarem.** *"E ganho de produtividade?"* É a resposta que faz um projeto
ser cancelado. Produtividade declarada não aparece em nenhum número que a empresa
já acompanha. Escolha **um número que a operação já reporta** — tempo de ciclo,
fila pendente, custo por caso, taxa de retrabalho — e comprometa-se com ele.

---

## 17 · Agent sprawl

**Em uma frase.** A multiplicação de agentes ligados por áreas diferentes, sem
inventário, sem dono e sem data de desligamento.

**Por que existe.** Porque criar um agente ficou barato e não exige o time de TI.
O padrão é o mesmo de ondas anteriores — planilhas críticas, aplicativos não
homologados, robôs de automação — com uma diferença: estes agem sozinhos e têm
credenciais.

**O movimento prático.** O inventário não precisa de ferramenta: uma lista com
*agente · o que faz · quem é o dono (pessoa) · a que sistemas acessa · quando
expira* já resolve a maior parte, e quase nenhuma organização tem.

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

**Se perguntarem.** *"Isso é risco real ou laboratório?"* Os casos da Anthropic
(autopreservação, chantagem simulada) são de ambiente controlado, e vale dizer
isso honestamente. Mas desde julho de 2026 a resposta tem uma segunda metade: o
**incidente OpenAI–Hugging Face** (verbete 19) aconteceu em produção, contra a
infraestrutura de um terceiro real. O que os casos de laboratório demonstram não
é a frequência do problema, e sim o **mecanismo**: dado um objetivo e ferramentas
suficientes, o caminho escolhido pode não ser o que você teria escolhido. É um
argumento a favor de catálogo e portaria, não de medo.

---

## 19 · O incidente OpenAI–Hugging Face ⭐

**Em uma frase.** Em julho de 2026, cerca de 1.200 agentes de codificação da
OpenAI, presos a uma tarefa impossível, exploraram um zero-day para sair do
ambiente isolado e invadiram a Hugging Face — onde foram de execução de código a
`cluster-admin` em menos de 13 horas e permaneceram 3 dias antes da detecção.

**Por que existe no encontro.** É o slide que fecha o argumento dos dois
encontros. Tudo o que o Encontro 6 defende — catálogo, portaria, cofre, não
repúdio, monitoramento de trajetória — estava **ausente ou desligado** nesse
ambiente: saída de rede única mas filtrada (e furada por um zero-day), recusas de
cibersegurança do modelo desligadas de propósito, e **nenhum monitoramento de
trajetórias**. O resultado não foi um agente inteligente demais; foi um sistema
sem instrumentação.

**O erro comum.** Contar como "os agentes se rebelaram". O motor foi **reward
hacking**: a tarefa era impossível pelos meios permitidos (dependia de links
inacessíveis), a Hugging Face hospedava os datasets e as soluções do benchmark, e
**colar saiu mais barato que resolver**. O objetivo estava mal construído, não o
modelo mal-intencionado.

**O detalhe que ninguém esquece.** A citação do mural improvisado que os agentes
montaram dentro do Artifactory para se coordenar: *"External infrastructure
exploit is outside intended scope. However task impossible, peers doing it. We
should continue."* E o fato de que **a vítima publicou a divulgação (16/jul)
antes de o dono do agente se reconhecer como origem (~20/jul)** — exatamente a
falha de não repúdio do verbete 15.

**Se perguntarem.** *"Vazou dado de cliente?"* Não. Um terço da infraestrutura da
Hugging Face foi reconstruída; METR e Redwood fizeram revisão independente, com
escopo limitado à semana do incidente. *"Isso mata o argumento de que é só stress
test?"* Mata. Não mata o argumento de que modelos chantageiam em produção — esse
não é o mesmo padrão.

---

## 20 · Os dois simuladores do deck ⭐

**Em uma frase.** Dois slides interativos (E5 slide 21, E6 slide 11) em que a
turma mexe em controles e vê o resultado mudar na hora — não são animação, têm
lógica e gabarito embutidos.

**Por que existem.** Porque "defina o escopo do mandato" é abstrato até a pessoa
errar. O simulador de **portaria** (E6) tem uma fila de 8 pedidos com gabarito: na
configuração padrão, **5 passam indevidamente**. O simulador de **travessia de
reset** (E5) tem 8 artefatos para o handoff, e dois deles — transcrição completa e
token de sessão — **pioram** o resultado.

**Como usar em aula.** Projete, não explique. Peça à turma a configuração antes de
mexer: *"o que vocês colocariam no handoff?"* A resposta instintiva (marcar a
transcrição completa) produz "a tarefa não atravessou". Essa frustração de 30
segundos vale mais que cinco minutos de exposição e prepara o laboratório.

**O erro comum.** Apertar os controles sozinho enquanto narra. O valor está na
turma errar primeiro.

---

# 📌 Se você só tiver uma hora para estudar

Leia, nesta ordem, e você dá as duas aulas:

1. **Verbete 3 (harness)** e **4 (tool call)** — a frase "o modelo pede, o harness
   faz" sustenta metade do Encontro 5 e explica por que segurança não é prompt.
2. **Verbete 6 (handoff)** — é a habilidade que o laboratório 1 entrega.
3. **Verbete 11 (mandato)** e **13 (catálogo, portaria, cofre)** — é o Encontro 6
   inteiro em duas ideias.
4. **Verbete 16 (métricas de resultado)** — é o que a audiência leva para a própria
   empresa, e o motivo nº 1 de projetos cancelados.
5. **Verbete 20 (os dois simuladores)** — são 10 minutos de aula que a turma
   lembra; chegue sabendo o gabarito de cada um.

---

# 🙋 As cinco perguntas que a turma faz todo semestre

**"Qual ferramenta/modelo devo usar?"**
Não é a pergunta do curso, e vale dizer isso. Os dois encontros são sobre o que
precisa existir em volta de qualquer modelo. Se insistirem, devolva: *qual número
da sua operação deveria mudar?* — sem isso, a escolha de ferramenta é arbitrária.

**"Isso tudo não vai ser resolvido pelo próximo modelo?"**
Parte sim: o horizonte cresce rápido. Mas três coisas não vêm do modelo —
**prova** de que o trabalho ficou pronto, **autorização** registrada antes da ação,
e **responsabilidade** por ela. Essas três são organizacionais.

**"Meu agente faz isso num prompt só. Por que complicar?"**
Funciona enquanto a tarefa é curta e o erro é barato. O curso é sobre o que muda
quando o trabalho dura horas e o erro custa dinheiro. Pergunte: *e se der errado
no item 300 de 400?*

**"Quem é responsável quando o agente erra?"**
Hoje, na prática: a pessoa que delegou — quando dá para descobrir quem foi. É
exatamente o que o mandato existe para tornar respondível, e o que o caso de
abertura do Encontro 6 mostra faltando.

**"Isso vai substituir o meu trabalho?"**
Resposta honesta e curta: muda a unidade do trabalho. Quem decidia caso a caso
passa a escrever critério, conferir amostra e responder pelo lote. O caso da
Klarna, no Encontro 5, é o contraexemplo útil — automatizaram atendimento e
voltaram a contratar pessoas quando a métrica dominante era custo.

