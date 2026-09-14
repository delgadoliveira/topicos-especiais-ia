from __future__ import annotations

import argparse
import pathlib
import re
import unicodedata
import zipfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parent


def _filename(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", normalized).strip("-").lower()


def build_package(
    student_id: str,
    student_name: str,
    agent_slug: str,
    output: pathlib.Path | None = None,
) -> pathlib.Path:
    agent = ROOT / "agents" / f"{agent_slug}.py"
    cases = ROOT / "eval" / "cases" / f"{agent_slug}.yaml"
    if not agent.exists():
        raise FileNotFoundError(f"agente nao encontrado: {agent}")
    if not cases.exists():
        raise FileNotFoundError(f"casos nao encontrados: {cases}")
    output = output or ROOT / "entregas" / (
        f"{_filename(student_id)}-{_filename(agent_slug)}.zip"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "student_id": student_id.strip(),
        "student_name": student_name.strip(),
        "agent_slug": agent_slug.strip(),
    }
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "submission.yaml",
            yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False),
        )
        archive.write(agent, "agent.py")
        archive.write(cases, "cases.yaml")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Empacota a entrega do agente.")
    parser.add_argument("--id", required=True, dest="student_id")
    parser.add_argument("--nome", required=True, dest="student_name")
    parser.add_argument("--agente", required=True, dest="agent_slug")
    parser.add_argument("--saida", type=pathlib.Path)
    args = parser.parse_args()
    path = build_package(
        args.student_id, args.student_name, args.agent_slug, args.saida
    )
    print(f"Entrega criada: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
