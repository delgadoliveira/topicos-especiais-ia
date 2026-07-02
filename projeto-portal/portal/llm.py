"""
Acesso ao modelo — 100% open source e gratuito via Hugging Face.

Regras de ouro (para a aula não travar):
  - MOCK_LLM=1  -> não chama a rede; devolve resposta determinística.
                   Use para testar contrato/UI/evals sem gastar chamadas.
  - Sem token   -> erro claro e amigável (não uma stack trace).
  - Falha de rede -> tenta de novo (retry com backoff) e usa timeout curto.

Token: pegue um gratuito em https://huggingface.co/settings/tokens (role "read")
e exporte como HF_TOKEN (ou, no Colab, use userdata).
"""
from __future__ import annotations

import os
import time

DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct"
BASE_URL = "https://router.huggingface.co/v1"


def _is_mock() -> bool:
    return os.getenv("MOCK_LLM", "").strip() in ("1", "true", "True")


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


def _mock_answer(messages: list[dict]) -> str:
    """Resposta determinística para modo offline/aula."""
    user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    palavras = user.split()
    trecho = " ".join(palavras[:25])
    return f"[MOCK] Resposta simulada para: {trecho}" + ("..." if len(palavras) > 25 else "")


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

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return (resp.choices[0].message.content or "").strip()
        except Exception as exc:  # rate limit, cold start, 503, timeout...
            last_error = exc
            if attempt < retries:
                time.sleep(1.5 * (attempt + 1))  # backoff simples
    raise RuntimeError(
        f"O modelo não respondeu após {retries + 1} tentativas ({last_error}). "
        "Tente de novo em alguns segundos ou rode com MOCK_LLM=1."
    )
