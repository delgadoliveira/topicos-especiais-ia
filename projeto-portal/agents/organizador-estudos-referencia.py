"""Caso resolvido dos encontros 5 e 6: os cinco componentes em versão mínima."""
import re

from portal import llm
from portal.base import AgentResult


def planejar_blocos(minutos):
    """Tool local: transforma tempo disponível em até três blocos possíveis."""
    quantidade = max(1, min(3, (minutos + 19) // 20))
    duracao = min(20, max(1, minutos // quantidade))
    return f"{quantidade} bloco(s) de até {duracao} minuto(s)"


TOOLS = {"planejar_blocos": planejar_blocos}
NUMEROS_SIMPLES = {
    "cinco": 5,
    "dez": 10,
    "quinze": 15,
    "vinte": 20,
    "trinta": 30,
    "quarenta": 40,
    "cinquenta": 50,
    "sessenta": 60,
}


def executar_tool(nome, argumento):
    """Executor explícito: somente tools conhecidas podem rodar."""
    if nome not in TOOLS:
        raise ValueError(f"Tool não permitida: {nome}")
    return TOOLS[nome](argumento)


def memoria_curta(history, limite=2):
    """Recupera somente as mensagens recentes do usuário."""
    mensagens = [
        item.get("content", "").strip()
        for item in history
        if item.get("role") == "user" and item.get("content", "").strip()
    ]
    return "\n".join(mensagens[-limite:])


def extrair_minutos(texto):
    """Extrai um tempo simples em minutos; retorna None quando ele não existe."""
    minutos = re.search(r"\b(\d{1,3})\s*(?:min|minuto|minutos)\b", texto, re.I)
    if minutos:
        return int(minutos.group(1))
    minutos_por_extenso = re.search(
        rf"\b({'|'.join(NUMEROS_SIMPLES)})\s*(?:min|minuto|minutos)\b",
        texto,
        re.I,
    )
    if minutos_por_extenso:
        return NUMEROS_SIMPLES[minutos_por_extenso.group(1).lower()]
    horas = re.search(r"\b(\d{1,2})\s*(?:h|hora|horas)\b", texto, re.I)
    return int(horas.group(1)) * 60 if horas else None


def formatar_resposta(conteudo):
    return (
        "Plano de estudo\n\n"
        f"{conteudo}\n\n"
        "Próximo passo: escolha a primeira prioridade e comece agora."
    )


def tem_tarefa_de_estudo(texto):
    """Distingue uma tarefa real de uma mensagem que informa apenas o tempo."""
    palavras = re.findall(r"[a-zá-úç]+", texto.lower())
    palavras_genericas = {
        "agora", "ainda", "apenas", "disponível", "disponivel", "hoje",
        "informei", "min", "minuto", "minutos", "monte", "plano", "para",
        "por", "só", "so", "tempo", "tenho", "um", "uma",
    }
    return any(
        palavra not in palavras_genericas
        and palavra not in NUMEROS_SIMPLES
        and len(palavra) > 2
        for palavra in palavras
    )


def resposta_valida(conteudo):
    """Contrato operacional verificável também pelo simulador determinístico."""
    prioridades = re.findall(
        r"(?ms)^\s*(?:\*\*)?([1-3])[.)](.*?)(?=^\s*(?:\*\*)?[1-3][.)]|\Z)",
        conteudo,
    )
    if [numero for numero, _ in prioridades] != ["1", "2", "3"]:
        return False

    for _, prioridade in prioridades:
        texto = prioridade.lower()
        if "motivo:" not in texto:
            return False
        acao = re.search(r"(?:ação|acao):\s*(.*)", prioridade, re.I | re.S)
        if not acao:
            return False
        duracoes = re.findall(
            r"\b(\d{1,3})\s*(?:min|minuto|minutos)\b",
            acao.group(1),
            re.I,
        )
        if not duracoes or any(int(duracao) > 20 for duracao in duracoes):
            return False

    return len(formatar_resposta(conteudo)) <= 900


def resposta_offline(blocos):
    """Saída fixa do simulador: demonstra o contrato sem fingir raciocínio."""
    duracao = re.search(r"até (\d+) minuto", blocos).group(1)
    return (
        f"1. Assunto principal — motivo: começar pelo mais importante; ação: estude por {duracao} minutos.\n"
        f"2. Segundo assunto — motivo: consolidar a sequência; ação: revise um exemplo por {duracao} minutos.\n"
        f"3. Revisão final — motivo: verificar o aprendizado; ação: explique o que entendeu por {duracao} minutos."
    )


class OrganizadorEstudosReferencia:
    slug = "organizador-estudos-referencia"
    name = "Organizador de Estudos (referência)"
    emoji = "📚"
    description = "Exemplo resolvido: transforma anotações em um plano curto."

    def run(self, message, history):
        text = message.strip()
        events = ["OBSERVE · validei a mensagem atual"]
        if not text:
            return AgentResult(
                answer="Envie uma matéria ou tarefa e o tempo disponível para eu organizar.",
                steps=events + ["STOP · entrada vazia recusada pelo guardrail"],
            )
        if len(text) > 4000:
            return AgentResult(
                answer="O texto é muito longo. Envie até 4.000 caracteres.",
                steps=events + ["STOP · limite de tamanho aplicado pelo guardrail"],
            )

        lembranca = memoria_curta(history)
        contexto = "\n".join(parte for parte in (lembranca, text) if parte)
        events.append(
            "MEMORY · recuperei mensagens recentes"
            if lembranca
            else "MEMORY · primeiro turno, sem lembrança anterior"
        )

        if not tem_tarefa_de_estudo(contexto):
            return AgentResult(
                answer="Qual matéria ou tarefa você precisa estudar?",
                steps=events + ["THINK · faltou a tarefa de estudo", "STOP · pedi o dado ausente"],
            )

        minutos = extrair_minutos(text)
        if minutos is None:
            minutos = extrair_minutos(lembranca)
        if minutos is None or minutos <= 0:
            return AgentResult(
                answer="Quanto tempo maior que zero você tem disponível para estudar hoje?",
                steps=events + ["THINK · faltou tempo disponível", "STOP · pedi o dado ausente"],
            )

        blocos = executar_tool("planejar_blocos", minutos)
        events.append(f"ACT · executei planejar_blocos: {blocos}")
        system_prompt = (
            "Você é um organizador de estudos acolhedor. "
            "Transforme as informações em exatamente três prioridades. "
            "Para cada uma, informe assunto, motivo e uma ação de até 20 minutos. "
            "Use o cálculo fornecido e não invente dados ausentes. "
            "A resposta completa deve ter no máximo 900 caracteres."
        )
        instrucao = (
            f"Contexto recente da conversa:\n{contexto}\n\n"
            f"Resultado da tool de tempo: {blocos}\n"
            "Crie somente as três prioridades; o sistema adicionará o próximo passo."
        )

        resposta = ""
        for tentativa in range(1, 3):
            events.append(f"THINK · tentativa {tentativa}: preparar pedido ao motor")
            resposta = llm.chat(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": instrucao},
                ],
                max_tokens=250,
            ).strip()
            if resposta.startswith("[MOCK · modo offline]"):
                resposta = resposta_offline(blocos)
            events.append(f"REFLECT · tentativa {tentativa}: verificar resposta")
            if resposta_valida(resposta):
                events.append("STOP · resposta válida")
                break
            instrucao += (
                "\nCorrija: use exatamente três itens numerados; em cada item inclua "
                "'motivo:' e 'ação:'; mantenha a resposta final em até 900 caracteres."
            )
        else:
            return AgentResult(
                answer="Não consegui criar um plano curto. Tente reduzir as informações.",
                steps=events + ["STOP · limite de duas tentativas atingido"],
            )

        return AgentResult(
            answer=formatar_resposta(resposta),
            steps=events,
        )


AGENT = OrganizadorEstudosReferencia()
