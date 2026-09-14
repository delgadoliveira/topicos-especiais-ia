import pathlib
import sqlite3
import tempfile
import unittest
import zipfile

import yaml

from portal.submissions import evaluate_submission, format_result


AGENT = """
from portal.base import AgentResult

class StudentAgent:
    slug = "agente-teste"
    name = "Agente Teste"
    emoji = "T"
    description = "Agente deterministico para teste."

    def run(self, message, history):
        text = message.strip()
        if not text:
            return AgentResult("Envie um texto.", steps=["entrada vazia recusada"])
        if len(text) > 4000:
            return AgentResult("Texto muito longo.", steps=["limite aplicado"])
        return AgentResult("Plano pronto.", steps=["entrada recebida", "plano criado"])

AGENT = StudentAgent()
"""

COMPONENT_AGENT = """
from portal import llm
from portal.base import AgentResult

def eco(texto):
    return texto

TOOLS = {"eco": eco}

def executar_tool(nome, argumento):
    return TOOLS[nome](argumento)

class StudentAgent:
    slug = "agente-teste"
    name = "Agente Teste"
    emoji = "T"
    description = "Agente com cinco componentes."

    def run(self, message, history):
        text = message.strip()
        if not text:
            return AgentResult("Envie um texto.", steps=["STOP vazio"])
        if len(text) > 4000:
            return AgentResult("Texto muito longo.", steps=["STOP limite"])
        contexto = " ".join(item.get("content", "") for item in history) + text
        dado = executar_tool("eco", contexto)
        for tentativa in range(2):
            resposta = llm.chat([
                {'role': 'system', 'content': 'Você cria planos curtos.'},
                {'role': 'user', 'content': dado},
            ])
            if resposta:
                break
        return AgentResult(
            "Plano pronto. " + resposta,
            steps=["MEMORY contexto", "ACT eco", "REFLECT resposta", "STOP sucesso"],
        )

AGENT = StudentAgent()
"""


class SubmissionTests(unittest.TestCase):
    def _package(self, folder: pathlib.Path, agent: str = AGENT) -> pathlib.Path:
        path = folder / "entrega.zip"
        metadata = {
            "student_id": "123",
            "student_name": "Aluno Teste",
            "agent_slug": "agente-teste",
        }
        cases = {
            "agent": "agente-teste",
            "cases": [
                {"input": "Organize isto", "must_contain": ["Plano"]},
                {"input": "", "must_contain": ["Envie"]},
                {"input": "x" * 4001, "must_contain": ["longo"]},
            ],
        }
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(
                "submission.yaml",
                yaml.safe_dump(metadata, allow_unicode=True),
            )
            archive.writestr("agent.py", agent)
            archive.writestr("cases.yaml", yaml.safe_dump(cases, allow_unicode=True))
        return path

    def test_complete_submission_is_graded_and_recorded(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = pathlib.Path(temp)
            database = folder / "grades.db"
            report = folder / "grades.csv"
            result, report_path = evaluate_submission(
                self._package(folder),
                timeout_s=5,
                db_path=database,
                csv_path=report,
            )

            self.assertEqual("A", result["concept"])
            self.assertEqual(100, result["score"])
            self.assertIn("component_evidence", result)
            self.assertEqual(report, report_path)
            connection = sqlite3.connect(database)
            try:
                row = connection.execute(
                    "SELECT student_id, concept, score FROM grades"
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(("123", "A", 100), row)

    def test_component_evidence_recognizes_theme_independent_agent(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = pathlib.Path(temp)
            result, _ = evaluate_submission(
                self._package(folder, COMPONENT_AGENT),
                timeout_s=5,
                db_path=folder / "grades.db",
                csv_path=folder / "grades.csv",
            )
            self.assertEqual(
                {
                    "persona_modelo": True,
                    "memoria": True,
                    "tools_executor": True,
                    "loop_controle": True,
                },
                result["component_evidence"],
            )
            report = format_result(result)
            self.assertIn("### Evidências formativas", report)
            self.assertIn("Persona + Modelo: **PRESENTE**", report)
            self.assertIn("não alteram o conceito", report)

    def test_unexpected_archive_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = pathlib.Path(temp)
            package = self._package(folder)
            with zipfile.ZipFile(package, "a") as archive:
                archive.writestr("../escape.txt", "nao extrair")

            with self.assertRaisesRegex(ValueError, "somente"):
                evaluate_submission(
                    package,
                    db_path=folder / "grades.db",
                    csv_path=folder / "grades.csv",
                )
            self.assertFalse((folder.parent / "escape.txt").exists())

    def test_slow_submission_times_out_and_is_recorded(self):
        slow_agent = AGENT.replace(
            "text = message.strip()",
            "while True:\n            pass\n        text = message.strip()",
        )
        with tempfile.TemporaryDirectory() as temp:
            folder = pathlib.Path(temp)
            result, _ = evaluate_submission(
                self._package(folder, slow_agent),
                timeout_s=0.1,
                db_path=folder / "grades.db",
                csv_path=folder / "grades.csv",
            )
            self.assertEqual("timeout", result["status"])
            self.assertEqual("C", result["concept"])

    def test_dangerous_student_code_is_rejected_before_execution(self):
        dangerous_agent = AGENT.replace(
            "from portal.base import AgentResult",
            "from portal.base import AgentResult\nimport os",
        )
        with tempfile.TemporaryDirectory() as temp:
            folder = pathlib.Path(temp)
            with self.assertRaisesRegex(ValueError, "politica de seguranca"):
                evaluate_submission(
                    self._package(folder, dangerous_agent),
                    db_path=folder / "grades.db",
                    csv_path=folder / "grades.csv",
                )
            self.assertFalse((folder / "grades.db").exists())

    def test_forbidden_builtin_alias_is_rejected(self):
        dangerous_agent = AGENT.replace(
            "class StudentAgent:",
            "runner = eval\n\nclass StudentAgent:",
        )
        with tempfile.TemporaryDirectory() as temp:
            folder = pathlib.Path(temp)
            with self.assertRaisesRegex(ValueError, "referencia a eval"):
                evaluate_submission(
                    self._package(folder, dangerous_agent),
                    db_path=folder / "grades.db",
                    csv_path=folder / "grades.csv",
                )


if __name__ == "__main__":
    unittest.main()
