from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import re
import sys

os.environ["MOCK_LLM"] = "1"
os.environ["MAX_REAL_CALLS"] = "0"
os.environ["JUDGE_ENABLED"] = "0"

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from portal.base import validate_agent
from portal.evaluation import run_case_details
from portal.runner import safe_run


def _load_agent(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location("student_submission", path)
    if spec is None or spec.loader is None:
        raise ValueError("nao foi possivel carregar agent.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "AGENT"):
        raise ValueError("agent.py nao expoe AGENT")
    return module.AGENT


def _load_cases(path: pathlib.Path) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        raise ValueError("cases.yaml precisa conter uma lista 'cases'")
    cases = data["cases"]
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict) or not isinstance(case.get("input"), str):
            raise ValueError(f"caso {index} precisa ter 'input' em texto")
    return cases


def _concept(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    return "C"


def evaluate(folder: pathlib.Path) -> dict:
    criteria = {
        "contrato": 0,
        "smoke_test": 0,
        "tres_casos": 0,
        "aprovacao": 0,
        "guardrail": 0,
        "observabilidade": 0,
    }
    problems: list[str] = []
    agent = _load_agent(folder / "agent.py")
    contract_problems = validate_agent(agent)
    if contract_problems:
        problems.extend(contract_problems)
    else:
        criteria["contrato"] = 20

    smoke, _, smoke_status = safe_run(agent, "Teste offline da entrega.", [])
    if smoke_status == "ok" and (smoke.answer or "").strip():
        criteria["smoke_test"] = 20
    else:
        problems.append(f"smoke test falhou: {smoke.error or 'resposta vazia'}")

    cases = _load_cases(folder / "cases.yaml")
    criteria["tres_casos"] = min(len(cases), 3) * 5
    case_results = []
    passed = 0
    edge_case_passed = False
    has_steps = False
    for index, case in enumerate(cases, start=1):
        ok, notes, result = run_case_details(agent, case)
        passed += int(ok)
        text = case["input"]
        if ok and (not text.strip() or len(text) > 4000):
            edge_case_passed = True
        has_steps = has_steps or bool(result.steps)
        case_results.append(
            {"case": index, "passed": ok, "notes": notes, "input_preview": text[:80]}
        )

    if cases:
        criteria["aprovacao"] = round(25 * passed / len(cases))
    if edge_case_passed:
        criteria["guardrail"] = 10
    if has_steps:
        criteria["observabilidade"] = 10

    source = (folder / "agent.py").read_text(encoding="utf-8")
    component_evidence = {
        "persona_modelo": bool(
            re.search(r"""["']role["']\s*:\s*["']system["']""", source)
            and "llm.chat" in source
            and callable(getattr(agent, "run", None))
        ),
        "memoria": False,
        "tools_executor": False,
        "loop_controle": False,
    }
    probe_case = next((case for case in cases if case.get("history")), None)
    if probe_case is None:
        probe_case = next((case for case in cases if case["input"].strip()), None)
    evidence_result, _, evidence_status = safe_run(
        agent,
        probe_case["input"] if probe_case else "Teste offline da entrega.",
        probe_case.get("history", []) if probe_case else [],
    )
    if evidence_status == "ok":
        event_names = [str(step).split(" ", 1)[0] for step in evidence_result.steps]
        component_evidence["memoria"] = (
            "MEMORY" in event_names and "history" in source
        )
        component_evidence["tools_executor"] = (
            "ACT" in event_names and "TOOLS" in source and "executar_tool" in source
        )
        component_evidence["loop_controle"] = bool(
            "REFLECT" in event_names
            and "STOP" in event_names
            and re.search(r"\bfor\b.+\brange\s*\(", source)
        )

    score = sum(criteria.values())
    concept = _concept(score)
    detail = [
        f"Contrato {criteria['contrato']}/20",
        f"smoke test {criteria['smoke_test']}/20",
        f"tres casos {criteria['tres_casos']}/15",
        f"aprovacao {criteria['aprovacao']}/25",
        f"guardrail {criteria['guardrail']}/10",
        f"observabilidade {criteria['observabilidade']}/10",
    ]
    if problems:
        detail.append("ajustes: " + "; ".join(problems))
    justification = ". ".join(detail) + "."
    return {
        "status": "completed",
        "score": score,
        "concept": concept,
        "justification": justification,
        "criteria": criteria,
        "cases": case_results,
        "problems": problems,
        "component_evidence": component_evidence,
    }


def main() -> int:
    folder = pathlib.Path(sys.argv[1])
    output = pathlib.Path(sys.argv[2])
    try:
        result = evaluate(folder)
    except Exception as exc:
        result = {
            "status": "error",
            "score": 0,
            "concept": "C",
            "justification": f"Entrega recebida, mas a avaliacao falhou: {type(exc).__name__}: {exc}",
            "criteria": {},
            "cases": [],
            "problems": [f"{type(exc).__name__}: {exc}"],
        }
    output.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
