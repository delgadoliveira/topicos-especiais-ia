"""
Observabilidade local — um log simples em JSONL (uma linha por interação).

Princípio: nunca logar segredos. Guardamos metadados úteis para depurar
(slug, latência, status, tamanho da resposta) e um trecho curto da entrada.
"""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
LOG_FILE = LOG_DIR / "interactions.jsonl"

_TOKEN_PATTERN = re.compile(r"hf_[A-Za-z0-9]{10,}")


def _redact(text: str) -> str:
    return _TOKEN_PATTERN.sub("hf_***", text or "")


def log_interaction(
    slug: str,
    message: str,
    answer: str,
    latency_s: float,
    status: str,
    error: str | None = None,
) -> None:
    """Registra uma interação. Falha de log nunca deve quebrar o portal."""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        record = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "slug": slug,
            "status": status,
            "latency_s": round(latency_s, 2),
            "input_preview": _redact(message)[:120],
            "answer_len": len(answer or ""),
            "error": _redact(error) if error else None,
        }
        with LOG_FILE.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass  # observabilidade é best-effort
