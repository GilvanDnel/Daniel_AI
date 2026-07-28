import unittest
from src.core.intents import is_greeting


class TestIntents(unittest.TestCase):
    def test_detects_simple_greeting(self):
        self.assertTrue(is_greeting("olá"))
        self.assertTrue(is_greeting("ola"))
        self.assertTrue(is_greeting("boa tarde"))

    def test_does_not_treat_question_as_greeting(self):
        self.assertFalse(is_greeting("como solicito férias?"))


if __name__ == "__main__":
    unittest.main()
