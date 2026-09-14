from __future__ import annotations

import os

from . import llm, runner


def _judge(question: str, answer: str) -> bool | None:
    if llm.is_mock_mode() or not llm.get_token():
        return None
    try:
        verdict = llm.chat(
            [
                {
                    "role": "system",
                    "content": "Responda apenas SIM ou NAO sobre o criterio.",
                },
                {"role": "user", "content": f"{question}\n\nResposta:\n{answer}"},
            ],
            max_tokens=5,
            temperature=0.0,
        )
        return verdict.strip().upper().startswith("SIM")
    except (RuntimeError, ValueError):
        return None


def run_case_details(agent, case: dict) -> tuple[bool, list[str], object]:
    notes: list[str] = []
    ok = True
    history = case.get("history", [])
    if not isinstance(history, list):
        raise ValueError("history precisa ser uma lista")
    result, latency, status = runner.safe_run(agent, case["input"], history)

    if status != "ok":
        return False, [f"execucao falhou: {result.error}"], result

    answer = result.answer or ""
    if not answer.strip():
        ok = False
        notes.append("resposta vazia")

    max_chars = case.get("max_chars")
    if max_chars is not None and len(answer) > int(max_chars):
        ok = False
        notes.append(f"resposta com {len(answer)} caracteres > {max_chars}")

    max_latency = case.get("max_latency_s")
    if max_latency is not None and latency > float(max_latency):
        ok = False
        notes.append(f"latencia {latency:.1f}s > {max_latency}s")

    for needle in case.get("must_contain", []):
        if needle.lower() not in answer.lower():
            ok = False
            notes.append(f"faltou conter: {needle!r}")

    for needle in case.get("must_not_contain", []):
        if needle.lower() in answer.lower():
            ok = False
            notes.append(f"nao deveria conter: {needle!r}")

    for prefix in case.get("must_have_step_prefixes", []):
        if not any(str(step).startswith(prefix) for step in result.steps):
            ok = False
            notes.append(f"faltou evento observavel: {prefix!r}")

    if case.get("judge"):
        verdict = _judge(case["judge"], answer)
        if verdict is True:
            notes.append("juiz: SIM")
        elif verdict is False:
            ok = False
            notes.append("juiz: NAO")
        else:
            notes.append("juiz: pulado (offline/sem token)")

    return ok, notes, result


def run_case(agent, case: dict) -> tuple[bool, list[str]]:
    ok, notes, _ = run_case_details(agent, case)
    return ok, notes
