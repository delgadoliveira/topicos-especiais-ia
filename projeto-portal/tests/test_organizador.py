import importlib.util
import pathlib
import unittest
from unittest.mock import patch


AGENT_PATH = (
    pathlib.Path(__file__).resolve().parents[1]
    / "agents"
    / "organizador-estudos-referencia.py"
)
SPEC = importlib.util.spec_from_file_location("organizador_referencia", AGENT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

VALID_PLAN = (
    "1. Frações — motivo: base; ação: revisar por 10 minutos.\n"
    "2. Equações — motivo: sequência; ação: praticar por 10 minutos.\n"
    "3. Revisão — motivo: verificar; ação: explicar por 5 minutos."
)


class OrganizadorTests(unittest.TestCase):
    def setUp(self):
        self.agent = MODULE.AGENT

    def test_memory_recovers_previous_user_message(self):
        history = [
            {"role": "user", "content": "Tenho prova de frações na sexta."},
            {"role": "assistant", "content": "Quanto tempo você tem?"},
        ]
        with patch.object(MODULE.llm, "chat", return_value=VALID_PLAN):
            result = self.agent.run("Tenho 40 minutos.", history)
        self.assertIn("Plano de estudo", result.answer)
        self.assertTrue(any(event.startswith("MEMORY") for event in result.steps))

    def test_tool_executor_rejects_unknown_tool(self):
        with self.assertRaisesRegex(ValueError, "não permitida"):
            MODULE.executar_tool("apagar_arquivos", 10)

    def test_loop_retries_once_then_stops(self):
        with patch.object(MODULE.llm, "chat", side_effect=["", VALID_PLAN]) as chat:
            result = self.agent.run(
                "Tenho prova de frações e 40 minutos.",
                [],
            )
        self.assertEqual(2, chat.call_count)
        self.assertIn("STOP · resposta válida", result.steps)

    def test_missing_time_stops_before_model(self):
        with patch.object(MODULE.llm, "chat") as chat:
            result = self.agent.run("Tenho prova de frações.", [])
        chat.assert_not_called()
        self.assertIn("Quanto tempo", result.answer)
        self.assertTrue(result.steps[-1].startswith("STOP"))

    def test_time_written_in_words_is_understood(self):
        with patch.object(MODULE.llm, "chat", return_value=VALID_PLAN):
            result = self.agent.run("Preciso revisar agentes e só tenho dez minutos.", [])
        self.assertIn("Plano de estudo", result.answer)
        self.assertTrue(any("1 bloco" in event for event in result.steps))

    def test_complete_answer_respects_character_limit(self):
        with patch.object(MODULE.llm, "chat", side_effect=["x" * 850, VALID_PLAN]):
            result = self.agent.run("Preciso revisar prompts em 30 minutos.", [])
        self.assertLessEqual(len(result.answer), 900)

    def test_current_time_overrides_stale_memory(self):
        history = [{"role": "user", "content": "Tenho prova de frações e 30 minutos."}]
        with patch.object(MODULE.llm, "chat", return_value=VALID_PLAN):
            result = self.agent.run("Agora tenho 10 minutos.", history)
        self.assertTrue(any("1 bloco" in event for event in result.steps))

    def test_time_only_asks_for_study_task(self):
        with patch.object(MODULE.llm, "chat") as chat:
            result = self.agent.run("Tenho 30 minutos hoje.", [])
        chat.assert_not_called()
        self.assertIn("matéria ou tarefa", result.answer)

    def test_short_available_time_is_not_inflated(self):
        self.assertEqual("1 bloco(s) de até 3 minuto(s)", MODULE.planejar_blocos(3))

    def test_long_available_time_keeps_actions_under_twenty_minutes(self):
        self.assertEqual("3 bloco(s) de até 20 minuto(s)", MODULE.planejar_blocos(90))

    def test_malformed_plan_retries(self):
        with patch.object(MODULE.llm, "chat", side_effect=["Plano genérico", VALID_PLAN]) as chat:
            result = self.agent.run("Preciso revisar agentes em 30 minutos.", [])
        self.assertEqual(2, chat.call_count)
        self.assertIn("STOP · resposta válida", result.steps)

    def test_each_priority_requires_reason_action_and_duration(self):
        incomplete = (
            "1. Frações — motivo: base; ação: revisar por 10 minutos.\n"
            "2. Equações — ação: praticar por 10 minutos.\n"
            "3. Revisão — motivo: verificar; ação: explicar por 5 minutos."
        )
        self.assertFalse(MODULE.resposta_valida(incomplete))

    def test_action_over_twenty_minutes_is_rejected(self):
        excessive = VALID_PLAN.replace("10 minutos", "25 minutos", 1)
        self.assertFalse(MODULE.resposta_valida(excessive))

    def test_offline_plan_uses_individual_capped_actions(self):
        plan = MODULE.resposta_offline(MODULE.planejar_blocos(90))
        self.assertTrue(MODULE.resposta_valida(plan))
        self.assertNotIn("3 bloco(s)", plan)


if __name__ == "__main__":
    unittest.main()
