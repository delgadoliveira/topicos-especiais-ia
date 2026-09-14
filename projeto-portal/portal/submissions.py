from __future__ import annotations

import ast
import csv
import json
import os
import pathlib
import sqlite3
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SUBMISSIONS_DIR = ROOT / "submissions"
DB_PATH = SUBMISSIONS_DIR / "grades.db"
CSV_PATH = SUBMISSIONS_DIR / "notas.csv"
REQUIRED_FILES = {"submission.yaml", "agent.py", "cases.yaml"}
MAX_PACKAGE_BYTES = 2_000_000
MAX_UNCOMPRESSED_BYTES = 5_000_000
FORBIDDEN_CALLS = {
    "__import__",
    "breakpoint",
    "compile",
    "delattr",
    "eval",
    "exec",
    "getattr",
    "globals",
    "help",
    "input",
    "locals",
    "memoryview",
    "open",
    "setattr",
    "type",
    "vars",
}
FORBIDDEN_NODES = (
    ast.AsyncFunctionDef,
    ast.Await,
    ast.Delete,
    ast.Global,
    ast.Lambda,
    ast.Nonlocal,
    ast.Yield,
    ast.YieldFrom,
)


def _safe_csv(value: object) -> object:
    if isinstance(value, str) and value.startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def _validate_archive(path: pathlib.Path) -> None:
    if path.stat().st_size > MAX_PACKAGE_BYTES:
        raise ValueError("o ZIP deve ter no maximo 2 MB")
    try:
        with zipfile.ZipFile(path) as archive:
            files = [item for item in archive.infolist() if not item.is_dir()]
            names = [item.filename for item in files]
            if set(names) != REQUIRED_FILES or len(names) != len(REQUIRED_FILES):
                raise ValueError(
                    "o ZIP deve conter somente submission.yaml, agent.py e cases.yaml na raiz"
                )
            if sum(item.file_size for item in files) > MAX_UNCOMPRESSED_BYTES:
                raise ValueError("o conteudo descompactado deve ter no maximo 5 MB")
            for item in files:
                if (item.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError("links simbolicos nao sao permitidos")
    except zipfile.BadZipFile as exc:
        raise ValueError("o arquivo enviado nao e um ZIP valido") from exc


def _extract_archive(path: pathlib.Path, destination: pathlib.Path) -> dict:
    _validate_archive(path)
    with zipfile.ZipFile(path) as archive:
        for name in REQUIRED_FILES:
            target = destination / name
            target.write_bytes(archive.read(name))
    metadata = yaml.safe_load((destination / "submission.yaml").read_text("utf-8"))
    if not isinstance(metadata, dict):
        raise ValueError("submission.yaml invalido")
    required = ("student_id", "student_name", "agent_slug")
    missing = [key for key in required if not str(metadata.get(key, "")).strip()]
    if missing:
        raise ValueError("faltam campos em submission.yaml: " + ", ".join(missing))
    return {key: str(metadata[key]).strip() for key in required}


def _validate_student_code(path: pathlib.Path) -> None:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename="agent.py")
    except (SyntaxError, UnicodeDecodeError) as exc:
        raise ValueError(f"agent.py invalido: {exc}") from exc

    problems: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            problems.append("use apenas 'from portal...' para importar")
        elif isinstance(node, ast.ImportFrom):
            names = {item.name for item in node.names}
            allowed = (
                node.level == 0
                and (
                    (node.module == "portal.base" and names <= {"AgentResult"})
                    or (node.module == "portal" and names == {"llm"})
                )
            )
            if not allowed:
                problems.append(f"import nao permitido na linha {node.lineno}")
        elif isinstance(node, FORBIDDEN_NODES):
            problems.append(
                f"{type(node).__name__} nao permitido na linha {node.lineno}"
            )
        elif isinstance(node, ast.Name):
            if node.id.startswith("__"):
                problems.append(f"nome privado nao permitido na linha {node.lineno}")
            if node.id in FORBIDDEN_CALLS:
                problems.append(
                    f"referencia a {node.id} nao permitida na linha {node.lineno}"
                )
        elif isinstance(node, ast.Attribute):
            if node.attr.startswith("_"):
                problems.append(f"atributo privado nao permitido na linha {node.lineno}")
            if isinstance(node.value, ast.Name) and node.value.id == "llm":
                if node.attr != "chat":
                    problems.append(
                        f"somente llm.chat e permitido na linha {node.lineno}"
                    )
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
                problems.append(
                    f"chamada a {node.func.id} nao permitida na linha {node.lineno}"
                )
        elif isinstance(node, (ast.ClassDef, ast.FunctionDef)):
            if node.decorator_list:
                problems.append(f"decoradores nao permitidos na linha {node.lineno}")
            if isinstance(node, ast.ClassDef) and (node.bases or node.keywords):
                problems.append(f"heranca nao permitida na linha {node.lineno}")

    if problems:
        unique = list(dict.fromkeys(problems))
        raise ValueError("agent.py viola a politica de seguranca: " + "; ".join(unique))


def _worker_environment() -> dict[str, str]:
    allowed = ("SYSTEMROOT", "WINDIR", "TEMP", "TMP")
    env = {name: os.environ[name] for name in allowed if os.environ.get(name)}
    dependency_path = str(pathlib.Path(yaml.__file__).resolve().parent.parent)
    env.update(
        {
            "MOCK_LLM": "1",
            "MAX_REAL_CALLS": "0",
            "JUDGE_ENABLED": "0",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONPATH": dependency_path,
        }
    )
    return env


def _record(metadata: dict, result: dict, db_path: pathlib.Path = DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                evaluated_at TEXT NOT NULL,
                student_id TEXT NOT NULL,
                student_name TEXT NOT NULL,
                agent_slug TEXT NOT NULL,
                score INTEGER NOT NULL,
                concept TEXT NOT NULL,
                status TEXT NOT NULL,
                justification TEXT NOT NULL,
                details_json TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            INSERT INTO grades (
                evaluated_at, student_id, student_name, agent_slug, score,
                concept, status, justification, details_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                metadata["student_id"],
                metadata["student_name"],
                metadata["agent_slug"],
                result["score"],
                result["concept"],
                result["status"],
                result["justification"],
                json.dumps(result, ensure_ascii=False),
            ),
        )
        connection.commit()
    finally:
        connection.close()


def export_csv(
    db_path: pathlib.Path = DB_PATH, csv_path: pathlib.Path = CSV_PATH
) -> pathlib.Path:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    try:
        rows = connection.execute(
            """
            SELECT evaluated_at, student_id, student_name, agent_slug, score,
                   concept, status, justification
            FROM grades ORDER BY id
            """
        ).fetchall()
    finally:
        connection.close()
    headers = [
        "data_avaliacao",
        "identificacao",
        "aluno",
        "agente",
        "pontuacao",
        "conceito",
        "status",
        "justificativa",
    ]
    with csv_path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(headers)
        writer.writerows([_safe_csv(value) for value in row] for row in rows)
    return csv_path


def evaluate_submission(
    package_path: str | os.PathLike[str],
    timeout_s: float = 20,
    db_path: pathlib.Path = DB_PATH,
    csv_path: pathlib.Path = CSV_PATH,
) -> tuple[dict, pathlib.Path]:
    package = pathlib.Path(package_path)
    if not package.exists():
        raise ValueError("selecione um arquivo ZIP")
    with tempfile.TemporaryDirectory(prefix="agent-submission-") as temp:
        folder = pathlib.Path(temp)
        metadata = _extract_archive(package, folder)
        _validate_student_code(folder / "agent.py")
        output = folder / "result.json"
        try:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "portal" / "submission_worker.py"),
                    str(folder),
                    str(output),
                ],
                cwd=ROOT,
                env=_worker_environment(),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=timeout_s,
                check=False,
            )
            if completed.returncode != 0 or not output.exists():
                result = {
                    "status": "error",
                    "score": 0,
                    "concept": "C",
                    "justification": (
                        "Entrega recebida, mas o avaliador encerrou sem resultado. "
                        "Revise agent.py e tente novamente."
                    ),
                    "criteria": {},
                    "cases": [],
                }
            else:
                result = json.loads(output.read_text(encoding="utf-8"))
        except subprocess.TimeoutExpired:
            result = {
                "status": "timeout",
                "score": 0,
                "concept": "C",
                "justification": (
                    f"Entrega recebida, mas excedeu o limite de {timeout_s:g}s. "
                    "Revise loops e operacoes demoradas."
                ),
                "criteria": {},
                "cases": [],
            }
    result["student"] = metadata
    _record(metadata, result, db_path)
    return result, export_csv(db_path, csv_path)


def format_result(result: dict) -> str:
    student = result["student"]
    lines = [
        f"## Conceito {result['concept']} — {result['score']}/100",
        f"**Aluno:** {student['student_name']}  ",
        f"**Identificacao:** {student['student_id']}  ",
        f"**Agente:** `{student['agent_slug']}`",
        "",
        result["justification"],
    ]
    if result.get("cases"):
        lines.extend(["", "### Casos"])
        for case in result["cases"]:
            marker = "PASSOU" if case["passed"] else "AJUSTAR"
            notes = "; ".join(case["notes"]) or "sem observacoes"
            lines.append(f"- Caso {case['case']}: **{marker}** — {notes}")
    if result.get("component_evidence"):
        labels = {
            "persona_modelo": "Persona + Modelo",
            "memoria": "Memória",
            "tools_executor": "Tools + Executor",
            "loop_controle": "Loop de Controle",
        }
        lines.extend(["", "### Evidências formativas"])
        for key, label in labels.items():
            marker = "PRESENTE" if result["component_evidence"].get(key) else "A DESENVOLVER"
            lines.append(f"- {label}: **{marker}**")
        lines.append("_Estes indicadores orientam o feedback e não alteram o conceito._")
    return "\n".join(lines)
