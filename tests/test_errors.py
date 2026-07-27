from src.core.errors import build_quota_message, extract_retry_seconds, is_quota_error


def test_detects_resource_exhausted():
    error = Exception("ResourceExhausted: 429 You exceeded your current quota. Please retry in 36.05s.")
    assert is_quota_error(error)
    assert extract_retry_seconds(error) == 36


def test_builds_user_friendly_quota_message():
    error = Exception("429 Please retry in 12.2s")
    message = build_quota_message(error)
    assert "limite de uso" in message
    assert "12 segundos" in message
