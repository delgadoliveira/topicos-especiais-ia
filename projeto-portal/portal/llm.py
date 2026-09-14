"""
Dois motores de resposta para a imersão.

  - MOCK_LLM=1: simulador Python local. Nenhum modelo de IA é executado,
    nenhuma API é chamada e nenhum token é necessário.
  - MOCK_LLM=0: modelo Qwen pela API OpenAI-compatible do Hugging Face.

O simulador serve para validar código, interface, guardrails e testes
determinísticos. A API real é opcional e serve para comparar qualidade.
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time

DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct"
BASE_URL = "https://router.huggingface.co/v1"
_CACHE: dict[str, str] = {}
_real_calls = 0
_STATE_LOCK = threading.Lock()


def _is_mock() -> bool:
    return os.getenv("MOCK_LLM", "1").strip() in ("1", "true", "True")


def is_mock_mode() -> bool:
    """Informa aos demais modulos se chamadas de rede estao desativadas."""
    return _is_mock()


def get_token() -> str | None:
    """Procura o HF_TOKEN no ambiente e, se estiver no Colab, no userdata."""
    token = os.getenv("HF_TOKEN")
    if token:
        return token.strip()
    try:  # Colab
        from google.colab import userdata  # type: ignore

        return userdata.get("HF_TOKEN")
    except Exception:
        return None


def get_model() -> str:
    return os.getenv("MODEL", DEFAULT_MODEL)


def runtime_summary() -> str:
    """Explica sem ambiguidade qual motor produz a resposta."""
    if _is_mock():
        return "simulador local · nenhum modelo de IA · sem API"
    return f"modelo real: {get_model()} · API do Hugging Face"


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name, "").strip()
    if not value:
        return default
    try:
        return max(0, int(value))
    except ValueError as exc:
        raise RuntimeError(f"{name} deve ser um número inteiro maior ou igual a zero.") from exc


def _cache_enabled() -> bool:
    return os.getenv("LLM_CACHE", "1").strip().lower() not in ("0", "false", "no")


def _cache_key(
    messages: list[dict], model: str, max_tokens: int, temperature: float
) -> str:
    payload = json.dumps(
        {
            "messages": messages,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _reserve_real_call() -> None:
    global _real_calls
    limit = _env_int("MAX_REAL_CALLS", 3)
    with _STATE_LOCK:
        if limit and _real_calls >= limit:
            raise RuntimeError(
                f"Limite de chamadas reais ({limit}) atingido nesta sessao. "
                "Continue com MOCK_LLM=1 ou reinicie o portal com um novo limite."
            )
        _real_calls += 1


def usage_summary() -> str:
    """Texto curto para mostrar aos alunos o consumo da sessão."""
    if _is_mock():
        return "simulador local · 0 chamadas reais"
    limit = _env_int("MAX_REAL_CALLS", 3)
    with _STATE_LOCK:
        used = _real_calls
    return f"Chamadas reais: {used}/{limit}" if limit else f"Chamadas reais: {used}"


def _mock_answer(messages: list[dict]) -> str:
    """Resposta determinística do simulador; não executa um modelo de IA."""
    user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    palavras = user.split()
    trecho = " ".join(palavras[:25])
    return (
        f"[MOCK · modo offline] Resposta simulada para: {trecho}"
        + ("..." if len(palavras) > 25 else "")
    )


def chat(
    messages: list[dict],
    model: str | None = None,
    max_tokens: int = 300,
    temperature: float = 0.3,
    retries: int = 2,
    timeout: float = 30.0,
) -> str:
    """Envia mensagens estilo OpenAI e devolve o texto da resposta.

    `messages` = [{"role": "system"|"user"|"assistant", "content": "..."}]
    """
    if _is_mock():
        return _mock_answer(messages)

    token = get_token()
    if not token:
        raise RuntimeError(
            "HF_TOKEN não encontrado. Crie um token gratuito em "
            "https://huggingface.co/settings/tokens e exporte como HF_TOKEN "
            "(ou rode com MOCK_LLM=1 para testar sem rede)."
        )

    from openai import OpenAI  # import tardio: não trava quem só usa MOCK

    client = OpenAI(base_url=BASE_URL, api_key=token, timeout=timeout)
    model = model or get_model()
    cache_key = _cache_key(messages, model, max_tokens, temperature)
    if _cache_enabled():
        with _STATE_LOCK:
            cached = _CACHE.get(cache_key)
        if cached is not None:
            return cached

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        _reserve_real_call()
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            answer = (resp.choices[0].message.content or "").strip()
            if _cache_enabled():
                with _STATE_LOCK:
                    _CACHE[cache_key] = answer
            return answer
        except Exception as exc:  # rate limit, cold start, 503, timeout...
            last_error = exc
            if attempt < retries:
                time.sleep(1.5 * (attempt + 1))  # backoff simples
    raise RuntimeError(
        f"O modelo não respondeu após {retries + 1} tentativas ({last_error}). "
        "Tente de novo em alguns segundos ou rode com MOCK_LLM=1."
    )
