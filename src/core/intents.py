"""Lightweight intent detection for messages that should not go to RAG."""

from __future__ import annotations

import re
import unicodedata


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower().strip())
    return "".join(char for char in text if not unicodedata.combining(char))


def is_greeting(message: str) -> bool:
    """Detect short greetings before querying the corporate knowledge base."""
    normalized = normalize_text(message)
    normalized = re.sub(r"[^\w\s]", "", normalized).strip()
    greetings = {
        "oi",
        "ola",
        "olá",
        "bom dia",
        "boa tarde",
        "boa noite",
        "e ai",
        "eae",
        "hello",
        "hi",
    }
    return normalized in greetings


def greeting_response() -> str:
    return (
        "Olá! Estou por aqui. Você pode me perguntar sobre documentos autorizados "
        "da DNEL SOM ou anexar um arquivo para uma análise temporária."
    )
