import unittest
from src.core.escalation import build_escalation_message, detect_sector


class TestEscalation(unittest.TestCase):
    def test_detects_rh_question(self):
        sector = detect_sector("Qual é a regra de férias?")
        self.assertEqual(sector["email"], "rh@dnelsom.com.br")

    def test_builds_fallback_message(self):
        message = build_escalation_message("Qual é o salário do diretor?")
        self.assertIn("Não encontrei", message)
        self.assertIn("rh@dnelsom.com.br", message)

    def test_generic_fallback_does_not_duplicate_sector_text(self):
        message = build_escalation_message("conte uma piada")
        self.assertNotIn("setor de setor responsável", message)
        self.assertIn("setor responsável", message)


if __name__ == "__main__":
    unittest.main()
