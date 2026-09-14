"""
Mini-harness de avaliação — duas camadas.

  1. Checks determinísticos (sempre rodam, offline): resposta não-vazia,
     latência e tamanho dentro do limite, substrings obrigatórias/proibidas.
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
        max_chars: 900              # opcional
        must_contain: ["- "]        # opcional
        must_not_contain: ["erro"]  # opcional
        judge: "O resumo é fiel ao texto e tem no máximo 3 tópicos?"  # opcional
"""
import glob
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import yaml  # noqa: E402

from portal import registry  # noqa: E402
from portal.evaluation import run_case as _run_case  # noqa: E402

CASES_DIR = pathlib.Path(__file__).parent / "cases"


def main(slug_filter: str | None) -> int:
    agents, errors = registry.discover("agents")
    for e in errors:
        print(f"⚠️  {e.module}: {e.reason}")

    files = [
        path
        for path in sorted(glob.glob(str(CASES_DIR / "*.yaml")))
        if not pathlib.Path(path).name.startswith("_")
    ]
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
