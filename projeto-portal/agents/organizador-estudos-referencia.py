"""
CASO PEDAGÓGICO RESOLVIDO — Organizador de Estudos.

Este agente acompanha os encontros 5 e 6. Ele mostra uma solução pequena,
com contrato, instrução, guardrails e passos observáveis.
"""
from portal import llm
from portal.base import AgentResult


class OrganizadorEstudosReferencia:
    slug = "organizador-estudos-referencia"
    name = "Organizador de Estudos (referência)"
    emoji = "📚"
    description = "Exemplo resolvido: transforma anotações em um plano curto."

    def run(self, message, history):
        text = message.strip()
        if not text:
            return AgentResult(
                answer="Envie matérias, prazo e tempo disponível para eu organizar.",
                steps=["Entrada vazia recusada"],
            )
        if len(text) > 4000:
            return AgentResult(
                answer="O texto é muito longo. Envie até 4.000 caracteres.",
                steps=["Limite de tamanho aplicado"],
            )

        steps = [
            "Validei a entrada",
            "Pedi três prioridades ao modelo",
        ]
        resposta = llm.chat(
            [
                {
                    "role": "system",
                    "content": (
                        "Você é um organizador de estudos acolhedor. "
                        "Transforme as informações em exatamente três prioridades. "
                        "Para cada uma, informe assunto, motivo e uma ação de até "
                        "20 minutos. Não invente dados ausentes."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Crie um plano para estas informações:\n{text}",
                },
            ],
            max_tokens=250,
        )
        steps.append("Organizei a resposta no formato combinado")

        return AgentResult(
            answer=(
                "Plano de estudo\n\n"
                f"{resposta}\n\n"
                "Próximo passo: escolha a primeira prioridade e comece agora."
            ),
            steps=steps,
        )


AGENT = OrganizadorEstudosReferencia()
