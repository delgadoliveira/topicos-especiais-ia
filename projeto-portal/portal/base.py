"""
Contrato do portal — a "língua comum" que todo agente precisa falar.

Um agente é qualquer objeto que tenha:
  - slug: str          identificador único, minúsculo, sem espaço (ex: "resumidor")
  - name: str          nome amigável (ex: "Resumidor de Textos")
  - emoji: str         um emoji para a UI
  - description: str   uma frase: o que ele faz
  - run(message, history) -> AgentResult

Não usamos herança obrigatória de propósito: basta o objeto ter esses atributos
e o método run(). Isso mantém o template do aluno o mais simples possível.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AgentResult:
    """O que todo agente devolve. Só `answer` é obrigatório."""
    answer: str
    steps: list[str] = field(default_factory=list)      # eventos de execução observáveis
    citations: list[str] = field(default_factory=list)  # fontes, se houver (RAG)
    error: str | None = None                            # preenchido só em caso de falha


REQUIRED_ATTRS = ("slug", "name", "emoji", "description")


def validate_agent(agent) -> list[str]:
    """Retorna uma lista de problemas encontrados. Lista vazia = agente válido."""
    problems: list[str] = []
    for attr in REQUIRED_ATTRS:
        value = getattr(agent, attr, None)
        if not isinstance(value, str) or not value.strip():
            problems.append(f"atributo '{attr}' ausente ou vazio")
    if not callable(getattr(agent, "run", None)):
        problems.append("método 'run(message, history)' ausente")
    slug = getattr(agent, "slug", "")
    if isinstance(slug, str) and slug and (" " in slug or slug != slug.lower()):
        problems.append("slug deve ser minúsculo e sem espaços (ex: 'meu-agente')")
    return problems
