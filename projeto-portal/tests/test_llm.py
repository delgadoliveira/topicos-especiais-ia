import os
import sys
import types
import unittest
from unittest.mock import patch

from portal import llm


class _Completions:
    def __init__(self):
        self.calls = 0

    def create(self, **kwargs):
        self.calls += 1
        message = types.SimpleNamespace(content=f"resposta-{self.calls}")
        return types.SimpleNamespace(choices=[types.SimpleNamespace(message=message)])


class LlmTests(unittest.TestCase):
    def setUp(self):
        llm._CACHE.clear()
        llm._real_calls = 0
        self.completions = _Completions()
        client = types.SimpleNamespace(
            chat=types.SimpleNamespace(completions=self.completions)
        )
        fake_openai = types.SimpleNamespace(OpenAI=lambda **kwargs: client)
        self.module_patch = patch.dict(sys.modules, {"openai": fake_openai})
        self.env_patch = patch.dict(
            os.environ,
            {
                "MOCK_LLM": "0",
                "HF_TOKEN": "teste",
                "MAX_REAL_CALLS": "2",
                "LLM_CACHE": "1",
            },
            clear=False,
        )
        self.module_patch.start()
        self.env_patch.start()

    def tearDown(self):
        self.env_patch.stop()
        self.module_patch.stop()

    def test_mock_does_not_consume_budget(self):
        os.environ["MOCK_LLM"] = "1"
        self.assertTrue(llm.is_mock_mode())
        answer = llm.chat([{"role": "user", "content": "ola"}])
        self.assertIn("modo offline", answer.lower())
        self.assertEqual(llm._real_calls, 0)

    def test_identical_request_uses_cache(self):
        messages = [{"role": "user", "content": "ola"}]
        first = llm.chat(messages, retries=0)
        second = llm.chat(messages, retries=0)
        self.assertEqual(first, second)
        self.assertEqual(self.completions.calls, 1)
        self.assertEqual(llm._real_calls, 1)

    def test_budget_blocks_request_before_provider_call(self):
        os.environ["MAX_REAL_CALLS"] = "1"
        llm.chat([{"role": "user", "content": "primeira"}], retries=0)
        with self.assertRaisesRegex(RuntimeError, "Limite de chamadas"):
            llm.chat([{"role": "user", "content": "segunda"}], retries=0)
        self.assertEqual(self.completions.calls, 1)

    def test_usage_summary_reports_real_calls(self):
        llm.chat([{"role": "user", "content": "ola"}], retries=0)
        self.assertEqual(llm.usage_summary(), "Chamadas reais: 1/2")


if __name__ == "__main__":
    unittest.main()
