"""
Registro de agentes — descobre automaticamente tudo em agents/.

Cada aluno cria UM arquivo: agents/<seu-slug>.py, que expõe uma variável
de módulo chamada AGENT (a instância do agente).

Tolerante a falhas de propósito: se o agente de um aluno quebrar (erro de
import, dependência faltando, token ausente), o portal continua de pé e
mostra o erro na tela, em vez de derrubar a turma inteira.
"""
from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass

from . import base


@dataclass
class LoadError:
    module: str
    reason: str


def discover(package: str = "agents") -> tuple[dict[str, object], list[LoadError]]:
    """Importa cada módulo de `agents/` e coleta os que expõem AGENT válido."""
    agents: dict[str, object] = {}
    errors: list[LoadError] = []

    pkg = importlib.import_module(package)
    for mod in pkgutil.iter_modules(pkg.__path__):
        name = mod.name
        if name.startswith("_"):  # _template_agent.py e afins são ignorados
            continue
        dotted = f"{package}.{name}"
        try:
            module = importlib.import_module(dotted)
        except Exception as exc:  # erro no import do aluno não derruba o portal
            errors.append(LoadError(dotted, f"falha ao importar: {exc}"))
            continue

        agent = getattr(module, "AGENT", None)
        if agent is None:
            errors.append(LoadError(dotted, "não expõe a variável AGENT"))
            continue

        problems = base.validate_agent(agent)
        if problems:
            errors.append(LoadError(dotted, "; ".join(problems)))
            continue

        slug = agent.slug
        if slug in agents:
            errors.append(LoadError(dotted, f"slug duplicado: '{slug}' já existe"))
            continue

        agents[slug] = agent

    return agents, errors
