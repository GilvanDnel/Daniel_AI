import unittest
from src.core.errors import build_quota_message, extract_retry_seconds, is_quota_error


class TestErrors(unittest.TestCase):
    def test_detects_resource_exhausted(self):
        error = Exception("ResourceExhausted: 429 You exceeded your current quota. Please retry in 36.05s.")
        self.assertTrue(is_quota_error(error))
        self.assertEqual(extract_retry_seconds(error), 36)

    def test_builds_user_friendly_quota_message(self):
        error = Exception("429 Please retry in 12.2s")
        message = build_quota_message(error)
        self.assertIn("limite de uso", message)
        self.assertIn("12 segundos", message)


if __name__ == "__main__":
    unittest.main()
