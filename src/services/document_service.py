"""Temporary document analysis service with Gemini LLM integration."""

from __future__ import annotations

from pathlib import Path

import google.generativeai as genai

from src.config.settings import settings
from src.utils.file_readers import read_document


def ask_temporary_document(
    file_path: str | Path,
    question: str | None = None,
    max_chars: int = 15000,
) -> str:
    """Analyze a temporary document using Gemini and answer the user's question."""
    text = read_document(file_path)
    if not text.strip():
        return "Não consegui extrair texto legível do arquivo enviado."

    extracted_text = text[:max_chars]
    is_truncated = len(text) > max_chars
    truncation_note = "\n[Nota: O texto do documento foi truncado para caber no limite de análise.]" if is_truncated else ""

    if not settings.google_api_key:
        preview = extracted_text[:2500]
        suffix = "\n\n[Prévia truncada.]" if len(extracted_text) > 2500 else ""
        return f"Recebi o documento temporário. Prévia extraída:\n\n{preview}{suffix}"

    genai.configure(api_key=settings.google_api_key)
    model = genai.GenerativeModel(settings.chat_model)

    user_query = question.strip() if question and question.strip() else "Faça um resumo executivo dos pontos principais deste documento."

    prompt = f"""Você é o Daniel, assistente corporativo inteligente da DNEL SOM.
O usuário enviou um documento temporário para análise imediata. Este documento NÃO está salvo na base permanente.

CONTEÚDO DO DOCUMENTO TEMPORÁRIO:
{extracted_text}{truncation_note}

PERGUNTA DO USUÁRIO:
{user_query}

REGRAS:
1. Responda à pergunta do usuário utilizando prioritariamente as informações extraídas do documento temporário.
2. Se a informação não constar no documento, indique isso claramente.
3. Mantenha tom profissional, objetivo e estruturado.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as exc:
        return (
            f"Recebi o arquivo temporário, mas encontrei um erro ao processar com a IA ({exc}). "
            f"Prévia do conteúdo:\n\n{extracted_text[:1500]}"
        )


def summarize_temporary_document(file_path: str | Path, max_chars: int = 2500) -> str:
    """Fallback function for extracted text preview."""
    return ask_temporary_document(file_path, question="Resuma os pontos principais", max_chars=max_chars)
