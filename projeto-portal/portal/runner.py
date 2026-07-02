"""Executa um agente com fronteira de erro + medição de latência + log.

Se o agente de um aluno estourar uma exceção, o portal NÃO cai: devolvemos
um AgentResult de erro amigável e registramos o ocorrido.
"""
from __future__ import annotations

import time

from . import base, observability


def safe_run(agent, message: str, history: list | None = None):
    """Roda agent.run com segurança. Retorna (AgentResult, latencia_s, status)."""
    history = history or []
    t0 = time.time()
    try:
        result = agent.run(message, history)
        # Tolerância: aceita str ou dict, mas o padrão é AgentResult.
        if isinstance(result, str):
            result = base.AgentResult(answer=result)
        elif isinstance(result, dict):
            result = base.AgentResult(
                answer=result.get("answer", ""),
                steps=result.get("steps", []),
                citations=result.get("citations", []),
            )
        elif not isinstance(result, base.AgentResult):
            raise TypeError("run() deve devolver um AgentResult (ou uma string).")
        if not (result.answer or "").strip():
            raise ValueError("run() devolveu uma resposta vazia.")
        status, error = "ok", None
    except Exception as exc:
        result = base.AgentResult(answer=f"⚠️ O agente falhou: {exc}", error=str(exc))
        status, error = "error", str(exc)

    latency = time.time() - t0
    observability.log_interaction(
        getattr(agent, "slug", "?"), message, result.answer, latency, status, error
    )
    return result, latency, status
