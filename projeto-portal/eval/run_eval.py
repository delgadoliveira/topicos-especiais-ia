"""
Mini-harness de avaliação — duas camadas.

  1. Checks determinísticos (sempre rodam, offline): resposta não-vazia,
     latência dentro do limite, substrings obrigatórias/proibidas.
  2. Juiz LLM (opcional): só roda se MOCK_LLM não estiver ligado e houver
     token. Faz uma pergunta sim/não sobre a qualidade da resposta.

Uso:
    python eval/run_eval.py                      # roda todos os casos em eval/cases/
    python eval/run_eval.py resumidor            # roda só os casos do slug 'resumidor'

Formato do caso (eval/cases/<slug>.yaml):
    agent: resumidor
    cases:
      - input: "..."
        max_latency_s: 25
        must_contain: ["- "]        # opcional
        must_not_contain: ["erro"]  # opcional
        judge: "O resumo é fiel ao texto e tem no máximo 3 tópicos?"  # opcional
"""
import glob
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import yaml  # noqa: E402

from portal import registry, runner, llm  # noqa: E402

CASES_DIR = pathlib.Path(__file__).parent / "cases"


def _judge(question: str, answer: str) -> bool | None:
    """Pergunta sim/não ao modelo. Retorna None se não der para julgar."""
    if os.getenv("MOCK_LLM", "").strip() in ("1", "true", "True"):
        return None
    if not llm.get_token():
        return None
    try:
        verdict = llm.chat(
            [
                {
                    "role": "system",
                    "content": "Você é um avaliador rigoroso. Responda APENAS 'SIM' ou 'NÃO'.",
                },
                {"role": "user", "content": f"{question}\n\nResposta avaliada:\n{answer}"},
            ],
            max_tokens=5,
            temperature=0.0,
        )
        return verdict.strip().upper().startswith("SIM")
    except Exception:
        return None


def _run_case(agent, case: dict) -> tuple[bool, list[str]]:
    notes: list[str] = []
    ok = True
    result, latency, status = runner.safe_run(agent, case["input"], [])

    if status != "ok":
        return False, [f"execução falhou: {result.error}"]

    ans = result.answer or ""
    if not ans.strip():
        ok = False
        notes.append("resposta vazia")

    limit = case.get("max_latency_s")
    if limit is not None and latency > float(limit):
        ok = False
        notes.append(f"latência {latency:.1f}s > {limit}s")

    for needle in case.get("must_contain", []):
        if needle.lower() not in ans.lower():
            ok = False
            notes.append(f"faltou conter: {needle!r}")

    for needle in case.get("must_not_contain", []):
        if needle.lower() in ans.lower():
            ok = False
            notes.append(f"não deveria conter: {needle!r}")

    if case.get("judge"):
        verdict = _judge(case["judge"], ans)
        if verdict is True:
            notes.append("juiz: SIM")
        elif verdict is False:
            ok = False
            notes.append("juiz: NÃO")
        else:
            notes.append("juiz: pulado (MOCK/sem token)")

    return ok, notes


def main(slug_filter: str | None) -> int:
    agents, errors = registry.discover("agents")
    for e in errors:
        print(f"⚠️  {e.module}: {e.reason}")

    files = sorted(glob.glob(str(CASES_DIR / "*.yaml")))
    if not files:
        print("Nenhum caso em eval/cases/. Crie eval/cases/<slug>.yaml.")
        return 1

    total = passed = 0
    for path in files:
        spec = yaml.safe_load(pathlib.Path(path).read_text(encoding="utf-8"))
        slug = spec["agent"]
        if slug_filter and slug != slug_filter:
            continue
        if slug not in agents:
            print(f"❌ [{slug}] agente não encontrado/carregado — pulando {path}")
            continue

        print(f"\n=== {slug} ({len(spec['cases'])} casos) ===")
        for i, case in enumerate(spec["cases"], 1):
            total += 1
            ok, notes = _run_case(agents[slug], case)
            passed += ok
            mark = "✅" if ok else "❌"
            print(f"{mark} caso {i}: {'; '.join(notes) or 'ok'}")

    print(f"\n📊 {passed}/{total} casos passaram.")
    return 0 if passed == total and total > 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
