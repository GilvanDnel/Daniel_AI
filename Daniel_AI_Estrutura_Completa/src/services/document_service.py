"""Temporary document analysis service."""

from __future__ import annotations

from pathlib import Path

from src.utils.file_readers import read_document


def summarize_temporary_document(file_path: str | Path, max_chars: int = 2500) -> str:
    """Return extracted text preview for a temporary document.

    The LLM summarization layer can be connected here later. For the MVP skeleton,
    this function gives a deterministic preview and keeps temporary files out of
    the corporate vector base.
    """
    text = read_document(file_path)
    if not text.strip():
        return "Não consegui extrair texto do arquivo enviado."
    preview = text[:max_chars]
    suffix = "\n\n[Prévia truncada para análise inicial.]" if len(text) > max_chars else ""
    return preview + suffix
