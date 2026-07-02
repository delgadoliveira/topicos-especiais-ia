"""
Preflight — valide o SEU agente antes de subir ao portal.

Uso:
    python check_agent.py agents/example_resumidor.py

O que faz (tudo em MOCK, sem gastar rede):
  1. importa o arquivo do agente;
  2. confere se ele expõe AGENT e cumpre o contrato;
  3. faz um smoke test: roda o agente com uma entrada de teste.

Sai com código 0 se passou, 1 se falhou (útil em CI).
"""
import importlib.util
import os
import pathlib
import sys

os.environ.setdefault("MOCK_LLM", "1")  # preflight nunca depende de rede
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from portal import base, runner  # noqa: E402


def _load_agent_module(path: str):
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(f"arquivo não encontrado: {path}")
    spec = importlib.util.spec_from_file_location(p.stem, p)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def main(path: str) -> int:
    print(f"🔍 Verificando {path}\n")
    try:
        module = _load_agent_module(path)
    except Exception as exc:
        print(f"❌ Falha ao importar: {exc}")
        return 1

    agent = getattr(module, "AGENT", None)
    if agent is None:
        print("❌ O arquivo não expõe a variável AGENT (ex: AGENT = MeuAgente()).")
        return 1
    print("✅ Expõe AGENT")

    problems = base.validate_agent(agent)
    if problems:
        for p in problems:
            print(f"❌ Contrato: {p}")
        return 1
    print(f"✅ Contrato ok — slug='{agent.slug}', nome='{agent.name}'")

    result, latency, status = runner.safe_run(agent, "Texto de teste para o smoke test.", [])
    if status != "ok":
        print(f"❌ Smoke test falhou: {result.error}")
        return 1
    print(f"✅ Smoke test ok — respondeu em {latency:.2f}s")
    print(f"\n📝 Resposta (MOCK):\n{result.answer[:300]}")
    print("\n🎉 Tudo certo! Seu agente está pronto para o portal.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python check_agent.py agents/<seu-arquivo>.py")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
