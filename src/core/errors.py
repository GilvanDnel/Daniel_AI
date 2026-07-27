"""User-facing error handling helpers."""

from __future__ import annotations

import re


def is_quota_error(error: Exception) -> bool:
    """Detect Gemini/API quota errors without depending on a specific exception class."""
    text = f"{type(error).__name__}: {error}".lower()
    return (
        "resourceexhausted" in text
        or "resource exhausted" in text
        or "quota" in text
        or "429" in text
        or "too many requests" in text
    )


def extract_retry_seconds(error: Exception) -> int | None:
    """Try to extract retry delay from Gemini error messages."""
    text = str(error)
    patterns = [
        r"retry in ([0-9]+(?:\.[0-9]+)?)s",
        r"retry after ([0-9]+(?:\.[0-9]+)?)s",
        r"retryDelay.*?([0-9]+(?:\.[0-9]+)?)s",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return max(1, int(float(match.group(1))))
    return None


def build_quota_message(error: Exception | None = None) -> str:
    retry_seconds = extract_retry_seconds(error) if error is not None else None
    wait_text = f"aguarde cerca de {retry_seconds} segundos" if retry_seconds else "aguarde alguns instantes"

    return (
        "Atingimos temporariamente o limite de uso da API de IA. "
        f"Por favor, {wait_text} e tente enviar sua pergunta novamente.\n\n"
        "Enquanto isso, você ainda pode usar recursos locais do Daniel, como análise de CSV/XLSX "
        "e visualização de dashboards, quando eles não dependerem de chamada ao modelo."
    )
