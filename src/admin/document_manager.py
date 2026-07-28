"""Document management module for Admin operations."""

from __future__ import annotations

from pathlib import Path

from src.config.settings import settings

DEFAULT_SECTORS = [
    "rh",
    "ti",
    "juridico",
    "comercial",
    "atendimento",
    "compliance",
    "financeiro",
]


def get_available_sectors() -> list[str]:
    """Return a list of available sector directories, sorted alphabetically."""
    root = settings.company_docs_path
    sectors = set(DEFAULT_SECTORS)

    if root.exists():
        for item in root.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                sectors.add(item.name.lower())

    return sorted(list(sectors))


def list_company_documents() -> dict[str, list[str]]:
    """Return a map of sector -> list of file names."""
    root = settings.company_docs_path
    doc_map: dict[str, list[str]] = {}

    sectors = get_available_sectors()
    for sector in sectors:
        sector_dir = root / sector
        if sector_dir.exists() and sector_dir.is_dir():
            files = [
                f.name
                for f in sorted(sector_dir.iterdir())
                if f.is_file() and not f.name.startswith(".")
            ]
            doc_map[sector] = files
        else:
            doc_map[sector] = []

    return doc_map


def save_admin_document(file_name: str, content_bytes: bytes, sector: str) -> Path:
    """Save an uploaded document to the designated sector directory."""
    if not file_name or not file_name.strip():
        raise ValueError("O nome do arquivo não pode ser vazio.")

    sector_clean = sector.lower().strip()
    if not sector_clean:
        raise ValueError("O setor deve ser especificado.")

    target_dir = settings.company_docs_path / sector_clean
    target_dir.mkdir(parents=True, exist_ok=True)

    # Sanitize filename (basic basename check)
    safe_name = Path(file_name).name
    file_path = target_dir / safe_name

    file_path.write_bytes(content_bytes)
    return file_path


def delete_admin_document(sector: str, file_name: str) -> bool:
    """Delete a document from a specific sector directory."""
    sector_clean = sector.lower().strip()
    safe_name = Path(file_name).name
    file_path = settings.company_docs_path / sector_clean / safe_name

    if file_path.exists() and file_path.is_file():
        file_path.unlink()
        return True
    return False
