"""
Agente de EXEMPLO (completo e funcional): Resumidor de Textos.

Estude este arquivo: ele é o modelo do que você vai construir.
Copie `agents/_template_agent.py` para criar o seu.
"""
from portal.base import AgentResult
from portal import llm


class ResumidorAgent:
    # --- metadados (aparecem no portal) ---
    slug = "resumidor"
    name = "Resumidor de Textos"
    emoji = "✂️"
    description = "Resume um texto longo em até 3 tópicos curtos, em português."

    # --- a tarefa ---
    def run(self, message, history):
        steps = [
            "Recebi o texto do usuário",
            "Pedi ao modelo um resumo em até 3 tópicos",
        ]
        resumo = llm.chat(
            [
                {
                    "role": "system",
                    "content": "Você resume textos em português. Devolva no máximo "
                    "3 tópicos curtos, começando cada um com '- '.",
                },
                {"role": "user", "content": f"Resuma o texto a seguir:\n\n{message}"},
            ],
            max_tokens=200,
        )
        return AgentResult(answer=resumo, steps=steps)


# O portal descobre o agente por esta variável:
AGENT = ResumidorAgent()
