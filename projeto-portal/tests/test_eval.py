import unittest
from unittest.mock import patch

from eval.run_eval import _run_case
from portal.base import AgentResult


class EvalTests(unittest.TestCase):
    def test_max_chars_is_enforced(self):
        result = AgentResult(answer="texto longo")
        with patch(
            "portal.evaluation.runner.safe_run",
            return_value=(result, 0.01, "ok"),
        ):
            ok, notes = _run_case(object(), {"input": "x", "max_chars": 5})
        self.assertFalse(ok)
        self.assertIn("caracteres > 5", notes[0])


if __name__ == "__main__":
    unittest.main()
