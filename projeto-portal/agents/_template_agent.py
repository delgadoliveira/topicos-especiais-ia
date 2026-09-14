"""
🧑‍🎓 TEMPLATE DO ALUNO — copie este arquivo para agents/<seu-slug>.py

Regras:
  1. Edite SÓ o seu arquivo. Não mexa em portal/ nem no agente dos colegas.
  2. Escolha um slug único, minúsculo e sem espaços (ex: "tutor-sql").
  3. Não faça chamadas de rede/leitura de arquivo no import: só dentro de run().
  4. Escopo de UMA tarefa. Preencha a frase:
       "Meu agente ajuda [usuário] a fazer [tarefa específica]
        usando [entrada] e entregando [saída verificável]."

Este template mostra os cinco componentes em versão mínima:
persona, modelo/simulador, memória curta, uma tool com executor e loop limitado.
Arquivos com nome iniciado por "_" são ignorados pelo portal (como este).
"""
from portal.base import AgentResult
from portal import llm


def minha_tool(texto):
    """TODO: faça um cálculo ou transformação pequena e previsível."""
    return len(texto.split())


TOOLS = {"contar_palavras": minha_tool}


def executar_tool(nome, argumento):
    if nome not in TOOLS:
        raise ValueError(f"Tool não permitida: {nome}")
    return TOOLS[nome](argumento)


def memoria_curta(history, limite=2):
    mensagens = [
        item.get("content", "").strip()
        for item in history
        if item.get("role") == "user" and item.get("content", "").strip()
    ]
    return "\n".join(mensagens[-limite:])


def resposta_valida(resposta):
    """TODO: adapte esta condição de sucesso à promessa do seu agente."""
    return bool(resposta) and len(resposta) <= 900


class MeuAgente:
    slug = "meu-agente"          # TODO: troque por um slug único
    name = "Meu Agente"          # TODO
    emoji = "🧠"                  # TODO
    description = "Descreva em uma frase o que ele faz."  # TODO

    def run(self, message, history):
        text = message.strip()
        events = ["OBSERVE · validei a entrada"]
        if not text:
            return AgentResult(
                answer="Envie um texto para eu processar.",
                steps=events + ["STOP · entrada vazia recusada"],
            )

        lembranca = memoria_curta(history)
        contexto = "\n".join(parte for parte in (lembranca, text) if parte)
        events.append("MEMORY · contexto recente preparado")
        resultado_tool = executar_tool("contar_palavras", contexto)
        events.append(f"ACT · contar_palavras devolveu {resultado_tool}")

        resposta = ""
        instrucao = (
            f"Contexto recente:\n{contexto}\n\n"
            f"A tool contou {resultado_tool} palavras."
        )
        for tentativa in range(1, 3):
            events.append(f"THINK · tentativa {tentativa}")
            resposta = llm.chat(
                [
                    {"role": "system", "content": "TODO: defina persona, tarefa, formato e limite."},
                    {"role": "user", "content": instrucao},
                ],
                max_tokens=250,
            ).strip()
            events.append(f"REFLECT · tentativa {tentativa}")
            if resposta_valida(resposta):
                events.append("STOP · resposta válida")
                break
            instrucao += "\nResponda de forma não vazia e com até 900 caracteres."
        else:
            return AgentResult(
                answer="Não consegui produzir uma resposta curta.",
                steps=events + ["STOP · limite de tentativas atingido"],
            )

        return AgentResult(answer=resposta, steps=events, citations=[])


AGENT = MeuAgente()
