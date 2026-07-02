"""
🧑‍🎓 TEMPLATE DO ALUNO — copie este arquivo para agents/<seu-slug>.py

Regras:
  1. Edite SÓ o seu arquivo. Não mexa em portal/ nem no agente dos colegas.
  2. Escolha um slug único, minúsculo e sem espaços (ex: "tutor-sql").
  3. Não faça chamadas de rede/leitura de arquivo no import: só dentro de run().
  4. Escopo de UMA tarefa. Preencha a frase:
       "Meu agente ajuda [usuário] a fazer [tarefa específica]
        usando [entrada] e entregando [saída verificável]."

Arquivos com nome iniciado por "_" são ignorados pelo portal (como este).
"""
from portal.base import AgentResult
from portal import llm


class MeuAgente:
    slug = "meu-agente"          # TODO: troque por um slug único
    name = "Meu Agente"          # TODO
    emoji = "🧠"                  # TODO
    description = "Descreva em uma frase o que ele faz."  # TODO

    def run(self, message, history):
        # Guardrail simples: entrada vazia não vira chamada ao modelo.
        if not message.strip():
            return AgentResult(answer="Envie um texto para eu processar.")

        steps = ["Recebi a mensagem"]  # TODO: registre seus passos

        # TODO: monte o prompt da SUA tarefa.
        resposta = llm.chat(
            [
                {"role": "system", "content": "TODO: instrua o modelo para a sua tarefa."},
                {"role": "user", "content": message},
            ],
            max_tokens=250,
        )
        steps.append("Gerei a resposta")

        return AgentResult(answer=resposta, steps=steps, citations=[])


AGENT = MeuAgente()
